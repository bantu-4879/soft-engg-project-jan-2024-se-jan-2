from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
import requests
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

class DiscourseUserUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id

discourseAuth_bp=Blueprint("discourseAuth_bp",__name__)
discourseAuth_api=Api(discourseAuth_bp)
discourseUserUtils=DiscourseUserUtils()
class DiscourseUserCreation(Resource):
    def post(self):
        """
        Usage 
        -----
        For the Discourse Id creation page.It takes the same user_id ,email and may be a new password.
        and it creates a new user.
        
        Parameters 
        ------
        form data sent with request 
        data format {
        'email': '','password':'','username':''
        }

        Returns 
        ----
        Status of request
        """

        form={}

        try:
            form =request.get_json()
            email=form.get("email","")
            password=form.get("password","")
            username=form.get("username","")
            name=form.get("name","")
        except Exception as e:
            logger.error(f"DiscourseUserCreation ->Error occured while getting form data : {e} ")
            raise InternalServerError
        else:
            if discourseUserUtils.is_blank(email) or discourseUserUtils.is_blank(password):
                raise BadRequest(status_msg=f"Email or Password is empty")
            if self.user_exists(username):
                raise AlreadyExistError(status_msg="Username is already in use")
            payload={
                "name": name,
                "email":email,
                "password":password,
                "username":username,
                "active":True
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':API_USERNAME,
                'Content-Type': 'application/json'
            }
            url = f'{DISCOURSE_BASE_URL}/users.json'
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                logger.info("New account created")
                raise Success_200(status_msg=response.message,status_code=response.status_code)
            else:
                raise BadRequest(
                    status_msg=response.error
                )

    def user_exists(self,username):
        url=f'{DISCOURSE_BASE_URL}/u/{username}.json'
        headers={
            'Api-key':API_KEY,
            'Api-Username':API_USERNAME
        }
        response=requests.get(url,headers=headers)
        if(response.status_code==200):
            return True
        else:
            return False


    def get(self,username):
        url=f'{DISCOURSE_BASE_URL}/u/{username}.json'
        headers={
            'Api-key':API_KEY,
            'Api-Username':API_USERNAME
        }
        response=requests.get(url,headers=headers)
        if(response.status_code==200):
            return response.json(),200
        else:
            return response.json(), response.status_code


discourseAuth_api.add_resource(DiscourseUserCreation,"/discourseRegister", "/discourseRegister/<string:username>")

