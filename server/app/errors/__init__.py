from .handlers import handle_password_mismatch
from argon2.exceptions import VerifyMismatchError, VerificationError

all_error_handlers = {
    'handle_password_mismatch': [VerifyMismatchError, VerificationError]
}
