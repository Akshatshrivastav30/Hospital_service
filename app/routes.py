from flask import Blueprint, request, jsonify
from .database import db
from .models import Patient

patients_bp = Blueprint("patients", __name__)


# GET all patients
@patients_bp.route("/", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify({"patients": [p.to_dict() for p in patients], "count": len(patients)}), 200


# GET single patient
@patients_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id, description="Patient not found")
    return jsonify(patient.to_dict()), 200


# CREATE patient
@patients_bp.route("/", methods=["POST"])
def create_patient():
    data = request.get_json()

    required = ["name", "age", "gender", "contact"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    patient = Patient(
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        contact=data["contact"],
        blood_group=data.get("blood_group"),
        diagnosis=data.get("diagnosis"),
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


# UPDATE patient
@patients_bp.route("/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id, description="Patient not found")
    data = request.get_json()

    for field in ["name", "age", "gender", "contact", "blood_group", "diagnosis"]:
        if field in data:
            setattr(patient, field, data[field])

    db.session.commit()
    return jsonify(patient.to_dict()), 200


# DELETE patient
@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id, description="Patient not found")
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": f"Patient {patient_id} deleted successfully"}), 200