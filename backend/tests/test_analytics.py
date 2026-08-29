import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_analytics_kpi_overview_and_audit_logs(client: AsyncClient, auth_headers):
    """Test analytics KPIs, most requested test ranking, and audit log generation."""
    admin_headers = auth_headers("admin")

    # Overview KPIs
    kpi_res = await client.get("/api/v1/analytics/overview", headers=admin_headers)
    assert kpi_res.status_code == 200
    kpis = kpi_res.json()
    assert "total_patients" in kpis
    assert "total_orders" in kpis
    assert "total_revenue" in kpis
    assert "avg_turnaround_time_hours" in kpis

    # Most requested tests
    mr_res = await client.get("/api/v1/analytics/most-requested", headers=admin_headers)
    assert mr_res.status_code == 200
    assert isinstance(mr_res.json(), list)

    # Audit Logs
    audit_res = await client.get("/api/v1/audit/logs", headers=admin_headers)
    assert audit_res.status_code == 200
    logs = audit_res.json()
    assert isinstance(logs, list)
