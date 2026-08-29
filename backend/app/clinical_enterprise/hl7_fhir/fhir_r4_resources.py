"""
AcuPath Enterprise LIS - HL7 FHIR Release 4 (R4) Schemas
Defines full clinical resource models for:
- DiagnosticReport
- Observation
- Specimen
- Patient
- ServiceRequest
- Practitioner
- Organization
- Bundle
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class FHIRCoding(BaseModel):
    system: Optional[str] = "http://loinc.org"
    version: Optional[str] = "2.74"
    code: str
    display: Optional[str] = None
    userSelected: Optional[bool] = False


class FHIRCodeableConcept(BaseModel):
    coding: List[FHIRCoding] = []
    text: Optional[str] = None


class FHIRIdentifier(BaseModel):
    use: Optional[str] = "official"  # usual | official | temp | secondary | old
    type: Optional[FHIRCodeableConcept] = None
    system: Optional[str] = "https://acupath.com/identifiers"
    value: str
    assigner: Optional[Dict[str, str]] = None


class FHIRReference(BaseModel):
    reference: str  # e.g. "Patient/PAT-12345"
    type: Optional[str] = None
    display: Optional[str] = None


class FHIRQuantity(BaseModel):
    value: float
    comparator: Optional[str] = None  # < | <= | >= | >
    unit: str
    system: Optional[str] = "http://unitsofmeasure.org"
    code: Optional[str] = None


class FHIRReferenceRange(BaseModel):
    low: Optional[FHIRQuantity] = None
    high: Optional[FHIRQuantity] = None
    type: Optional[FHIRCodeableConcept] = None
    appliesTo: List[FHIRCodeableConcept] = []
    age: Optional[Dict[str, Any]] = None
    text: Optional[str] = None


class FHIRObservation(BaseModel):
    resourceType: str = "Observation"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identifier: List[FHIRIdentifier] = []
    status: str = "final"  # registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown
    category: List[FHIRCodeableConcept] = [
        FHIRCodeableConcept(
            coding=[FHIRCoding(system="http://terminology.hl7.org/CodeSystem/observation-category", code="laboratory", display="Laboratory")]
        )
    ]
    code: FHIRCodeableConcept
    subject: FHIRReference
    effectiveDateTime: Optional[str] = None
    issued: Optional[str] = None
    performer: List[FHIRReference] = []
    valueQuantity: Optional[FHIRQuantity] = None
    valueString: Optional[str] = None
    valueCodeableConcept: Optional[FHIRCodeableConcept] = None
    interpretation: List[FHIRCodeableConcept] = []
    note: List[Dict[str, str]] = []
    referenceRange: List[FHIRReferenceRange] = []
    specimen: Optional[FHIRReference] = None


class FHIRSpecimen(BaseModel):
    resourceType: str = "Specimen"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identifier: List[FHIRIdentifier] = []
    accessionIdentifier: Optional[FHIRIdentifier] = None
    status: str = "available"  # available | unavailable | unsatisfactory | entered-in-error
    type: Optional[FHIRCodeableConcept] = None
    subject: FHIRReference
    receivedTime: Optional[str] = None
    collection: Optional[Dict[str, Any]] = None
    container: List[Dict[str, Any]] = []


class FHIRDiagnosticReport(BaseModel):
    resourceType: str = "DiagnosticReport"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identifier: List[FHIRIdentifier] = []
    basedOn: List[FHIRReference] = []
    status: str = "final"  # registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown
    category: List[FHIRCodeableConcept] = [
        FHIRCodeableConcept(
            coding=[FHIRCoding(system="http://terminology.hl7.org/CodeSystem/v2-0074", code="LAB", display="Laboratory")]
        )
    ]
    code: FHIRCodeableConcept
    subject: FHIRReference
    effectiveDateTime: Optional[str] = None
    issued: Optional[str] = None
    performer: List[FHIRReference] = []
    resultsInterpreter: List[FHIRReference] = []
    specimen: List[FHIRReference] = []
    result: List[FHIRReference] = []  # References to Observation resources
    conclusion: Optional[str] = None
    conclusionCode: List[FHIRCodeableConcept] = []
    presentedForm: List[Dict[str, Any]] = []  # PDF attachments in base64


class FHIRBundle(BaseModel):
    resourceType: str = "Bundle"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "document"  # document | message | transaction | transaction-response | batch | searchset | collection
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    entry: List[Dict[str, Any]] = []
