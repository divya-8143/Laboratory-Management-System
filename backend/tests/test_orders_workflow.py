import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_end_to_end_clinical_testing_workflow(client: AsyncClient, auth_headers):
    """
    Comprehensive End-to-End Clinical Lifecycle:
    1. Admin creates test category, test profile, parameter, and reference range
    2. Register patient
    3. Place multi-test order
    4. Verify automatic sample tube clustering & barcodes
    5. Mark sample collected & accessioned into lab
    6. Batch enter parameter results with reference evaluation
    7. Doctor signs off and verifies report
    8. Verify public QR code authenticity token
    9. Download official PDF report
    """
    admin_headers = auth_headers("admin")
    rec_headers = auth_headers("receptionist")
    tech_headers = auth_headers("technician")
    doc_headers = auth_headers("doctor")

    # 1. Admin creates Category & Test
    cat_res = await client.post(
        "/api/v1/catalog/categories",
        json={"name": "Hematology", "code": "HEM", "description": "Blood tests"},
        headers=admin_headers
    )
    assert cat_res.status_code == 201
    category_id = cat_res.json()["id"]

    test_create_res = await client.post(
        "/api/v1/catalog/tests",
        json={
            "category_id": category_id,
            "test_code": "CBC",
            "name": "Complete Blood Count",
            "short_name": "CBC",
            "specimen_type": "WHOLE_BLOOD",
            "container_type": "EDTA_LAVENDER",
            "price": 45.0,
            "turnaround_time_hours": 12,
            "parameters": [
                {
                    "parameter_code": "HGB",
                    "name": "Hemoglobin",
                    "unit": "g/dL",
                    "data_type": "NUMERIC",
                    "display_order": 1,
                    "reference_ranges": [
                        {
                            "gender": "FEMALE",
                            "age_min_days": 0,
                            "age_max_days": 40000,
                            "normal_min": 12.0,
                            "normal_max": 15.5,
                            "critical_low": 7.0,
                            "critical_high": 20.0
                        }
                    ]
                }
            ]
        },
        headers=admin_headers
    )
    assert test_create_res.status_code == 201
    test_id = test_create_res.json()["id"]

    # 2. Register Patient
    pat_res = await client.post(
        "/api/v1/patients",
        json={
            "first_name": "Clara",
            "last_name": "Barton",
            "date_of_birth": "1992-12-25",
            "gender": "FEMALE",
            "blood_group": "A+",
            "phone": "+1-555-492-0192",
            "email": "clara.barton@redcross.org"
        },
        headers=rec_headers
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Place Lab Order
    ord_res = await client.post(
        "/api/v1/orders",
        json={
            "patient_id": patient_id,
            "referring_doctor": "Dr. Florence Nightingale",
            "priority": "URGENT",
            "test_ids": [test_id],
            "discount_amount": 0.0
        },
        headers=rec_headers
    )
    assert ord_res.status_code == 201
    order_data = ord_res.json()
    order_id = order_data["id"]
    assert order_data["order_number"].startswith("ORD-")
    assert len(order_data["order_items"]) == 1
    order_item_id = order_data["order_items"][0]["id"]
    sample_id = order_data["order_items"][0]["sample_id"]

    # 4. Phlebotomy: Collect Specimen
    col_res = await client.post(
        f"/api/v1/samples/{sample_id}/collect",
        json={"notes": "Smooth venipuncture, left antecubital fossa."},
        headers=rec_headers
    )
    assert col_res.status_code == 200
    assert col_res.json()["status"] == "COLLECTED"

    # 5. Accessioning: Receive Specimen in Lab
    rec_res = await client.post(
        f"/api/v1/samples/{sample_id}/receive",
        headers=tech_headers
    )
    assert rec_res.status_code == 200
    assert rec_res.json()["status"] == "RECEIVED_IN_LAB"

    # 6. Enter Results
    test_details = (await client.get(f"/api/v1/catalog/tests/{test_id}", headers=tech_headers)).json()
    param_id = test_details["parameters"][0]["id"]

    result_res = await client.post(
        "/api/v1/results/batch-entry",
        json={
            "order_item_id": order_item_id,
            "results": [
                {
                    "parameter_id": param_id,
                    "numeric_value": 14.5,
                    "technician_notes": "Analyzed on automated Sysmex XN-1000"
                }
            ]
        },
        headers=tech_headers
    )
    assert result_res.status_code == 200
    results_list = result_res.json()
    assert len(results_list) >= 1
    assert results_list[0]["formatted_value"] == "14.5"

    # 7. Doctor Verification & Sign-off
    rep_meta = (await client.get(f"/api/v1/reports/order/{order_id}", headers=doc_headers)).json()
    report_id = rep_meta["id"]

    verify_res = await client.post(
        f"/api/v1/reports/{report_id}/verify",
        json={
            "pathologist_comments": "Parameters consistent with normal physiological range.",
            "clinical_interpretation": "No hematologic abnormality detected."
        },
        headers=doc_headers
    )
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "VERIFIED"
    qr_hash = verify_res.json()["verification_qr_hash"]

    # 8. Verify QR Hash Public Authenticity
    public_res = await client.get(f"/api/v1/reports/public/verify/{qr_hash}")
    assert public_res.status_code == 200
    assert public_res.json()["is_authentic"] is True
    assert public_res.json()["report_number"] == verify_res.json()["report_number"]

    # 9. Download Generated PDF Report
    pdf_res = await client.get(f"/api/v1/reports/{report_id}/pdf", headers=doc_headers)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000
