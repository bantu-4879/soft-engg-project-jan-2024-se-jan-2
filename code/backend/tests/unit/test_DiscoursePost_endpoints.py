from application.globals import API_VERSION
import time
from conftest import (
    admin_user_id,
    admin_web_token,
    student_web_token,
    student_user_id
)


def test_discourse_allcategories_api_with_fixture_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/dicourse/categories' page is requested (GET) by user to get all the existing categories 
    THEN check that the response is 200
    """

    headers = {
    "Content-type": "application/json",
    "web_token": student_web_token,
    "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/discourse/categories",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200  


def test_discourse_category_api_with_fixture_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/dicourse/category' page is requested (GET) by user to get a single categories 
    THEN check that the response is 200
    """

    headers = {
    "Content-type": "application/json",
    "web_token": student_web_token,
    "user_id": student_user_id,
    }
    category_id =""
    response = test_client.get(
        f"/api/{API_VERSION}/discourse/category/{category_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200  


def test_discourse_category_api_with_fixture_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/dicourse/category' page is requested (POST) by admin/staff to create a category
    THEN check that the response is 200
    """

    headers = {
    "Content-type": "application/json",
    "web_token": admin_web_token,
    "user_id": admin_user_id,
    }

    response = test_client.put(
        f"/api/{API_VERSION}/discourse/category",
        json={
            "category_name": "Test Category",
            "color": "blue",
            "text_color": "black",
            "permission_staff": "",
            "parent_category_id": "",
            "permission_all": "",
            "category_description": "This is a test category"
        }, 
        headers=headers,
    )
    response = response.get_json()
    assert  response["status_code"] == 200  


def test_discourse_tag_api_with_fixture_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/dicourse/tags' page is requested (GET) by user to get all the existing tags
    THEN check that the response is 200
    """
    headers = {
    "Content-type": "application/json",
    "web_token": student_web_token,
    "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/discourse/tags",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200  