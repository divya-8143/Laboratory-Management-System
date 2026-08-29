"""
AcuPath Enterprise LIS - FHIR R4 to Internal ORM Converter
Transforms clinical test orders, samples, and results into standard FHIR R4 JSON bundles.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from .fhir_r4_resources import (
    FHIRDiagnosticReport, FHIRObservation, FHIRSpecimen,
    FHIRCodeableConcept, FHIRCoding, FHIRQuantity, FHIRReferenceRange,
    FHIRReference, FHIRIdentifier, FHIRBundle
)


class FHIRConverterService:
    """Bi-directional translator between AcuPath LIS database models and FHIR R4 Clinical Resources."""

    @staticmethod
    def report_to_fhir_bundle(
        report_data: Dict[str, Any],
        patient_data: Dict[str, Any],
        order_data: Dict[str, Any],
        results_data: List[Dict[str, Any]],
        doctor_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Converts an entire verified laboratory report into a FHIR R4 Document Bundle."""
        bundle_entries = []

        patient_ref = f"Patient/{patient_data.get('id', 'PAT-001')}"
        doctor_ref = f"Practitioner/{doctor_data.get('id', 'DOC-001')}" if doctor_data else "Practitioner/DOC-DEFAULT"

        # 1. Convert Specimen
        specimen_id = order_data.get("samples", [{}])[0].get("id", "SMP-001") if order_data.get("samples") else "SMP-001"
        specimen = FHIRSpecimen(
            id=specimen_id,
            identifier=[FHIRIdentifier(value=order_data.get("samples", [{}])[0].get("barcode", "SMP-BARCODE"))] if order_data.get("samples") else [],
            status="available",
            type=FHIRCodeableConcept(
                coding=[FHIRCoding(code="WHOLE_BLOOD", display="Venous Whole Blood", system="http://snomed.info/sct")]
            ),
            subject=FHIRReference(reference=patient_ref, display=f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}"),
            receivedTime=datetime.utcnow().isoformat() + "Z"
        )
        bundle_entries.append({"fullUrl": f"urn:uuid:{specimen.id}", "resource": specimen.dict(exclude_none=True)})

        # 2. Convert Observations (Results)
        obs_references = []
        for res in results_data:
            param = res.get("parameter", {})
            param_code = param.get("parameter_code", "PARAM")
            param_name = param.get("name", "Test Parameter")
            unit = param.get("unit", "")
            val = res.get("numeric_value")

            flag = res.get("flag", "NORMAL")
            interp_coding = []
            if flag == "HIGH":
                interp_coding = [FHIRCoding(system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", code="H", display="High")]
            elif flag == "LOW":
                interp_coding = [FHIRCoding(system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", code="L", display="Low")]
            elif flag in ["CRITICAL_HIGH", "CRITICAL_LOW"]:
                interp_coding = [FHIRCoding(system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", code="A", display="Critical Abnormal")]

            obs = FHIRObservation(
                id=res.get("id", str(len(obs_references) + 1)),
                identifier=[FHIRIdentifier(value=res.get("id", ""))],
                status="final",
                code=FHIRCodeableConcept(
                    coding=[FHIRCoding(code=param_code, display=param_name, system="http://loinc.org")],
                    text=param_name
                ),
                subject=FHIRReference(reference=patient_ref),
                performer=[FHIRReference(reference=doctor_ref)],
                valueQuantity=FHIRQuantity(value=float(val), unit=unit, code=unit) if val is not None else None,
                valueString=res.get("text_value") if val is None else None,
                interpretation=[FHIRCodeableConcept(coding=interp_coding)] if interp_coding else [],
                effectiveDateTime=res.get("created_at", datetime.utcnow().isoformat() + "Z"),
                specimen=FHIRReference(reference=f"urn:uuid:{specimen.id}")
            )
            bundle_entries.append({"fullUrl": f"urn:uuid:{obs.id}", "resource": obs.dict(exclude_none=True)})
            obs_references.append(FHIRReference(reference=f"urn:uuid:{obs.id}", display=param_name))

        # 3. Convert DiagnosticReport
        report = FHIRDiagnosticReport(
            id=report_data.get("id", "REP-001"),
            identifier=[FHIRIdentifier(value=report_data.get("report_number", "REP-NUMBER"))],
            status="final",
            code=FHIRCodeableConcept(
                coding=[FHIRCoding(code="LAB-REPORT", display="Clinical Laboratory Report", system="http://loinc.org")]
            ),
            subject=FHIRReference(reference=patient_ref, display=f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}"),
            effectiveDateTime=report_data.get("verified_at", datetime.utcnow().isoformat() + "Z"),
            issued=datetime.utcnow().isoformat() + "Z",
            performer=[FHIRReference(reference=doctor_ref)],
            resultsInterpreter=[FHIRReference(reference=doctor_ref)],
            specimen=[FHIRReference(reference=f"urn:uuid:{specimen.id}")],
            result=obs_references,
            conclusion=report_data.get("clinical_interpretation", "Within normal limits.")
        )
        bundle_entries.append({"fullUrl": f"urn:uuid:{report.id}", "resource": report.dict(exclude_none=True)})

        bundle = FHIRBundle(entry=bundle_entries)
        return bundle.dict(exclude_none=True)
