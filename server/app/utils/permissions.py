import datetime
import uuid
from functools import wraps

import jwt
from flask import current_app, request

from app.errors.handlers import error_response
from app.errors.messages import BAD_TOKEN_MSG


def _encode_jwt(additional_token_data, expires_delta):
    now = datetime.datetime.utcnow()
    token_data = {
        'iat': now,
        'nbf': now,
        'iss': current_app.config['JWT_DECODE_ISSUER'],
        'aud': current_app.config['JWT_DECODE_ISSUER'],
        'jti': str(uuid.uuid4()),
        'exp': now + expires_delta
    }
    token_data.update(additional_token_data)
    encoded_token = jwt.encode(
        payload=token_data,
        key=current_app.config['JWT_PRIVATE_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    ).decode('utf-8')
    return encoded_token


def encode_access_token(identity):
    token_data = {
        'email': identity,
        'type': 'access',
    }
    return _encode_jwt(token_data, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])


def encode_refresh_token(identity):
    token_data = {
        'email': identity,
        'type': 'refresh',
    }

    return _encode_jwt(token_data, current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])


def decode_jwt(encoded_token):
    data = jwt.decode(
        jwt=encoded_token,
        key=current_app.config['JWT_PUBLIC_KEY'],
        algorithms=current_app.config['JWT_ALGORITHM'],
        audience=current_app.config['JWT_DECODE_ISSUER'],
        issuer=current_app.config['JWT_DECODE_ISSUER'],
        leeway=0
    )

    # Make sure that any custom claims we expect in the token are present
    if 'jti' not in data:
        data['jti'] = None
    if 'email' not in data:
        return error_response(BAD_TOKEN_MSG)
    if 'type' not in data:
        data['type'] = 'access'
    if data['type'] not in ('refresh', 'access'):
        return error_response(BAD_TOKEN_MSG)
    if data['type'] == 'access':
        if 'fresh' not in data:
            data['fresh'] = False
    return data


def get_jwt_identity():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return

    parts = auth_header.strip().split()
    if len(parts) != 2:
        return

    encoded_token = parts[1]
    token = decode_jwt(encoded_token)
    return token['email']


# def secure_webhook(api_method):
#     """Secure aries agent calls"""
#
#     @wraps(api_method)
#     def secure_webhook_func(*args, **kwargs):
#         auth_header = request.headers.get('x-api-key', None)
#         if not auth_header:
#             return error_response(NO_TOKEN_MSG)
#         if auth_header != current_app.config['ARIES_API_KEY']:
#             return error_response(BAD_TOKEN_MSG)
#
#         return api_method(*args, **kwargs)
#
#     return secure_webhook_func


def with_identity(api_method):
    """create JWT identity object for request"""

    @wraps(api_method)
    def with_identity_func(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return error_response(BAD_TOKEN_MSG)

        kwargs["identity"] = identity
        result = api_method(*args, **kwargs)
        return result

    return with_identity_func
