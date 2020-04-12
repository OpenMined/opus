import BaseClient from "./baseClient";
import { TokenManager } from "../storage";

class ApiClient extends BaseClient {
  getAuthorizationHeaders() {
    return { Authorization: `Bearer ${TokenManager.getToken()}` };
  }

  async login(body) {
    return this.post("/users/login", { body, noAuthHeader: true });
  }

  async register(body) {
    return this.post("/users/register", { body, noAuthHeader: true });
  }

  async providers() {
    return this.get("/sso/providers");
  }

  async revokeGithubToken() {
    return this.post("/sso/github/revoke");
  }

  async requestSSICredentials() {
    return this.get("/ssi/request");
  }
}

export default ApiClient;
