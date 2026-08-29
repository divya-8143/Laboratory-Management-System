export type RoleType = 'ADMIN' | 'RECEPTIONIST' | 'TECHNICIAN' | 'DOCTOR' | 'PATIENT';

export type GenderType = 'MALE' | 'FEMALE' | 'OTHER';

export type SpecimenType =
  | 'WHOLE_BLOOD'
  | 'SERUM'
  | 'PLASMA'
  | 'URINE'
  | 'CSF'
  | 'STOOL'
  | 'SPUTUM'
  | 'SWAB'
  | 'SYNOVIAL_FLUID';

export type ContainerType =
  | 'EDTA_LAVENDER'
  | 'SST_GOLD_YELLOW'
  | 'PLAIN_RED'
  | 'SODIUM_CITRATE_BLUE'
  | 'SODIUM_FLUORIDE_GREY'
  | 'HEPARIN_GREEN'
  | 'STERILE_CONTAINER';

export type OrderPriority = 'ROUTINE' | 'URGENT' | 'STAT';

export type OrderStatus = 'PENDING' | 'SAMPLE_COLLECTED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';

export type SampleStatus = 'PENDING_COLLECTION' | 'COLLECTED' | 'RECEIVED_IN_LAB' | 'PROCESSING' | 'COMPLETED' | 'REJECTED';

export type ResultFlag = 'NORMAL' | 'LOW' | 'HIGH' | 'CRITICAL_LOW' | 'CRITICAL_HIGH' | 'ABNORMAL';

export type ReportStatus = 'DRAFT' | 'VERIFIED' | 'PUBLISHED' | 'AMENDED';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: RoleType;
  phone?: string;
  department?: string;
  license_number?: string;
  signature_image_url?: string;
  is_active: boolean;
  created_at: string;
}

export interface Patient {
  id: string;
  patient_code: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: GenderType;
  blood_group: string;
  phone: string;
  email?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  medical_history_notes?: string;
  age_years: number;
  created_at: string;
}

export interface ReferenceRange {
  id: string;
  parameter_id: string;
  gender: string;
  age_min_days: number;
  age_max_days: number;
  normal_min?: number;
  normal_max?: number;
  critical_low?: number;
  critical_high?: number;
  qualitative_normal?: string;
}

export interface TestParameter {
  id: string;
  test_id: string;
  parameter_code: string;
  name: string;
  unit?: string;
  data_type: string;
  display_order: number;
  reference_ranges: ReferenceRange[];
}

export interface TestCategory {
  id: string;
  name: string;
  code: string;
  description?: string;
}

export interface Test {
  id: string;
  category_id: string;
  test_code: string;
  name: string;
  short_name?: string;
  description?: string;
  specimen_type: SpecimenType;
  container_type: ContainerType;
  price: number;
  turnaround_time_hours: number;
  is_active: boolean;
  category?: TestCategory;
  parameters: TestParameter[];
}

export interface OrderItem {
  id: string;
  order_id: string;
  test_id: string;
  test?: Test;
  sample_id?: string;
  price: number;
  status: string;
}

export interface Payment {
  id: string;
  payment_reference: string;
  amount: number;
  payment_method: string;
  paid_at: string;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  subtotal: number;
  discount_amount: number;
  tax_amount: number;
  total_amount: number;
  paid_amount: number;
  balance_amount: number;
  payment_status: 'UNPAID' | 'PARTIALLY_PAID' | 'PAID';
  payments: Payment[];
}

export interface SampleStatusHistory {
  id: string;
  from_status?: string;
  to_status: string;
  comments?: string;
  timestamp: string;
  changed_by?: User;
}

export interface Sample {
  id: string;
  order_id: string;
  barcode: string;
  specimen_type: SpecimenType;
  container_type: ContainerType;
  status: SampleStatus;
  collected_at?: string;
  collector?: User;
  received_at?: string;
  rejection_reason?: string;
  notes?: string;
  status_history: SampleStatusHistory[];
}

export interface TestResult {
  id: string;
  order_item_id: string;
  parameter_id: string;
  parameter?: TestParameter;
  numeric_value?: number;
  text_value?: string;
  formatted_value: string;
  flag: ResultFlag;
  reference_range_display?: string;
  is_abnormal: boolean;
  is_critical: boolean;
  technician_notes?: string;
  entered_at: string;
}

export interface LabReport {
  id: string;
  order_id: string;
  report_number: string;
  status: ReportStatus;
  verified_by_doctor?: User;
  verified_at?: string;
  pathologist_comments?: string;
  clinical_interpretation?: string;
  pdf_filename?: string;
  verification_qr_hash: string;
  download_count: number;
  created_at: string;
}

export interface Order {
  id: string;
  order_number: string;
  patient_id: string;
  patient?: Patient;
  referring_doctor?: string;
  clinical_notes?: string;
  priority: OrderPriority;
  status: OrderStatus;
  subtotal: number;
  discount_amount: number;
  tax_amount: number;
  total_amount: number;
  order_items: OrderItem[];
  invoice?: Invoice;
  lab_report?: LabReport;
  created_at: string;
}

export interface KPIOverview {
  total_patients: number;
  total_orders: number;
  total_tests_conducted: number;
  total_revenue: number;
  total_collected_revenue: number;
  total_outstanding_balance: number;
  pending_orders: number;
  processing_orders: number;
  completed_orders: number;
  cancelled_orders: number;
  samples_pending_collection: number;
  samples_collected: number;
  samples_in_lab: number;
  samples_rejected: number;
  avg_turnaround_time_hours: number;
}

export interface MostRequestedTest {
  test_id: string;
  test_code: string;
  test_name: string;
  category_name: string;
  order_count: number;
  total_revenue_generated: number;
}

export interface RevenueTrend {
  period: string;
  gross_revenue: number;
  net_collected: number;
  order_count: number;
}

export interface CategoryDistribution {
  category_name: string;
  category_code: string;
  test_count: number;
  percentage: number;
}

export interface AuditLogItem {
  id: string;
  user_id?: string;
  user?: User;
  action: string;
  entity_name: string;
  entity_id?: string;
  details?: string;
  ip_address?: string;
  timestamp: string;
}
