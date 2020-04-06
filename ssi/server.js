var http = require('http');
var parser = require('body-parser');
var cors = require('cors');
var path = require('path');
var { createTerminus } = require('@godaddy/terminus');
var express = require('express');
var ngrok = require('ngrok');
var cache = require('./model');

require('dotenv').config();

const { AgencyServiceClient, Credentials } = require("@streetcred.id/service-clients");
const client = new AgencyServiceClient(new Credentials(process.env.ACCESSTOK, process.env.SUBKEY));

var app = express();
app.use(cors());
app.use(parser.json());
app.use(express.static(path.join(__dirname, 'build')))

app.get('*', function (req, res) {
    res.sendFile(path.join(__dirname, '/build/index.html'));
});

// WEBHOOK ENDPOINT
app.post('/webhook', async function (req, res) {
    try {
        console.log("got webhook" + req + "   type: " + req.body.message_type);
        if (req.body.message_type === 'new_connection') {
                    console.log("new connection notif");

            var params =
            {
                credentialOfferParameters: {
                    definitionId: process.env.CRED_DEF_ID,
                    connectionId: req.body.object_id
                }
            }
            await client.createCredential(params);
        }
        else if (req.body.message_type === 'credential_request') {
                                console.log("cred request notif");

            const attribs = cache.get(req.body.data.ConnectionId)
            if (attribs) {
                var param_obj = JSON.parse(attribs);
                const params = {
                    values: {
                        "Full Name": param_obj["name"],
                        "Title": param_obj["title"],
                        "Company Name": param_obj["org"],
                        "Phone Number": param_obj["phone"],
                        "Email": param_obj["email"]
                    }
                }
                await client.issueCredential(req.body.object_id, params);
            }
        }
    }
    catch (e) {
        console.log(e.message || e.toString());
    }
});

//FRONTEND ENDPOINT
app.post('/api/issue', cors(), async function (req, res) {
    const invite = await getInvite();
    const attribs = JSON.stringify(req.body);

    cache.add(invite.connectionId, attribs);
    res.status(200).send({ invite_url: invite.invitation });
});


const getInvite = async () => {
    try {
        var result = await client.createConnection({
            connectionInvitationParameters: {}
        });
        return result;
    } catch (e) {
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