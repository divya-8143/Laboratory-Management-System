import uuid
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from sqlalchemy.orm import selectinload

from app.models.patient import Patient
from app.models.user import User, RoleType
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.patient import PatientCreate, PatientUpdate
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundException, ConflictException


class PatientService:
    @staticmethod
    async def generate_patient_code(db: AsyncSession) -> str:
        """Generate formatted unique code: PAT-YYYY-XXXXX"""
        year = datetime.utcnow().year
        prefix = f"PAT-{year}-"
        result = await db.execute(
            select(func.count(Patient.id)).where(Patient.patient_code.like(f"{prefix}%"))
        )
        count = result.scalar() or 0
        return f"{prefix}{count + 1:04d}"

    @staticmethod
    async def create_patient(
        db: AsyncSession,
        patient_in: PatientCreate,
        creator_id: Optional[str] = None
    ) -> Patient:
        # Check duplicate phone or email if provided
        if patient_in.email:
            existing = await db.execute(select(Patient).where(Patient.email == patient_in.email.lower()))
            if existing.scalars().first():
                raise ConflictException(f"Patient with email '{patient_in.email}' already exists.")

        patient_code = await PatientService.generate_patient_code(db)
        user_id = None

        # Optionally create portal user account
        if patient_in.create_portal_account and patient_in.email and patient_in.portal_password:
            portal_user = User(
                id=str(uuid.uuid4()),
                email=patient_in.email.lower().strip(),
                hashed_password=get_password_hash(patient_in.portal_password),
                first_name=patient_in.first_name,
                last_name=patient_in.last_name,
                role=RoleType.PATIENT,
                phone=patient_in.phone,
                is_active=True
            )
            db.add(portal_user)
            await db.flush()
            user_id = portal_user.id

        patient = Patient(
            id=str(uuid.uuid4()),
            patient_code=patient_code,
            user_id=user_id,
            first_name=patient_in.first_name.strip(),
            last_name=patient_in.last_name.strip(),
            date_of_birth=patient_in.date_of_birth,
            gender=patient_in.gender,
            blood_group=patient_in.blood_group,
            phone=patient_in.phone.strip(),
            email=patient_in.email.lower().strip() if patient_in.email else None,
            address=patient_in.address,
            city=patient_in.city,
            postal_code=patient_in.postal_code,
            emergency_contact_name=patient_in.emergency_contact_name,
            emergency_contact_phone=patient_in.emergency_contact_phone,
            medical_history_notes=patient_in.medical_history_notes,
            allergies=patient_in.allergies
        )
        db.add(patient)

        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=creator_id,
            action=AuditActionEnum.CREATE_PATIENT,
            entity_name="Patient",
            entity_id=patient.id,
            details=f"Registered patient {patient.full_name} ({patient.patient_code})"
        )
        db.add(audit)

        await db.commit()
        await db.refresh(patient)
        return patient

    @staticmethod
    async def get_patient_by_id(db: AsyncSession, patient_id: str) -> Optional[Patient]:
        result = await db.execute(
            select(Patient)
            .options(selectinload(Patient.orders))
            .where(Patient.id == patient_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_patient_by_code(db: AsyncSession, patient_code: str) -> Optional[Patient]:
        result = await db.execute(
            select(Patient)
            .options(selectinload(Patient.orders))
            .where(Patient.patient_code == patient_code.strip().upper())
        )
        return result.scalars().first()

    @staticmethod
    async def list_patients(
        db: AsyncSession,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Patient], int]:
        query = select(Patient)
        count_query = select(func.count(Patient.id))

        if search:
            pattern = f"%{search.strip()}%"
            filter_clause = or_(
                Patient.first_name.ilike(pattern),
                Patient.last_name.ilike(pattern),
                Patient.patient_code.ilike(pattern),
                Patient.phone.ilike(pattern),
                Patient.email.ilike(pattern)
            )
            query = query.where(filter_clause)
            count_query = count_query.where(filter_clause)

        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        offset = (page - 1) * limit
        query = query.order_by(desc(Patient.created_at)).offset(offset).limit(limit)
        result = await db.execute(query)
        patients = list(result.scalars().all())

        return patients, total

    @staticmethod
    async def update_patient(
        db: AsyncSession,
        patient_id: str,
        patient_in: PatientUpdate,
        actor_id: Optional[str] = None
    ) -> Patient:
        patient = await PatientService.get_patient_by_id(db, patient_id)
        if not patient:
            raise NotFoundException("Patient", patient_id)

        update_data = patient_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(patient, key, value)

        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=actor_id,
            action=AuditActionEnum.UPDATE_PATIENT,
            entity_name="Patient",
            entity_id=patient.id,
            details=f"Updated details for patient {patient.full_name} ({patient.patient_code})"
        )
        db.add(audit)

        await db.commit()
        await db.refresh(patient)
        return patient
