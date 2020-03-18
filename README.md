# Private Identity Server (PIS)

- `/client` - Create React App front-end for identity service
- `/server` - Flask private identity server

## Purpose

The goal of this project is to allow individuals to be able to reliably and verifiably present information about themselves to third-parties without also sharing their identity.

There are two important components to this:
1. Their identity, while not shared with the third party, is verified by multiple authorities. This is important to ensure that the individual is actually a unique person and not, say, a bot.
2. Sharing information about this individual securely without sharing information that would identify them to the third party.

Without 1, the information transferred in 2 is far less useful and cannot be trusted for many circumstances.

### How do we accomplish this?
In the interest of expediency, we are choosing to accomplish this by creating a service which allows you to sign in with a variety of other services, including Facebook, LinkedIn, and Twitter. Each of these sign-ins bolsters your identity - while just having a Facebook account linked does not provide much verification that you are a real, individual person, having 8 accounts (some of which with services that have a vested interest in preventing botting/spam accounts) provides greater verification. This addresses purpose 1.

In addition, we are implementing a Single Sign On (SSO) server for this service as well. This will allow third-party applications to receive permission to get certain data points about an individual by way of querying the APIs of the accounts in question. During this single-sign on, the user interacting with the third-party service will see which fields the third party is asking for, as well as which of the linked services will provide those fields.

Importantly, *we do not cache, log, or otherwise store any data provided by these third-party APIs*. We simply provide the information to the third party. In addition, we will limit the fields we expose to reduce the risk of reidentifying the user.

### Cons to this approach
This approach has a number of flaws that we can seek to mitigate. However, there are limits to what we can do while a) preserving a simple UX and b) releasing a functional product ASAP. The most major flaw is that the user must trust the host of this PIS to not use their SSO credentials for nefarious purposes. We are just comitting to the user that we are not storing their information. This is perhaps addressible by asking them to enter a password, without which, their credentials are unusable. This would have to be entered every time they SSO with the PIS system, akin to how users have to enter a "master password" when interacting with a password manager. If anyone has any insight on how to implement this, please reach out to Grayson or open an issue.

## Requirements
#### Legend
- May not be necessary for MVP ![#f03c15](https://placehold.it/15/f03c15/000000?text=+)
- Needs more thought/conversation ![#1589F0](https://placehold.it/15/1589F0/000000?text=+)

#### Requirements List (High-Level)
* Landing page explaining the project
* Single Sign On integration with Multiple Providers
    * Providers:
        * Google
        * Facebook
        * Twitter
        * Linkedin
        * Banks (Capital One, etc.)
        * Etc.
    * Should allow for ease of connecting all social accounts into one PIS account
    * No data other than the credentials and unique identifiers for accessing the corresponding APIs should be stored in the PIS DB
* Vending Credentials for Identity Verification
    * Accomplished by Aries, in the long run. See https://hackmd.io/qeso7QTVRXqXf4uL6cbdgQ?sync=&type= for more info
    * Credential should be specific to the third-party organization requesting the data
        * i.e. if Verily wants access to birthdate and sex information, they will receive a token that is specific to their service for querying information about this user. This would be different from the token generated for another COV19 screening application asking for the same information from the same user.
    * Credential should include which fields are accessible via the token in question
    * Credential should be revokable by the user
    * Credential should be acquired by the third-party application via a single-sign on flow where this identity server is the identity provider
* Securely disclosing personal information to third-party applications without disclosing the identity of the person involved
    * In-memory data retrieval from the various SSO destinations will be necessary
    * API that will be accessible to these third-party applications to retrieve that data in real-time, authenticated by the credential
        * List of disambiguated data fields accessible via the API, along with each source that can provide that information
            * Some sophisticated change-management will be needed here, as this will be subject to change often. Especially given that we want to allow for this to be hosted in a decentralized fashion.
        * API Documentation
        * In addition to the data fields provided, we should provide information as to the strength of the individual's identity within our system.
            * For example, we could say "this individual's identity has been verified through Facebook, Twitter, Github, Google, and LinkedIn" ![#1589F0](https://placehold.it/15/1589F0/000000?text=+)
        * When returning data via this API, we should indicate which source(s) said data originated from with each field.
            * For example, if we return "birthdate", we should include "as verified by Facebook and LinkedIn"
            * In case of conflicting information, we should return multiple results with the source of each ![#1589F0](https://placehold.it/15/1589F0/000000?text=+)

* Easily deployable server to distribute the trust accross more than one hosting platform
    * Assume each deployment will be utilizing its own database for storing user SSO-related data and credentials
    * Dockerize the application(s) for ease of deploy with thorough deployment instructions
    * Terraform (or other Infrastructure as Code) configuration for multiple cloud providers could make it easier ![#f03c15](https://placehold.it/15/f03c15/000000?text=+)


## Open Questions
* How do we make the transition away from the short-term, semi-centrilized model to utilizing Aries?
* How can we easily allow for quick deployment as we make updates to this core application to all the various organizations hosting it?
* What technology stack should we use to get this off the ground quickly, but also allow for ease of hosting by third parties?
* How should we implement single-sign on?
    * https://authlib.org/ seems like a good option, especially since it covers our needs for an OAuth Client as well
* Will we meet the terms of use for Facebook, Twitter, etc. in order to extract information?
    * We should run this proposal by legal counsel in order to verify our approach. For now, we'll proceed assuming we'll get approval in the long-run.

## Needs
* Security Audit / Review
* Accessibility Audit / Review
* Python-experienced folks who can implement Single Sign On
* Folks experienced in designing, developing, and documenting public APIs


## Running the Application

Make sure you have `docker` installed on your system.

1. run `docker-compose build`
2. run `docker-compose up`

This will start both the client/server application, and both will reload automatically as you make changes.

## Further Documentation

See the Readmes within the `client/` and `server/` directories for more information.
