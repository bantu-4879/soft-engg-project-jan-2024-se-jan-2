# --------------------  Imports  --------------------

import hashlib
import time
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

# --------------------  Code  --------------------


class FAQUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def convert_faq_to_dict(self, faq):
        faq_dict = vars(faq)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in faq_dict:
            del faq_dict["_sa_instance_state"]
        attachments = self.get_faq_attachments(faq_id=faq.id)
        faq_dict["attachments"] = attachments

        return faq_dict

    def get_faq_attachments(self, faq_id):
        faq_attch = FAQAttachment.query.filter_by(faq_id=faq_id).all()
        attachments = []
        for att in faq_attch:
            file_path = att.attachment_location
            img_base64 = ""
            if is_img_path_valid(file_path):
                img_base64 = convert_img_to_base64(file_path)
            d_ = {"attachment_loc": img_base64}
            attachments.append(d_)
        return attachments

    def generate_faq_id(self, title: str) -> str:
        """
        FAQ id is generated from faq question and user id and timestamp
        """
        # generate unique id
        ts = str(int(time.time_ns()))
        string = f"{title}_{ts}"
        faq_id = hashlib.md5(string.encode()).hexdigest()
        return faq_id

    def save_faq_attachments(self, attachments: list, faq_id: str, operation: str):
        # get list of files from db for the faq
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {faq_id_{number-extension-if-needed}_.{file_format}
        # operation : create_faq onlu admin can do it

        total_attachments = len(attachments)
        num_successful_attachments = 0

        if total_attachments == 0:
            return (False, "Attachments are empty.")

        files = [
            file
            for file in os.listdir(FAQ_ATTACHMENTS_PATH)
            if file.startswith(f"{faq_id}")
        ]
        number_extension = len(files)  # starting point

        for attach in attachments:
            # attach will be of format {attachment_loc:'', user_id:''}
            # attachment_loc will contain base64 version of image while data transfer is occuring between backend and frontend
            # attachment_loc will contain image path when data is retried from db by backend
            # attachment_loc will contain base64 image when creating new attachment

            if attach["attachment_location"]:
                if is_base64(attach["attachment_location"].split(",")[1]):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        attach["attachment_location"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = f"{faq_id}_{number_extension}.{file_format}"
                        file_path = os.path.join(FAQ_ATTACHMENTS_PATH, file_name)
                        if convert_base64_to_img(file_path, encoded_data):
                            # successfully image saved and now add entry to database
                            try:
                                # while creating a faq a student can upload multiple attachments
                                # verify whether each attachment is unique
                                attach = {}
                                attach["faq_id"] = faq_id
                                attach["attachment_location"] = file_path
                                faq_attach = FAQAttachment(**attach)
                                db.session.add(faq_attach)
                                db.session.commit()
                                num_successful_attachments += 1
                                number_extension += 1
                            except Exception as e:
                                logger.error(
                                    f"FAQAPI->post : Error occured while creating a FAQ Attachment : {e}"
                                )
        return (
            True,
            f"Total {num_successful_attachments} / {total_attachments} attchements are valid and added successfully.",
        )


faq_bp = Blueprint("faq_bp", __name__)
faq_api = Api(faq_bp)
faq_util = FAQUtils()


class FAQAPI(Resource):
    #@token_required
    #@users_required(users=["student", "support", "admin"])
    def get(self):
        # get all faq and return
        """
        Usage
        -----
        Get all faqs

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        try:
            all_faqs = []
            faqs = FAQ.query.all()
            for faq in faqs:
                f = faq_util.convert_faq_to_dict(faq)
                all_faqs.append(f)
            logger.info(f"All FAQs found : {len(all_faqs)}")

            return success_200_custom(data=all_faqs)
        except Exception as e:
            logger.error(f"FAQAPI->get : Error occured while fetching FAQ data : {e}")
            raise InternalServerError

    #@token_required
    #@users_required(users=["admin"])
    def post(self):
        details = {
            "question": "",
            "solution": "",
            "tags_list": "",
            "created_by": "",
        }
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if faq_util.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(f"FAQAPI->post : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if details["question"] == "" or details["tags_list"] == "":
                raise BadRequest(
                    status_msg=f"FAQ question and at least one tag is required"
                )
            faq_id = faq_util.generate_faq_id(details["question"])
            details["id"] = faq_id
            # details["created_by"] = user_id
            faq = FAQ(**details)
            try:
                db.session.add(faq)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"FAQAPI->post : Error occured while creating a new faq : {e}"
                )

                raise InternalServerError(
                    status_msg="Error occured while creating a new faq"
                )
            else:
                logger.info("FAQ created successfully.")

                # add attachments now
                status, message = faq_util.save_faq_attachments(
                    attachments, faq_id, operation="create_faq"
                )
                raise Success_200(status_msg=f"FAQ created successfully. {message}")


faq_api.add_resource(FAQAPI, "/")  # path is /api/v1/faq

# --------------------  END  --------------------
