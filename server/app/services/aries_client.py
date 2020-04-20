from datetime import datetime

import requests
from flask import current_app

from app.services.ssi import get_credential_definition_id


def base_post(url, body=None):
    params = {
        'url': url,
        'headers': {'x-api-key': str(current_app.config['AGENT_API_KEY'])}
    }
    if body:
        params['json'] = body
    return requests.post(**params)


def creat_invitation():
    response = base_post(f"{current_app.config['ARIES_AGENT_URL']}/connections/create-invitation")
    return response.json()


def get_schema(attributes=None):
    if attributes is None:
        attributes = ["email", "time"]

    schema_body = {
        "schema_name": "verified-email",
        "schema_version": "1.2.2",
        "attributes": attributes,
    }
    response = base_post(f"{current_app.config['ARIES_AGENT_URL']}/schemas", schema_body)
    return response.json()


def send_credentials_offer(message):
    return base_post(
        f"{current_app.config['ARIES_AGENT_URL']}/issue-credential/send-offer",
        {
            "auto_issue": False,
            "connection_id": message["connection_id"],
            "cred_def_id": get_credential_definition_id(),
        }
    )


def issue_credentials(credential_exchange_id, email):
    response = base_post(
        f"{current_app.config['ARIES_AGENT_URL']}/issue-credential/records/{credential_exchange_id}/issue",
        {
            "credential_preview": {
                "attributes": [
                    {
                        "name": "email",
                        "value": email,
                        "mime-type": "text/plain",
                    },
                    {
                        "name": "time",
                        "value": str(datetime.utcnow()),
                        "mime-type": "text/plain",
                    },
                ]
            }
        },
    )
    return response.json()


def create_credentials(schema_id):
    response = base_post(
        f"{current_app.config['ARIES_AGENT_URL']}/credential-definitions",
        {"schema_id": schema_id}
    )
    return response.json()
