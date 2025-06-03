import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
import os
from datetime import datetime, timedelta
from app.core.auth import create_access_token
from app.models.database import User

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create the test database
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    # Create a test user
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/IWm",  # "password123"
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_superuser(db):
    # Create a test superuser
    user = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/IWm",  # "password123"
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_token(test_user):
    # Create a test token
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": test_user.email}, expires_delta=access_token_expires
    )
    return access_token

@pytest.fixture(scope="function")
def test_superuser_token(test_superuser):
    # Create a test token for superuser
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": test_superuser.email}, expires_delta=access_token_expires
    )
    return access_token 