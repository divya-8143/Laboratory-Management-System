import uuid
from datetime import date, datetime
from app.core.database import SessionLocal, sync_engine, Base
from app.core.security import get_password_hash
from app.models.user import User, RoleType
from app.models.patient import Patient, GenderEnum, BloodGroupEnum
from app.models.catalog import (
    TestCategory,
    Test,
    TestParameter,
    ReferenceRange,
    SpecimenTypeEnum,
    ContainerTypeEnum,
    ParameterDataTypeEnum
)


def seed_database():
    Base.metadata.create_all(bind=sync_engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_admin = db.query(User).filter_by(email="admin@acupath.com").first()
        if existing_admin:
            print("Database already contains seed data.")
            return

        print("Seeding Enterprise Laboratory Management System...")

        # 1. Seed Users for All 5 Roles
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@acupath.com",
            hashed_password=get_password_hash("Admin@12345"),
            first_name="Alexander",
            last_name="Wright",
            role=RoleType.ADMIN,
            phone="+1-800-555-0101",
            department="Executive Administration",
            is_active=True
        )

        receptionist_user = User(
            id=str(uuid.uuid4()),
            email="reception@acupath.com",
            hashed_password=get_password_hash("Reception@12345"),
            first_name="Sarah",
            last_name="Jenkins",
            role=RoleType.RECEPTIONIST,
            phone="+1-800-555-0102",
            department="Front Desk & Registration",
            is_active=True
        )

        technician_user = User(
            id=str(uuid.uuid4()),
            email="technician@acupath.com",
            hashed_password=get_password_hash("Technician@12345"),
            first_name="Marcus",
            last_name="Vance",
            role=RoleType.TECHNICIAN,
            phone="+1-800-555-0103",
            department="Diagnostic Pathology & Hematology",
            license_number="MLS-ASCP-892410",
            is_active=True
        )

        doctor_user = User(
            id=str(uuid.uuid4()),
            email="doctor@acupath.com",
            hashed_password=get_password_hash("Doctor@12345"),
            first_name="Dr. Eleanor",
            last_name="Pemberton",
            role=RoleType.DOCTOR,
            phone="+1-800-555-0104",
            department="Clinical Pathology & Medical Direction",
            license_number="MD-PATH-492019",
            signature_image_url="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='60'><text x='10' y='40' font-family='cursive' font-size='24' fill='%231a365d'>Dr. E. Pemberton, MD</text></svg>",
            is_active=True
        )

        patient_user = User(
            id=str(uuid.uuid4()),
            email="john.doe@gmail.com",
            hashed_password=get_password_hash("Patient@12345"),
            first_name="John",
            last_name="Doe",
            role=RoleType.PATIENT,
            phone="+1-555-019-2834",
            is_active=True
        )

        db.add_all([admin_user, receptionist_user, technician_user, doctor_user, patient_user])
        db.flush()

        # 2. Seed Initial Patients
        patient_1 = Patient(
            id=str(uuid.uuid4()),
            patient_code="PAT-2026-0001",
            user_id=patient_user.id,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1988, 6, 15),
            gender=GenderEnum.MALE,
            blood_group=BloodGroupEnum.O_POSITIVE,
            phone="+1-555-019-2834",
            email="john.doe@gmail.com",
            address="452 Elmwood Terrace, Apt 3B",
            city="Metropolis",
            postal_code="94016",
            emergency_contact_name="Jane Doe",
            emergency_contact_phone="+1-555-019-2835",
            medical_history_notes="History of mild hypertension. No known drug allergies."
        )

        patient_2 = Patient(
            id=str(uuid.uuid4()),
            patient_code="PAT-2026-0002",
            first_name="Maria",
            last_name="Rodriguez",
            date_of_birth=date(1995, 3, 22),
            gender=GenderEnum.FEMALE,
            blood_group=BloodGroupEnum.A_POSITIVE,
            phone="+1-555-482-9102",
            email="m.rodriguez@example.com",
            address="784 Sunset Blvd",
            city="Metropolis",
            postal_code="94018",
            emergency_contact_name="Carlos Rodriguez",
            emergency_contact_phone="+1-555-482-9100",
            medical_history_notes="Routine annual executive wellness panel."
        )

        db.add_all([patient_1, patient_2])
        db.flush()

        # 3. Seed Test Categories
        cat_hema = TestCategory(
            id=str(uuid.uuid4()),
            name="Hematology",
            code="HEM",
            description="Complete blood counts, coagulation profiles, and cellular morphologic analysis.",
            display_order=1
        )
        cat_biochem = TestCategory(
            id=str(uuid.uuid4()),
            name="Clinical Biochemistry",
            code="BIO",
            description="Metabolic panels, liver function, renal function, lipid profiles, and enzymes.",
            display_order=2
        )
        cat_endo = TestCategory(
            id=str(uuid.uuid4()),
            name="Endocrinology & Immunology",
            code="IMM",
            description="Hormone assays, thyroid panels, infectious disease serology.",
            display_order=3
        )
        cat_urine = TestCategory(
            id=str(uuid.uuid4()),
            name="Urinalysis & Clinical Microscopy",
            code="URI",
            description="Physicochemical and microscopic evaluation of urine specimens.",
            display_order=4
        )

        db.add_all([cat_hema, cat_biochem, cat_endo, cat_urine])
        db.flush()

        # 4. Seed Tests, Parameters & Reference Ranges

        # TEST 1: Complete Blood Count (CBC with Differential)
        test_cbc = Test(
            id=str(uuid.uuid4()),
            category_id=cat_hema.id,
            test_code="CBC",
            name="Complete Blood Count with 5-Part Differential",
            short_name="CBC",
            description="Comprehensive automated assessment of white blood cells, red blood cells, hemoglobin, and platelets.",
            specimen_type=SpecimenTypeEnum.WHOLE_BLOOD,
            container_type=ContainerTypeEnum.EDTA_LAVENDER,
            price=45.00,
            turnaround_time_hours=12
        )
        db.add(test_cbc)
        db.flush()

        # CBC Parameters
        p_wbc = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="WBC", name="White Blood Cell Count", unit="10^3/uL", display_order=1)
        p_rbc = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="RBC", name="Red Blood Cell Count", unit="10^6/uL", display_order=2)
        p_hgb = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="HGB", name="Hemoglobin", unit="g/dL", display_order=3)
        p_hct = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="HCT", name="Hematocrit", unit="%", display_order=4)
        p_plt = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="PLT", name="Platelet Count", unit="10^3/uL", display_order=5)
        p_mcv = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="MCV", name="Mean Corpuscular Volume", unit="fL", display_order=6)
        p_neut = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="NEUT", name="Neutrophils %", unit="%", display_order=7)
        p_lymph = TestParameter(id=str(uuid.uuid4()), test_id=test_cbc.id, parameter_code="LYMPH", name="Lymphocytes %", unit="%", display_order=8)

        db.add_all([p_wbc, p_rbc, p_hgb, p_hct, p_plt, p_mcv, p_neut, p_lymph])
        db.flush()

        # CBC Reference Ranges
        db.add_all([
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_wbc.id, gender="BOTH", normal_min=4.5, normal_max=11.0, critical_low=2.0, critical_high=30.0),
            # HGB Male
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hgb.id, gender="MALE", normal_min=13.8, normal_max=17.2, critical_low=7.0, critical_high=20.0),
            # HGB Female
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hgb.id, gender="FEMALE", normal_min=12.1, normal_max=15.1, critical_low=7.0, critical_high=20.0),
            # RBC Male & Female
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_rbc.id, gender="MALE", normal_min=4.7, normal_max=6.1),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_rbc.id, gender="FEMALE", normal_min=4.2, normal_max=5.4),
            # Platelets
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_plt.id, gender="BOTH", normal_min=150.0, normal_max=450.0, critical_low=50.0, critical_high=1000.0),
            # Hematocrit
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hct.id, gender="MALE", normal_min=40.7, normal_max=50.3),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hct.id, gender="FEMALE", normal_min=36.1, normal_max=44.3),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_mcv.id, gender="BOTH", normal_min=80.0, normal_max=96.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_neut.id, gender="BOTH", normal_min=40.0, normal_max=70.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_lymph.id, gender="BOTH", normal_min=20.0, normal_max=40.0),
        ])

        # TEST 2: Lipid Profile
        test_lipid = Test(
            id=str(uuid.uuid4()),
            category_id=cat_biochem.id,
            test_code="LIPID",
            name="Comprehensive Lipid Profile",
            short_name="Lipid Panel",
            description="Quantification of total cholesterol, HDL, LDL, and triglycerides for cardiovascular risk assessment.",
            specimen_type=SpecimenTypeEnum.SERUM,
            container_type=ContainerTypeEnum.SST_GOLD_YELLOW,
            price=60.00,
            turnaround_time_hours=24
        )
        db.add(test_lipid)
        db.flush()

        p_chol = TestParameter(id=str(uuid.uuid4()), test_id=test_lipid.id, parameter_code="CHOL", name="Total Cholesterol", unit="mg/dL", display_order=1)
        p_trig = TestParameter(id=str(uuid.uuid4()), test_id=test_lipid.id, parameter_code="TRIG", name="Triglycerides", unit="mg/dL", display_order=2)
        p_hdl = TestParameter(id=str(uuid.uuid4()), test_id=test_lipid.id, parameter_code="HDL", name="HDL Cholesterol", unit="mg/dL", display_order=3)
        p_ldl = TestParameter(id=str(uuid.uuid4()), test_id=test_lipid.id, parameter_code="LDL", name="LDL Cholesterol (Calculated)", unit="mg/dL", display_order=4)

        db.add_all([p_chol, p_trig, p_hdl, p_ldl])
        db.flush()

        db.add_all([
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_chol.id, gender="BOTH", normal_min=100.0, normal_max=200.0, critical_high=300.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_trig.id, gender="BOTH", normal_min=35.0, normal_max=150.0, critical_high=500.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hdl.id, gender="MALE", normal_min=40.0, normal_max=80.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_hdl.id, gender="FEMALE", normal_min=50.0, normal_max=90.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_ldl.id, gender="BOTH", normal_min=0.0, normal_max=100.0, critical_high=190.0),
        ])

        # TEST 3: Fasting Blood Glucose (FBG)
        test_fbg = Test(
            id=str(uuid.uuid4()),
            category_id=cat_biochem.id,
            test_code="FBG",
            name="Fasting Blood Glucose",
            short_name="Fasting Glucose",
            description="Evaluation of plasma glucose after minimum 8-hour fast.",
            specimen_type=SpecimenTypeEnum.PLASMA,
            container_type=ContainerTypeEnum.SODIUM_FLUORIDE_GREY,
            price=25.00,
            turnaround_time_hours=8
        )
        db.add(test_fbg)
        db.flush()

        p_gluc = TestParameter(id=str(uuid.uuid4()), test_id=test_fbg.id, parameter_code="GLU", name="Glucose, Fasting", unit="mg/dL", display_order=1)
        db.add(p_gluc)
        db.flush()

        db.add(ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_gluc.id, gender="BOTH", normal_min=70.0, normal_max=99.0, critical_low=50.0, critical_high=400.0))

        # TEST 4: Liver Function Panel (LFT)
        test_lft = Test(
            id=str(uuid.uuid4()),
            category_id=cat_biochem.id,
            test_code="LFT",
            name="Comprehensive Liver Function Panel",
            short_name="LFT",
            description="Assessment of hepatic parenchymal integrity, biliary function, and protein synthesis.",
            specimen_type=SpecimenTypeEnum.SERUM,
            container_type=ContainerTypeEnum.SST_GOLD_YELLOW,
            price=75.00,
            turnaround_time_hours=24
        )
        db.add(test_lft)
        db.flush()

        p_alt = TestParameter(id=str(uuid.uuid4()), test_id=test_lft.id, parameter_code="ALT", name="Alanine Aminotransferase (ALT/SGPT)", unit="U/L", display_order=1)
        p_ast = TestParameter(id=str(uuid.uuid4()), test_id=test_lft.id, parameter_code="AST", name="Aspartate Aminotransferase (AST/SGOT)", unit="U/L", display_order=2)
        p_bili = TestParameter(id=str(uuid.uuid4()), test_id=test_lft.id, parameter_code="TBIL", name="Total Bilirubin", unit="mg/dL", display_order=3)
        p_alb = TestParameter(id=str(uuid.uuid4()), test_id=test_lft.id, parameter_code="ALB", name="Albumin", unit="g/dL", display_order=4)

        db.add_all([p_alt, p_ast, p_bili, p_alb])
        db.flush()

        db.add_all([
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_alt.id, gender="MALE", normal_min=9.0, normal_max=50.0, critical_high=500.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_alt.id, gender="FEMALE", normal_min=7.0, normal_max=35.0, critical_high=500.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_ast.id, gender="BOTH", normal_min=10.0, normal_max=40.0, critical_high=500.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_bili.id, gender="BOTH", normal_min=0.2, normal_max=1.2, critical_high=15.0),
            ReferenceRange(id=str(uuid.uuid4()), parameter_id=p_alb.id, gender="BOTH", normal_min=3.5, normal_max=5.2),
        ])

        db.commit()
        print("Database seeded successfully with default roles, clinical tests, and multi-tier reference ranges!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
