import pytest
from fastapi.testclient import TestClient
from app.models.database import User

def test_create_user(client, test_superuser_token):
    response = client.post(
        "/api/users/",
        headers={"Authorization": f"Bearer {test_superuser_token}"},
        json={
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data

def test_create_user_duplicate_email(client, test_superuser_token, test_user):
    response = client.post(
        "/api/users/",
        headers={"Authorization": f"Bearer {test_superuser_token}"},
        json={
            "email": test_user.email,
            "full_name": "Duplicate User",
            "password": "password123"
        }
    )
    assert response.status_code == 400

def test_get_current_user(client, test_token):
    response = client.get(
        "/api/users/me/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_update_current_user(client, test_token):
    response = client.put(
        "/api/users/me/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "email": "updated@example.com",
            "full_name": "Updated User",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["full_name"] == "Updated User"

def test_get_all_users(client, test_superuser_token):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {test_superuser_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_all_users_unauthorized(client, test_token):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 403

def test_login_success(client, test_user):
    response = client.post(
        "/api/token",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/api/token",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401 