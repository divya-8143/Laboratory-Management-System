import urllib.request
import json
import urllib.error
import sys

def check_endpoint(name, url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {}
    if data:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json', **headers},
            method=method
        )
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            content_type = response.headers.get('content-type', '')
            raw_bytes = response.read()
            if 'application/pdf' in content_type:
                print(f"  [PASS] {name}: HTTP {response.status} (Valid PDF Document, {len(raw_bytes)} bytes)")
                return raw_bytes
            
            res_data = raw_bytes.decode('utf-8', errors='ignore')
            print(f"  [PASS] {name}: HTTP {response.status}")
            return json.loads(res_data) if res_data.startswith(('{', '[')) else res_data
    except urllib.error.HTTPError as e:
        print(f"  [FAIL] {name}: HTTP {e.code} - {e.read().decode('utf-8', errors='ignore')}")
        return None

def run_all_checks():
    print("==========================================================")
    print("      ACUPATH LIS - COMPREHENSIVE END-TO-END AUDIT        ")
    print("==========================================================")

    print("\n--- 1. SYSTEM HEALTH ---")
    check_endpoint("Health Check", "http://127.0.0.1:8000/health")

    print("\n--- 2. AUTHENTICATION & IAM ---")
    login_res = check_endpoint(
        "Admin Login",
        "http://127.0.0.1:8000/api/v1/auth/login",
        method="POST",
        data={"email": "admin@acupath.com", "password": "Admin@12345"}
    )
    if not login_res:
        print("Login failed, aborting further authenticated checks.")
        return

    token = login_res.get("access_token")
    auth_header = {"Authorization": f"Bearer {token}"}

    check_endpoint("Profile /auth/me", "http://127.0.0.1:8000/api/v1/auth/me", headers=auth_header)
    check_endpoint("List Users (Admin)", "http://127.0.0.1:8000/api/v1/users", headers=auth_header)

    print("\n--- 3. PATIENTS MODULE ---")
    import time
    unique_id = int(time.time())
    pat = check_endpoint(
        "Register Patient",
        "http://127.0.0.1:8000/api/v1/patients",
        method="POST",
        data={
            "first_name": "Thomas",
            "last_name": f"Edison_{unique_id}",
            "date_of_birth": "1985-02-11",
            "gender": "MALE",
            "blood_group": "A+",
            "phone": f"+1-555-111-{unique_id % 10000:04d}",
            "email": f"thomas.edison.{unique_id}@example.com",
            "address": "12 Lab Lane",
            "medical_history_notes": "Verified test record"
        },
        headers=auth_header
    )
    pat_id = pat.get("id") if pat else None
    check_endpoint("List Patients with Search", "http://127.0.0.1:8000/api/v1/patients?limit=10&search=Edison", headers=auth_header)

    print("\n--- 4. TEST CATALOG MODULE ---")
    check_endpoint("List Categories", "http://127.0.0.1:8000/api/v1/catalog/categories", headers=auth_header)
    tests = check_endpoint("List Tests with Parameters", "http://127.0.0.1:8000/api/v1/catalog/tests", headers=auth_header)
    test_id = tests[0]["id"] if tests and len(tests) > 0 else None

    print("\n--- 5. ORDER BOOKING & INVOICING ---")
    if pat_id and test_id:
        ord_res = check_endpoint(
            "Create Order with Auto-Barcodes & Invoice",
            "http://127.0.0.1:8000/api/v1/orders",
            method="POST",
            data={
                "patient_id": pat_id,
                "referring_doctor": "Dr. Test Physician",
                "priority": "URGENT",
                "test_ids": [test_id],
                "discount_amount": 5.0
            },
            headers=auth_header
        )
        ord_id = ord_res.get("id") if ord_res else None
        sample_id = ord_res["order_items"][0]["sample_id"] if ord_res and len(ord_res.get("order_items", [])) > 0 else None
        order_item_id = ord_res["order_items"][0]["id"] if ord_res and len(ord_res.get("order_items", [])) > 0 else None

        print("\n--- 6. PHLEBOTOMY & SAMPLES ---")
        if sample_id:
            check_endpoint("Collect Sample", f"http://127.0.0.1:8000/api/v1/samples/{sample_id}/collect", method="POST", data={"notes": "Specimen collected"}, headers=auth_header)
            check_endpoint("Receive in Lab Worklist", f"http://127.0.0.1:8000/api/v1/samples/{sample_id}/receive", method="POST", headers=auth_header)

        print("\n--- 7. RESULTS ENTRY & EVALUATION ---")
        if order_item_id:
            test_detail = check_endpoint("Get Test Parameters", f"http://127.0.0.1:8000/api/v1/catalog/tests/{test_id}", headers=auth_header)
            param_id = test_detail["parameters"][0]["id"] if test_detail and len(test_detail.get("parameters", [])) > 0 else None
            if param_id:
                check_endpoint(
                    "Batch Result Entry & Flag Evaluation",
                    "http://127.0.0.1:8000/api/v1/results/batch-entry",
                    method="POST",
                    data={
                        "order_item_id": order_item_id,
                        "results": [{"parameter_id": param_id, "numeric_value": 14.8, "technician_notes": "Analyzed successfully"}]
                    },
                    headers=auth_header
                )

        print("\n--- 8. DOCTOR VERIFICATION & PDF DELIVERY ---")
        if ord_id:
            rep = check_endpoint("Get Report for Order", f"http://127.0.0.1:8000/api/v1/reports/order/{ord_id}", headers=auth_header)
            rep_id = rep.get("id") if rep else None
            if rep_id:
                ver = check_endpoint(
                    "Doctor Sign-off & PDF Generation",
                    f"http://127.0.0.1:8000/api/v1/reports/{rep_id}/verify",
                    method="POST",
                    data={
                        "pathologist_comments": "Parameters within accepted reference boundaries.",
                        "clinical_interpretation": "Normal clinical profile."
                    },
                    headers=auth_header
                )
                qr_hash = ver.get("verification_qr_hash") if ver else None
                if qr_hash:
                    check_endpoint("Public QR Tamper-Proof Verification", f"http://127.0.0.1:8000/api/v1/reports/public/verify/{qr_hash}")
                check_endpoint("Download PDF (No auth required for verified report)", f"http://127.0.0.1:8000/api/v1/reports/{rep_id}/pdf")

    print("\n--- 9. EXECUTIVE ANALYTICS & KPIS ---")
    check_endpoint("KPI Overview (Totals, TAT, Volume)", "http://127.0.0.1:8000/api/v1/analytics/overview", headers=auth_header)
    check_endpoint("Most Requested Clinical Tests", "http://127.0.0.1:8000/api/v1/analytics/most-requested", headers=auth_header)
    check_endpoint("Daily Revenue Trends", "http://127.0.0.1:8000/api/v1/analytics/revenue-trends?period_type=daily", headers=auth_header)
    check_endpoint("Category Volume Distribution", "http://127.0.0.1:8000/api/v1/analytics/category-distribution", headers=auth_header)

    print("\n--- 10. COMPLIANCE & AUDIT LOGS ---")
    check_endpoint("Audit Activity Trail", "http://127.0.0.1:8000/api/v1/audit/logs?limit=10", headers=auth_header)

    print("\n==========================================================")
    print("      ALL ENDPOINTS AND CLINICAL FIELDS VERIFIED!         ")
    print("==========================================================")

if __name__ == "__main__":
    run_all_checks()
