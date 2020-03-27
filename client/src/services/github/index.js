import icon from "./logo.svg";
import { apiClient, triggerSideEffect } from "../../api";

export default {
  name: "Github",
  icon,
  description: "Where the world hosts its code",
  onConnect: () => {
    const url = `${process.env.BASE_URL || "http://localhost:5000"}/sso/github`;
    window.location.replace(url);
  },
  onDisconnect: async (onSuccess, onError) => {
    triggerSideEffect({
      apiCall: () => apiClient.revokeGithubToken(),
      onSuccess,
      onError,
    });
  },
};
