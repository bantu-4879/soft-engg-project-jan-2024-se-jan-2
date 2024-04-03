from application.globals import API_VERSION
import time
from conftest import (
    student_user_id,
    admin_user_id,
    admin_web_token,
)


def test_badge_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/management/badge' page is requested (POST) by admin to add a badge
    THEN check that the response is 200 and database added the badge successfully
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    
    
    random_badge_name = f"Badge {str(int(time.time()))}"

    response = test_client.post(
        f"/api/{API_VERSION}/management/badge",
        json={
            "badge_name": random_badge_name,
            "badge_picture_location": f"static/badge/{random_badge_name}.png",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_asssign_badge_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/management/assign/badge' page is requested (POST) by admin to assign a badge 
    THEN check that the response is 200 and database added the badge successfully to the user
    """

    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    

    badge_name = "Badge 1712135032"
    
    response = test_client.post(
        f"/api/{API_VERSION}/management/assign/badge",
        json={
            "badge_name": badge_name,
            "user_id": student_user_id,
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_asssign_disciplinary_card_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/management/<string:user_id>/card' page is requested (POST) by admin to assign a badge 
    THEN check that the response is 200 and database added the card successfully to the user
    """

    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    
    
    response = test_client.put(
        f"/api/{API_VERSION}/management/{student_user_id}/card",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
