"""initial enterprise schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-29 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, default='PATIENT'),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('license_number', sa.String(100), nullable=True),
        sa.Column('signature_image_url', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_role', 'users', ['role'])

    # Patients
    op.create_table(
        'patients',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('patient_code', sa.String(50), unique=True, nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), unique=True, nullable=True),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(20), nullable=False),
        sa.Column('blood_group', sa.String(20), nullable=False, default='UNKNOWN'),
        sa.Column('phone', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('emergency_contact_name', sa.String(100), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(50), nullable=True),
        sa.Column('medical_history_notes', sa.Text(), nullable=True),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_patients_patient_code', 'patients', ['patient_code'])
    op.create_index('ix_patients_first_name', 'patients', ['first_name'])
    op.create_index('ix_patients_last_name', 'patients', ['last_name'])
    op.create_index('ix_patients_phone', 'patients', ['phone'])

    # Test Categories
    op.create_table(
        'test_categories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('code', sa.String(50), unique=True, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
    )

    # Tests
    op.create_table(
        'tests',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('category_id', sa.String(36), sa.ForeignKey('test_categories.id'), nullable=False),
        sa.Column('test_code', sa.String(50), unique=True, nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('short_name', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('specimen_type', sa.String(50), nullable=False),
        sa.Column('container_type', sa.String(50), nullable=False),
        sa.Column('price', sa.Float(), nullable=False, default=0.0),
        sa.Column('turnaround_time_hours', sa.Integer(), default=24),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_tests_test_code', 'tests', ['test_code'])
    op.create_index('ix_tests_name', 'tests', ['name'])

    # Test Parameters
    op.create_table(
        'test_parameters',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('test_id', sa.String(36), sa.ForeignKey('tests.id'), nullable=False),
        sa.Column('parameter_code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('unit', sa.String(50), nullable=True),
        sa.Column('data_type', sa.String(50), default='NUMERIC', nullable=False),
        sa.Column('display_order', sa.Integer(), default=0),
        sa.Column('formula_expression', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
    )

    # Reference Ranges
    op.create_table(
        'reference_ranges',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('parameter_id', sa.String(36), sa.ForeignKey('test_parameters.id'), nullable=False),
        sa.Column('gender', sa.String(20), default='BOTH', nullable=False),
        sa.Column('age_min_days', sa.Integer(), default=0, nullable=False),
        sa.Column('age_max_days', sa.Integer(), default=43800, nullable=False),
        sa.Column('normal_min', sa.Float(), nullable=True),
        sa.Column('normal_max', sa.Float(), nullable=True),
        sa.Column('critical_low', sa.Float(), nullable=True),
        sa.Column('critical_high', sa.Float(), nullable=True),
        sa.Column('qualitative_normal', sa.String(100), nullable=True),
        sa.Column('interpretation_text', sa.Text(), nullable=True),
    )

    # Orders
    op.create_table(
        'orders',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_number', sa.String(50), unique=True, nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id'), nullable=False),
        sa.Column('referring_doctor', sa.String(150), nullable=True),
        sa.Column('clinical_notes', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(50), default='ROUTINE', nullable=False),
        sa.Column('status', sa.String(50), default='PENDING', nullable=False),
        sa.Column('subtotal', sa.Float(), default=0.0, nullable=False),
        sa.Column('discount_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('tax_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('total_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_orders_order_number', 'orders', ['order_number'])
    op.create_index('ix_orders_patient_id', 'orders', ['patient_id'])
    op.create_index('ix_orders_status', 'orders', ['status'])

    # Samples
    op.create_table(
        'samples',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('barcode', sa.String(50), unique=True, nullable=False),
        sa.Column('specimen_type', sa.String(50), nullable=False),
        sa.Column('container_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='PENDING_COLLECTION', nullable=False),
        sa.Column('collected_at', sa.DateTime(), nullable=True),
        sa.Column('collected_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('received_at', sa.DateTime(), nullable=True),
        sa.Column('received_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_samples_barcode', 'samples', ['barcode'])
    op.create_index('ix_samples_status', 'samples', ['status'])

    # Sample Status History
    op.create_table(
        'sample_status_history',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('sample_id', sa.String(36), sa.ForeignKey('samples.id'), nullable=False),
        sa.Column('from_status', sa.String(50), nullable=True),
        sa.Column('to_status', sa.String(50), nullable=False),
        sa.Column('changed_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    # Order Items
    op.create_table(
        'order_items',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('test_id', sa.String(36), sa.ForeignKey('tests.id'), nullable=False),
        sa.Column('sample_id', sa.String(36), sa.ForeignKey('samples.id'), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('status', sa.String(50), default='PENDING', nullable=False),
    )

    # Test Results
    op.create_table(
        'test_results',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_item_id', sa.String(36), sa.ForeignKey('order_items.id'), nullable=False),
        sa.Column('parameter_id', sa.String(36), sa.ForeignKey('test_parameters.id'), nullable=False),
        sa.Column('sample_id', sa.String(36), sa.ForeignKey('samples.id'), nullable=False),
        sa.Column('numeric_value', sa.Float(), nullable=True),
        sa.Column('text_value', sa.String(255), nullable=True),
        sa.Column('formatted_value', sa.String(255), nullable=False),
        sa.Column('flag', sa.String(50), default='NORMAL', nullable=False),
        sa.Column('reference_range_display', sa.String(255), nullable=True),
        sa.Column('is_abnormal', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_critical', sa.Boolean(), default=False, nullable=False),
        sa.Column('technician_notes', sa.Text(), nullable=True),
        sa.Column('entered_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('entered_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Lab Reports
    op.create_table(
        'lab_reports',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('orders.id'), unique=True, nullable=False),
        sa.Column('report_number', sa.String(50), unique=True, nullable=False),
        sa.Column('status', sa.String(50), default='DRAFT', nullable=False),
        sa.Column('verified_by_doctor_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('pathologist_comments', sa.Text(), nullable=True),
        sa.Column('clinical_interpretation', sa.Text(), nullable=True),
        sa.Column('pdf_filename', sa.String(255), nullable=True),
        sa.Column('pdf_path', sa.Text(), nullable=True),
        sa.Column('verification_qr_hash', sa.String(100), unique=True, nullable=False),
        sa.Column('download_count', sa.Integer(), default=0, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Invoices
    op.create_table(
        'invoices',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('orders.id'), unique=True, nullable=False),
        sa.Column('invoice_number', sa.String(50), unique=True, nullable=False),
        sa.Column('subtotal', sa.Float(), default=0.0, nullable=False),
        sa.Column('discount_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('tax_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('total_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('paid_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('balance_amount', sa.Float(), default=0.0, nullable=False),
        sa.Column('payment_status', sa.String(50), default='UNPAID', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Payments
    op.create_table(
        'payments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('invoice_id', sa.String(36), sa.ForeignKey('invoices.id'), nullable=False),
        sa.Column('payment_reference', sa.String(100), unique=True, nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(50), default='CASH', nullable=False),
        sa.Column('transaction_id', sa.String(100), nullable=True),
        sa.Column('received_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=False),
    )

    # Audit Logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('entity_name', sa.String(100), nullable=False),
        sa.Column('entity_id', sa.String(100), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('old_state', sa.JSON(), nullable=True),
        sa.Column('new_state', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(255), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('payments')
    op.drop_table('invoices')
    op.drop_table('lab_reports')
    op.drop_table('test_results')
    op.drop_table('order_items')
    op.drop_table('sample_status_history')
    op.drop_table('samples')
    op.drop_table('orders')
    op.drop_table('reference_ranges')
    op.drop_table('test_parameters')
    op.drop_table('tests')
    op.drop_table('test_categories')
    op.drop_table('patients')
    op.drop_table('users')
