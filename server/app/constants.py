from enum import Enum

CASCADE = "all"
KEEP_PARENTS = "save-update, merge, refresh-expire, expunge"

SUCCESS = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500


class Extensions(Enum):
    PASSWORD_HASHER = 'password_hasher'
    REQUIRE_OAUTH = 'require_oauth'
    AUTHORIZATION = 'authorization'
    AUTHLIB_FLASK_CLIENT = 'authlib.integrations.flask_client'
