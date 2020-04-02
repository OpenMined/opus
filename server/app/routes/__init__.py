from .users import users
from .sso import sso
from .oauth import oauth

all_blueprints = [
    users,
    sso,
    oauth,
]
