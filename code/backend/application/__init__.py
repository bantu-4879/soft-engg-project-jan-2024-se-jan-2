# --------------------  Imports  --------------------

from flask import Flask
from flask_migrate import Migrate
from application.config import DevelopmentConfig, TestingConfig
from application.database import db
from application.logger import logger
from application.globals import API_VERSION
from application.views.auth_bp import auth_bp
from application.views.user_management_bp import user_management_bp
from application.views.student_bp import student_bp
from application.views.staff_bp import staff_bp
from application.views.admin_bp import admin_bp
from application.views.faq_bp import faq_bp
from application.views.ticket_bp import ticket_bp
from application.views.inbox_bp import inbox_bp
from application.views.tags_bp import tags_bp
from application.views.discourseAuth_bp import discourseAuth_bp
from application.views.stats_bp import stats_bp
from application.views.ticket_tracking_bp import tracking_bp
from application.views.userDetails_bp import userDetails_bp
from flask_cors import CORS
from application.models import *
import os
#from application.g_webhook import gchat_webhook
from application.views.inbox_bp import post_message
from application.views.discoursePost_bp import discoursePost_bp
#from code.backend.celery_worker import celery_init_app
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
    migrate = Migrate(app, db, render_as_batch=True)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix=f"/api/{API_VERSION}/auth") 
    app.register_blueprint(student_bp, url_prefix=f"/api/{API_VERSION}/student")  
    app.register_blueprint(staff_bp, url_prefix=f"/api/{API_VERSION}/staff") 
    app.register_blueprint(admin_bp, url_prefix=f"/api/{API_VERSION}/admin") 
    app.register_blueprint(ticket_bp, url_prefix=f"/api/{API_VERSION}/ticket") 
    app.register_blueprint(faq_bp, url_prefix=f"/api/{API_VERSION}/faq") 
    app.register_blueprint(user_management_bp,url_prefix=f"/api/{API_VERSION}/management")
    app.register_blueprint(inbox_bp, url_prefix=f"/api/{API_VERSION}/inbox")
    app.register_blueprint(discourseAuth_bp, url_prefix=f"/api/{API_VERSION}/discourseAuth")
    app.register_blueprint(tags_bp, url_prefix=f"/api/{API_VERSION}/tags")
    app.register_blueprint(tracking_bp,url_prefix=f"/api/{API_VERSION}/tracking")
    app.register_blueprint(stats_bp,url_prefix=f"/api/{API_VERSION}/data" )
    app.register_blueprint(discoursePost_bp,url_prefix=f"/api/{API_VERSION}/discourse")
    app.register_blueprint(userDetails_bp,url_prefix=f"/api/{API_VERSION}/userDetails")
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

    if not os.path.exists(TestingConfig.db_path):
        print("Creating Testing Database")
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

    #gchat_webhook()
    #post_message(0,"This is a test message!","inbox")

    #initializing celery 
    return app