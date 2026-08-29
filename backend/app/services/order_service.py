import uuid
import secrets
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem, OrderStatusEnum, OrderPriorityEnum
from app.models.patient import Patient
from app.models.catalog import Test, TestParameter
from app.models.sample import Sample, SampleStatusHistory, SampleStatusEnum
from app.models.billing import Invoice, Payment, PaymentStatusEnum, PaymentMethodEnum
from app.models.report import LabReport, ReportStatusEnum
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.order import OrderCreate, PaymentCreate
from app.core.exceptions import NotFoundException, ConflictException, ClinicalValidationError


class OrderService:
    @staticmethod
    async def generate_order_number(db: AsyncSession) -> str:
        year = datetime.utcnow().year
        prefix = f"ORD-{year}-"
        result = await db.execute(
            select(func.count(Order.id)).where(Order.order_number.like(f"{prefix}%"))
        )
        count = result.scalar() or 0
        return f"{prefix}{count + 1:05d}"

    @staticmethod
    async def generate_invoice_number(db: AsyncSession) -> str:
        year = datetime.utcnow().year
        prefix = f"INV-{year}-"
        result = await db.execute(
            select(func.count(Invoice.id)).where(Invoice.invoice_number.like(f"{prefix}%"))
        )
        count = result.scalar() or 0
        return f"{prefix}{count + 1:05d}"

    @staticmethod
    async def generate_sample_barcode(db: AsyncSession) -> str:
        random_digits = secrets.randbelow(900000000) + 100000000
        return f"SMP-{random_digits}"

    @staticmethod
    async def create_order(
        db: AsyncSession,
        order_in: OrderCreate,
        creator_id: Optional[str] = None
    ) -> Order:
        # 1. Verify Patient
        patient = await db.execute(select(Patient).where(Patient.id == order_in.patient_id))
        patient_obj = patient.scalars().first()
        if not patient_obj:
            raise NotFoundException("Patient", order_in.patient_id)

        # 2. Fetch Tests
        tests_res = await db.execute(
            select(Test)
            .options(selectinload(Test.parameters))
            .where(Test.id.in_(order_in.test_ids))
        )
        tests = list(tests_res.scalars().all())
        if len(tests) != len(order_in.test_ids):
            raise ClinicalValidationError("One or more selected test IDs are invalid or inactive.")

        # 3. Compute Financials
        subtotal = sum(t.price for t in tests)
        discount = min(order_in.discount_amount, subtotal)
        tax = 0.0  # Medical diagnostics typically zero or flat
        total = max(0.0, subtotal - discount + tax)

        order_number = await OrderService.generate_order_number(db)
        order_id = str(uuid.uuid4())

        order = Order(
            id=order_id,
            order_number=order_number,
            patient_id=order_in.patient_id,
            referring_doctor=order_in.referring_doctor,
            clinical_notes=order_in.clinical_notes,
            priority=order_in.priority,
            status=OrderStatusEnum.PENDING,
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax,
            total_amount=total,
            created_by_id=creator_id
        )
        db.add(order)

        # 4. Cluster Tests into Required Sample Tubes (Grouped by specimen and container)
        tube_groups = {}  # (specimen_type, container_type) -> list of tests
        for t in tests:
            key = (t.specimen_type, t.container_type)
            tube_groups.setdefault(key, []).append(t)

        for (specimen_type, container_type), group_tests in tube_groups.items():
            barcode = await OrderService.generate_sample_barcode(db)
            sample = Sample(
                id=str(uuid.uuid4()),
                order_id=order_id,
                barcode=barcode,
                specimen_type=specimen_type,
                container_type=container_type,
                status=SampleStatusEnum.PENDING_COLLECTION,
                notes=f"Required for: {', '.join(t.short_name or t.name for t in group_tests)}"
            )
            db.add(sample)
            await db.flush()

            # Create Order Items linked to this sample
            for t in group_tests:
                order_item = OrderItem(
                    id=str(uuid.uuid4()),
                    order_id=order_id,
                    test_id=t.id,
                    sample_id=sample.id,
                    price=t.price,
                    status="PENDING"
                )
                db.add(order_item)

        # 5. Create Billing Invoice
        invoice_number = await OrderService.generate_invoice_number(db)
        invoice = Invoice(
            id=str(uuid.uuid4()),
            order_id=order_id,
            invoice_number=invoice_number,
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax,
            total_amount=total,
            paid_amount=0.0,
            balance_amount=total,
            payment_status=PaymentStatusEnum.UNPAID if total > 0 else PaymentStatusEnum.PAID
        )
        db.add(invoice)

        # 6. Initialize Draft Lab Report with secure QR verification hash
        report_number = f"REP-{order_number.replace('ORD-', '')}"
        qr_hash = secrets.token_urlsafe(24)
        report = LabReport(
            id=str(uuid.uuid4()),
            order_id=order_id,
            report_number=report_number,
            status=ReportStatusEnum.DRAFT,
            verification_qr_hash=qr_hash
        )
        db.add(report)

        # 7. Audit Log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=creator_id,
            action=AuditActionEnum.CREATE_ORDER,
            entity_name="Order",
            entity_id=order.id,
            details=f"Placed test order {order.order_number} with {len(tests)} tests for {patient_obj.full_name}"
        )
        db.add(audit)

        await db.commit()
        return await OrderService.get_order_by_id(db, order_id)

    @staticmethod
    async def get_order_by_id(db: AsyncSession, order_id: str) -> Optional[Order]:
        query = (
            select(Order)
            .options(
                selectinload(Order.patient),
                selectinload(Order.order_items).selectinload(OrderItem.test),
                selectinload(Order.samples).selectinload(Sample.status_history),
                selectinload(Order.invoice).selectinload(Invoice.payments),
                selectinload(Order.lab_report)
            )
            .where(Order.id == order_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def list_orders(
        db: AsyncSession,
        patient_id: Optional[str] = None,
        status: Optional[OrderStatusEnum] = None,
        priority: Optional[OrderPriorityEnum] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Order], int]:
        query = (
            select(Order)
            .options(
                selectinload(Order.patient),
                selectinload(Order.order_items).selectinload(OrderItem.test),
                selectinload(Order.invoice).selectinload(Invoice.payments),
                selectinload(Order.lab_report)
            )
        )
        count_query = select(func.count(Order.id))

        if patient_id:
            query = query.where(Order.patient_id == patient_id)
            count_query = count_query.where(Order.patient_id == patient_id)
        if status:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)
        if priority:
            query = query.where(Order.priority == priority)
            count_query = count_query.where(Order.priority == priority)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.join(Patient).where(
                or_(
                    Order.order_number.ilike(pattern),
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.patient_code.ilike(pattern),
                    Patient.phone.ilike(pattern)
                )
            )
            count_query = count_query.join(Patient).where(
                or_(
                    Order.order_number.ilike(pattern),
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.patient_code.ilike(pattern),
                    Patient.phone.ilike(pattern)
                )
            )

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        offset = (page - 1) * limit
        query = query.order_by(desc(Order.created_at)).offset(offset).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    @staticmethod
    async def record_payment(
        db: AsyncSession,
        order_id: str,
        payment_in: PaymentCreate,
        receiver_id: Optional[str] = None
    ) -> Invoice:
        order = await OrderService.get_order_by_id(db, order_id)
        if not order:
            raise NotFoundException("Order", order_id)
        if not order.invoice:
            raise NotFoundException("Invoice for order", order_id)

        invoice = order.invoice
        if invoice.balance_amount <= 0:
            raise ClinicalValidationError("Invoice is already fully paid.")

        pay_amount = min(payment_in.amount, invoice.balance_amount)
        payment_ref = f"PAY-{secrets.randbelow(900000) + 100000}"

        payment = Payment(
            id=str(uuid.uuid4()),
            invoice_id=invoice.id,
            payment_reference=payment_ref,
            amount=pay_amount,
            payment_method=payment_in.payment_method,
            transaction_id=payment_in.transaction_id,
            received_by_id=receiver_id,
            notes=payment_in.notes
        )
        db.add(payment)

        invoice.paid_amount += pay_amount
        invoice.balance_amount = max(0.0, invoice.total_amount - invoice.paid_amount)
        if invoice.balance_amount == 0:
            invoice.payment_status = PaymentStatusEnum.PAID
        else:
            invoice.payment_status = PaymentStatusEnum.PARTIALLY_PAID

        # Audit
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=receiver_id,
            action=AuditActionEnum.RECORD_PAYMENT,
            entity_name="Payment",
            entity_id=payment.id,
            details=f"Received payment of ${pay_amount:.2f} for invoice {invoice.invoice_number}"
        )
        db.add(audit)

        await db.commit()
        await db.refresh(invoice)
        return invoice
