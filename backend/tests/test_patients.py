import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_patient_registration_and_code_generation(client: AsyncClient, auth_headers):
    """Test patient registration with auto-generated PAT code."""
    headers = auth_headers("receptionist")
    payload = {
        "first_name": "Alexander",
        "last_name": "Fleming",
        "date_of_birth": "1980-05-12",
        "gender": "MALE",
        "blood_group": "O+",
        "phone": "+1-555-890-1234",
        "email": "alexander.fleming@hospital.org",
        "address": "100 Medical Center Blvd",
        "medical_history_notes": "No known allergies."
    }

    response = await client.post("/api/v1/patients", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["patient_code"].startswith("PAT-")
    assert data["first_name"] == "Alexander"
    assert data["last_name"] == "Fleming"
    assert data["age_years"] >= 40


@pytest.mark.asyncio
async def test_patient_search_and_pagination(client: AsyncClient, auth_headers):
    """Test patient query with name search and pagination."""
    headers = auth_headers("receptionist")
    
    # Register patient first
    await client.post(
        "/api/v1/patients",
        json={
            "first_name": "Alexander",
            "last_name": "Fleming",
            "date_of_birth": "1980-05-12",
            "gender": "MALE",
            "blood_group": "O+",
            "phone": "+1-555-890-5555",
            "email": "fleming.search@hospital.org"
        },
        headers=headers
    )

    # Search by Fleming
    response = await client.get("/api/v1/patients?search=Fleming", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    assert data["items"][0]["last_name"] == "Fleming"
