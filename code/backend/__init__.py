# --------------------  Imports  --------------------

from flask import Flask
from application.config import DevelopmentConfig, TestingConfig
from application.database import db
from application.logger import logger
from application.globals import API_VERSION
from application.views.routes import auth_bp
from application.views.student_bp import student_bp
from application.views.support_bp import support_bp
from application.views.admin_bp import admin_bp
from application.views.faq_bp import faq_bp
from application.views.ticket_bp import ticket_bp
from flask_cors import CORS


# --------------------  Code  --------------------


def create_app(env_type="dev"):
    app = Flask(__name__, template_folder="templates")
    if env_type == "dev":
        app.config.from_object(DevelopmentConfig)
        logger.info("Development environment configured.")
    if env_type == "test":
        app.config.from_object(TestingConfig)
        logger.info("Testing environment configured.")

    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix=f"/api/{API_VERSION}/auth")
    app.register_blueprint(student_bp, url_prefix=f"/api/{API_VERSION}/student")
    app.register_blueprint(support_bp, url_prefix=f"/api/{API_VERSION}/support")
    app.register_blueprint(admin_bp, url_prefix=f"/api/{API_VERSION}/admin")
    app.register_blueprint(ticket_bp, url_prefix=f"/api/{API_VERSION}/ticket")
    app.register_blueprint(faq_bp, url_prefix=f"/api/{API_VERSION}/faq")

    app.app_context().push()
    db.create_all()
    db.session.commit()

    return app