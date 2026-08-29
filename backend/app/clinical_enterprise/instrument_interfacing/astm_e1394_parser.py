"""
AcuPath Enterprise LIS - ASTM E1394-97 High-Level Message Protocol
Parses Header (H), Patient (P), Order (O), Result (R), Comment (C), Scientific (S), and Terminator (L) records.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import datetime
import enum


class ASTMRecordType(str, enum.Enum):
    HEADER = "H"
    PATIENT = "P"
    ORDER = "O"
    RESULT = "R"
    COMMENT = "C"
    SCIENTIFIC = "S"
    TERMINATOR = "L"


@dataclass
class ASTMResultRecord:
    sequence_number: int = 1
    universal_test_id: str = ""
    measurement_value: str = ""
    units: str = ""
    reference_ranges: str = ""
    abnormal_flag: str = ""  # N, L, H, LL, HH, A
    result_status: str = "F"  # F = Final, P = Preliminary, C = Corrected
    operator_id: str = ""
    test_datetime: Optional[datetime.datetime] = None
    instrument_id: str = ""


@dataclass
class ASTMOrderRecord:
    sequence_number: int = 1
    specimen_id: str = ""
    instrument_specimen_id: str = ""
    universal_test_id: str = ""
    priority: str = "R"  # R = Routine, S = STAT, U = Urgent
    requested_datetime: Optional[datetime.datetime] = None
    collection_datetime: Optional[datetime.datetime] = None
    specimen_action_code: str = "N"  # N = New, C = Cancel
    specimen_type: str = ""
    results: List[ASTMResultRecord] = field(default_factory=list)


@dataclass
class ASTMPatientRecord:
    sequence_number: int = 1
    patient_id: str = ""
    patient_name: str = ""
    birthdate: str = ""
    gender: str = ""
    attending_physician: str = ""
    orders: List[ASTMOrderRecord] = field(default_factory=list)


@dataclass
class ASTMMessage:
    sender_name: str = ""
    receiver_name: str = ""
    processing_id: str = "P"  # P = Production, D = Debug, T = Training
    version_number: str = "1394-97"
    message_datetime: Optional[datetime.datetime] = None
    patients: List[ASTMPatientRecord] = field(default_factory=list)


class ASTME1394Parser:
    """Parser for parsing ASTM 1394 records into strongly typed message objects."""

    @staticmethod
    def parse_message(records: List[str], field_delimiter: str = "|", repeat_delimiter: str = "\\", component_delimiter: str = "^", escape_delimiter: str = "&") -> ASTMMessage:
        msg = ASTMMessage()
        current_patient: Optional[ASTMPatientRecord] = None
        current_order: Optional[ASTMOrderRecord] = None

        for rec in records:
            if not rec.strip():
                continue
            fields = rec.strip().split(field_delimiter)
            rec_type = fields[0].strip().upper()

            if rec_type == "H":
                msg.sender_name = fields[4] if len(fields) > 4 else "ANALYZER"
                msg.receiver_name = fields[9] if len(fields) > 9 else "ACUPATH_LIS"

            elif rec_type == "P":
                current_patient = ASTMPatientRecord(
                    sequence_number=int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else 1,
                    patient_id=fields[2] if len(fields) > 2 else (fields[3] if len(fields) > 3 else ""),
                    patient_name=fields[5] if len(fields) > 5 else "",
                    birthdate=fields[7] if len(fields) > 7 else "",
                    gender=fields[8] if len(fields) > 8 else "U"
                )
                msg.patients.append(current_patient)
                current_order = None

            elif rec_type == "O":
                current_order = ASTMOrderRecord(
                    sequence_number=int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else 1,
                    specimen_id=fields[2] if len(fields) > 2 else "",
                    instrument_specimen_id=fields[3] if len(fields) > 3 else "",
                    universal_test_id=fields[4] if len(fields) > 4 else "",
                    priority=fields[5] if len(fields) > 5 else "R",
                    specimen_type=fields[15] if len(fields) > 15 else "WHOLE_BLOOD"
                )
                if current_patient:
                    current_patient.orders.append(current_order)
                else:
                    # Anonymous patient container
                    current_patient = ASTMPatientRecord()
                    current_patient.orders.append(current_order)
                    msg.patients.append(current_patient)

            elif rec_type == "R":
                res = ASTMResultRecord(
                    sequence_number=int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else 1,
                    universal_test_id=fields[2] if len(fields) > 2 else "",
                    measurement_value=fields[3] if len(fields) > 3 else "",
                    units=fields[4] if len(fields) > 4 else "",
                    reference_ranges=fields[5] if len(fields) > 5 else "",
                    abnormal_flag=fields[6] if len(fields) > 6 else "N",
                    result_status=fields[8] if len(fields) > 8 else "F",
                    operator_id=fields[10] if len(fields) > 10 else "",
                    instrument_id=fields[13] if len(fields) > 13 else ""
                )
                if current_order:
                    current_order.results.append(res)

        return msg
