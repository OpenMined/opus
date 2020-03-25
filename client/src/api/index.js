import ApiClient from "./apiClient";

const apiClient = new ApiClient({
  baseUrl: process.env.BASE_URL || "http://localhost:5000",
});
export { apiClient };
