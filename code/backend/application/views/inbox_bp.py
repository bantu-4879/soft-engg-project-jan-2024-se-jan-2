#TOKEN SPECS MISSING! Add the token_required, etc. 

# IMPORTS
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from application.globals import *
from datetime import datetime
from application.views.user_utils import time_to_str


now = time_to_str(datetime.now())


# message_utils with relative functions
class MessageUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def convert_message_to_dict(self, message):
        msg_dict = vars(message)
        if "_sa_instance_state" in msg_dict:
            del msg_dict["_sa_instance_state"]
        return msg_dict


# post_message function to send a message to the db 
def post_message(send_to, message, message_type, received_at=now, have_read=False):
    """
    Usage
    -----
    Send Message into the built-in Inbox
    Send Message to the GChat using Webhook
    (Discern based on the message_type parameter)

    Parameters
    ----------
    send_to: user_id of the reciever
    message: message body
    recieved_at: timestamp
    have_read: defaults to False
    message_type: [inbox,gchat,email,both_inbox_email]

    Returns
    -------

    """
    new_message = Inbox(
        user_id=send_to,
        message=message,
        received_at=received_at,
        have_read=have_read,
        message_type=message_type.lower(),
    )
    try:
        db.session.add(new_message)
        db.session.commit()
    except Exception as e:
        logger.error(
            f"MessageUtils->post_message : Error occured while creating a new message : {e}"
        )
        raise InternalServerError(
            status_msg="Error occured while sending the message. "
        )
    else:
        logger.info("Message sent successfully.")


inbox_bp = Blueprint("inbox_bp", __name__)
inbox_api = Api(inbox_bp)
inbox_util = MessageUtils()


class InboxAPI(Resource):
    # get the messages for dispaly in the student inbox
    def get(self, user_id="",message_id=-1):
        if inbox_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        try:
            user_messages = []
            messages = Inbox.query.filter_by(user_id=user_id).all()
            for message in messages:
                m = inbox_util.convert_message_to_dict(message)
                user_messages.append(m)
            logger.info(f"All Messages found")

            return success_200_custom(data=user_messages)

        except Exception as e:
            logger.error(
                f"InboxAPI->get : Error occured while fetching user messages: {e}"
            )
            raise InternalServerError

        return user_messages

    def delete(self, user_id="",message_id=-1):
        #check if message exists 
        try:
            message = Inbox.query.filter_by(id=message_id).first()
        except Exception as e:
            logger.error(
                f"InboxAPI->delete : Error occured while fetching the message : {e}"
            )
            raise InternalServerError
        else:
            if message: 
                db.session.delete(message)
                db.session.commit()
                raise Success_200(status_msg="Message Deleted!")
            else:
                raise NotFoundError(status_msg="Message does not exist!")

inbox_api.add_resource(InboxAPI, "/<string:user_id>", endpoint="inbox_get")
inbox_api.add_resource(InboxAPI, "/<string:user_id>/<int:message_id>", endpoint="inbox_delete")

