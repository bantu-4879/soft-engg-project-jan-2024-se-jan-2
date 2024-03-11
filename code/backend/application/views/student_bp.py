# --------------------  Imports  --------------------

from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import User, Ticket,VoteTable
from application.globals import *

# --------------------  Code  --------------------


class StudentUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id


student_bp = Blueprint("student_bp", __name__)
student_api = Api(student_bp)
student_util = StudentUtils()


class StudentAPI(Resource):
    @token_required
    @users_required(users=["Student"])
    def get(self, user_id):
        """
        Usage
        -----
        Get a details of student from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if student_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(
                f"StudentAPI->get : Error occured while fetching student data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role.name == "Student":
                    n_tickets_created = Ticket.query.filter_by(
                        created_by=user_id
                    ).count()
                    n_tickets_resolved = Ticket.query.filter_by(
                        created_by=user_id, status="resolved"
                    ).count()
                    n_tickets_pending = n_tickets_created - n_tickets_resolved
                    n_tickets_upvoted = VoteTable.query.filter_by(
                        voter_id=user_id
                    ).count()
                    student_dict = student_util.convert_user_data_to_dict(user)
                    student_dict["n_tickets_created"] = n_tickets_created
                    student_dict["n_tickets_resolved"] = n_tickets_resolved
                    student_dict["n_tickets_pending"] = n_tickets_pending
                    student_dict["n_tickets_upvoted"] = n_tickets_upvoted

                    return success_200_custom(data=student_dict)
                else:
                    raise BadRequest(status_msg="User must be a student.")
            else:
                raise NotFoundError(status_msg="Student user id does not exists")

    @token_required
    @users_required(users=["Student"])
    def put(self, user_id):
        """
        Usage
        ------
        Update student profile,
        Student can update first name, last name, email, password, profile picture location
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
                f"StudentAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            student_util.update_user_profile_data(user_id, form)


student_api.add_resource(StudentAPI, "/<string:user_id>")  # path is /api/v1/student

# --------------------  END  --------------------