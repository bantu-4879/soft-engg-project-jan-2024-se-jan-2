from application.globals import API_VERSION
import time
from conftest import (
    admin_user_id,
    admin_web_token,
)


headers = {
    "Content-type": "application/json",
    "web_token": admin_web_token,
    "user_id": admin_user_id,
}


def test_register_page_with_fixture_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/auth/register' page is requested (GET)
    THEN check that the response is 405 i.e. method not allowed as no get method is defined for that endpoint
    """
    response = test_client.get(
        f"/api/{API_VERSION}/auth/register",
        headers=headers,
    )
    assert response.status_code == 405  # 405 METHOD NOT ALLOWED, GET not defined


def test_register_page_with_fixture_post_400_missing_data(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/register' page is requested (POST) with empty data fields
    THEN check that the response is 400 i.e. bad request
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/register",
        json={
            "first_name": "",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 400  # bad request
    assert "empty or invalid" in response["message"]  # first_name is empty


def test_register_page_with_fixture_post_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/register' page is requested (POST) with all correctly filled data fields for a new user
    THEN check that the response is 200 i.e. the account is created successfully
    """

    random_email = f"tushar{str(int(time.time()))}@gmail.com"

    response = test_client.post(
        f"/api/{API_VERSION}/auth/register",
        json={
            "first_name": "tushar",
            "last_name": "",
            "email": random_email,
            "password": "1234",
            "retype_password": "1234",
            "role": "student",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200  # account created successfully


def test_register_page_with_fixture_post_409_email_exists(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/register' page is requested (POST) with already existing email id
    THEN check that the response is 409 i.e. Email already exists
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/register",
        json={
            "first_name": "tushar",
            "last_name": "",
            "email": "tushar@gmail.com",
            "password": "1234",
            "retype_password": "1234",
            "role": "student",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 409  # Email already exists


def test_register_page_with_fixture_post_400_invalid_data(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/register' page is requested (POST) with invalid or non matching passwords
    THEN check that the response is 400.
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/register",
        json={
            "first_name": "tushar",
            "last_name": "",
            "email": "tushar@gmail.com",
            "password": "12345",
            "retype_password": "1234",
            "role": "student",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 400  # password not matching


def test_login_page_with_fixture_post_400_missing_data(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/login' page is requested (POST) with empty fields
    THEN check that the response is 400.
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/login",
        json={
            "email": "tushar@gmail.com",
            "password": "",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 400  # empty fields, bad request
    assert "empty" in response["message"]


def test_login_page_with_fixture_post_401_unauthenticated(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/login' page is requested (POST) with wrong password
    THEN check that the response is 401
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/login",
        json={
            "email": "tushar@gmail.com",
            "password": "1234567",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 401


def test_login_page_with_fixture_post_404_user_not_exist(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/login' page is requested (POST) with wrong email
    THEN check that the response is 404
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/login",
        json={
            "email": "tushar12345678@gmail.com",
            "password": "1234",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 404


def test_login_page_with_fixture_post_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/login' page is requested (POST) with correct user details
    THEN check that the response is 200 and user name is correct
    """

    response = test_client.post(
        f"/api/{API_VERSION}/auth/login",
        json={
            "email": "tushar_dummy@gmail.com",
            "password": "1234",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert response["message"]["first_name"] == "dummy"


def test_newusers_page_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/newUsers' page is requested (GET) with correct admin details
    THEN check that the response is 200.
    """

    response = test_client.get(
        f"/api/{API_VERSION}/auth/newUsers",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
