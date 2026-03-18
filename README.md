# NoDO-02 — Dockerized Healthcare Flask API

> A containerized Python Flask REST API for managing patient records, built with DevOps best practices.

---

## Tech Stack

| Layer         | Tool                          |
| ------------- | ----------------------------- |
| Language      | Python 3.11                   |
| Framework     | Flask 3.0                     |
| Database      | SQLite (via Flask-SQLAlchemy) |
| Container     | Docker (Multi-stage build)    |
| Orchestration | Docker Compose                |
| Server        | Gunicorn (Production WSGI)    |
| Testing       | Pytest                        |

---

## Project Structure

```
nodo-02/
├── app/
│   ├── __init__.py       # App factory + CORS + /health route
│   ├── database.py       # SQLAlchemy instance
│   ├── models.py         # Patient model
│   └── routes.py         # CRUD endpoints
├── tests/
│   └── test_patients.py  # Pytest test suite (8 tests)
├── index.html            # Web UI dashboard
├── Dockerfile            # Multi-stage build (builder + production)
├── docker-compose.yml    # Container orchestration
├── requirements.txt      # Python dependencies
├── .dockerignore         # Exclude unnecessary files from image
├── .gitignore
└── run.py                # App entrypoint
```

---

## Getting Started

### Prerequisites

- Docker Desktop (running)
- Python 3.11+ (for local testing)

### Step 1 — Clone & navigate

```bash
cd nodo-02
```

### Step 2 — Start the container

```bash
docker compose up --build
```

Wait for:

```
healthcare-api | [INFO] Listening at: http://0.0.0.0:5000
healthcare-api | [INFO] Booting worker with pid: 7
healthcare-api | [INFO] Booting worker with pid: 8
```

### Step 3 — Verify it's running

```bash
docker ps
```

Expected output:

```
CONTAINER ID   IMAGE                   PORTS                      NAMES
xxxxxxxxxxxx   healthcare-api:latest   0.0.0.0:5001->5000/tcp     healthcare-api
```

---

## API Endpoints

| Method | Endpoint             | Description        | Status Code |
| ------ | -------------------- | ------------------ | ----------- |
| GET    | `/health`            | Health check       | 200         |
| GET    | `/api/patients/`     | Get all patients   | 200         |
| GET    | `/api/patients/<id>` | Get patient by ID  | 200         |
| POST   | `/api/patients/`     | Create new patient | 201         |
| PUT    | `/api/patients/<id>` | Update patient     | 200         |
| DELETE | `/api/patients/<id>` | Delete patient     | 200         |

---

## Testing the API

### 1. Health Check

```bash
curl http://localhost:5001/health
```

Expected:

```json
{
  "service": "healthcare-api",
  "status": "healthy"
}
```

---

### 2. Create a Patient

```bash
curl -X POST http://localhost:5001/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ravi Kumar",
    "age": 35,
    "gender": "Male",
    "contact": "9876543210",
    "blood_group": "O+",
    "diagnosis": "Hypertension"
  }'
```

Expected:

```json
{
  "id": 1,
  "name": "Ravi Kumar",
  "age": 35,
  "gender": "Male",
  "contact": "9876543210",
  "blood_group": "O+",
  "diagnosis": "Hypertension",
  "created_at": "2026-03-18T17:23:20.720459",
  "updated_at": "2026-03-18T17:23:20.720459"
}
```

---

### 3. Get All Patients

```bash
curl http://localhost:5001/api/patients/
```

Expected:

```json
{
  "count": 1,
  "patients": [...]
}
```

---

### 4. Get Patient by ID

```bash
curl http://localhost:5001/api/patients/1
```

Expected:

```json
{
  "id": 1,
  "name": "Ravi Kumar",
  ...
}
```

---

### 5. Update a Patient

```bash
curl -X PUT http://localhost:5001/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Hypertension - Under Control"
  }'
```

Expected:

```json
{
  "id": 1,
  "diagnosis": "Hypertension - Under Control",
  ...
}
```

---

### 6. Delete a Patient

```bash
curl -X DELETE http://localhost:5001/api/patients/1
```

Expected:

```json
{
  "message": "Patient 1 deleted successfully"
}
```

---

## Web UI Dashboard

A standalone HTML dashboard to interact with the API visually.

### Run the UI

```bash
open index.html
```

This opens the dashboard directly in your browser. No server needed.

### Features

- Health check indicator
- View all patient records
- Add new patients via form
- Edit existing patient details
- Delete patients with confirmation
- Live patient count

> Make sure Docker container is running before opening the UI.

---

## Postman Collection

Import `NoDO-02-Healthcare-API.postman_collection.json` into Postman for a ready-to-use collection of all endpoints.

**Import steps:**

1. Open Postman
2. Click **Import** (top left)
3. Select the JSON file
4. Collection appears in sidebar under `NoDO-02 Healthcare API`

---

## Running Tests

The test suite uses **in-memory SQLite** — completely isolated from the running Docker container.

### Step 1 — Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt pytest flask-cors
```

### Step 3 — Run tests

```bash
python -m pytest tests/ -v
```

### Expected output

```
============================= test session starts ==============================
collected 8 items

tests/test_patients.py::test_health                         PASSED  [ 12%]
tests/test_patients.py::test_create_patient                 PASSED  [ 25%]
tests/test_patients.py::test_create_patient_missing_fields  PASSED  [ 37%]
tests/test_patients.py::test_get_all_patients_empty         PASSED  [ 50%]
tests/test_patients.py::test_get_patient_by_id              PASSED  [ 62%]
tests/test_patients.py::test_get_nonexistent_patient        PASSED  [ 75%]
tests/test_patients.py::test_update_patient                 PASSED  [ 87%]
tests/test_patients.py::test_delete_patient                 PASSED  [100%]

============================== 8 passed in 0.35s ===============================
```

### Test coverage

| Test                                 | What it validates                             |
| ------------------------------------ | --------------------------------------------- |
| `test_health`                        | `/health` returns 200 and healthy status      |
| `test_create_patient`                | POST creates record and returns 201           |
| `test_create_patient_missing_fields` | Missing fields returns 400 with error message |
| `test_get_all_patients_empty`        | Empty DB returns count 0                      |
| `test_get_patient_by_id`             | GET by ID returns correct record              |
| `test_get_nonexistent_patient`       | Invalid ID returns 404                        |
| `test_update_patient`                | PUT updates field correctly                   |
| `test_delete_patient`                | DELETE removes record and confirms            |

---

## Docker Details

### Multi-stage Dockerfile

| Stage        | Purpose                         | Included in final image |
| ------------ | ------------------------------- | ----------------------- |
| `builder`    | Installs deps with gcc compiler | No — discarded          |
| `production` | Runs the app as non-root user   | Yes                     |

### Key security practices

- Non-root user `healthcare` runs the app
- No build tools (`gcc`) in the final image
- `.dockerignore` excludes secrets, cache, and local DB
- Gunicorn production server (not Flask dev server)
- Health check built into both Dockerfile and Compose
- Named volume persists SQLite data across restarts

### Useful Docker commands

```bash
# Start in background
docker compose up -d --build

# View live logs
docker compose logs -f

# Stop container
docker compose down

# Check container health
docker ps

# Inspect image size
docker images healthcare-api
```

---

## Next Steps

| Phase   | Topic                                                  |
| ------- | ------------------------------------------------------ |
| NoDO-03 | GitHub Actions CI/CD pipeline                          |
| NoDO-04 | Kubernetes deployment (Deployment + Service + Ingress) |
| NoDO-05 | Terraform infrastructure provisioning on AWS           |
