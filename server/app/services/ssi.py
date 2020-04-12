from flask import current_app

from app.services import aries_client as aries


def get_credential_definition_id():
    credential_definition_id = current_app.config.get("ARIES_CREDENTIAL_DEFINITION_ID")
    if credential_definition_id is not None:
        return credential_definition_id

    schema_response = aries.get_schema()
    credential_definition_response = aries.create_credentials(schema_response["schema_id"])

    credential_definition_id = credential_definition_response["credential_definition_id"]

    current_app.logger.info(f"cred def id: {credential_definition_id}")
    current_app.config['ARIES_CREDENTIAL_DEFINITION_ID'] = credential_definition_id
    return credential_definition_id
