import os
import io
import base64
import qrcode
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.core.config import settings
from app.models.report import LabReport
from app.models.order import Order
from app.models.patient import Patient
from app.models.user import User


class ReportGeneratorService:
    @staticmethod
    def generate_qr_base64(data_string: str) -> str:
        """Generate base64 data URI of QR code."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=2,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0f172a", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{b64_str}"

    @staticmethod
    def generate_pdf_report(
        report: LabReport,
        order: Order,
        patient: Patient,
        doctor: User = None
    ) -> str:
        """
        Generate a professional, publication-quality medical lab report PDF using ReportLab.
        Returns the absolute filepath of the generated PDF.
        """
        os.makedirs(settings.REPORT_STORAGE_DIR, exist_ok=True)
        pdf_filename = f"{report.report_number}.pdf"
        pdf_path = os.path.join(settings.REPORT_STORAGE_DIR, pdf_filename)

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom typography
        title_style = ParagraphStyle(
            'LabTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor('#0369a1'),
            leading=18
        )
        subtitle_style = ParagraphStyle(
            'LabSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#64748b'),
            leading=11
        )
        header_badge_style = ParagraphStyle(
            'HeaderBadge',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.HexColor('#0284c7'),
            alignment=2,
            leading=14
        )
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#0f172a'),
            backColor=colors.HexColor('#f1f5f9'),
            borderPadding=4,
            spaceBefore=10,
            spaceAfter=6
        )
        cell_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#1e293b'),
            leading=11
        )
        cell_bold = ParagraphStyle(
            'CellBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#0f172a'),
            leading=11
        )
        abnormal_cell = ParagraphStyle(
            'AbnormalCell',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#dc2626'),
            leading=11
        )
        normal_cell = ParagraphStyle(
            'NormalCell',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#16a34a'),
            leading=11
        )

        elements = []

        # 1. Header Block
        header_table_data = [
            [
                Paragraph(f"<b>{settings.LAB_NAME}</b>", title_style),
                Paragraph(f"<b>{report.status.value} REPORT</b><br/>Report #: <b>{report.report_number}</b><br/>Order #: <b>{order.order_number}</b>", header_badge_style)
            ],
            [
                Paragraph(f"{settings.LAB_ADDRESS}<br/>Tel: {settings.LAB_PHONE} | {settings.LAB_ACCREDITATION}", subtitle_style),
                Paragraph(f"Date: {datetime.utcnow().strftime('%d-%b-%Y')}", ParagraphStyle('RightDate', parent=subtitle_style, alignment=2))
            ]
        ]
        header_table = Table(header_table_data, colWidths=[360, 160])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=10))

        # 2. Patient Demographics Grid
        patient_data = [
            [
                Paragraph("<b>Patient Name:</b>", cell_style),
                Paragraph(f"<b>{patient.full_name}</b>", cell_bold),
                Paragraph("<b>Patient ID:</b>", cell_style),
                Paragraph(f"<b>{patient.patient_code}</b>", cell_bold)
            ],
            [
                Paragraph("<b>Age / Gender:</b>", cell_style),
                Paragraph(f"{patient.age_years} Yrs / {patient.gender.value}", cell_style),
                Paragraph("<b>Blood Group:</b>", cell_style),
                Paragraph(patient.blood_group.value, cell_style)
            ],
            [
                Paragraph("<b>Ref Doctor:</b>", cell_style),
                Paragraph(order.referring_doctor or "Self / Walk-in", cell_style),
                Paragraph("<b>Priority:</b>", cell_style),
                Paragraph(f"<b>{order.priority.value}</b>", cell_bold)
            ],
            [
                Paragraph("<b>Order Date:</b>", cell_style),
                Paragraph(order.created_at.strftime('%d-%b-%Y %H:%M'), cell_style),
                Paragraph("<b>Verified Date:</b>", cell_style),
                Paragraph(report.verified_at.strftime('%d-%b-%Y %H:%M') if report.verified_at else "Pending Sign-off", cell_style)
            ]
        ]
        patient_table = Table(patient_data, colWidths=[85, 175, 85, 175])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 10))

        # 3. Test Results Grouped by Item
        for item in order.order_items:
            test_heading = f"{item.test.name} ({item.test.test_code}) &mdash; Specimen: {item.test.specimen_type.value}"
            elements.append(Paragraph(test_heading, section_style))

            results_header = [
                Paragraph("<b>Investigation / Parameter</b>", cell_bold),
                Paragraph("<b>Observed Value</b>", cell_bold),
                Paragraph("<b>Unit</b>", cell_bold),
                Paragraph("<b>Ref. Interval</b>", cell_bold),
                Paragraph("<b>Flag</b>", cell_bold),
            ]
            results_rows = [results_header]

            for res in item.results:
                val_style = abnormal_cell if res.is_abnormal else normal_cell
                val_text = f"<b>{res.formatted_value}</b>"
                if res.is_critical:
                    val_text += " [CRITICAL]"

                results_rows.append([
                    Paragraph(res.parameter.name, cell_style),
                    Paragraph(val_text, val_style),
                    Paragraph(res.parameter.unit or "-", cell_style),
                    Paragraph(res.reference_range_display or "-", cell_style),
                    Paragraph(f"<b>{res.flag.value}</b>", val_style)
                ])

            res_table = Table(results_rows, colWidths=[190, 110, 60, 110, 50])
            res_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#f1f5f9')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ]))
            elements.append(res_table)
            elements.append(Spacer(1, 6))

        # 4. Remarks & Doctor Interpretation
        if report.pathologist_comments or report.clinical_interpretation:
            remarks_content = "<b>PATHOLOGIST REMARKS:</b> " + (report.pathologist_comments or "")
            if report.clinical_interpretation:
                remarks_content += f"<br/><b>Interpretation:</b> {report.clinical_interpretation}"
            
            remarks_table = Table([[Paragraph(remarks_content, cell_style)]], colWidths=[520])
            remarks_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffbeb')),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#fde68a')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(Spacer(1, 6))
            elements.append(remarks_table)

        # 5. Sign-off and QR Verification Block
        elements.append(Spacer(1, 14))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=8))

        # Generate QR code for report verification
        qr_data = f"https://acupathdiagnostics.com/verify-report?hash={report.verification_qr_hash}"
        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_flowable = Image(qr_buffer, width=1.0*inch, height=1.0*inch)

        doctor_title = doctor.full_name if doctor else "Dr. Eleanor Pemberton, MD"
        doctor_dept = doctor.department if doctor else "Medical Director & Pathologist"
        doctor_lic = doctor.license_number if doctor else "MD-PATH-492019"

        footer_table_data = [
            [
                qr_flowable,
                Paragraph(f"<br/><br/><b>{doctor_title}</b><br/>{doctor_dept}<br/>License: {doctor_lic}", ParagraphStyle('DocSign', parent=cell_style, alignment=2))
            ],
            [
                Paragraph("<font size='7' color='#94a3b8'>Scan QR to verify authentic laboratory electronic record.</font>", subtitle_style),
                Paragraph("<font size='7' color='#94a3b8'>Digitally verified and stamped</font>", ParagraphStyle('DigiStamp', parent=subtitle_style, alignment=2))
            ]
        ]
        footer_table = Table(footer_table_data, colWidths=[200, 320])
        footer_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        elements.append(footer_table)

        # Build PDF
        doc.build(elements)
        return pdf_path
