from json import JSONDecodeError

from argon2.exceptions import VerifyMismatchError, VerificationError
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy.orm import exc
from werkzeug.exceptions import BadRequest

all_error_handlers = {
    'handle_password_mismatch': [VerifyMismatchError, VerificationError],
    'handle_bad_request': [BadRequest, JSONDecodeError],
    'handle_expired_token': [ExpiredSignatureError, DecodeError],
    'handle_not_found': [exc.NoResultFound, exc.MultipleResultsFound]
}
