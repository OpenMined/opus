from datetime import datetime

import requests
from flask import current_app

from app.services.ssi import get_credential_definition_id


def creat_invitation():
    response = requests.post(f"{current_app.config['ARIES_AGENT_URL']}/connections/create-invitation")
    return response.json()


def get_schema(attributes=None):
    if attributes is None:
        attributes = ["email", "time"]

    schema_body = {
        "schema_name": "verified-email",
        "schema_version": "1.2.2",
        "attributes": attributes,
    }
    response = requests.post(f"{current_app.config['ARIES_AGENT_URL']}/schemas", json=schema_body)
    return response.json()


def send_credentials_offer(message):
    return requests.post(
        f"{current_app.config['ARIES_AGENT_URL']}/issue-credential/send-offer",
        json={
            "auto_issue": False,
            "connection_id": message["connection_id"],
            "cred_def_id": get_credential_definition_id(),
        }
    )


def issue_credentials(credential_exchange_id, email):
    return requests.post(
        f"{current_app.config['ARIES_AGENT_URL']}/issue-credential/records/{credential_exchange_id}/issue",
        json={
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


def create_credentials(schema_id):
    response = requests.post(
        f"{current_app.config['ARIES_AGENT_URL']}/credential-definitions", json={"schema_id": schema_id}
    )
    return response.json()
