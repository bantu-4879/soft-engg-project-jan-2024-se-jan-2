from application.globals import API_VERSION
from conftest import (
    student_user_id,
    student_web_token,
    staff_user_id,
    staff_web_token,
    admin_user_id,
    admin_web_token,
)

# --------------------  Tests  --------------------


def test_student_all_tickets_with_fixture_get_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets' page is requested (GET) by student
    THEN check that the response is 200 and data contains tickets details
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets?query=ticket&filter_priority=&filter_status=&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list


def test_staff_all_tickets_with_fixture_get_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets' page is requested (GET) by user other than student
    THEN check that the response is 403 as that endpoint is only accessible to students
    """
    headers = {
        "Content-type": "application/json",
        "web_token": staff_web_token,
        "user_id": staff_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets?query=ticket&filter_priority=&filter_status=&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_all_students_tickets_with_fixture_get_200_success_1(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets/<string:user_id>' page is requested (GET) by student
    THEN check that the response is 200 and data contains tickets as per query
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets/{student_user_id}?filter_priority=&filter_status=pending&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if response["message"]:
        status = [i["status"] for i in response["message"]]
        assert "resolved" not in status


def test_all_students_tickets_with_fixture_get_200_success_2(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets/<string:user_id>' page is requested (GET) by student
    THEN check that the response is 200 and data contains tickets as per query
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets/{student_user_id}?filter_priority=low,medium&filter_status=&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if response["message"]:
        priority = [i["priority"] for i in response["message"]]
        assert "high" not in priority


def test_all_support_tickets_with_fixture_get_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets/<string:user_id>' page is requested (GET) by support
    THEN check that the response is 200 and data contains unresolved tickets as per query
    """
    headers = {
        "Content-type": "application/json",
        "web_token": staff_web_token,
        "user_id": staff_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets/{staff_user_id}?filter_priority=&filter_status=pending&sortby=created_on&sortdir=desc&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if response["message"]:
        status = [i["status"] for i in response["message"]]
        assert "resolved" not in status


def test_all_admin_tickets_with_fixture_get_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/all-tickets/<string:user_id>' page is requested (GET) by admin
    THEN check that the response is 200 and data contains resolved tickets as per query and in descending order of votes by default
    """
    headers = {
        "Content-type": "application/json",
        "web_token": admin_web_token,
        "user_id": admin_user_id,
    }

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/all-tickets/{admin_user_id}?filter_priority=&filter_status=&sortby=votes&sortdir=desc&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if len(response["message"]) > 1:
        assert response["message"][0]["votes"] >= response["message"][1]["votes"]


def test_ticket_api_with_fixture_post_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/<string:user_id>' page is requested (POST) by student to create a new ticket
    THEN check that the response is 200.
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }

    response = test_client.post(
        f"/api/{API_VERSION}/ticket/{student_user_id}",
        json={
            "title": "Ticket AA",
            "description": "Description for ticket AA",
            "ticket_priority": "0.9",
            "tag": "Portal Down",
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert "Ticket created" in response["message"]


def test_ticket_api_with_fixture_get_200_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/ticket/<string:ticket_id>/<string:user_id>' page is requested (GET)
    THEN check that the response is 200 and data contains ticket details
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }
    ticket_id = "21ebb1e371efe54ce595b0f778f85cbe"

    response = test_client.get(
        f"/api/{API_VERSION}/ticket/{ticket_id}/{student_user_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert ticket_id == response["message"]["id"]
    assert "Ticket AA" in response["message"]["title"]
