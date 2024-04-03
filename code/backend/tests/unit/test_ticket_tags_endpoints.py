from application.globals import API_VERSION
import time
from conftest import (
    student_user_id,
    student_web_token,
    staff_user_id,
    staff_web_token,
    admin_user_id,
    admin_web_token,
)


def test_tag_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/tags/add-tag' page is requested (POST) by user to add tag
    THEN check that the response is 200 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    
    
    random_tag_name = f"Tag {str(int(time.time()))}"

    response = test_client.post(
        f"/api/{API_VERSION}/tags/add-tag",
        json={
            "name":random_tag_name,
            "description": "This is tag description"
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_tag_api_with_fixture_put_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/tags/add-tag' page is requested (PUT) by user to update tag
    THEN check that the response is 200 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    
    tag_id = "1"
    random_tag_name = f"Tag {str(int(time.time()))}"

    response = test_client.put(
        f"/api/{API_VERSION}/tags/{tag_id}",
        json={
            "name":random_tag_name,
            "description": "This is tag description"
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_tag_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/tags/all-tags' page is requested (GET) by user to get all tags
    THEN check that the response is 200 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }    

    response = test_client.get(
        f"/api/{API_VERSION}/tags/all-tags",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200



def test_ticket_tag_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/tags/<string:ticket_id>' page is requested (GET) by user to get tags
    THEN check that the response is 200 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }    

    ticket_id = "dc292bf4bde7700762e0a07e84c831b0"
    response = test_client.get(
        f"/api/{API_VERSION}/tags/{ticket_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_ticket_tag_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/tags/<string:ticket_id>' page is requested (POST) by user to add tags to a ticket
    THEN check that the response is 200  
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }    

    ticket_id = "dc292bf4bde7700762e0a07e84c831b0"
    response = test_client.get(
        f"/api/{API_VERSION}/tags/{ticket_id}",
        json={
            "tag_ids":[1]
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200