# --------------------  Imports  --------------------

from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
from application.logger import logger


# --------------------  Code  --------------------

__all__ = [
    "success_200_custom",
    "Success_200",
    "Success_201",
    "BadRequest",
    "Unauthenticated",
    "PermissionDenied",
    "NotFoundError",
    "MethodNotAllowed",
    "AlreadyExistError",
    "InternalServerError",
]


def success_200_custom(data):  # custom success response with data
    status_code = 200
    category = "success"
    logger.info(f"200 - Custom success 200 response sent")
    return {
        "message": data,
        "category": category,
        "status": status_code,
    }


class Success_200(HTTPException):  # 200
    def __init__(
        self,
        status_code=200,
        status_msg="Successful Request",
        category="success",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class Success_201(HTTPException):  # 201
    def __init__(
        self,
        status_code=201,
        status_msg="Successful Request",
        category="success",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class BadRequest(HTTPException):  # 400
    def __init__(
        self,
        status_code=400,
        status_msg="Invalid Data Received",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class Unauthenticated(HTTPException):  # 401
    def __init__(
        self,
        status_code=401,
        status_msg="Token Missing or Invalid",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class PermissionDenied(HTTPException):  # 403
    def __init__(
        self,
        status_code=403,
        status_msg="User Does Not Have Permission",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class NotFoundError(HTTPException):  # 404
    def __init__(
        self,
        status_code=404,
        status_msg="Data Not Found",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class MethodNotAllowed(HTTPException):  # 405
    def __init__(
        self,
        status_code=405,
        status_msg="This Method Is Not Allowed",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class AlreadyExistError(HTTPException):  # 409
    def __init__(
        self,
        status_code=409,
        status_msg="Data Already Exist",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


class InternalServerError(HTTPException):  # 500
    def __init__(
        self,
        status_code=500,
        status_msg="Internal Server Error",
        category="error",
    ):
        logger.info(f"{status_code} - {status_msg}")
        message = {
            "message": status_msg,
            "category": category,
            "status": status_code,
        }
        self.response = make_response(
            jsonify(message),
            status_code,
        )


# --------------------  END  --------------------