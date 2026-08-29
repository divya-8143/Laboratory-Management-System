from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    patients,
    catalog,
    orders,
    samples,
    results,
    reports,
    analytics,
    audit
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(patients.router)
api_router.include_router(catalog.router)
api_router.include_router(orders.router)
api_router.include_router(samples.router)
api_router.include_router(results.router)
api_router.include_router(reports.router)
api_router.include_router(analytics.router)
api_router.include_router(audit.router)
