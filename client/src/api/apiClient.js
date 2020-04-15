import BaseClient from "./baseClient";
import { TokenManager } from "../storage";
class ApiClient extends BaseClient {
  getAuthorizationHeaders() {
    return { Authorization: `Bearer ${TokenManager.getToken()}` };
  }

  async login(body) {
    return this.post("/users/login", { body });
  }

  async generateLoginURL() {
    return this.get("/users/qr_login");
  }

  async register(body) {
    return this.post("/users/register", { body });
  }

  async providers() {
    return this.get("/sso/providers", { noAuthHeader: false });
  }

  async revokeGithubToken() {
    return this.post("/sso/github/revoke", { noAuthHeader: false });
  }
}

export default ApiClient;
