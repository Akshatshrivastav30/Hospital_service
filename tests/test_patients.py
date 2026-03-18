import pytest
from app import create_app
from app.database import db as _db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── Health check ──────────────────────────────
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "healthy"


# ── Create patient ────────────────────────────
def test_create_patient(client):
    payload = {
        "name": "Ravi Kumar",
        "age": 35,
        "gender": "Male",
        "contact": "9876543210",
        "blood_group": "O+",
        "diagnosis": "Hypertension",
    }
    res = client.post("/api/patients/", json=payload)
    assert res.status_code == 201
    assert res.json["name"] == "Ravi Kumar"
    assert res.json["id"] == 1


def test_create_patient_missing_fields(client):
    res = client.post("/api/patients/", json={"name": "Incomplete"})
    assert res.status_code == 400
    assert "Missing fields" in res.json["error"]


# ── Get patients ──────────────────────────────
def test_get_all_patients_empty(client):
    res = client.get("/api/patients/")
    assert res.status_code == 200
    assert res.json["count"] == 0


def test_get_patient_by_id(client):
    client.post("/api/patients/", json={
        "name": "Priya Singh", "age": 28, "gender": "Female", "contact": "9000000001"
    })
    res = client.get("/api/patients/1")
    assert res.status_code == 200
    assert res.json["name"] == "Priya Singh"


def test_get_nonexistent_patient(client):
    res = client.get("/api/patients/999")
    assert res.status_code == 404


# ── Update patient ────────────────────────────
def test_update_patient(client):
    client.post("/api/patients/", json={
        "name": "Amit Shah", "age": 45, "gender": "Male", "contact": "9111111111"
    })
    res = client.put("/api/patients/1", json={"diagnosis": "Diabetes Type 2"})
    assert res.status_code == 200
    assert res.json["diagnosis"] == "Diabetes Type 2"


# ── Delete patient ────────────────────────────
def test_delete_patient(client):
    client.post("/api/patients/", json={
        "name": "Delete Me", "age": 30, "gender": "Male", "contact": "9000000000"
    })
    res = client.delete("/api/patients/1")
    assert res.status_code == 200
    assert "deleted" in res.json["message"]