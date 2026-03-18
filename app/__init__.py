from flask import Flask
from flask_cors import CORS
from .database import db
from .routes import patients_bp


def create_app(config=None):
    app = Flask(__name__)

    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthcare.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-me-in-production"

    if config:
        app.config.update(config)

    CORS(app)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(patients_bp, url_prefix="/api/patients")

    # Create tables on first run
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "healthcare-api"}, 200

    return app