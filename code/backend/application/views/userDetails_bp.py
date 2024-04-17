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


class UserDetailsUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id


userDetails_bp = Blueprint("userDetails_bp", __name__)
userDetails_api = Api(userDetails_bp)
userDetails_util = UserDetailsUtils()


class UserdetailsAPI(Resource):
    
    def get(self, user_id):
        
        if userDetails_util.is_blank(user_id):
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
                return success_200_custom(data=user.to_dict())  
            else:
                raise NotFoundError(status_msg="User not found")

    

userDetails_api.add_resource(UserdetailsAPI, "/<string:user_id>")  # path is /api/v2/userDetails/<user_id>

# --------------------  END  --------------------