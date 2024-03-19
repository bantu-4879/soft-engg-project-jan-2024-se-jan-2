from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from application.globals import *
from application.globals import DISCOURSE_BASE_URL,API_USERNAME,API_KEY



