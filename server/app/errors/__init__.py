from json import JSONDecodeError

from argon2.exceptions import VerifyMismatchError, VerificationError
from sqlalchemy.orm import exc
from werkzeug.exceptions import BadRequest

from .handlers import handle_password_mismatch

all_error_handlers = {
    'handle_password_mismatch': [VerifyMismatchError, VerificationError],
    'handle_bad_request': [BadRequest, JSONDecodeError],
    'handle_not_found': [exc.NoResultFound, exc.MultipleResultsFound]
}
