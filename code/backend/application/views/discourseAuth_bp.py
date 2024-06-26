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
from application.views.inbox_bp import post_message

class DiscourseUserUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id

discourseAuth_bp=Blueprint("discourseAuth_bp",__name__)
discourseAuth_api=Api(discourseAuth_bp)
discourseUserUtils=DiscourseUserUtils()
class DiscourseUserCreation(Resource):

    @token_required
    @users_required(users=["student","staff","admin"])
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
            user_id=form.get("user_id", "") 
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
            
            user=User.query.filter_by(id=user_id).first()
            if(user):
                print("userExists")
            else:
                raise NotFoundError(status_msg="user not present")
            payload={
                "name": name,
                "email":email,
                "password":password,
                "username":username,
            }
            headers={
                'Api-Key':API_KEY,
                'Api-Username':API_USERNAME,
                'Content-Type': 'application/json'
            }
            url = f'{DISCOURSE_BASE_URL}/users.json'
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                logger.info("The connection was estabilished")
                responseJs=response.json()
                print(responseJs)
                if(responseJs["success"]):
                    user.discourse_username=username
                    db.session.add(user)
                    db.session.commit()
                    post_message(user_id, f"You have registered on discourse with username-{username} and activate your account from your email.", "inbox")
                    raise Success_200(status_msg=responseJs["message"],status_code=response.status_code)
                else:
                    raise AlreadyExistError(status_msg=responseJs["message"],status_code=405)
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

    @token_required
    @admin_required
    def get(self,username):
        url=f'{DISCOURSE_BASE_URL}/u/{username}.json'
        headers={
            'Api-key':API_KEY,
            'Api-Username':API_USERNAME
        }
        response=requests.get(url,headers=headers)
        if(response.status_code==200):
            return response.json(),response.status_code
        else:
            return response.json(), response.status_code

class DiscourseIdExists(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id
    
    @token_required
    def get(self,user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                username = user.discourse_username
                return {"username": username}, 200
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            logger.error(
                f"Cannot retrieve user from user id: {user_id}. Error: {str(e)}"
            )
            raise InternalServerError(status_msg="Unknown error occurred")
class DiscourseAddMedorators(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id
    
    @token_required
    @admin_required
    def get(self):
        """
        usage
        -------
        This is used to get the list of users who are staff members of the ticket_app and can be added to the group of ticket application on the discourse 

        parameters
        ------

        returns
        -------

        """
        try:
            staff_members=User.query.join(User.role).filter(Role.name.in_(["Staff"])).all()
        except Exception as e:
            logger.error(f"DiscourseAddMedorators -> get : Error occured while fetching db data : {e}")
            raise InternalServerError
        
        else:
            data=[]
            for user in staff_members:
                _d={}
                _d["user_id"] = user.id
                _d["first_name"] = user.first_name
                _d["last_name"] = user.second_name
                _d["email"] = user.email
                _d["Discourse_Username"] = user.discourse_username
                data.append(_d)
            return success_200_custom(data=data)
    
    @token_required
    @admin_required
    def put(self,user_id):
        """
        Usage
        -----
        When admin updated the user is added to the ticket staff group.

        Parameters
        ----------

        Returns
        -------

        """
        try:
            form=request.get_json()
            user_id=form.get("user_id","")
        except Exception as e:
            logger.error(f"DiscourseAddMedorators->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if discourseUserUtils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")
            
            user=User.query.filter_by(id=user_id).first()
            if user:
                username=user.discourse_username
                payload={
                    "usernames":username
                }
                import json
                payload_string = json.dumps(payload)
                print(payload_string)
                headers={
                    'Api-key':API_KEY,
                    'Api-Username':API_USERNAME,
                    'Content-Type':'application/json'
                }
                id=41
                url=f'{DISCOURSE_BASE_URL}/groups/{id}/members.json'
                response = requests.put(url,payload_string,headers=headers)
                if response.status_code == 200:
                    logger.info("Member added to the group.")
                    response=response.json()
                    print(response)
                    if(response["success"] =='OK'):
                        raise Success_200(status_msg="User added successfully.")
                else:
                    raise BadRequest(status_code=400,status_msg="The user could not be added.")
            
    @token_required
    @admin_required
    def delete(self,user_id):
        """
        Usage
        -----
        When admin deletes the moderator, in discourse the staff is removed from the group of staff

        Parameters
        ----------

        Returns
        -------

        """
        try:
            form=request.get_json()
            user_id=form.get("user_id","")
        except Exception as e:
            logger.error(f"DiscourseAddMedorators->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if discourseUserUtils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")
            
            user=User.query.filter_by(id=user_id).first()
            if user:
                username=user.discourse_username
                payload={
                    "usernames":username
                }
                headers={
                    'Api-key':API_KEY,
                    'Api-Username':API_USERNAME,
                    'Content-Type':'application/json'
                }
                id=41
                url=f'{DISCOURSE_BASE_URL}/groups/{id}/members.json'
                payload={
                    "usernames":username
                }
                response = requests.delete(url,payload,headers=headers)
                if response.status_code == 200:
                    logger.info("Staff member removed from the group")
                    if(response.success):
                        raise Success_200(status_msg=response.message,status_code=response.status_code)
                else:
                    raise BadRequest(
                        status_msg=response.error)

class DiscourseGroupMessages(Resource):
    def __init__(self,user_id=None):
        self.user_id=user_id
    
    @token_required
    @users_required(users=['staff','admin'])
    def get(self,user_id):
        """
        usage
        -------
        This is used to get the messages of a user , who is part of the staff team and part of the group.

        parameters
        ------
        This takes the user_id and finds the username from discourse

        returns

        -------
        it returns the messages of the corresponding user if he exists

        """

        if discourseUserUtils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(
                f"Discourse group Messages API->get : Error occured while fetching user data : {e}"
            )
            raise InternalServerError
        else:
            if user.discourse_username:
                username=user.discourse_username
                headers={
                    "Api-Key":API_KEY,
                    "Api-Username":username
                }
                url=f'{DISCOURSE_BASE_URL}/topics/private-messages/{username}.json'
                try:
                    response=requests.get(url,headers=headers)
                except Exception as e:
                    logger.error(
                f"Discourse group Messages API->get : Error occured while fetching data from discourse : {e}"
            )
                if response.status_code == 200:
                    logger.info("Messages received from discourse")
                    return success_200_custom(data=response.json())    
                else:
                    raise BadRequest(status_msg=response.message)
            else:
                raise NotFoundError(status_msg="Staff not registered on discourse , register on discourse first.")
        

class Notifications(Resource):

    @token_required
    def get(self,user_id):
        """
        Usage
        -----
        Gets the Notifications belonging to a particular user on discourse.

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
        
        # if DiscourseUserUtils.is_blank(user_id):
        #     raise BadRequest(status_msg="User id  is missing for discourse.")
        headers={
            'Api-Key':API_KEY,
            'Api-Username':username
        }
        url=f'{DISCOURSE_BASE_URL}/notifications.json'
        response=requests.get(url,headers=headers)
        if(response.status_code == 200):
            response=response.json()
            notifications=response["notifications"]
            data=[]
            for notification in notifications:
                _d = {}
                _d["id"] = notification["id"]
                _d["created_at"] = notification["created_at"]
                _d["type"] = notification["notification_type"]
                _d["topic_id"] = notification["topic_id"]
                _d["slug"]=notification["slug"]
                data.append(_d)
            return success_200_custom(data=data)
        else:
            raise NotFoundError(status_msg="could not load notifications.")

        
        

discourseAuth_api.add_resource(DiscourseUserCreation,"/discourseRegister", "/discourseRegister/<string:username>")
discourseAuth_api.add_resource(DiscourseAddMedorators,"/addStaff",'/addStaff/<string:user_id>')
discourseAuth_api.add_resource(DiscourseGroupMessages,"/getMessages/<string:user_id>")
discourseAuth_api.add_resource(DiscourseIdExists,'/discourseExists/<string:user_id>')
discourseAuth_api.add_resource(Notifications,'/notifications/<string:user_id>')