from application.globals import API_VERSION
import time
from conftest import (
    admin_user_id,
    admin_web_token,
    student_web_token,
    student_user_id
)


def test_discourse_auth_api_with_fixture_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/dicourse/discourseRegister' page is requested (POST) with all correctly filled data fields for a new user
    THEN check that the response is 200 i.e. the account is created successfully
    """

    headers = {
    "Content-type": "application/json",
    "web_token": student_web_token,
    "user_id": student_user_id,
    }

    response = test_client.post(
        f"/api/{API_VERSION}/discourse/discourseRegister",
        json={
            "user_id": student_user_id,
            "email": "tushar1711892521@gmail.com",
            "password": "Password#12345678",
            "username": "tushar",
            "name": "Tushar Supe",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200  