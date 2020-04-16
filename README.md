# Private Identity Server

- `/client` - Create React App front-end for identity service
- `/server` - Flask private identity server
- `/ssi` - Streetcred Self Sovereign Identity service

## Running the Application

1. You will need a `.env` file in your `ssi` directory (`/ssi/.env`). This provides your Streetcred credentials to the `ssi` service. Your `.env` file will follow the same format as show in this demo [here](https://github.com/streetcred-id/iiw-demo). The `.env` file should be laid out as such:
```
# Developer Credentials #
ACCESSTOK = '< Your Access Token Here >'
SUBKEY = '< Your Subscription Key Here >'

# Credential Definition #
CRED_DEF_ID = '< Your Credential Definition Here >'

# Verification Definition #
VERIFICATION_DEF_ID = '< Your Verification Definition Here>'
```

2. To generate your own developer credentials you will have to create an organisation on the Streetcred developer portal. This will provide you with an Access Token and Subscription Key which you can add to your `.env` file. More detailed instructions can be found [here](https://github.com/streetcred-id/iiw-demo).

3. Make sure you have `docker` installed on your system. Next, run `docker-compose build`.

4. run `docker-compose up`

This will start both the client/server application, and both will reload automatically as you make changes.

## Further Documentation

See the Readmes within the `client/`, `server/`, `/ssi` directories for more information.
