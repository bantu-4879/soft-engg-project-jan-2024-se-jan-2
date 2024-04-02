from application.globals import API_VERSION
from conftest import (
    student_user_id,
    student_web_token,
)

def test_inbox_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/inbox/<string:user_id>' page is requested (GET) by user
    THEN check that the response is 200 and data contains inbox messages details 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/inbox/{student_user_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    