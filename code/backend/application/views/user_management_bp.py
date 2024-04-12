from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.views.inbox_bp import post_message
from application.responses import *
from application.models import User, Ticket, Badge, AssignBadge
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
        
    def update_badge_table(self, details: dict):
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
        badge = Badge(
            badge_name = details["badge_name"],
            badge_picture_location= details["badge_picture_location"]
            )
        db.session.add(badge)
        db.session.commit()

    def update_assign_badge_table(self, details: dict):
        """
        Usage
        -----
        Update AssignBadge table

        Parameters
        ----------
        details : dict with badge and user details

        Returns
        -------
        details

        """
        badge = AssignBadge(
            badge_name = details["badge_name"],
            user_id = details["user_id"]
            )
        db.session.add(badge)
        db.session.commit()


user_management_bp = Blueprint("user_management_utils", __name__)
user_management_api = Api(user_management_bp)
user_management_util = UserManagementUtils()

class BadgeAPI(Resource):
    def get(self, user_id=""): 
        try:
            user_badges = []
            badge_names = []
            badges = AssignBadge.query.filter_by(user_id=user_id).all()
            for badge in badges:
                b = AssignBadge.to_dict(badge)
                user_badges.append(b)
                badge_names.append(b["badge_name"])
            logger.info(f"All Badges found")

            return success_200_custom(data=badge_names)

        except Exception as e:
            logger.error(
                f"BadgeAPI->get : Error occured while fetching user badges: {e}"
            )
            raise InternalServerError
    

    @token_required
    @users_required(users=["Admin"])
    def post(self):
        """
        Usage
        -----
        Create Badge

        Parameters
        ----------
        form data sent with request
        data format {
                    'badge_name':'',
                    'badge_picture_location':''
                    }

        Returns
        -------
        Status

        """

        details = {
            "badge_name": "",
            "badge_picture_location":"",
        }

        try:
            form = request.get_json()
            
        except Exception as e:
            logger.error(
                f"Badge->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            for key in details:
                value = form.get(key, "")
                if user_management_util.is_blank(value):
                    raise BadRequest(status_msg=f"{key} is empty or invalid")
                else:
                    details[key] = value

            if details:        
                user_management_util.update_badge_table(details=details)
            
                logger.info("Badge Created")
                raise Success_200(
                    status_msg="Badge Created Successfully."
                )

            else:
                raise BadRequest(
                    status_msg="Cannot create Badge"
                )

    @token_required
    @users_required(users=["Admin"])       
    def delete(self,badge_id):
        """
        Delete a badge from the database.

        Parameters
        ----------
        badge_name : str
            The id of the badge to be deleted.

        Raises
        ------
        Exception
            If the deletion fails for any reason.
        """
        try:
            badge = Badge.query.filter_by(id=badge_id).first()
            if badge:
                db.session.delete(badge)
                db.session.commit()
                logger.info(f"Badge '{badge_id}' deleted successfully.")
                raise Success_200(
                    status_msg="Badge Deleted Successfully."
                )
            else:
                logger.warning(f"Badge '{badge_id}' not found in the database.")
                raise NotFoundError(
                    status_msg="Badge Not Found"
                )
        except Exception as e:
            logger.error(f"Error occurred while deleting badge '{badge_id}': {e}")
            raise e

class AssignBadgeAPI(Resource):

    @token_required
    @users_required(users=["Admin"])
    def post(self):
        """
        Usage
        -----
        Create Badge

        Parameters
        ----------
        form data sent with request
        data format {
                    'user_email':'',
                    'badge_name':''
                    }

        Returns
        -------
        Status

        """

        details = {
            "user_id":"",
            "badge_name":"",
        }

        try:
            form = request.get_json()
            
        except Exception as e:
            logger.error(
                f"AssignBadge->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            for key in details:
                value = form.get(key, "")
                if user_management_util.is_blank(value):
                    raise BadRequest(status_msg=f"{key} is empty or invalid")
                else:
                    details[key] = value

            print(details)
            if details:        
                user = User.query.filter_by(id=details["user_id"]).first()
                if user: 
                    user_id = user.id
                    details["user_id"] = user_id
                    print (details)
                    user_management_util.update_assign_badge_table(details=details)
                
                    logger.info("Badge Assigned")
                    post_message(user_id, "Congratulations! You've been awarded a new badge!", "inbox")
                    raise Success_200(
                        status_msg="Badge Assigned Successfully"
                    )

            else:
                raise BadRequest(
                    status_msg="Cannot assign Badge"
                )
    
    @token_required
    @users_required(users=["Admin"])        
    def delete(self,badge_assign_id):
        """
        Revoke a badge.

        Parameters
        ----------
        badge_id : int
            The id of the badge to be revoked.

        Raises
        ------
        Exception
            If the revoke fails for any reason.
        """
        try:
            badge = AssignBadge.query.filter_by(id=badge_assign_id).first()
            if badge:
                user_id = badge.user_id
                db.session.delete(badge)
                db.session.commit()
                logger.info(f"Badge '{badge_assign_id}' revoked successfully.")
                post_message(user_id, "Your badge has been revoked!", "inbox")
                raise Success_200(
                    status_msg="Badge Revoked Successfully."
                )
            else:
                logger.warning(f"Badge '{badge_assign_id}' not found in the database.")
                raise NotFoundError(
                    status_msg="Badge Not Found"
                )
        except Exception as e:
            logger.error(f"Error occurred while deleting badge '{badge_assign_id}': {e}")
            raise e

class UserManagementAPI(Resource):
    @token_required
    @users_required(users=["Admin"])
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

user_management_api.add_resource(UserManagementAPI, "/<string:user_id>/card")  
user_management_api.add_resource(BadgeAPI, "/badge", "/badge/<int:badge_id>", "/badge/<string:user_id>")
user_management_api.add_resource(AssignBadgeAPI, "/assign/badge", "/assign/badge/<int:badge_assign_id>")