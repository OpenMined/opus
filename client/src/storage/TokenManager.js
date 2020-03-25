const STORAGE_KEYS = {
  EXPIRES_AT: "expires_at",
  REFRESH_TOKEN: "refresh_token",
  ACCESS_TOKEN: "access_token",
};

function jwtDecode(token) {
  return JSON.parse(window.atob(token.split(".")[1]));
}

export default class TokenManager {
  static getToken() {
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  }

  static getRefreshToken() {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  }
  static isAuthenticated() {
    // Check whether the current time is past the
    // Access token's expiry time
    const expiresAt = Number(localStorage.getItem(STORAGE_KEYS.EXPIRES_AT));
    return (
      TokenManager.getToken() && expiresAt && new Date().getTime() < expiresAt
    );
  }
  static setSession = ({ access_token, refresh_token }) => {
    const { exp } = jwtDecode(access_token);
    localStorage.setItem(STORAGE_KEYS.EXPIRES_AT, (exp * 1000).toString());
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh_token);
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, access_token);
  };

  static clearTokenStorage = () => {
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.EXPIRES_AT);
  };
}
