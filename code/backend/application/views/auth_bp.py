#routes go here!
# --------------------  Imports  --------------------

import os
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.responses import *
from application.models import User,Role,Authentication
from application.globals import TOKEN_VALIDITY, BACKEND_ROOT_PATH
from application.database import db
import time
from application.views.user_utils import UserUtils
from application.common_utils import (
    token_required,
    admin_required,
    convert_img_to_base64,
    is_img_path_valid,
)

# --------------------  Code  --------------------


class AuthUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def update_auth_table(self, details: dict):
        """
        Usage
        -----
        Update auth table while logging in and creating new account

        Parameters
        ----------
        details : dict with user details

        Returns
        -------
        updated user object

        """
        if details["operation"] == "login":
            user = User.query.filter_by(email=details["email"]).first()
            user.authentication.token = details["web_token"]
            user.is_logged = True
            user.authentication.token_created = int(time.time())
            user.authentication.token_expired = details["token_expiry_on"]
            db.session.commit()

        if details["operation"] == "register":
            role_id=Role.query.filter_by(name=details["role"]).first().id
            user = User(
                id=details["user_id"],
                email=details["email"],
                password=details["password"],
                role_id=role_id,
                first_name=details["first_name"],
                second_name=details["second_name"]
            )
            auth=Authentication(
                user_id=details["user_id"]
            )
            db.session.add(user)
            db.session.add(auth)
            db.session.commit()

        if details["operation"] == "verify_user":
            user = User.query.filter_by(id=details["user_id"]).first()
            user.is_approved = True
            db.session.commit()

        if details["operation"] == "delete_user":
            user = User.query.filter_by(id=details["user_id"]).first()
            if user:
                auth = Authentication.query.filter_by(id=user.authentication.id).first()
                if auth:
                    db.session.delete(auth)
                    db.session.commit()
            db.session.delete(user)
            db.session.commit()
            

        return user


auth_bp = Blueprint("auth_bp", __name__)
auth_api = Api(auth_bp)
auth_utils = AuthUtils()


class Login(Resource):
    def post(self):
        """
        Usage
        -----
        For the user login page. It checks user data and raise appropriate error
        if required. Else it generates user token and returns it.

        Parameters
        ----------
        form data sent with request
        data format {'email':'', 'password':''}

        Returns
        -------
        User web token

        """
        form = {}

        # get form data
        try:
            form = request.get_json()
            email = form.get("email", "")
            password = form.get("password", "")
        except Exception as e:
            logger.error(f"Login->post : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if auth_utils.is_blank(email) or auth_utils.is_blank(password):
                raise BadRequest(status_msg=f"Email or Password is empty")

            details = {"email": email, "password": password, "operation": "login"}

            # verify form data
            if auth_utils.is_email_valid(email) and auth_utils.is_password_valid(
                password
            ):
                # check if user exists

                user = User.query.filter_by(email=email).first()
                if user:
                    # user exists
                    user_id = user.id
                    print(password,user.password)
                    if password == user.password:
                        print(user.role.name)
                        # password is correct so log in user if user is verified
                        if user.is_approved or user.role.name == "admin":
                            #  generate token
                            token_expiry_on = int(int(time.time()) + TOKEN_VALIDITY)
                            web_token = auth_utils.generate_web_token(
                                email, token_expiry_on
                            )
                            details["web_token"] = web_token
                            details["token_expiry_on"] = token_expiry_on

                            # update auth table
                            user = auth_utils.update_auth_table(details=details)

                            # get profile pic
                            profile_pic = user.profile_photo_loc
                            if profile_pic == "":
                                profile_pic = os.path.join(
                                    BACKEND_ROOT_PATH,
                                    "databases",
                                    "images",
                                    "profile_pics",
                                    "dummy_profile.png",
                                )
                            img_base64 = ""
                            if is_img_path_valid(profile_pic):
                                img_base64 = convert_img_to_base64(profile_pic)

                            logger.info("User logged in.")
                            return success_200_custom(
                                data={
                                    "user_id": user_id,
                                    "web_token": web_token,
                                    "token_expiry_on": token_expiry_on,
                                    "role": user.role.name,
                                    "first_name": user.first_name,
                                    "last_name": user.second_name,
                                    "email": user.email,
                                    "profile_photo_loc": img_base64,
                                }
                            )
                        else:
                            # user details are correct but user is not verified by admin
                            raise Unauthenticated(
                                status_msg="User is not verified by Admin."
                            )
                    else:
                        # password is wrong
                        raise Unauthenticated(status_msg="Password is incorrect")
                else:
                    # user does not exists
                    raise NotFoundError(status_msg="User does not exists")
            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification"
                )


class Register(Resource):
    def post(self):
        """
        Usage
        -----
        For the user register page. It checks user data and raise appropriate error
        if required. Created user account and it generates user token and returns it.

        Parameters
        ----------
        form data sent with request
        data format {'first_name':'', 'last_name':'', 'email':'',
                    'password':'', 'retype_password':'', 'role':''}
        'last_name' is optional

        Returns
        -------
        User web token

        """

        details = {
            "email": "",
            "password": "",
            "retype_password": "",
            "role": "",
            "first_name":"",
            "second_name":"",
        }

        # get form data
        try:
            form = request.get_json()
        except Exception as e:
            logger.error(
                f"Register->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            for key in details:
                value = form.get(key, "")
                details[key] = value
                if auth_utils.is_blank(value) and key != "second_name":
                    raise BadRequest(status_msg=f"{key} is empty or invalid")
            details["operation"] = "register"

            # verify registration form data
            if auth_utils.verify_register_form(details):
                # check if user exists
                user = User.query.filter_by(email=details["email"]).first()
                if user:
                    # user exists means email is already in use
                    raise AlreadyExistError(status_msg="Email is already in use")
                else:
                    # generate unique user_id
                    user_id = auth_utils.generate_user_id(email=details["email"])

                    # create new user in Auth table
                    details["user_id"] = user_id
                    user = auth_utils.update_auth_table(details=details)

                    # Redirect to login page in frontend
                    # No need to create web_token as during login it will
                    # be created

                    logger.info("New account created")
                    raise Success_200(
                        status_msg="Account created successfully. Now please login."
                    )

            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification OR Password did not match."
                )


class NewUsers(Resource):
    # Admin access required
    # get user_id and token from headers
    # verify token and role of the user

    @token_required
    @admin_required
    def get(self):
        """
        Usage
        -----
        Get all new users which are not verified.
        Only admin can access this.

        Parameters
        ----------

        Returns
        -------
        New users dict

        """

        # get new users data from auth table
        try:
            all_users = (
                User.query.join(User.role).filter(Role.name.in_(["Student", "Staff"])).all()
            )
        except Exception as e:
            logger.error(f"NewUsers->get : Error occured while fetching db data : {e}")
            raise InternalServerError
        else:
            # convert to list of dict
            data = []
            for user in all_users:
                _d = {}
                _d["user_id"] = user.id
                _d["first_name"] = user.first_name
                _d["last_name"] = user.second_name
                _d["email"] = user.email
                _d["role"] = user.role.name
                data.append(_d)
            return success_200_custom(data=data)

    @token_required
    @admin_required
    def put(self, user_id):
        """
        Usage
        -----
        When admin verifies user, update user.is_verified to True in auth table

        Parameters
        ----------

        Returns
        -------

        """
        # get form data
        try:
            form = request.get_json()
            user_id = form.get("user_id", "")
        except Exception as e:
            logger.error(f"NewUsers->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if auth_utils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")

            details = {"user_id": user_id, "operation": "verify_user"}

            # check if user exists
            user = User.query.filter_by(id=user_id).first()
            if user:
                # user exists , proceed to update
                user = auth_utils.update_auth_table(details=details)
                raise Success_200(status_msg="User verified and updated in database.")
            else:
                raise NotFoundError(status_msg="User does not exists.")

    @token_required
    @admin_required
    def delete(self, user_id):
        """
        Usage
        -----
        When admin rejects user, update user.is_verified to False in auth table

        Parameters
        ----------

        Returns
        -------

        """
        # get form data
        try:
            form = request.get_json()
            user_id = form.get("user_id", "")
        except Exception as e:
            logger.error(
                f"NewUsers->delete : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if auth_utils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")
            details = {"user_id": user_id, "operation": "delete_user"}

            # check if user exists
            user = User.query.filter_by(id=user_id).first()
            if user:
                # user exists , proceed to update
                user = auth_utils.update_auth_table(details=details)
                raise Success_200(
                    status_msg="Verification failed so user deleted in database."
                )
            else:
                raise NotFoundError(status_msg="User does not exists.")


auth_api.add_resource(Login, "/login")  # path is /api/v1/auth
auth_api.add_resource(Register, "/register")
auth_api.add_resource(NewUsers, "/newUsers", "/newUsers/<string:user_id>")

# --------------------  END  --------------------