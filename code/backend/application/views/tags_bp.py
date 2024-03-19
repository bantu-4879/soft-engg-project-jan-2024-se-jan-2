# - Creating tags
# - getting tags
# - update tags
# - delete tags


from flask import Blueprint, request
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


class TagsUtil(UserUtils):
    def convert_tags_to_dict(self, tags):
        tags_dict = vars(tags)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in tags_dict:
            del tags_dict["_sa_instance_state"]

        return tags_dict


tags_bp = Blueprint("tags_bp", __name__)
tags_api = Api(tags_bp)
tags_util = TagsUtil()


class TagsAPI(Resource):

    def get(self):
        # this method is used to get all of the available tags
        try:
            all_tags = []
            tags = Tags.query.all()
            for tag in tags:
                t = tags_util.convert_tags_to_dict(tag)
                all_tags.append(t)
            logger.info(f"All tags found!")
            return success_200_custom(data=all_tags)
        except Exception as e:
            logger.error(f"TagsAPI->get : Error occured while fetching Tag data : {e}")
            raise InternalServerError

    def post(self):
        details = {"name": "", "description": ""}
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                if tags_util.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TagsAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            tag = Tags(name=details["tag_name"], description=details["description"])
            try: 
                db.session.add(tag)
                db.session.commit() 
            except Exception as e:
                logger.error(
                    f"TagsAPI->post : Error occured while creating a new tag : {e}"
                )
                raise InternalServerError(
                    status_msg="Error occured while creating a new tag"
                )
            else:
                logger.info("Tag created successfully.")
                raise Success_200(status_msg="Tag created successfully")


    # is there a need to update/edit the tags?
    def put(self):
        return ""

    def delete(self, tag_id=-1):
        try:
            tag = Tags.query.filter_by(id=tag_id).first()
        except Exception as e:
            logger.error(
                f"TagsAPI->delete : Error occured while fetching the tag : {e}"
            )
            raise InternalServerError
        else:
            if tag:
                db.session.delete(tag)
                db.session.commit()
                raise Success_200(status_msg="Tag Deleted")
            else:
                raise NotFoundError(status_msg="Tag Does Not Exist")


tags_api.add_resource(TagsAPI, "/all-tags", endpoint="tags_get")
tags_api.add_resource(TagsAPI, "/add-tag", endpoint="tags_post")
tags_api.add_resource(TagsAPI, "/<int:tag_id>", endpoint="tags_delete")


class TicketTagsAPI(Resource):
    def get(self, ticket_id=""):
        if tags_util.is_blank(ticket_id):
            raise BadRequest(status_msg="Ticket id is missing.")
        try:
            ticket_tags = []
            tags_ids = Tickets_Tags.query.filter_by(ticket_id=ticket_id)
            for tag in tags_ids:
                tag_obj = Tags.query.filter_by(id=tag)
                t = tags_util.convert_tags_to_dict(tag_obj)
                ticket_tags.append(t)
            logger.info(f"All ticket tags found!")
            return success_200_custom(data=ticket_tags)
        except Exception as e:
            logger.error(
                f"TicketTagsAPI->get : Error occured while fetching ticket tags : {e}"
            )
            raise InternalServerError

    def post(self, ticket_id=""):
        details = {
            "tag_ids": [],
        }
        if tags_util.is_blank(ticket_id):
            raise BadRequest(status_msg="Ticket id is missing.")

        # check if ticket exists
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketTagAPI->post : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                try:
                    form = request.get_json()
                    for key in details:
                        value = form.get(key, "")
                        if tags_util.is_blank(value):
                            value = ""
                        details[key] = value
                except Exception as e:
                    logger.error(
                        f"TicketTagsAPI->post : Error occured while getting form data : {e}"
                    )
                    raise InternalServerError
                else:
                    for tag in details["tag_ids"]:
                        each_ticket_tag = Tickets_Tags(tag_id=tag, ticket_id=ticket_id)
                        try:
                            db.session.add(each_ticket_tag)
                            db.session.commit()
                        except Exception as e:
                            logger.error(
                                f"FAQAPI->post : Error occured while adding new tag : {e}"
                            )

                            raise InternalServerError(
                                status_msg="Error occured while adding a new tag"
                            )

    def put(self):
        return ""

    def delete(self):
        return ""


# tags_api.add_resource(TicketTagsAPI, "/", endpoint="tags_get")
