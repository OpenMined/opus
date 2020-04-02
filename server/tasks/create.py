import os
import time

from app.models import Users, OAuth2Client
from invoke import task, Collection
from werkzeug.security import gen_salt

from app import create_app

create_collection = Collection('create')


def get_env(test=False):
    env = 'test' if test else 'development'
    os.environ['FLASK_CONFIGURATION'] = env
    return env


@task(help={
    'username': "The username of the user you want to create",
    'email': "The email of the user you want to create",
    'password': "The password of the user you want to create"
})
def user(ctx, username='test', password='123'):
    get_env()
    app = create_app()

    with app.app_context():
        user = Users.query.filter_by(email=f'{username}@example.com').first()
        if not user:
            Users.create(email=f'{username}@example.com', username=username, password=password)
    print("User has been created")


create_collection.add_task(user)


@task(help={
    "email": "The email to which the client will be attached",
    "client_name": "Third party client name",
    "client_uri": "Third party client uri. Used for validating requests",
    "grant_types": "The allowed grant_types.",
    "redirect_uri": "Allowed redirect urls after successful call to oauth/authorization",
    "response_type": "The allowed response types. "
                     "Should be one of code, id_token, token or a mix of them for a hybrid flow",
    "scope": "What resources the third party is allowed to request.",
    "token_endpoint_auth_method": "We'll enforce the third party to provide "
                                  "client_id and client_code as basic auth during oauth/token access token request"
})
def client(ctx,
           email='test@example.com',
           client_name="Awesome Client",
           client_uri="http://localhost:5001",
           grant_types="authorization_code",
           redirect_uris="http://localhost:5001",
           response_types="code id_token token",
           scope="profile username",
           token_endpoint_auth_method="client_secret_basic"):
    get_env()
    app = create_app()

    with app.app_context():
        client_id = gen_salt(24)
        user = Users.query.filter_by(email=email).first()
        if not user:
            print(f"User with email {email} could not be found")
        client = OAuth2Client.create(client_id=client_id, user_id=user.id)
        # Mixin doesn't set the issue_at date
        client.client_id_issued_at = int(time.time())
        if client.token_endpoint_auth_method == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        client_metadata = {
            "client_name": client_name,
            "client_uri": client_uri,
            "grant_types": grant_types.split(),
            "redirect_uris": redirect_uris.split(),
            "response_types": response_types.split(),
            "scope": scope,
            "token_endpoint_auth_method": token_endpoint_auth_method
        }
        client.set_client_metadata(client_metadata)
        client.save()
    print("Client has been created")


create_collection.add_task(client)


@task
def test_data(ctx):
    user(ctx)
    client(ctx)


create_collection.add_task(test_data)
