import pytest
import os
import sys
import uuid
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SYNC_DATABASE_URL"] = "sqlite:///:memory:"

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, RoleType

test_async_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(autouse=True)
async def prepare_database():
    """Create all tables in memory before each test and drop after."""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def seed_users(db_session: AsyncSession):
    """Seed test users for all 5 roles."""
    users = {
        "admin": User(
            id=str(uuid.uuid4()),
            email="admin@test.com",
            hashed_password=get_password_hash("AdminPass123"),
            first_name="Admin",
            last_name="User",
            role=RoleType.ADMIN,
            is_active=True
        ),
        "receptionist": User(
            id=str(uuid.uuid4()),
            email="reception@test.com",
            hashed_password=get_password_hash("RecepPass123"),
            first_name="Reception",
            last_name="User",
            role=RoleType.RECEPTIONIST,
            is_active=True
        ),
        "technician": User(
            id=str(uuid.uuid4()),
            email="tech@test.com",
            hashed_password=get_password_hash("TechPass123"),
            first_name="Tech",
            last_name="User",
            role=RoleType.TECHNICIAN,
            is_active=True
        ),
        "doctor": User(
            id=str(uuid.uuid4()),
            email="doctor@test.com",
            hashed_password=get_password_hash("DocPass123"),
            first_name="Dr. Eleanor",
            last_name="Pemberton",
            role=RoleType.DOCTOR,
            license_number="MD-TEST-999",
            is_active=True
        ),
        "patient": User(
            id=str(uuid.uuid4()),
            email="patient@test.com",
            hashed_password=get_password_hash("PatPass123"),
            first_name="John",
            last_name="Doe",
            role=RoleType.PATIENT,
            is_active=True
        )
    }
    for u in users.values():
        db_session.add(u)
    await db_session.commit()
    return users


@pytest.fixture
def auth_headers(seed_users):
    """Helper to generate Authorization headers for each role."""
    def _headers(role_name: str):
        user = seed_users[role_name]
        token = create_access_token(subject=user.id, role=user.role.value)
        return {"Authorization": f"Bearer {token}"}
    return _headers
