from application.globals import API_VERSION
from conftest import (
    student_user_id,
    student_web_token,
    staff_user_id,
    staff_web_token,
    admin_user_id,
    admin_web_token,
)
from application.database import db
from application.models import Authentication, User

# --------------------  Tests  --------------------


def test_student_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/student/<string:user_id>' page is requested (GET) by student
    THEN check that the response is 200 and data contains students personal data
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/student/{student_user_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert response["message"]["id"] == student_user_id
    assert response["message"]["first_name"] == "tushar"


def test_student_api_with_fixture_put_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/student/<string:user_id>' page is requested (PUT) by student to update details
    THEN check that the response is 200 and database contains updated data
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.put(
        f"/api/{API_VERSION}/student/{student_user_id}",
        json={
            "first_name": "tushar",
            "second_name": "supe",
            "email": "tushar1711892521@gmail.com",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    user = User.query.filter_by(id=student_user_id).first()
    assert user.second_name == "supe"


def test_support_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/support/<string:user_id>' page is requested (GET) by support
    THEN check that the response is 200 and data contains supports personal data
    """
    headers = {
        "Content-type": "application/json",
        "web_token": staff_web_token,
        "user_id": staff_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/staff/{staff_user_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert response["message"]["id"] == staff_user_id
    assert response["message"]["first_name"] == "Leo"


def test_admin_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/admin/<string:user_id>' page is requested (GET) by admin
    THEN check that the response is 200 and data contains admins personal data
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/admin/{admin_user_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert response["message"]["id"] == admin_user_id
    assert response["message"]["first_name"] == "max"
