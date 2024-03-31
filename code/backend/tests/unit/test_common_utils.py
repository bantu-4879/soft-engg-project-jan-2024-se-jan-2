# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is testing file for common utils.

# --------------------  Imports  --------------------

from application.globals import API_VERSION
from conftest import (
    admin_user_id,
    admin_web_token,
)

# --------------------  Tests  --------------------

headers = {
    "Content-type": "application/json",
    "web_token": admin_web_token,
    "user_id": admin_user_id,
}


def test_common_utils_token_required_with_fixture_get_401(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/newusers' page is requested (GET) with missing or invalid token
    THEN check that the response is 401
    """
    headers = {
        "Content-type": "application/json",
        "web_token": "",
        "user_id": admin_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/auth/newUsers",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 401
    assert "Token is empty or missing" in response["message"]


def test_common_utils_token_required_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/auth/newusers' page is requested (GET) with valid token for admin
    THEN check that the response is 200
    """

    response = test_client.get(
        f"/api/{API_VERSION}/auth/newUsers",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
