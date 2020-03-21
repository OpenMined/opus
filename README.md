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

Importantly, *we do not cache, log, or otherwise store any data provided by these third-party APIs*. We simply provide the information to the third party. In addition, we will limit the fields we expose to reduce the risk of re-identifying the user.

### Cons to this approach
This approach has a number of flaws that we can seek to mitigate. However, there are limits to what we can do while a) preserving a simple UX and b) releasing a functional product ASAP. The most major flaw is that the user must trust the host of this PIS to not use their SSO credentials for nefarious purposes. We are just committing to the user that we are not storing their information. This is perhaps addressable by asking them to enter a password, without which, their credentials are unusable. This would have to be entered every time they SSO with the PIS system, akin to how users have to enter a "master password" when interacting with a password manager. If anyone has any insight on how to implement this, please reach out to Grayson or open an issue.

### Importance

One of the main ways this technology is useful is as a mechanism for combatting disinformation. By aggregating sources of identity verification, we can bolster the user's claim that they are a real individual with verifiable information associated with their identity. Additionally, the ability to convey this information without sharing the user's identity allows us to share what would otherwise be more sensitive information quickly and in a way that is more palatable to the end-user.

One of the more driving use cases for this technology is managing information related to COVID19.

In the coming months, many world health experts predict we will be faced with the prospect of long-term, strict social distancing in order to prevent the complete overwhelming of our healthcare services. Some speculate that we could be facing waves of this distancing for over a year's time while vaccines and cures are developed and tested for safety.

In the face of this, in order for our interconnected world to continue to function, we are going to need the ability to track who is a disease risk, who is not, and who has achieved immunity (insofar as that's possible).

> Ultimately, however, I predict that we’ll restore the ability to socialize safely by developing more sophisticated ways to identify who is a disease risk and who isn’t, and discriminating—legally—against those who are.
>
> We can see harbingers of this in the measures some countries are taking today. Israel is going to use the cell-phone location data with which its intelligence services track terrorists to trace people who’ve been in touch with known carriers of the virus. Singapore does exhaustive contact tracing and publishes detailed data on each known case, all but identifying people by name.

Source: https://www.technologyreview.com/s/615370/coronavirus-pandemic-social-distancing-18-months/

We can take Singapore's approach (see https://co.vid19.sg/), which is to make all of this information 100% public and make those infected identifiable with minimal effort, or we can develop systems that allow us to share this information in a way that preserves the privacy of the individuals in question. If we are to enter into a situation where we have to legally discriminate in order to reestablish normalcy in our lives, I believe we must do so in a way that maintains the privacy of the individuals in question. This project, if successful, will enable folks to verify their status from multiple third-party sources without compromising their identity or sharing their locations directly with those sources.


## User Flow
Here's one view on how this service could work from the perspective of an end-user wanting to verify their COVID-19 infection status for the purposes of interacting with local businesses. For the purposes of this discussion, let's call this user Alice.

1. Alice hears about this new screening service that businesses are using to help mitigate their role in the spread of COVID-19. She follows a link from a news article she read online to our homepage.
2. Alice signs up on the OMPIS web app to start connecting their accounts together.
3. After signing into her new account, she sees a list of all of our SSO partners. There's a COVID-specific list and an identity-bolstering list. She goes down the list of the COVID sites, some of which she already has an account for - USA Location Tracing for COVID App, USA COVID infection likeilhood calculator App, USA contract tracing alerts App - and uses single-sign-on (SSO) with each one to hook it into her OMPIS account.
    * At the time of this writing, there are no clear, widely-adopted applications to handle these use-cases, but many folks have already begun work on trying to solve these problems. See http://safepaths.mit.edu/ for a privacy-preserving way of managing location-tracking and contact tracing).
4. After signing in with the various COVID apps, she is alerted that her identity still needs more strength behind it, and is suggested a list of SSO-accounts with which to bolster her claim as an individual. She would SSO into Facebook, her banking institution, and her Google account. This strengthens her identity score past the threshold for scanning into the stores she wants to go to.
5. Once she gets to the store, she'll be able to sign into her OMPIS account and pull up a short-lived, one-time-use QR code. Upon scanning that code, the system in question will query the COVID apps in real-time and retrieve the identity strength score from our application. Since Alice has been signed up for location tracing for awhile, has been carefully avoiding public gatherings, has a high identity strength score, she has a low infection likelihood score, she is allowed into the store.

The store only receives the data surrounding the conclusions of these various applications without having to receive any direct access to the data those applications needed in order to make said conclusions. In addition, the store doesn't know anything about Alice as an individual, other than the fact that she has an OMPIS account and has had her identity verified by these other services.

There are a number of technical considerations that need to be accounted for in the above user flow - it's meant more to generally illustrate how the solution would work than lay out an exact plan. For example, we would need to make sure we can secure the QR code handshake. Those details are yet to have been worked out.

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
    * Credential should be revocable by the user
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

* Easily deployable server to distribute the trust across more than one hosting platform
    * The separate hosts will not communicate in any way. Therefore, if a user has linked many accounts to host A, then they would have to repeat that process on host B in order to utilize SSO with host B.
    * Assume each deployment will be utilizing its own database for storing user SSO-related data and credentials
    * Dockerize the application(s) for ease of deploy with thorough deployment instructions
    * Terraform (or other Infrastructure as Code) configuration for multiple cloud providers could make it easier ![#f03c15](https://placehold.it/15/f03c15/000000?text=+)


## Open Questions
* How do we make the transition away from the short-term, semi-centrilized model to utilizing Aries?
* How can we easily allow for quick deployment as we make updates to this core application to all the various organizations hosting it?
* Will we meet the terms of use for Facebook, Twitter, etc. in order to extract information?
    * We should run this proposal by legal counsel in order to verify our approach. For now, we'll proceed assuming we'll get approval in the long-run.
* How can we secure the transmission of sensitive information in-person while still providing a seamless UX?

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
