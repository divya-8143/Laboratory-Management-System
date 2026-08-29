"""
AcuPath Enterprise LIS - HL7 Message Builder
Constructs standardized ORU_R01, ORM_O01, OML_O21, ADT_A01, ADT_A08 clinical messages.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import uuid

from .hl7_v2_parser import HL7Message, HL7Segment, HL7Delimiter


class HL7MessageBuilder:
    """Builder class for constructing HL7 laboratory messages according to CLSI & IHE LAW profiles."""

    def __init__(
        self,
        sending_application: str = "ACUPATH_LIS",
        sending_facility: str = "ACUPATH_CENTRAL_LAB",
        receiving_application: str = "HOSPITAL_EMR",
        receiving_facility: str = "MAIN_CAMPUS",
        version: str = "2.5.1"
    ):
        self.sending_app = sending_application
        self.sending_fac = sending_facility
        self.recv_app = receiving_application
        self.recv_fac = receiving_facility
        self.version = version

    def create_msh_segment(self, message_type: str, control_id: Optional[str] = None) -> HL7Segment:
        cid = control_id or f"MSG-{uuid.uuid4().hex[:12].upper()}"
        now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        msh = HL7Segment("MSH")
        msh.set_field(1, "|")
        msh.set_field(2, "^~\\&")
        msh.set_field(3, self.sending_app)
        msh.set_field(4, self.sending_fac)
        msh.set_field(5, self.recv_app)
        msh.set_field(6, self.recv_fac)
        msh.set_field(7, now_str)
        msh.set_field(8, "")
        msh.set_field(9, message_type)
        msh.set_field(10, cid)
        msh.set_field(11, "P")  # Production
        msh.set_field(12, self.version)
        msh.set_field(15, "NE")  # Accept ACK Condition
        msh.set_field(16, "AL")  # Application ACK Condition
        msh.set_field(18, "UNICODE UTF-8")
        return msh

    def create_pid_segment(
        self,
        patient_id: str,
        first_name: str,
        last_name: str,
        date_of_birth: Union[datetime, str],
        gender: str,
        address: str = "",
        phone: str = "",
        national_id: str = "",
        blood_group: str = ""
    ) -> HL7Segment:
        pid = HL7Segment("PID")
        pid.set_field(1, "1")  # Set ID
        pid.set_field(2, patient_id)
        pid.set_field(3, f"{patient_id}^^^ACUPATH^MR")  # Internal MRN
        if national_id:
            pid.set_field(4, f"{national_id}^^^GOV^SS")

        # Name: Last^First^Middle^Suffix^Prefix
        pid.set_field(5, f"{last_name}^{first_name}^^^")

        # DOB
        if isinstance(date_of_birth, datetime):
            dob_str = date_of_birth.strftime("%Y%m%d")
        else:
            dob_str = str(date_of_birth).replace("-", "")[:8]
        pid.set_field(7, dob_str)

        # Sex (M/F/O/U)
        pid.set_field(8, gender.upper()[:1] if gender else "U")

        # Address: Street^Other^City^State^Zip^Country
        if address:
            pid.set_field(11, f"{address}^^^^USA")

        # Phone
        if phone:
            pid.set_field(13, f"{phone}^PRN^PH^^^")

        return pid

    def create_pv1_segment(
        self,
        visit_number: str,
        patient_class: str = "O",  # O = Outpatient, I = Inpatient, E = Emergency
        assigned_location: str = "LAB_OPD_01",
        referring_doctor: str = ""
    ) -> HL7Segment:
        pv1 = HL7Segment("PV1")
        pv1.set_field(1, "1")
        pv1.set_field(2, patient_class)
        pv1.set_field(3, assigned_location)
        if referring_doctor:
            pv1.set_field(8, f"DOC001^{referring_doctor}^^^^^MD")
        pv1.set_field(19, visit_number)
        return pv1

    def create_orc_segment(
        self,
        order_control: str = "RE",  # NW = New Order, RE = Observations/Results, SC = In Process
        placer_order_number: str = "",
        filler_order_number: str = "",
        order_status: str = "CM",    # IP = In Process, CM = Completed, CA = Cancelled
        order_datetime: Optional[datetime] = None
    ) -> HL7Segment:
        now_dt = order_datetime or datetime.utcnow()
        dt_str = now_dt.strftime("%Y%m%d%H%M%S")

        orc = HL7Segment("ORC")
        orc.set_field(1, order_control)
        orc.set_field(2, f"{placer_order_number}^EMR" if placer_order_number else "")
        orc.set_field(3, f"{filler_order_number}^ACUPATH" if filler_order_number else "")
        orc.set_field(5, order_status)
        orc.set_field(9, dt_str)
        return orc

    def create_obr_segment(
        self,
        set_id: int,
        placer_order_number: str,
        filler_order_number: str,
        universal_service_id: str,  # Test Code^Test Name^Coding System (e.g. LOINC)
        specimen_received_datetime: Optional[datetime] = None,
        observation_datetime: Optional[datetime] = None,
        result_status: str = "F",    # F = Final, C = Corrected, P = Preliminary
        pathologist_signature: str = ""
    ) -> HL7Segment:
        obr = HL7Segment("OBR")
        obr.set_field(1, str(set_id))
        obr.set_field(2, f"{placer_order_number}^EMR" if placer_order_number else "")
        obr.set_field(3, f"{filler_order_number}^ACUPATH" if filler_order_number else "")
        obr.set_field(4, universal_service_id)

        rec_dt = specimen_received_datetime or datetime.utcnow()
        obs_dt = observation_datetime or datetime.utcnow()

        obr.set_field(7, obs_dt.strftime("%Y%m%d%H%M%S"))
        obr.set_field(14, rec_dt.strftime("%Y%m%d%H%M%S"))
        obr.set_field(22, obs_dt.strftime("%Y%m%d%H%M%S"))
        obr.set_field(25, result_status)
        if pathologist_signature:
            obr.set_field(32, f"DOC999^{pathologist_signature}^^^^^MD")
        return obr

    def create_obx_segment(
        self,
        set_id: int,
        value_type: str,  # NM = Numeric, ST = String, CE = Coded Entry, TX = Text
        observation_identifier: str,  # Code^Name^System
        sub_id: str,
        observation_value: str,
        units: str = "",
        reference_range: str = "",
        abnormal_flags: str = "",  # N = Normal, L = Low, H = High, LL = Critical Low, HH = Critical High, A = Abnormal
        observation_result_status: str = "F",
        analysis_datetime: Optional[datetime] = None,
        instrument_id: str = "SYSMEX-XN1000"
    ) -> HL7Segment:
        dt_str = (analysis_datetime or datetime.utcnow()).strftime("%Y%m%d%H%M%S")

        obx = HL7Segment("OBX")
        obx.set_field(1, str(set_id))
        obx.set_field(2, value_type)
        obx.set_field(3, observation_identifier)
        obx.set_field(4, str(sub_id))
        obx.set_field(5, str(observation_value))
        obx.set_field(6, f"{units}^{units}^UCUM" if units else "")
        obx.set_field(7, reference_range)
        obx.set_field(8, abnormal_flags)
        obx.set_field(11, observation_result_status)
        obx.set_field(14, dt_str)
        obx.set_field(18, instrument_id)
        return obx

    def create_spm_segment(
        self,
        set_id: int,
        specimen_id: str,
        specimen_type: str,
        collection_datetime: Optional[datetime] = None,
        source_site: str = "ANTECUBITAL_VEIN"
    ) -> HL7Segment:
        dt_str = (collection_datetime or datetime.utcnow()).strftime("%Y%m%d%H%M%S")

        spm = HL7Segment("SPM")
        spm.set_field(1, str(set_id))
        spm.set_field(2, f"{specimen_id}^ACUPATH_BARCODE")
        spm.set_field(4, f"{specimen_type}^{specimen_type}^HL70487")
        spm.set_field(8, f"{source_site}^Left Arm^SNOMED")
        spm.set_field(17, dt_str)
        return spm
