# Private Identity Server (PIS)

- `/client` - Create React App front-end for identity service
- `/server` - Flask private identity server

## Requirements
#### Legend
- May not be necessary for MVP ![#f03c15](https://placehold.it/15/f03c15/000000?text=+)
- Needs more thought/conversation ![#1589F0](https://placehold.it/15/1589F0/000000?text=+)

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
    * We should run this proposal by legal counsel in order to verify our approach

## Needs
* Security Audit / Review
* Accessibility Audit / Review
* Python folks who can implement Single Sign On
* Folks experienced in designing, developing, and documenting public APIs
