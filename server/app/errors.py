from flask import jsonify

from app.constants import UNAUTHORIZED, FORBIDDEN, BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND

MESSAGE_KEY = 'message'
BAD_PERMISSIONS_MSG = 'bad_permissions'
BAD_REQUEST_MSG = 'bad_request'
NO_TOKEN_MSG = 'no_token'
BAD_TOKEN_MSG = 'bad_token'
NOT_MATCHING_PASSWORDS_MSG = 'password_not_matching'
USER_NOT_FOUND_MSG = 'user_not_found'
INVALID_CREDENTIAL_MSG = 'invalid_credentials'
SERVER_ERROR_MSG = 'server_error'
MESSAGES = {
    NO_TOKEN_MSG: {
        "message": {MESSAGE_KEY: "Missing Authorization Header"},
        "status_code": UNAUTHORIZED,
    },
    BAD_TOKEN_MSG: {
        "message": {MESSAGE_KEY: "Please provide a valid token"},
        "status_code": UNAUTHORIZED,
    },
    BAD_PERMISSIONS_MSG: {
        "message": {MESSAGE_KEY: "Bad permissions"},
        "status_code": FORBIDDEN,
    },
    BAD_REQUEST_MSG: {
        "message": {MESSAGE_KEY: "Bad request"},
        "status_code": BAD_REQUEST,
    },
    NOT_MATCHING_PASSWORDS_MSG: {
        "message": {MESSAGE_KEY: "Passwords do not match"},
        "status_code": BAD_REQUEST,
    },
    USER_NOT_FOUND_MSG: {
        "message": {MESSAGE_KEY: "User not found"},
        "status_code": NOT_FOUND,
    },
    INVALID_CREDENTIAL_MSG: {
        "message": {MESSAGE_KEY: "Invalid credentials"},
        "status_code": UNAUTHORIZED,
    },
    SERVER_ERROR_MSG: {
        "message": {MESSAGE_KEY: "Something went wrong. Please try again later"},
        "status_code": INTERNAL_SERVER_ERROR,
    }
}


def error_response(message_type):
    message = dict(MESSAGES[message_type]['message'])
    status_code = MESSAGES[message_type]['status_code']
    return jsonify(message), status_code
