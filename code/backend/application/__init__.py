# --------------------  Imports  --------------------

from flask import Flask
from application.config import DevelopmentConfig, TestingConfig
from application.database import db
from application.logger import logger
from application.globals import API_VERSION
from application.views.auth_bp import auth_bp
# from application.views import student_bp
# from application.views import support_bp
# from application.views import admin_bp
# from application.views import faq_bp
# from application.views import ticket_bp
from flask_cors import CORS
from application.models import *
import os
from application.g_webhook import gchat_webhook

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
    # app.register_blueprint(student_bp, url_prefix=f"/api/{API_VERSION}/student") --> 
    # app.register_blueprint(support_bp, url_prefix=f"/api/{API_VERSION}/support") --> 
    # app.register_blueprint(admin_bp, url_prefix=f"/api/{API_VERSION}/admin") -->
    # app.register_blueprint(ticket_bp, url_prefix=f"/api/{API_VERSION}/ticket") -->
    # app.register_blueprint(faq_bp, url_prefix=f"/api/{API_VERSION}/faq") --> 

    app.app_context().push()

    print("the app context is there")
    if not os.path.exists(DevelopmentConfig.db_path):
        db.create_all()
        app.app_context().push()
        print("the database is getting created.")
        role1=Role(
            name="Admin"
        )
        role2=Role(
            name="Staff"
        )
        role3=Role(
            name="Student"
        )
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit()

    gchat_webhook()
    return app