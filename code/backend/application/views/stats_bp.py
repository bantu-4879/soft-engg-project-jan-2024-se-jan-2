# - getting ticket statistics $
# - generate report API $

# IMPORTS
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from application.globals import *
from datetime import datetime
from application.views.user_utils import time_to_str
from datetime import date
from sqlalchemy import and_
from application.views.ticket_bp import TicketUtils

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


stats_bp = Blueprint("stats_bp", __name__)
stats_api = Api(stats_bp)
stats_util = StatsUtils()


class StatsAPI(Resource):
    def get(self):
        return

    # @token_required
    # @users_required(users=["Admin"])
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
            date1 = date(int(d1[:4]), int(d1[4:5]), int(d1[5:]))
            date2 = date(int(d2[:4]), int(d2[4:5]), int(d2[5:]))
            if details["resolved"] == False:
                tickets = stats_util.num_tickets_in_time_period(date1, date2)
            else: 
                tickets = stats_util.num_resolved_tickets_in_time_period(date1, date2)

        #convert tickets into json objects!!
            return success_200_custom(data=tickets)


stats_api.add_resource(StatsAPI, "/", endpoint="stats_get")
