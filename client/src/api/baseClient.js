import _ from "lodash";
import fetch from "node-fetch";

const rxOne = /^[\],:{}\s]*$/;
const rxTwo = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g;
const rxThree = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g;
const rxFour = /(?:^|:|,)(?:\s*\[)+/g;
const isJSON = (input) =>
  input.length &&
  rxOne.test(
    input.replace(rxTwo, "@").replace(rxThree, "]").replace(rxFour, "")
  );

class BaseClient {
  constructor({ headers, baseUrl }) {
    this.baseUrl = baseUrl;
    this.headers = {
      ...{
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      ...headers,
    };
  }

  queryParams(params) {
    return Object.keys(params)
      .map((k) => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
      .join("&");
  }

  getAuthorizationHeaders() {
    return {};
  }

  async generateRequest(options) {
    const {
      timeout = 10000,
      body = {},
      headers = {},
      path = "",
      method = "GET",
      noAuthHeader = false,
    } = options;

    let requestBody = null;
    let url = `${this.baseUrl}${path}`;

    if ("GET" === method && !_.isEmpty(body)) {
      const params = _.isString(body) ? JSON.parse(body) : body;
      url += (url.indexOf("?") === -1 ? "?" : "&") + this.queryParams(params);
    } else {
      requestBody = _.isEmpty(body)
        ? null
        : _.isString(body)
        ? body
        : JSON.stringify(body);
    }

    return {
      url,
      body: requestBody,
      cors: true,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...headers,
        ...(noAuthHeader
          ? {}
          : await this.getAuthorizationHeaders(requestBody)),
      },
      method,
      timeout,
    };
  }

  async fetch(path, props) {
    const { url, ...params } = await this.generateRequest({ path, ...props });
    const response = await fetch(url, params);
    const responseData = await response.text();
    return isJSON(responseData) ? JSON.parse(responseData) : responseData;
  }

  get(path, options) {
    return this.fetch(path, { ...options, ...{ method: "GET" } });
  }

  post(path, options) {
    return this.fetch(path, { ...options, ...{ method: "POST" } });
  }

  put(path, options) {
    return this.fetch(path, { ...options, ...{ method: "PUT" } });
  }

  delete(path, options) {
    return this.fetch(path, { ...options, ...{ method: "DELETE" } });
  }
}

export default BaseClient;
