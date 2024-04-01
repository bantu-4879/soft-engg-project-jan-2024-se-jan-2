from application import create_app
import pytest
from application.logger import logger 



# Please set following required constants to mimic a specific user role.

# STUDENT
student_user_id = "7e2a3837cce86cdc7d198ab20275984f"
student_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InR1c2hhckBnbWFpbC5jb20iLCJleHBpcnkiOjE3MTI4Mzk4NDB9.W5rJyvLD-p7kUKYwhOa3FCFx-dVxqtKwqCWP74mttPI"
 
# SUPPORT
support_user_id = "fb58cddff315e18f87a86f94dc191891"
support_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heC5kb2VAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE3MTE3OTI4NTh9.-E6BeaQRSb9ULY2spHRBDE5obB5Hy6HD4TzYajcpCSI"
# ADMIN
admin_user_id = "7a848f03778ea5e30de4dc6850c6b67e"
admin_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heEBnbWFpbC5jb20iLCJleHBpcnkiOjE3MTI3NTcxNzF9.Te9-HyOU-ihXOlRKIn2Tiq1xHw6HBmyKTLG062Fc15k"
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