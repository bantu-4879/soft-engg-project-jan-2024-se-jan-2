from celery.schedules import crontab

# from flask import current_app as app
from models import db

# from app import get_user

broker_url = "redis://localhost:6379/1"
result_backend = "redis://localhost:6379/2"
broker_connection_retry_on_startup = True
timezone = "Asia/Kolkata"

beat_schedule = {
    "daily_user_reminder": {
        "task": "tasks.priority_update",
        "schedule": crontab(hour=11, minute=57),
        # "schedule" : 20.0,
    },
    # "monthly_admin_report": {
    #     "task": "tasks.monthly_report",
    #     "schedule": crontab(hour=11, minute=57, day_of_month=1),
    #     # "schedule" : 20.0,
    # },
}