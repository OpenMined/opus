from .messages import error_response, INCORRECT_PASSWORD


def handle_password_mismatch():
    return error_response(INCORRECT_PASSWORD)
