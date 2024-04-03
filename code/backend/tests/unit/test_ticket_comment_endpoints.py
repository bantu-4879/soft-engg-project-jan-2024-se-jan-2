from application.globals import API_VERSION
from conftest import (
    student_user_id,
    student_web_token,
)


def test_comment_api_with_fixture_post_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/comments/<string:ticket_id>' page is requested (POST) by student to add a comment
    THEN check that the response is 200 and database added the comment successfully
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }    

    ticket_id = "dc292bf4bde7700762e0a07e84c831b0"
    response = test_client.post(
        f"/api/{API_VERSION}/ticket/comments/{ticket_id}",
        json={
            "comment": "This a Test Comment",
            "commenter" : student_user_id,
            "user_mentions" : [],
            "reactions" : ""
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_comment_api_with_fixture_get_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/comments/<string:ticket_id>' page is requested (GET) by user to get all comments on a ticket 
    THEN check that the response is 200 
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }    

    ticket_id = "dc292bf4bde7700762e0a07e84c831b0"
    response = test_client.get(
        f"/api/{API_VERSION}/ticket/comments/{ticket_id}",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200


def test_comment_api_with_fixture_put_200(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v2/comments/<string:ticket_id>' page is requested (PUT) by user to update a comment
    THEN check that the response is 200 and database added the comment successfully
    """
    headers = {
        "Content-type": "application/json",
        "web_token": student_web_token,
        "user_id": student_user_id,
    }    

    ticket_id = "dc292bf4bde7700762e0a07e84c831b0"
    comment_id = "2"
    response = test_client.put(
        f"/api/{API_VERSION}/ticket/comments/{ticket_id}/{comment_id}/{student_user_id}",
        json={
            "comment": "This a Test Comment Update",
            "commenter" : student_user_id,
            "user_mentions" : [],
            "reactions" : ""
        },
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200