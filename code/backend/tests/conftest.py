# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: Contains fixtures for testing.

# --------------------  Imports  --------------------

from application import create_app
import pytest
from application.logger import logger

# --------------------  Constants  --------------------

# Please set following required constants to mimic a specific user role.

# STUDENT
student_user_id = "ccec26f5a52560cd22a2965287dc4ad9"
student_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJvdHVzaGFyMjNAZ21haWwuY29tIiwiZXhwaXJ5IjoxNjc5NTY2MzU3LjkxOTg4Mzd9.CQNw31kdMXbJ3O2lWkNkb_EDC5wayIgdreU-6Tgoims"
 
# SUPPORT
support_user_id = "a5997f803b4dfbdb0a7f17b012ca1697"
support_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJvdHVzaGFyMjNAZ21haWwuY29tIiwiZXhwaXJ5IjoxNjc5NTY2MzU3LjkxOTg4Mzd9.CQNw31kdMXbJ3O2lWkNkb"

# ADMIN
admin_user_id = "3ad51db3c4defba9c7f1ca7549712e25"
admin_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY2RlZkBlbWFpbC5jb20iLCJleHBpcnkiOjE2Nzg0Mzc0NTQuOTc1MjAwN30.IaIPV8Ps_AxN_YiCkAVm7p1hPEgi5hYvqV17B0EeFRc"

# --------------------  Code  --------------------

# before testing set current dir to `\code\backend`
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(env_type="test")
    logger.info("Testing fixture set.")
    
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!