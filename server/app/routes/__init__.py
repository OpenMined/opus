from .oauth import oauth
from .ssi import ssi
from .sso import sso
from .users import users
from .webhooks import webhooks

all_blueprints = [
    users,
    sso,
    oauth,
    ssi,
    webhooks
]
