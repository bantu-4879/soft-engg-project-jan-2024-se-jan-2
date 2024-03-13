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


class StatsUtils(): 
    def get_data_for_admin():
        return ""



class StatsAPI(): 
    def get(self): 
        return ""
    
    def post(self): 
        return ""

