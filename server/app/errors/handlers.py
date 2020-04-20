from flask import jsonify

from .messages import INCORRECT_PASSWORD, MESSAGES, MESSAGE_KEY, BAD_REQUEST_MSG, NOT_FOUND_MSG, NO_TOKEN_MSG


def handle_password_mismatch():
    return error_response(INCORRECT_PASSWORD)


def handle_bad_request(e):
    return error_response(BAD_REQUEST_MSG, e.msg)


def handle_not_found(e):
    return error_response(NOT_FOUND_MSG, e.msg)


def handle_expired_token(e):
    return error_response(NO_TOKEN_MSG, e.args[0])


def error_response(message_type, message=None):
    """
    Formats the error message and send the correct error code
    :param message_type: the message type for the particular error
    :param message: optional custom message for the given error type
    :return: json response, status code
    """
    response_message = dict(MESSAGES[message_type]['message']) if not message else {MESSAGE_KEY: message}
    status_code = MESSAGES[message_type]['status_code']
    return jsonify(response_message), status_code
