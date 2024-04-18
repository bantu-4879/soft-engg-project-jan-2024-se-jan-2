from celery.schedules import crontab

# from flask import current_app as app
# from models import db

# from app import get_user

broker_url = "redis://localhost:6379/1"
result_backend = "redis://localhost:6379/2"
broker_connection_retry_on_startup = True
timezone = "Asia/Kolkata"
imports = ("tasks",)

beat_schedule = {
    "test_task": {
        "task": "tasks.test_task",
        "schedule": crontab(hour=20, minute=26),
        # "schedule" : 20.0,
    },
    "monthly_admin_report": {
        "task": "tasks.send_monthly_ticket_report",
        "schedule": crontab(hour=10, minute=30, day_of_month=18),
        # "schedule" : 20.0,
    },
}
