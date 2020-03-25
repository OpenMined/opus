import BaseClient from "./baseClient";
import { TokenManager } from "../storage";
class ApiClient extends BaseClient {
  getAuthorizationHeaders() {
    return { Authorization: TokenManager.getToken() };
  }

  async login(body) {
    return this.post("/users/login", { body });
  }

  async register(body) {
    return this.post("/users/register", { body });
  }

  async providers() {
    return this.get("/sso/providers", { noAuthHeader: false });
  }
}

export default ApiClient;
