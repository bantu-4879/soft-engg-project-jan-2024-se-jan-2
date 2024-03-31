from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import User, Ticket
from application.globals import *

# --------------------  Code  --------------------


class StaffUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id


staff_bp = Blueprint("staff_bp", __name__)
staff_api = Api(staff_bp)
staff_util = StaffUtils()


class StaffAPI(Resource):
    @token_required
    @users_required(users=["staff"])
    def get(self, user_id):
        """
        Usage
        -----
        Get a details of staff team member from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if staff_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(
                f"staffAPI->get : Error occured while fetching staff data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role_id == 2:
                    n_tickets_resolved = Ticket.query.filter_by(
                        resolved_by=user_id
                    ).count()
                    n_total_unresolved_tickets = Ticket.query.filter_by(
                        ticket_status="pending"
                    ).count()
                    staff_dict = staff_util.convert_user_data_to_dict(user)
                    staff_dict["n_tickets_resolved"] = n_tickets_resolved
                    staff_dict[
                        "n_total_unresolved_tickets"
                    ] = n_total_unresolved_tickets

                    return success_200_custom(data=staff_dict)
                else:
                    raise BadRequest(status_msg="User must be a support staff.")
            else:
                raise NotFoundError(status_msg="Support staff does not exists")

    @token_required
    @users_required(users=["staff"])
    def put(self, user_id):
        """
        Usage
        ------
        Update support profile,
        #support can update first name, last name, email, password, profile picture location
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
            logger.error(
                f"StaffAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            staff_util.update_user_profile_data(user_id, form)


staff_api.add_resource(StaffAPI, "/<string:user_id>")  # path is /api/v1/support

# --------------------  END  --------------------
