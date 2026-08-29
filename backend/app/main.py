import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, sync_engine, async_engine
from app.core.exceptions import ClinicalLMSException
from app.api.v1.router import api_router
from seed_data import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and pre-seed initial clinical catalog
    print(f"Starting {settings.PROJECT_NAME} (v{settings.VERSION})...")
    Base.metadata.create_all(bind=sync_engine)
    try:
        seed_database()
    except Exception as e:
        print(f"Auto-seed note: {e}")
    yield
    # Shutdown
    print("Shutting down laboratory engine...")
    await async_engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount generated static files & reports directory
if os.path.exists(settings.REPORT_STORAGE_DIR):
    app.mount("/static/reports", StaticFiles(directory=settings.REPORT_STORAGE_DIR), name="reports")

# Exception handler
@app.exception_handler(ClinicalLMSException)
async def clinical_exception_handler(request: Request, exc: ClinicalLMSException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["System"])
async def health_check():
    """System health & readiness check."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
