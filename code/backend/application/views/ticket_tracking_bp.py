# a - change ticket status () put
# b- change priority (manual) put
# c- create ticket data - ( open , time resolve etc ) post
# d- send notifications when assigning -- > jobs
# e- send status report
# f- escalation + ( adding a new entry to the ticket data table , with the same ticket id )

import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from application.logger import logger
import hashlib
import time
from application.database import db
from application.common_utils import (
    token_required,
    users_required,
)
from application.common_utils import (
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils, time_to_str
from application.responses import *
from application.globals import *
from application.models import *
from copy import deepcopy
from application.notifications import send_email

# UTILS


class TicketTrackingUtils(UserUtils):
    def convert_data_to_dict(self, ticket_data):
        data_dict = vars(ticket_data)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in data_dict:
            del data_dict["_sa_instance_state"]

        return data_dict


tracking_bp = Blueprint("ticket_tracking_bp", __name__)
tracking_api = Api(tracking_bp)
tracking_utils = TicketTrackingUtils()


class TicketTrackingAPI(Resource):
    def get(self, ticket_id=""):
        if tracking_utils.is_blank(ticket_id):
            raise BadRequest(status_msg="Ticket id is missing")

        try:
            # check if ticket_id is unique or not
            data = TicketData.query.filter_by(ticket_id=ticket_id).first()
            tracking_data = TicketData.to_dict(data)
            logger.info(f"Tracking data found!")
            return success_200_custom(data=tracking_data)
        except Exception as e:
            logger.error(
                f"TicketTrackingAPI->get : Error occured while fetching ticket tracking data: {e}"
            )
            raise InternalServerError

    def put(self, ticket_id=""):

        details = {
            "resolved_at": "",
            "assigned_at": "",
            "inProgress_at": "",
            "closed_at": "",
            "reopened_at": "",
        }
        if tracking_utils.is_blank(ticket_id):
            raise BadRequest(status_msg="Ticket id is missing")
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                details[key] = value
        except Exception as e:
            logger.error(f"TrackingAPI->put : Error occured while getting form data : {e}")
            raise InternalServerError
        #print(details)
        try:
            ticket_data = TicketData.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketTrackingAPI->put : Error occured while fetching the ticket data : {e}"
            )
            raise InternalServerError
        #print(ticket_data)
        if ticket_data:
            if details["resolved_at"] != "":
                ticket_data.resolved_at = datetime.datetime.now()
            if details["assigned_at"] != "":
                ticket_data.assigned_at = datetime.datetime.now()
            if details["inProgress_at"] != "":
                ticket_data.inProgress_at = datetime.datetime.now()
            if details["closed_at"] != "":
                ticket_data.closed_at = datetime.datetime.now()
            if details["reopened_at"] != "":
                ticket_data.reopened_at = datetime.datetime.now()
                ticket = Ticket.query.filter_by(id=ticket_id).first()
                if ticket.solution == None: 
                    ticket.solution = " "
                elif "ESCALATED!" in ticket.solution:
                    pass
                else: 
                    ticket.solution = "ESCALATED!" + ticket.solution; 

            #print(ticket_data.reopened_at)
            db.session.commit()
            logger.info(f"TicketTracking data updated")
            raise Success_200(status_msg="TicketTracking data updated successfully.")

    def delete(self, ticket_id=""):
        return


tracking_api.add_resource(
    TicketTrackingAPI, "/<string:ticket_id>", endpoint="ticket_tracking"
)
# tracking_api.add_resource(TicketTrackingAPI, "/<string:ticket_id>/<string:status>", endpoint="ticket_tracking_update")
