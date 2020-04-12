from .messages import error_response, INCORRECT_PASSWORD
from ..constants import BAD_REQUEST, NOT_FOUND


def handle_password_mismatch():
    return error_response(INCORRECT_PASSWORD)


def handle_bad_request(e):
    return error_response(BAD_REQUEST, e.message)


def handle_not_found(e):
    return error_response(NOT_FOUND, e.message)
