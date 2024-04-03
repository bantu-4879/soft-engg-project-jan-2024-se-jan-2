        # a - change ticket status ()
        # b- change priority (manual) 
        # c- create ticket data - ( open , time resolve etc )
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

#UTILS 

class TicketTrackingUtils(UserUtils): 
    def convert_data_to_dict(self, ticket_data): 
        data_dict = vars(ticket_data)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in data_dict:
            del data_dict["_sa_instance_state"]

        return data_dict