"""
AcuPath Enterprise LIS - HL7 v2.x Standards Engine
Compliant with Health Level Seven (HL7) Version 2.3.1, 2.4, 2.5, and 2.5.1
Supports Parsing, Serialization, Validation, and Segment Manipulation for Laboratory Data Exchange.
"""

from typing import Dict, List, Optional, Any, Union, Tuple, Set
from datetime import datetime
import re
import enum
import uuid
import logging

logger = logging.getLogger("acupath.hl7")


class HL7Delimiter:
    FIELD = "|"
    COMPONENT = "^"
    REPETITION = "~"
    ESCAPE = "\\"
    SUBCOMPONENT = "&"
    SEGMENT = "\r"


class HL7MessageType(str, enum.Enum):
    ORU_R01 = "ORU^R01^ORU_R01"  # Observation Result Unsolicited
    ORM_O01 = "ORM^O01^ORM_O01"  # Order Message
    OML_O21 = "OML^O21^OML_O21"  # Laboratory Order Message
    ADT_A01 = "ADT^A01^ADT_A01"  # Patient Admit / Registration
    ADT_A08 = "ADT^A08^ADT_A08"  # Patient Information Update
    ADT_A03 = "ADT^A03^ADT_A03"  # Patient Discharge / End Encounter
    ACK = "ACK^R01^ACK"          # General Acknowledgment
    QRY_Q02 = "QRY^Q02^QRY_Q02"  # Query for Results


class HL7SegmentType(str, enum.Enum):
    MSH = "MSH"  # Message Header
    PID = "PID"  # Patient Identification
    PV1 = "PV1"  # Patient Visit
    ORC = "ORC"  # Common Order
    OBR = "OBR"  # Observation Request (Test Header)
    OBX = "OBX"  # Observation / Result Segment
    NTE = "NTE"  # Notes and Comments
    SPM = "SPM"  # Specimen Segment
    SAC = "SAC"  # Specimen Container Detail
    TQ1 = "TQ1"  # Timing / Quantity
    ERR = "ERR"  # Error Segment
    MSA = "MSA"  # Message Acknowledgment


class HL7Field:
    """Represents an HL7 v2 field with component and subcomponent hierarchies."""

    def __init__(self, value: Union[str, List[Any]] = "", delimiters: Optional[HL7Delimiter] = None):
        self.delimiters = delimiters or HL7Delimiter()
        self.raw_value = value if isinstance(value, str) else ""
        self.components: List[str] = []
        self.repetitions: List[List[str]] = []
        self._parse(value)

    def _parse(self, value: Union[str, List[Any]]):
        if isinstance(value, str):
            if self.delimiters.REPETITION in value:
                reps = value.split(self.delimiters.REPETITION)
                for r in reps:
                    self.repetitions.append(r.split(self.delimiters.COMPONENT))
                self.components = self.repetitions[0] if self.repetitions else []
            elif self.delimiters.COMPONENT in value:
                self.components = value.split(self.delimiters.COMPONENT)
                self.repetitions = [self.components]
            else:
                self.components = [value]
                self.repetitions = [[value]]
        elif isinstance(value, list):
            self.components = [str(x) for x in value]
            self.repetitions = [self.components]
            self.raw_value = self.delimiters.COMPONENT.join(self.components)

    def get_component(self, index: int, default: str = "") -> str:
        """1-based component retrieval."""
        idx = index - 1
        if 0 <= idx < len(self.components):
            return self.components[idx]
        return default

    def set_component(self, index: int, value: str):
        """1-based component assignment."""
        idx = index - 1
        while len(self.components) <= idx:
            self.components.append("")
        self.components[idx] = value
        self.raw_value = self.delimiters.COMPONENT.join(self.components)

    def to_hl7(self) -> str:
        if len(self.repetitions) > 1:
            return self.delimiters.REPETITION.join(
                self.delimiters.COMPONENT.join(comp) for comp in self.repetitions
            )
        return self.delimiters.COMPONENT.join(self.components)

    def __str__(self) -> str:
        return self.to_hl7()

    def __repr__(self) -> str:
        return f"<HL7Field: {self.to_hl7()}>"


class HL7Segment:
    """Represents an individual HL7 Segment (e.g. MSH, PID, OBR, OBX)."""

    def __init__(self, segment_name: str, fields: Optional[List[HL7Field]] = None, delimiters: Optional[HL7Delimiter] = None):
        self.name = segment_name.strip().upper()
        self.delimiters = delimiters or HL7Delimiter()
        self.fields: List[HL7Field] = fields or []

    @classmethod
    def from_string(cls, raw_line: str, delimiters: Optional[HL7Delimiter] = None) -> "HL7Segment":
        d = delimiters or HL7Delimiter()
        line = raw_line.strip("\r\n")
        if not line:
            return cls("", [], d)

        parts = line.split(d.FIELD)
        seg_name = parts[0]
        field_objs: List[HL7Field] = []

        if seg_name == "MSH":
            # In MSH, field 1 is the field separator '|' and field 2 is encoding characters
            field_objs.append(HL7Field(d.FIELD, d))
            for p in parts[1:]:
                field_objs.append(HL7Field(p, d))
        else:
            for p in parts[1:]:
                field_objs.append(HL7Field(p, d))

        return cls(seg_name, field_objs, d)

    def get_field(self, index: int, default: str = "") -> str:
        """1-based field retrieval."""
        idx = index if self.name == "MSH" else index - 1
        if 0 <= idx < len(self.fields):
            return self.fields[idx].to_hl7()
        return default

    def get_field_obj(self, index: int) -> Optional[HL7Field]:
        idx = index if self.name == "MSH" else index - 1
        if 0 <= idx < len(self.fields):
            return self.fields[idx]
        return None

    def set_field(self, index: int, value: Union[str, HL7Field]):
        idx = index if self.name == "MSH" else index - 1
        field_obj = value if isinstance(value, HL7Field) else HL7Field(str(value), self.delimiters)
        while len(self.fields) <= idx:
            self.fields.append(HL7Field("", self.delimiters))
        self.fields[idx] = field_obj

    def to_hl7(self) -> str:
        if self.name == "MSH":
            enc = self.fields[1].to_hl7() if len(self.fields) > 1 else "^~\\&"
            rest = [f.to_hl7() for f in self.fields[2:]]
            return f"MSH|{enc}|" + "|".join(rest)
        return self.name + "|" + "|".join(f.to_hl7() for f in self.fields)

    def __str__(self) -> str:
        return self.to_hl7()


class HL7Message:
    """Represents a complete HL7 v2 Message composed of sequential segments."""

    def __init__(self, segments: Optional[List[HL7Segment]] = None, delimiters: Optional[HL7Delimiter] = None):
        self.delimiters = delimiters or HL7Delimiter()
        self.segments: List[HL7Segment] = segments or []

    @classmethod
    def from_string(cls, raw_hl7_text: str) -> "HL7Message":
        delims = HL7Delimiter()
        raw_clean = raw_hl7_text.replace("\r\n", "\r").replace("\n", "\r")
        lines = [l for l in raw_clean.split("\r") if l.strip()]
        segments: List[HL7Segment] = []

        for line in lines:
            if line.startswith("MSH"):
                if len(line) >= 8:
                    delims.FIELD = line[3]
                    delims.COMPONENT = line[4]
                    delims.REPETITION = line[5]
                    delims.ESCAPE = line[6]
                    delims.SUBCOMPONENT = line[7]
            seg = HL7Segment.from_string(line, delims)
            if seg.name:
                segments.append(seg)

        return cls(segments, delims)

    def get_segments(self, segment_name: str) -> List[HL7Segment]:
        name_upper = segment_name.strip().upper()
        return [s for s in self.segments if s.name == name_upper]

    def get_first_segment(self, segment_name: str) -> Optional[HL7Segment]:
        segs = self.get_segments(segment_name)
        return segs[0] if segs else None

    def add_segment(self, segment: HL7Segment):
        self.segments.append(segment)

    def to_hl7(self) -> str:
        return "\r".join(s.to_hl7() for s in self.segments) + "\r"

    @property
    def message_control_id(self) -> str:
        msh = self.get_first_segment("MSH")
        return msh.get_field(10) if msh else ""

    @property
    def message_type(self) -> str:
        msh = self.get_first_segment("MSH")
        return msh.get_field(9) if msh else ""

    @property
    def sending_facility(self) -> str:
        msh = self.get_first_segment("MSH")
        return msh.get_field(4) if msh else ""

    @property
    def receiving_facility(self) -> str:
        msh = self.get_first_segment("MSH")
        return msh.get_field(6) if msh else ""
