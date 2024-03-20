from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
import requests
from application.common_utils import (
    token_required,
    users_required,
    admin_required,
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
from application.database import db

class DiscourseUserUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id

discoursePost_bp=Blueprint("discoursePost_bp",__name__)
discoursePost_api=Api(discoursePost_bp)
discourseUserUtils=DiscourseUserUtils()

class Categories(Resource):
    """
    usage 
    ------
    This gives the list of principal categories and then let the students create post in that category.
    
    parameters 
    -------
    this takes nothing it returns the list of categories. 

    
    """

    @token_required
    @users_required(users=['Student','Staff','Admin'])
    def get(self):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
            "include_subcategories":True
        }
        url=f'{DISCOURSE_BASE_URL}/categories.json'
        response=requests.get(url,headers=headers)
        if(response.status_code == 200):
            response=response.json()
            print(response.keys())
            categories=response["category_list"]["categories"]
            data=[]
            for category in categories:
                _d = {}
                _d["id"] = category["id"]
                _d["name"] = category["name"]
                _d["color"] = category["color"]
                _d["text_color"] = category["text_color"]
                _d["description"] = category["description"]
                data.append(_d)
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load categories")

        
    

class Tags(Resource):
    print("resource")
    #get,#post


class DiscourseTopics(Resource):
    print("")

class TicketThread(Resource):
    @token_required
    @users_required(users=['Student','Staff','Admin'])
    def post(self):
        user_id_rec = request.headers.get("user_id", "")
        user=User.query.filter_by(id=user_id_rec).first()
        username=user.discourse_username
        form=request.get_json()
        topic_id=form.get("topic_id","")
        category_id=form.get("category_id")




discoursePost_api.add_resource(Categories,"/categories")
        

