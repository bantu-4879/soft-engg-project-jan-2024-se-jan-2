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
TicketUtils=DiscourseUserUtils()
class AllCategories(Resource):
    """
    usage 
    ------
    This gives the list of principal categories and then let the students create post in that category.
    
    parameters 
    -------
    this takes nothing it returns the list of categories. 

    
    """
    #@token_required
    #@users_required(users=['Student','Staff','Admin'])
    def get(self):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
            "include_subcategories":'true'
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

class Categories(Resource):
    """
    usage 
    ------
    This gives the details about a single categpry and then let the students create post in that category.
    
    parameters 
    -------
    this takes category id and returns details.

    
    """

    #@token_required
    def get(self,category_id):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
            "include_subcategories":'true'
        }
        url=f'{DISCOURSE_BASE_URL}/c/{category_id}/show.json'
        response=requests.get(url,headers=headers)
        if(response.status_code == 200):
            response=response.json()
            category=response["category"]
            data={}
            data["id"] = category["id"]
            data["name"] = category["name"]
            data["color"] = category["color"]
            data["text_color"] = category["text_color"]
            data["description"] = category["description"]
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load category data")

    #@token_required
    #@users_required(users=['Staff','Admin'])
    def post(self):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME
        }
        form={}

        try:
            form =request.get_json()
            category_name=form.get("name","")
            color=form.get("color", "") 
            text_color=form.get("text-color","")
            permission_staff=form.get("Staff",0)
            parent_category_id=form.get("parent_category","")
            permission_all=form.get("All",1)
            category_description=form.get("description","")
        except Exception as e:
            logger.error(f"DiscourseCategoryCreation ->Error occured while getting form data : {e} ")
            raise InternalServerError
        else:
            if discourseUserUtils.is_blank(category_name) or discourseUserUtils.is_blank(color) or discourseUserUtils.is_blank(text_color):
                raise BadRequest(status_msg=f"Category Name, Color or text color cannot be empty")
            if self.category_exists(category_name=category_name):
                raise AlreadyExistError(status_msg="The category with given name already exists.")
            payload={
                "name":category_name,
                "color":color,
                "text_color":text_color,
                "parent_category_id":parent_category_id,
                "permissions":{
                    "everyone":permission_all,
                    "staff":permission_staff
                },
                "description":category_description
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':API_USERNAME
            }
            url=f'{DISCOURSE_BASE_URL}/categories.json'
            response=requests.post(url,json=payload,headers=headers)
            if response.status_code == 200:
                logger.info("Success.")
                raise Success_200(status_msg="category created successfully",status_code=response.status_code)
            else:
                raise BadRequest(
                    status_msg=response.error
                )
        
    def category_exists(self,category_name):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
            "include_subcategories":'false'
        }
        url=f'{DISCOURSE_BASE_URL}/categories.json'
        response=requests.get(url,headers=headers)
        if(response.status_code == 200):
            response=response.json()
            print(response.keys())
            categories=response["category_list"]["categories"]
            for category in categories:
                if(str.lower(category["name"])==str.lower(category_name)):
                    return True
            return False
    

class Tags(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id

    
    @token_required
    def get(self):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
        }
        url=f'{DISCOURSE_BASE_URL}/tags.json'
        response=requests.get(url,headers=headers)
        if(response.status_code == 200):
            response=response.json()
            tags=response["tags"]
            data=[]
            for tag in tags:
                _d = {}
                _d["id"] = tag["id"]
                _d["name"] = tag["text"]
                data.append(_d)
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load Tags data")
    
    @token_required
    @users_required(users='Staff')
    def post(self):
        try:
            form = request.get_json()
            tag_name = form.get("name", "")
        except Exception as e:
            logger.error(f"DiscourseTagCreation: Post ->Error occured while getting form data : {e} ")
            raise InternalServerError

        # Validate form data
        if discourseUserUtils.is_blank(tag_name):
            raise BadRequest(status_msg=f"Tag Name cannot be empty")

        # Create payload
        payload = {
            "name": tag_name
        }
        # Send request to Discourse API
        headers = {'Api-Key': API_KEY, 'Api-Username': API_USERNAME}
        url = f'{DISCOURSE_BASE_URL}/tag_groups.json'
        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            if response.status_code == 200:
                return response_data, 200
            else:
                return {"error": response_data.get("error", "Unknown error")}, response.status_code
        except Exception as e:
            return {"error": f"Error occurred while making request to Discourse API: {e}"}, 500


class DiscourseTopics(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id

    #@token_required
    def get(self,user_id,topic_id):
        """
        Usage
        -----
        Gets a single topic from its topic Id , if it can be viewed by a username.

        Parameters
        ----------
        form data sent with request

        Returns
        -------
        """
        try:
            user=User.query.filter_by(id=user_id).first()
            if not user:
                raise NotFoundError(status_msg="User does not exist.")
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting the user : {e}"
            )
            raise InternalServerError
        if (user.discourse_username):
            username=user.discourse_username
        else:
            raise BadRequest(status_msg="The user is not registered on Discourse register on discourse first.")
        
        if TicketUtils.is_blank(user_id) or TicketUtils.is_blank(topic_id):
            raise BadRequest(status_msg="User id or Topic Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':username
        }
        payload={
            'topic_id':topic_id
        }
        url=f"{DISCOURSE_BASE_URL}/t/{topic_id}.json"
        try:
            response=requests.get(url,headers=headers,payload=payload) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting topic from discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot get topic from discourse")
        else:
            response=response.json()
            print(response)
            if(response["status"]==200):
                return success_200_custom(data=response)
            else:
                raise BadRequest(status_code=401,status_msg="Cannot load topic")


        
        
        

    @token_required
    @users_required(users='Student')
    def post(self,user_id,ticket_id):
        """
        Usage
        -----
        Create a new topic thread on discourse. Only a student can create.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """

        details={
            "title":"",
            "raw":"",
            "topic_id":"", #required for a new Post
            "sub_category":"",
            "target_recepients":"",
            "created_at":"",
            "reply_to_post_number":"",
            "embed_url":"",

        }
        try:
            user=User.query.filter_by(id=user_id).first()
            if not user:
                raise NotFoundError(status_msg="User does not exist.")
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting the user : {e}"
            )
            raise InternalServerError
        if (user.discourse_username):
            username=user.discourse_username
        else:
            raise BadRequest(status_msg="The user is not registered on Discourse register on discourse first.")

        if TicketUtils.is_blank(user_id) or TicketUtils.is_blank(ticket_id):
            raise BadRequest(status_msg="User id or Ticket Id is missing for discourse Post.")
        try:
            form=request.get_json()
            for key in details:
                value=form.get(key,"")
                if TicketUtils.is_blank(value):
                    value=""
                    details[key]=value
                print(details)
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if details["title"] =="" or details["raw"]=="":
                raise BadRequest(
                    status_msg="Ticket title or the message cannot be empty"
                )
        try:
            ticket=Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting the ticket data : {e}"
            )
            raise InternalServerError
        else:
            logger.info("Uploading the attachments to discourse.")
            header1={
                'Api-Key':API_KEY,
                'Api-Username':username,
                'Content-type':'multipart/form-data'
            }
            params={
                "type":'composer',
                "synchronous":'true'
            }
            raw+=f"\n"
            url=f"{DISCOURSE_BASE_URL}/uploads.json"
            if 'files' in request.files:
                files=request.files.getlist('files')
                if len(files) !=0 :
                    image_urls=[]
                    for i,file in enumerate(files):
                        file_name=file.filename
                        with open(file,'rb') as f:
                            files={
                                "file":(f.read())}
                        try:
                            response=requests.post(url,headers=header1,files=files,data=params) 
                        except Exception as e:
                            logger.error(
                                f"Discourse API TicketAPI->post : Error occured while uploading image {file_name}to discourse  : {e}"
                            )    
                            raise InternalServerError(status_msg="Cannot upload image to discourse.")
                        else:
                            response=response.json()
                            image_urls.append(response["short_url"])
                    for image_url in image_urls:
                        details["raw"]+=f"![]({image_url})\n"
            header={
                'Api-Key':API_KEY,
                'Api-Username':username,
                'Content-type':'application/json'
            }
            default_category=4
            payload={
                "title":details["title"],
                "raw":details["raw"],
                "topic_id":details["topic_id"],
                "category":default_category,
                "sub_category":details["sub_category"],
                "reply_to_post_number":details["reply_to_post_number"],
                "created_at":details["created_at"],
                "embed_url":details["embed_url"]
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':username,
                'Content-Type':'application/x-www-form-urlencoded'
            }




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



discoursePost_api.add_resource(AllCategories,"/categories")
discoursePost_api.add_resource(Categories,"/category","/category/<int:category_id>")
discoursePost_api.add_resource(Tags,'/tags')

