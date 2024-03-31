from application import create_app
import pytest
from application.logger import logger 



# Please set following required constants to mimic a specific user role.

# STUDENT
student_user_id = "963144cc7c2592c25b6e9ec020f90e3d"
student_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcnkuZG9lQGV4YW1wbGUuY29tIiwiZXhwaXJ5IjoxNzEyNzMzODEzfQ.0Q2fmfFRYyDlM0Bw5CyU5wdMrtEq2GWfK643nc5Iy1Q"
 
# SUPPORT
support_user_id = "fb58cddff315e18f87a86f94dc191891"
support_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heC5kb2VAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE3MTE3OTI4NTh9.-E6BeaQRSb9ULY2spHRBDE5obB5Hy6HD4TzYajcpCSI"
# ADMIN
admin_user_id = "23463b99b62a72f26ed677cc556c44e8"
admin_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImV4YW1wbGVAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE3MTE3Mzc5NDd9.COw3CXy9EpT2RDDaQgZ54k8ap4V0x-dGi7gSv2molJo"
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