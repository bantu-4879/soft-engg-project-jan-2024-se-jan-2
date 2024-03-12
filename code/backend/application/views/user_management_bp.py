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
from application.database import db

# --------------------  Code  --------------------


class UserManagementUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id



    def get_user_activity(self, user_id: str):
        """
        Usage
        -----
        Get User Activity

        Parameters
        ----------
        user_id : int

        Returns
        -------
        details

        """
        return "Yellow"
    
    def update_user_table(self, details: dict):
        """
        Usage
        -----
        Update User table

        Parameters
        ----------
        details : dict with user details

        Returns
        -------
        details

        """
        user_id = details.get("user_id")
        card = details.get("card")
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.card = card
            db.session.add(user)
            db.session.commit()
        else:
            raise NotFoundError(status_msg="User does not exist.")

    

user_management_bp = Blueprint("user_management_utils", __name__)
user_management_api = Api(user_management_bp)
user_management_util = UserManagementUtils()


class UserManagementAPI(Resource):
    # @token_required
    # @users_required(users=["Admin"])
    def put(self, user_id):
        """
        Usage
        ------
        Update admin profile,
        #admin can assign cards to students for disciplinary actions 
        ------
        Args:
            user_id (string): id of user
        ------
        Parameters
        ------
        Form data send with request

        Returns
        ------
        """
        try:
            user_id = user_id
        except Exception as e:
            logger.error(f"UserManagement->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if user_management_util.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")
            
            card = user_management_util.get_user_activity(user_id)

            details = {"user_id": user_id, "card":card}

            # check if user exists
            user = User.query.filter_by(id=user_id).first()
            if user:
                # user exists , proceed to update
                user = user_management_util.update_user_table(details=details)
                raise Success_200(status_msg="User card updated in database.")
            else:
                raise NotFoundError(status_msg="User does not exists.")

user_management_api.add_resource(UserManagementAPI, "/<string:user_id>/card")  # path is /api/v1/user-management