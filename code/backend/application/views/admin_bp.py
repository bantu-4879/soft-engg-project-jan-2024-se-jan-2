# --------------------  Imports  --------------------

from datetime import datetime
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


# --------------------  Code  --------------------


class AdminUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def get_timestamps_for_ticket_counting(self):
        date_format = "%Y-%m-%d %H:%M:%S"
        per_day_seconds = 24 * 60 * 60

        current_date = datetime.datetime.now()
        current_day = current_date.day
        current_month = current_date.month
        current_year = current_date.year
        current_weekday = current_date.isoweekday()  # monday = 1

        current_timestamp = datetime.datetime.timestamp(current_date)

        this_day_start = datetime.datetime.strptime(
            f"{current_year}-{str(current_month).zfill(2)}-{str(current_day).zfill(2)} 00:00:00",
            date_format,
        )
        this_day_start_timestamp = datetime.datetime.timestamp(this_day_start)

        this_week_start_timestamp = current_timestamp - (
            (current_timestamp - this_day_start_timestamp)
            + (per_day_seconds * (current_weekday - 1))
        )

        this_month_start = datetime.datetime.strptime(
            f"{current_year}-{str(current_month).zfill(2)}-{str(1).zfill(2)} 00:00:00",
            date_format,
        )
        this_month_start_timestamp = datetime.datetime.timestamp(this_month_start)
        return (
            current_timestamp,
            this_day_start_timestamp,
            this_week_start_timestamp,
            this_month_start_timestamp,
        )


admin_bp = Blueprint("admin_bp", __name__)
admin_api = Api(admin_bp)
admin_util = AdminUtils()


class AdminAPI(Resource):
    @token_required
    @users_required(users=["admin"])
    def get(self, user_id):
        """
        Usage
        -----
        Get a details of admin from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if admin_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(
                f"AdminAPI->get : Error occured while fetching admin data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role_id == 1:
                    n_total_unresolved_tickets = Ticket.query.filter_by(
                        ticket_status="pending"
                    ).count()
                    n_total_resolved_tickets = Ticket.query.filter_by(
                        ticket_status="resolved"
                    ).count()
                    ticket_creation_timestamp_list = [
                        ticket.created_at for ticket in Ticket.query.all()
                    ]
                    (
                        current_timestamp,
                        this_day_start_timestamp,
                        this_week_start_timestamp,
                        this_month_start_timestamp,
                    ) = admin_util.get_timestamps_for_ticket_counting()
                    # n_tickets_today = sum(
                    #     [
                    #         1
                    #         for ts in ticket_creation_timestamp_list
                    #         if current_timestamp >= ts >= this_day_start_timestamp
                    #     ]
                    # )
                    # n_tickets_week = sum(
                    #     [
                    #         1
                    #         for ts in ticket_creation_timestamp_list
                    #         if current_timestamp >= ts >= this_week_start_timestamp
                    #     ]
                    # )
                    # n_tickets_month = sum(
                    #     [
                    #         1
                    #         for ts in ticket_creation_timestamp_list
                    #         if current_timestamp >= ts >= this_month_start_timestamp
                    #     ]
                    # )
                    n_tickets_today = 1 
                    n_tickets_month = 1
                    n_tickets_week = 1
                    all_users_role_verification_list = [
                        (user.role_id, user.is_approved) for user in User.query.all()
                    ]
                    n_student = sum(
                        [
                            1
                            for elem in all_users_role_verification_list
                            if elem[0] == "student"
                        ]
                    )
                    n_support = sum(
                        [
                            1
                            for elem in all_users_role_verification_list
                            if elem[0] == "staff"
                        ]
                    )
                    n_admin = sum(
                        [
                            1
                            for elem in all_users_role_verification_list
                            if elem[0] == "admin"
                        ]
                    )
                    n_student_new = sum(
                        [
                            1
                            for elem in all_users_role_verification_list
                            if (elem[0] == "student" and elem[1] == 0)
                        ]
                    )
                    n_support_new = sum(
                        [
                            1
                            for elem in all_users_role_verification_list
                            if (elem[0] == "Staff" and elem[1] == 0)
                        ]
                    )
                    

                    admin_dict = admin_util.convert_user_data_to_dict(user)
                    
                    admin_dict[
                        "n_total_unresolved_tickets"
                    ] = n_total_unresolved_tickets
                    admin_dict["n_total_resolved_tickets"] = n_total_resolved_tickets
                    admin_dict["n_tickets_today"] = n_tickets_today
                    admin_dict["n_tickets_week"] = n_tickets_week
                    admin_dict["n_tickets_month"] = n_tickets_month
                    admin_dict["n_student"] = n_student
                    admin_dict["n_support"] = n_support
                    admin_dict["n_admin"] = n_admin
                    admin_dict["n_student_new"] = n_student_new
                    admin_dict["n_support_new"] = n_support_new
                    
                    return success_200_custom(data=admin_dict)
                else:
                    raise BadRequest(status_msg="User must be a Admin.")
            else:
                raise NotFoundError(status_msg="Admin does not exists")

    @token_required
    @users_required(users=["admin"])
    def put(self, user_id):
        """
        Usage
        ------
        Update admin profile,
        #admin can update first name, last name, email, password, profile picture location
        ------
        Args:
            user_id (integer): id of user
        ------
        Parameters
        ------
        Form data send with request

        Returns
        ------
        """
        try:
            form = request.get_json()
        except Exception as e:
            logger.error(f"AdminAPI->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            admin_util.update_user_profile_data(user_id, form)


admin_api.add_resource(AdminAPI, "/<string:user_id>")  # path is /api/v1/admin

# --------------------  END  --------------------
