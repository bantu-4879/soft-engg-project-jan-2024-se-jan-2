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


now = time_to_str(datetime.now())


class StatsUtils(UserUtils): 
    def get_data_for_admin():
        return ""

stats_bp = Blueprint("stats_bp", __name__)
stats_api = Api(stats_bp)
stats_util = StatsUtils()

class StatsAPI(Resource): 
    def get(self): 
        info = []
        return success_200_custom(data=info)

stats_api.add_resource(StatsAPI, "/", endpoint="stats_get")
    

