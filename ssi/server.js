const http = require('http');
const parser = require('body-parser');
const cors = require('cors');
const { createTerminus } = require('@godaddy/terminus');
const express = require('express');
const ngrok = require('ngrok');
const cache = require('./model');
// const request = require('request');

require('dotenv').config();

const { AgencyServiceClient, Credentials } = require("@streetcred.id/service-clients");
const client = new AgencyServiceClient(new Credentials(process.env.ACCESSTOK, process.env.SUBKEY));

var app = express();
app.use(cors());
app.use(parser.json());

// WEBHOOK ENDPOINT
app.post('/webhook', async function (req, res) {
    try {
        console.log("got webhook" + req + "   type: " + req.body.message_type);
        if (req.body.message_type === 'new_connection') {
            console.log("New connection.");

            var credentialValues = JSON.parse(cache.get("userRegistrationBody"));
            var params =
            {
                credentialOfferParameters: {
                    definitionId: process.env.CRED_DEF_ID,
                    connectionId: cache.get("connectionId"),
                    automaticIssuance: true,
                    credentialValues: {
                        email: credentialValues["email"],
                        password: credentialValues["password"],
                    }
                }
            }
            console.log(params);
            await client.createCredential(params);
        }
        else if (req.body.message_type === 'verification') {
            console.log('New verification: '+ req.body.object_id);
        }
    }
    catch (e) {
        console.log(e.message || e.toString());
    }
});

app.post('/users/register', async function (req, res) {
    // Add data attributes to the cache so they can be retrieved later.
    cache.add("userRegistrationBody", JSON.stringify(req.body));

    const invite = await getInvite();
    cache.add("connectionId", invite.connectionId);
    res.status(200).send({ inviteURL: invite.invitation });
});

const getInvite = async () => {
    try {
        var result = await client.createConnection({
            connectionInvitationParameters: {}
        });
        return result;
    } catch (e) {
        console.log("createConnection: Streetcred API call error!")
        console.log(e.message || e.toString());
    }
}

app.get('/users/qr_login', async function (req, res) {
    const verification = await getLoginQRCode();
    cache.add("verificationId", verification.verificationId);
    res.status(200).send({
        verificationId: verification.verificationId, 
        verificationURL: verification.verificationRequestData 
    });
});

const getLoginQRCode = async () => {
    try {
        var result = await client.createVerificationFromPolicy(
            process.env.VERIFICATION_DEF_ID
        );
        return result;
    } catch (e) {
        console.log("createVerificationFromPolicy: Streetcred API call error!")
        console.log(e.message || e.toString());
    }
}

app.post('/users/login_verifications', async function (req, res) {
    const verification = await getVerification(req.body.verification_id);
    res.status(200).send(verification);
});

const getVerification = async (verificationId) => {
    try {
        var result = await client.getVerification(
            verificationId
        );
        return result;
    } catch (e) {
        console.log("getVerification: Streetcred API call error!")
        console.log(e.message || e.toString());
    }
}

// for graceful closing
var server = http.createServer(app);

async function onSignal() {
    var webhookId = cache.get("webhookId");
    const p1 = await client.removeWebhook(webhookId);
    return Promise.all([p1]);
}
createTerminus(server, {
    signals: ['SIGINT', 'SIGTERM'],
    healthChecks: {},
    onSignal
});

const PORT = process.env.PORT || 3002;
var server = server.listen(PORT, async function () {
    const url_val = await ngrok.connect(PORT);
    console.log("============= \n\n" + url_val + "\n\n =========");
    var response = await client.createWebhook({
        webhookParameters: {
            url: url_val + "/webhook",  // process.env.NGROK_URL
            type: "Notification"
        }
    });
    
    cache.add("webhookId", response.id);
    console.log('Listening on port %d', server.address().port);
});