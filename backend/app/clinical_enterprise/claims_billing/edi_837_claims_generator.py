"""
AcuPath Enterprise LIS - HIPAA ANSI X12 837P Professional Health Care Claim Generator
Generates electronic insurance claims for clinical laboratory services.
"""

from typing import Dict, List, Optional, Any
import datetime
import uuid


class EDI837ClaimsGenerator:
    """Constructs ANSI X12 837P electronic claim transactions."""

    @staticmethod
    def generate_837p_claim_file(
        submitter_id: str,
        receiver_id: str,
        billing_provider: Dict[str, Any],
        subscriber_patient: Dict[str, Any],
        claim_lines: List[Dict[str, Any]]
    ) -> str:
        control_number = f"{uuid.uuid4().hex[:9].upper()}"
        today_str = datetime.date.today().strftime("%Y%m%d")
        time_str = datetime.datetime.now().strftime("%H%M")

        segments = []
        # Interchange Control Header (ISA)
        segments.append(f"ISA*00*          *00*          *ZZ*{submitter_id:<15}*ZZ*{receiver_id:<15}*{today_str[2:]}*{time_str}*^*00501*{control_number}*0*P*:~")
        # Functional Group Header (GS)
        segments.append(f"GS*HC*{submitter_id}*{receiver_id}*{today_str}*{time_str}*1*X*005010X222A1~")
        # Transaction Set Header (ST)
        segments.append(f"ST*837*0001*005010X222A1~")
        # Submitter Name (BHT)
        segments.append(f"BHT*0019*00*{control_number}*{today_str}*{time_str}*CH~")
        # 1000A Submitter Name
        segments.append(f"NM1*41*2*ACUPATH CENTRAL LAB*****46*{submitter_id}~")
        segments.append(f"PER*IC*BILLING DEPT*TE*8005550199*EM*claims@acupath.com~")
        # 1000B Receiver Name
        segments.append(f"NM1*40*2*BLUE CROSS BLUE SHIELD*****46*{receiver_id}~")
        # 2000A Billing Provider
        segments.append(f"HL*1**20*1~")
        segments.append(f"PRV*BI*PXC*291U00000X~")
        segments.append(f"NM1*85*2*{billing_provider.get('name', 'ACUPATH LABORATORIES')}*****XX*{billing_provider.get('npi', '1992817263')}~")
        segments.append(f"N3*{billing_provider.get('address', '100 MEDICAL CENTER BLVD')}~")
        segments.append(f"N4*{billing_provider.get('city', 'BOSTON')}*{billing_provider.get('state', 'MA')}*{billing_provider.get('zip', '02115')}~")

        # 2000B Subscriber / Patient
        segments.append(f"HL*2*1*22*0~")
        segments.append(f"SBR*P*18*******MB~")
        segments.append(f"NM1*IL*1*{subscriber_patient.get('last_name', 'DOE')}*{subscriber_patient.get('first_name', 'JOHN')}****MI*{subscriber_patient.get('member_id', 'XYZ987654321')}~")
        segments.append(f"DMG*D8*{subscriber_patient.get('dob', '19850101')}*{subscriber_patient.get('gender', 'M')}~")

        # 2300 Claim Information
        total_charge = sum(line.get("charge", 0.0) for line in claim_lines)
        segments.append(f"CLM*{subscriber_patient.get('order_id', 'ORD001')}*{total_charge:.2f}***11:B:1*Y*A*Y*Y~")
        segments.append(f"HI*ABK:{subscriber_patient.get('primary_icd10', 'Z00.00')}~")

        # 2400 Service Lines
        for i, line in enumerate(claim_lines, 1):
            segments.append(f"LX*{i}~")
            segments.append(f"SV1*HC:{line.get('cpt_code', '80053')}*{line.get('charge', 50.0):.2f}*UN*1***1~")
            segments.append(f"DTP*472*D8*{today_str}~")

        # Transaction Trailer (SE)
        segments.append(f"SE*{len(segments) - 2}*0001~")
        # Functional Group Trailer (GE)
        segments.append(f"GE*1*1~")
        # Interchange Control Trailer (IEA)
        segments.append(f"IEA*1*{control_number}~")

        return "\n".join(segments)
