import base64
import io
import re

import qrcode
from flasgger import swag_from
from flask import Blueprint, current_app, jsonify
from sqlalchemy import and_

from app.constants import SUCCESS
from app.models import SessionState, Users
from app.services import aries_client as aries
from app.utils.permissions import with_identity
from app.utils.spec import docs_path

BASE_URL = '/ssi'
SSI_REQUEST = {'rule': '/request', 'methods': ['GET'], 'endpoint': 'request'}
SSI_STATE = {'rule': '/state/:connection_id', 'methods': ['POST'], 'endpoint': 'state'}

ssi = Blueprint(name='ssi', import_name=__name__, url_prefix=BASE_URL)


@ssi.route(**SSI_REQUEST)
@swag_from(
    docs_path('api', 'ssi', 'ssi_request.yaml'), methods=['GET'], endpoint='ssi.request'
)
@with_identity
def ssi_request(identity):
    invite = aries.creat_invitation()

    connection_id = invite["connection_id"]
    invitation_url = invite["invitation_url"]

    SessionState.create(
        connection_id=connection_id,
        invite_url=invitation_url,
        state="invite-created",
        user_id=Users.query.find_by(email=identity).one()
    )
    streetcred_url = re.sub(
        r"^https?:\/\/\S*\?", "didcomm://invite?", invitation_url
    )

    stream = io.BytesIO()
    qr_png = qrcode.make(invitation_url)
    qr_png.save(stream, "PNG")
    qr_png_b64 = base64.b64encode(stream.getvalue()).decode("utf-8")

    return jsonify({
        "qr_png": qr_png_b64,
        "streetcred_url": streetcred_url,
        "invitation_url": invitation_url,
        "connection_id": connection_id,
    }), SUCCESS


@ssi.route(**SSI_STATE)
@swag_from(
    docs_path('api', 'ssi', 'ssi_state.yaml'), methods=['POST'], endpoint='ssi.state'
)
@with_identity
def ssi_state(connection_id, identity):
    session = SessionState.query \
        .join(Users, Users.user_id == Users.user_id) \
        .filter(and_(Users.email == identity, SessionState.connection_id == connection_id)) \
        .one()

    return jsonify({"state": session.state}), SUCCESS
