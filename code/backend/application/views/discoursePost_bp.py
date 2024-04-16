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
            categories=response["category_list"]["categories"]
            data=[]
            for category in categories:
                _d = {}
                _d["id"] = category["id"]
                _d["name"] = category["name"]
                _d["color"] = category["color"]
                _d["text_color"] = category["text_color"]
                _d["description"] = category["description"]
                _d["slug"]=category["slug"]
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
            data["slug"]=category["slug"]
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

class SubCategoriesAll(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id
    
    #@token_required
    def get(self,category_id):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME,
            "include_subcategories":'true'
        }
        url=f'{DISCOURSE_BASE_URL}/categories.json'
        params={
            'include_subcategories':'true'
        }
        response=requests.get(url,headers=headers,params=params)
        if(response.status_code == 200):
            response=response.json()
            for category in response['category_list']['categories']:
                if category['id'] == category_id:
                    category_req=category
            data=[]
            for sub_category in category_req["subcategory_list"]:
                _d={}
                _d["id"] = sub_category["id"]
                _d["name"] = sub_category["name"]
                _d["color"] = sub_category["color"]
                _d["text_color"] = sub_category["text_color"]
                _d["description"] = sub_category["description"]
                _d["slug"]=sub_category["slug"]
                data.append(_d)
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load category data")

class CategoryTopicsAll(Resource):
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
    def get(self,slug,category_id):
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME
        }
        url=f'{DISCOURSE_BASE_URL}/c/{slug}/{category_id}.json'
        try:
            response=requests.get(url,headers=headers)
        except Exception as e:
            logger.error(
                f"DiscourseCategoryTopics Lists -> Error occured while getting form data : {e} "
            )
        if(response.status_code == 200):
            response=response.json()
            topics=response["topic_list"]["topics"]
            data=[]
            for topic in topics:
                _d={}
                _d["id"]=topic["id"]
                _d["title"]=topic["title"]
                _d["posts_count"]=topic["posts_count"]
                _d["created_at"]=topic["created_at"]
                _d["last_modified_at"]=topic["last_posted_at"]
                data.append(_d)
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load categories")

class Tags(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id

    
    #@token_required
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
    
    #@token_required
    #@users_required(users='Staff')
    def post(self):
        try:
            form = request.get_json()
            tags=form.get("tags",[])
        except Exception as e:
            logger.error(f"DiscourseTagCreation: Post ->Error occured while getting form data : {e} ")
            raise InternalServerError

        # Validate form data
        if len(tags)==0:
            raise BadRequest(status_msg=f"Tag Names List cannot be empty")

        default_category=14
        # Create payload
        payload = {
            "title":"Creating sample tags for general use in the category created for this App.",
            "raw":"This post is being used for creating tags which can be used by students to create posts.",
            "category":default_category,
            "skip_validations":'true',
            "auto_track":'true',
            "tags":tags
        }
        # Send request to Discourse API
        headers = {'Api-Key': API_KEY, 'Api-Username': API_USERNAME}
        url = f'{DISCOURSE_BASE_URL}/posts.json'
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

    @token_required
    def get(self,user_id,ticket_id):
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
            raise InternalServerError(status_msg="User not found.")
        try:
            ticket=Ticket.query.filter_by(id=ticket_id).first()
            if not user:
                raise NotFoundError(status_msg="Ticket does not exist.")
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting the ticket : {e}"
            )
            raise InternalServerError(status_msg="Ticket not found.")
        if (user.discourse_username):
            username=user.discourse_username
        else:
            raise BadRequest(status_msg="The user is not registered on Discourse register on discourse first.")
        
        if TicketUtils.is_blank(user_id):
            raise BadRequest(status_msg="User id or Topic Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME
        }
        topic_id=ticket.thread_link
        if(topic_id):
            url=f"{DISCOURSE_BASE_URL}/t/{topic_id}.json"
            try:
                response=requests.get(url,headers=headers) 
            except Exception as e:
                logger.error(
                    f"Discourse API TicketAPI->post : Error occured while getting topic from discourse : {e}"
                )    
                raise InternalServerError(status_msg="Cannot get topic from discourse")
            if(response.status_code==200):
                response=response.json()
                return success_200_custom(data=response)
            else:
                raise BadRequest(status_code=401,status_msg="Cannot load topic")
        else:
            raise BadRequest(status_msg="This ticket does not have a discourse thread.")
        

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
            "topic_id":"", #required for a new Post under a topic
            "sub_category":"",
            "created_at":"",
            "reply_to_post_number":"",
            "embed_url":"",
            "category":"",
            "tags":""

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
            title = request.form.get('title')
            raw = request.form.get('raw')
            topic_id = request.form.get('topic_id')
            sub_category = request.form.get('sub_category')
            created_at = request.form.get('created_at')
            reply_to_post_number = request.form.get('reply_to_post_number')
            embed_url = request.form.get('embed_url')
            category = request.form.get('category')
            tags = request.form.get('tags')

            details["title"] = title if title else ""
            details["raw"] = raw if raw else ""
            details["topic_id"] = topic_id if topic_id else ""
            details["sub_category"] = sub_category if sub_category else ""
            details["created_at"] = created_at if created_at else ""
            details["reply_to_post_number"] = reply_to_post_number if reply_to_post_number else ""
            details["embed_url"] = embed_url if embed_url else ""
            details["category"] = category if category else ""
            details["tags"] = tags if tags else ""
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
            if(ticket.user_id != user_id):
                raise BadRequest(status_code=403,status_msg="You cannot create discourse thread for this topic.")
            logger.info("Uploading the attachments to discourse.")
            header1={
                'Api-Key':API_KEY,
                'Api-Username':API_USERNAME,
            }
            params={
                "type":"image",
                "synchronous":True
            }
            raw=raw+f"\n"
            url=f"{DISCOURSE_BASE_URL}/uploads.json"
            if 'files' in request.files:
                uploaded_files = request.files.getlist('files')
                if uploaded_files:
                    image_urls = []
                    print("I am here . line 456")
                    for i, uploaded_file in enumerate(uploaded_files):
                        file_name = uploaded_file.filename
                        files = {"files[]": (uploaded_file.filename,uploaded_file.stream,uploaded_file.content_type)}
                        try:
                            response = requests.post(url, headers=header1, files=files,data=params)
                            response.raise_for_status()
                        except Exception as e:
                            logger.error(
                                f"Discourse API TicketAPI->post : Error occurred while uploading image {file_name} to discourse: {e}"
                            )    
                            raise InternalServerError(status_msg="Cannot upload image to discourse.")
                        else:
                            logger.info("Images successfully uploaded")
                            response_json = response.json()
                            image_urls.append(response_json["short_url"])
                    for image_url in image_urls:
                        details["raw"]=details["raw"]+f"![]({image_url})\n"
            header={
                'Api-Key':API_KEY,
                'Api-Username':username,
                'Content-type':'application/json'
            }
            print(details["raw"])
            default_category=14
            payload={
                "title":details["title"],
                "raw":details["raw"],
                "topic_id":details["topic_id"],
                "category":"14",
                "sub_category":details["sub_category"],
                "reply_to_post_number":details["reply_to_post_number"],
                "created_at":details["created_at"],
                "embed_url":details["embed_url"],
                "tags[]":details["tags"]
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':username
            }
            print(payload)
            url2=f"{DISCOURSE_BASE_URL}/posts.json"
            try:
                response=requests.post(url=url2,headers=headers,json=payload)
            except Exception as e:
                    logger.error(
                            f"Discourse API TicketAPI->post : Error occured while uploading image {file_name}to discourse  : {e}"
                        )    
                    raise InternalServerError(status_msg="Cannot upload image to discourse.")
            if(response.status_code==200):
                response=response.json()
                ticket.thread_link=response["id"]
                try:
                    db.session.add(ticket)
                    db.session.commit()
                except Exception as e:
                    logger.error(
                        f"Discourse API TicketAPI->post : Error while adding thread link to discourse: {e}"
                    )
                    raise InternalServerError(status_msg="Cannot add the discourse topic data to database.")

                data={}
                data["id"] = response["id"]
                data["name"] = response["name"]
                data["created_at"] = response["created_at"]
                data["raw"] = response["raw"]
                return success_200_custom(data=data)
            else:
                raise BadRequest(status_code=403,status_msg="Cannot create post.pictures uploaded")


    @token_required
    @users_required(users=['staff'])
    def put(self,topic_id):
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
        
        if TicketUtils.is_blank(topic_id):
            raise BadRequest(status_msg="Topic Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':API_USERNAME
        }
        url=f"{DISCOURSE_BASE_URL}/t/{topic_id}.json"
        try:
            response=requests.get(url,headers=headers) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while locking topic status on discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot connect to the discourse for locking the post on discourse")
        if(response.status_code==200):
            response=response.json()
            if(response["closed"]=="true"):
                url2=f"{DISCOURSE_BASE_URL}/t/{topic_id}/status.json"
                header2={
                    'Api-Key':API_KEY,
                    'Api-Username':API_USERNAME
                }
                payload={
                    "status":"closed",
                    "enabled":"false"
                }
                try:
                    response=requests.put(url=url2,headers=header2,json=payload)
                except Exception as e:
                    logger.error(
                        f"Discourse API TicketAPI->Topic status update : Error occured while unlocking topic status on discourse : {e}"
                    )    
                    raise InternalServerError(status_msg="Cannot connect to the discourse for unlocking the post on discourse")
            else:
                url2=f"{DISCOURSE_BASE_URL}/t/{topic_id}/status.json"
                header2={
                    'Api-Key':API_KEY,
                    'Api-Username':API_USERNAME
                }
                payload={
                    "status":"closed",
                    "enabled":"true"
                }
                try:
                    response=requests.put(url=url2,headers=header2,json=payload)
                except Exception as e:
                    logger.error(
                        f"Discourse API TicketAPI->Topic status update : Error occured while locking topic status on discourse : {e}"
                    )    
                    raise InternalServerError(status_msg="Cannot connect to the discourse for locking the post on discourse")
        else:
            raise BadRequest(status_code=401,status_msg="Cannot access the topic on discourse.")

    @token_required
    @users_required(users=['Student','Staff'])
    def delete(self,user_id,topic_id):
        """
        Usage
        -----
        Deletes a single topic from its topic Id , if it is by that user or the user is staff.

        Parameters
        ----------
        parameters sent in the path.

        Returns
        -------
        """
        try:
            user=User.query.filter_by(id=user_id).first()
            if not user:
                raise NotFoundError(status_msg="User does not exist.")
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->delete : Error occured while getting the user : {e}"
            )
            raise InternalServerError
        if (user.discourse_username):
            username=user.discourse_username
        else:
            raise BadRequest(status_msg="The user is not registered on Discourse register on discourse first.")
        
        if TicketUtils.is_blank(user_id):
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
            response=requests.get(url,headers=headers) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->delete : Error occured while deleting topic from discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot delete topic from discourse")
        if(response.status_code==200):
            response=response.json()
            post_username=response["name"]
            if(post_username!=username):
                if(user.role.name !='staff'):
                    raise BadRequest(status_code=403,status_msg="You cannot delete this post.")
                else:
                    header2={
                        'Api-Key':API_KEY,
                        'Api-Username':API_USERNAME
                    }
                    try:
                        response=requests.delete(url=url,headers=header2)
                    except Exception as e:
                        logger.error(
                f"Discourse API TicketAPI->delete : Error occured while deleting topic from discourse : {e}"
            )       
                    if(response.status_code==200):
                        raise Success_200(status_code=response.status_code,response_msg="Successfully deleted the thread")
                    else:
                        raise InternalServerError(status_msg="Cannot delete the topic.")
            else:
                try:
                    response=requests.delete(url=url,headers=headers)
                except Exception as e:
                    logger.error(
                        f"Discourse API TicketAPI->delete : Error occured while deleting topic from discourse : {e}"
                    )
                if(response.status_code==200):
                    raise Success_200(status_code=response.status_code,response_msg="Successfully deleted the thread")
                else:
                    raise InternalServerError(status_msg="Cannot delete the topic.")
        else:
            raise BadRequest(status_code=401,status_msg="Cannot load topic with this topic id")
        
        

class DiscoursePosts(Resource):

    @token_required
    def get(self,user_id,post_id):
        """
        Usage
        -----
        Get a post on discourse with its post id.

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
        
        if TicketUtils.is_blank(user_id) or TicketUtils.is_blank(post_id):
            raise BadRequest(status_msg="User id or Post Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':username
        }
        url=f"{DISCOURSE_BASE_URL}/posts/{post_id}.json"
        try:
            response=requests.get(url,headers=headers) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while getting topic from discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot get post from discourse")
        if(response.status_code==200):
            response=response.json()
            print(response)
            return success_200_custom(data=response)
        else:
            raise BadRequest(status_code=401,status_msg="Cannot load Post")

    @token_required
    @users_required(users=['student','staff','admin'])
    def post(self,user_id):
        """
        Usage
        -----
        Reply to a topic created on discourse.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """

        details={
            "title":"",
            "raw":"",
            "topic_id":"", #required for a new Post under a topic
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

        if TicketUtils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing for discourse Post.")
        try:
            form=request.form
            title = request.form.get('title')
            raw = request.form.get('raw')
            topic_id = request.form.get('topic_id')
            created_at = request.form.get('created_at')
            reply_to_post_number = request.form.get('reply_to_post_number')
            embed_url = request.form.get('embed_url')

            details["title"] = title if title else ""
            details["raw"] = raw if raw else ""
            details["topic_id"] = topic_id if topic_id else ""
            details["created_at"] = created_at if created_at else ""
            details["reply_to_post_number"] = reply_to_post_number if reply_to_post_number else ""
            details["embed_url"] = embed_url if embed_url else ""

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
            if details["topic_id"] =="":
                raise BadRequest(
                    status_msg="The topic_id cannot be empty."
                )
            header1={
                'Api-Key':API_KEY,
                'Api-Username':API_USERNAME,
            }
            params={
                "type":"image",
                "synchronous":True
            }
            raw=raw+f"\n"
            url=f"{DISCOURSE_BASE_URL}/uploads.json"
            if 'files' in request.files:
                uploaded_files = request.files.getlist('files')
                if uploaded_files:
                    image_urls = []
                    print("I am here . line 456")
                    for i, uploaded_file in enumerate(uploaded_files):
                        file_name = uploaded_file.filename
                        files = {"files[]": (uploaded_file.filename,uploaded_file.stream,uploaded_file.content_type)}
                        try:
                            logger.info("Uploading the attachments to discourse.")
                            response = requests.post(url, headers=header1, files=files,data=params)
                            response.raise_for_status()
                        except Exception as e:
                            logger.error(
                                f"Discourse API TicketAPI->post : Error occurred while uploading image {file_name} to discourse: {e}"
                            )    
                            raise InternalServerError(status_msg="Cannot upload image to discourse.")
                        else:
                            logger.info("Images successfully uploaded")
                            response_json = response.json()
                            image_urls.append(response_json["short_url"])
                    for image_url in image_urls:
                        details["raw"]=details["raw"]+f"![]({image_url})\n"
            payload={
                "title":details["title"],
                "raw":details["raw"],
                "topic_id":details["topic_id"],
                "reply_to_post_number":details["reply_to_post_number"],
                "created_at":details["created_at"],
                "embed_url":details["embed_url"],
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':username
            }
            url2=f"{DISCOURSE_BASE_URL}/posts.json"
            try:
                response=requests.post(url=url2,headers=headers,json=payload)
            except Exception as e:
                    logger.error(
                            f"Discourse API TicketAPI->post : Error occured while uploading image {file_name}to discourse  : {e}"
                        )    
                    raise InternalServerError(status_msg="Cannot upload image to discourse.")
            if(response.status_code==200):
                response=response.json()
                data={}
                data["id"] = response["id"]
                data["name"] = response["name"]
                data["created_at"] = response["created_at"]
                data["raw"] = response["raw"]
                return success_200_custom(data=data)
            else:
                raise BadRequest(status_code=403,status_msg="Cannot create post.pictures uploaded")


class TopicNotifications(Resource):

    def __init__(self,user_id=None):
        self.user_id=user_id

    def post(self,user_id,topic_id,notification_level):
        """
        Usage
        -----
        Sets a notification topic from its topic Id , if it can be viewed by a username.

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
        
        if TicketUtils.is_blank(user_id):
            raise BadRequest(status_msg="User id or Topic Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':username
        }
        url=f"{DISCOURSE_BASE_URL}/t/{topic_id}/notifications.json"
        payload={
            "notification_level":str(notification_level)
        }
        try:
            response=requests.get(url,headers=headers,json=payload) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while setting notification level for topic on discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot connect to the discourse for liking the post on discourse")
        if(response.status_code==200):
            response=response.json()
            raise Success_200(status_code=200,status_msg="The status was modified.")
        else:
            raise BadRequest(status_code=401,status_msg="Cannot modify the notification for topic.")
class LikingPosts(Resource):

    def __init__(self,user_id=None):
        self.user_id=user_id
    
    def post(self,user_id,post_id):
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
        
        if TicketUtils.is_blank(user_id):
            raise BadRequest(status_msg="User id or Topic Id is missing for discourse.")
        
        headers={
            'Api-Key':API_KEY,
            'Api-Username':username
        }
        url=f"{DISCOURSE_BASE_URL}/post_actions.json"
        payload={
            "id":str(post_id),
            "post_action_type_id":'2',
            "flag_topic":False

        }
        try:
            response=requests.get(url,headers=headers,json=payload) 
        except Exception as e:
            logger.error(
                f"Discourse API TicketAPI->post : Error occured while liking post on discourse : {e}"
            )    
            raise InternalServerError(status_msg="Cannot connect to the discourse for liking the post on discourse")
        if(response.status_code==200):
            response=response.json()
            print(response)
            return success_200_custom(data=response)
        else:
            raise BadRequest(status_code=401,status_msg="Cannot like the post")




discoursePost_api.add_resource(AllCategories,"/categories")
discoursePost_api.add_resource(Categories,"/category","/category/<int:category_id>")
discoursePost_api.add_resource(Tags,'/tags')
discoursePost_api.add_resource(
    DiscourseTopics,
   '/topic/<string:user_id>/<string:ticket_id>',
   '/topic/status_update/<int:topic_id>'
)
discoursePost_api.add_resource(CategoryTopicsAll,'/category/topics/<string:slug>/<int:category_id>')
discoursePost_api.add_resource(SubCategoriesAll,'/category/subcategories/<int:category_id>')
discoursePost_api.add_resource(DiscoursePosts,'/topic/reply/<string:user_id>','/topic/change_status/<string:user_id>/<string:ticket_id>')
discoursePost_api.add_resource(LikingPosts,'/post/like/<string:user_id>/<int:post_id>')
discoursePost_api.add_resource(TopicNotifications,'/topic/notification/<string:user_id>/<int:topic_id>/<int:notification_level>')