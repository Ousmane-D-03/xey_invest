from uuid import uuid4

from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine


client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)

def build_user_payload(role="investor"):
    suffix = uuid4().hex[:8]
    return {
        "username": f"testuser_{suffix}",
        "email": f"test_{suffix}@test.com",
        "password": "test123",
        "role": role,
    }


def register_and_login_user(role="investor"):
    payload = build_user_payload(role=role)
    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return payload, token


def build_campaign_payload():
    return {
        "title": "Campagne test",
        "description": "Description de test",
        "goal_amount": 1000.0,
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-12-01T00:00:00",
        "sector": "Tech",
        "unit_price": 10.0,
        "total_parts": 100,
        "yield_rate": 0.1,
        "repayment_duration": 12,
    }


def test_register_success():
    response = client.post("/auth/register", json=build_user_payload())

    assert response.status_code == 200
    assert "user_id" in response.json()


def test_register_duplicate_returns_existing_user():
    payload = build_user_payload()

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["user_id"] == first_response.json()["user_id"]


def test_login_success():
    payload = build_user_payload()
    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_login_with_wrong_password_fails():
    payload = build_user_payload()
    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_create_campaign_for_project_owner_succeeds():
    _, token = register_and_login_user(role="project_owner")

    response = client.post(
        "/campaign/campaigns",
        json=build_campaign_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Campagne test"


def test_create_investment_for_active_campaign_succeeds():
    _, owner_token = register_and_login_user(role="project_owner")
    _, admin_token = register_and_login_user(role="admin")

    campaign_response = client.post(
        "/campaign/campaigns",
        json=build_campaign_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    campaign_id = campaign_response.json()["id"]

    status_response = client.patch(
        f"/campaign/campaigns/{campaign_id}/status",
        json={"status": "active"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert status_response.status_code == 200

    _, investor_token = register_and_login_user(role="investor")
    investment_response = client.post(
        "/investment/investments",
        json={"nombrePartAchetees": 5, "campaign_id": campaign_id},
        headers={"Authorization": f"Bearer {investor_token}"},
    )

    assert investment_response.status_code == 200
    assert investment_response.json()["campaign_id"] == campaign_id


def test_create_distribution_for_campaign_succeeds():
    _, owner_token = register_and_login_user(role="project_owner")

    campaign_response = client.post(
        "/campaign/campaigns",
        json=build_campaign_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    campaign_id = campaign_response.json()["id"]

    response = client.post(
        "/distribution/distribution",
        json={"campaign_id": campaign_id},
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == 200
    assert response.json()["campaign_id"] == campaign_id

def teardown_module():
    Base.metadata.drop_all(bind=engine)


