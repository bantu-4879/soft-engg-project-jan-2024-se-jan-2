# --------------------  Imports  --------------------

import os

# --------------------  Code  --------------------

BACKEND_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
ENV_TYPE = "dev"  # "test"
BASE = f"http://{HOST}:{PORT}"
API_VERSION = "v2"
TOKEN_VALIDITY = 864000  # seconds
ACCEPTED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
PROFILE_PIC_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "profile_pics"
)
TICKET_ATTACHMENTS_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "ticket_attachments"
)
FAQ_ATTACHMENTS_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "faq_attachments"
)

# Mailhog runs at http://127.0.0.1:8025/
SMTP_SERVER_HOST = "127.0.0.1"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "osts_group_14@gmail.com"  # dummy mail and password
SENDER_PASSWORD = "1234"


#Discourse runs at http://127.0.0.1:4200/
DISCOURSE_BASE_URL='http://127.0.0.1:3000'
API_USERNAME='ticketAppAdmin'
API_KEY='6e42f16cbd5b3058c002d81bbf2cf08d6c34e63a0dbd027c61ea5acb33462f2d'
# --------------------  END  --------------------