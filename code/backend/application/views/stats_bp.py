# - getting ticket statistics $
# - generate report API $

# IMPORTS
from flask import Blueprint, request,send_from_directory,send_file
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    admin_required
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from application.globals import *
from datetime import datetime
from application.views.user_utils import time_to_str
from datetime import date, timedelta
from sqlalchemy import and_
from application.views.ticket_bp import TicketUtils
from tasks import export_ticket_csv_task

now = time_to_str(datetime.now())


class StatsUtils(UserUtils):
    def num_tickets_in_time_period(self, date1, date2):
        tickets_found = Ticket.query.filter(
            Ticket.created_at.between(date1, date2)
        ).all()

        return tickets_found

    def num_resolved_tickets_in_time_period(self, date1, date2):
        tickets_found = Ticket.query.filter(
            and_(Ticket.created_at.between(date1, date2)),
            Ticket.ticket_status == "resolved",
        ).all()

        return tickets_found

    def num_tickets_today(self, date):
        tickets_found = Ticket.query.filter_by(created_at=date).all()
        return tickets_found

    def new_users_registered(self, date):
        return

    def total_users(self):
        total_students = User.query.filter_by(role_id=3).all()
        total_staff = User.query.filter_by(role_id=2).all()
        total_admin = User.query.filter_by(role_id=1).all()
        return len(total_admin), len(total_staff), len(total_students)

    def str_to_date(self, date_str):
        format = "%Y-%m-%d"
        date = datetime.strptime(date_str, format).date()
        return date


stats_bp = Blueprint("stats_bp", __name__)
stats_api = Api(stats_bp)
stats_util = StatsUtils()


class StatsAPI(Resource):

    @token_required
    def get(self):
        try:
            data = {
                "new_users_registered": 0,
                "total_open_tickets": 0,
                "total_resolved_tickets": 0,
                "tickets_raised_today": 0,
                "tickets_raised_month": 0,
                "tickets_raised_week": 0,
                "total_admin": 0,
                "total_support_staff": 0,
                "total_students": 0,
            }
            data["total_admin"], data["total_support_staff"], data["total_students"] = (
                stats_util.total_users()
            )
            # data["tickets_raised_week"] = len(stats_util.num_tickets_in_time_period())
            data["total_open_tickets"] = len(
                Ticket.query.filter(Ticket.ticket_status != "Resolved").all()
            )
            data["new_users_registered"] = len(
                User.query.filter_by(is_approved=False).all()
            )
            data["total_resolved_tickets"] = len(
                Ticket.query.filter_by(ticket_status="Resolved").all()
            )
            data["tickets_raised_today"] = len(
                stats_util.num_tickets_today(datetime.now())
            )
            data["tickets_raised_month"] = len(
                stats_util.num_tickets_in_time_period(
                    date.today().replace(day=1) - timedelta(days=1), datetime.now()
                )
            )
            data["tickets_raised_week"] = len(stats_util.num_tickets_in_time_period(datetime.now() - timedelta(days=7),datetime.now()))

            return success_200_custom(data=data)

        except Exception as e:
            logger.error(
                f"StatsAPI->get : Error occured while fetching data: {e}"
            )
            raise InternalServerError

    @token_required
    @users_required(users=["admin"])
    def post(self):
        details = {"date1": "", "date2": "", "resolved": ""}
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                details[key] = value
        except Exception as e:
            logger.error(
                f"StatsAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            d1 = details["date1"]
            d2 = details["date2"]
            date1 = stats_util.str_to_date(d1)
            date2 = stats_util.str_to_date(d2)
            if details["Resolved"] == False:
                tickets = stats_util.num_tickets_in_time_period(date1, date2)
            else:
                tickets = stats_util.num_resolved_tickets_in_time_period(date1, date2)

            # convert tickets into json objects!!
            tickets_found = []
            for t in tickets:
                tickets_found.append(Ticket.to_dict(t))
            return success_200_custom(data=tickets_found)


class StatsReport(Resource):

    @token_required
    @users_required(users=['admin'])
    def get(self):
        logger.info("Generating report and then sending that to user.")
        task_result = export_ticket_csv_task.delay()

        # Once the task is completed, retrieve the CSV filename
        task_result.wait()  # Wait for the task to finish
        csv_filename = task_result.result.get('csv_filename')

        # Send the generated CSV file to the user
        csv_directory = '../../databases/csv_files/'  # Path to csv_files directory
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), csv_directory, csv_filename))

        # Send the generated CSV file to the user
        return send_file(csv_path, as_attachment=True)



stats_api.add_resource(StatsAPI, "/", endpoint="stats_get")
stats_api.add_resource(StatsReport,'/generate_report')
