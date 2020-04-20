from flasgger.utils import swag_from
from flask import Blueprint, request, jsonify, current_app

from app.constants import SUCCESS
from app.models import SessionState, Users
from app.services import aries_client as aries
from app.utils.spec import docs_path

BASE_URL = '/webhooks/agent'
TOPIC_CONNECTIONS = {'rule': '/topic/connections/', 'methods': ['POST'], 'endpoint': 'connection'}
TOPIC_ISSUE_CREDENTIAL = {'rule': '/topic/issue_credential/', 'methods': ['POST'], 'endpoint': 'issue_credential'}

webhooks = Blueprint(name='webhooks', import_name=__name__, url_prefix=BASE_URL)


@webhooks.route(**TOPIC_CONNECTIONS)
@swag_from(
    docs_path('api', 'webhooks', 'topic_connections.yaml'), methods=['POST'], endpoint='webhooks.connection'
)
def webhooks_connections():
    message = request.get_json()
    current_app.logger.info(f'webhook received - topic: connections body: {message}')

    handler = connection_handlers.get(message.get('state'))
    if handler:
        handler(message)

    return jsonify({'message': 'success'}), SUCCESS


@webhooks.route(**TOPIC_ISSUE_CREDENTIAL)
@swag_from(
    docs_path('api', 'webhooks', 'topic_issue_credential.yaml'), methods=['POST'], endpoint='webhooks.issue_credential'
)
def webhooks_issue_credential():
    message = request.get_json()
    if message['state'] != 'request_received':
        current_app.logger.info(f'Received message {message}')
        return jsonify({'message': 'success'}), SUCCESS

    credential_exchange_id = message['credential_exchange_id']
    connection_id = message['connection_id']

    current_app.logger.info(
        'Sending credential issue for credential exchange '
        f'{credential_exchange_id} and connection {connection_id}'
    )

    user = Users.query \
        .join(SessionState, SessionState.user_id == Users.id) \
        .filter(SessionState.connection_id == connection_id) \
        .one()

    try:
        response = aries.issue_credentials(credential_exchange_id, user.email)
        current_app.logger.info('webhooks_issue_credential')
        current_app.logger.info(response)
    except Exception:
        current_app.logger.exception('Error issuing credential:')
        SessionState.query \
            .filter(SessionState.connection_id == connection_id) \
            .first() \
            .update({'state': 'credential-error'})

    return jsonify({'message': 'success'}), SUCCESS


def handle_connection_request(message):
    connection_id = message['connection_id']
    SessionState.query \
        .filter(SessionState.connection_id == connection_id) \
        .first() \
        .update({'state': 'connection-request-received'})


def handle_connection_response(message):
    SessionState.query \
        .filter(SessionState.connection_id == message['connection_id']) \
        .one() \
        .update({'state': 'connection-formed'})
    try:
        response = aries.send_credentials_offer(message)
        current_app.logger.info('handle_connection_response')
        current_app.logger.info(response.json())
        response.raise_for_status()
    except Exception as e:
        current_app.logger.exception(f'Error sending credential offer: {e.msg}')
        SessionState.query \
            .filter(SessionState.connection_id == str(message['connection_id'])) \
            .one() \
            .update({'state': 'offer-error'})


connection_handlers = {
    'request': handle_connection_request,
    'response': handle_connection_response
}
