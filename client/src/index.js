import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import { CSSReset, ThemeProvider } from "@chakra-ui/core";
import theme from "./theme";

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CSSReset />
    <App />
  </ThemeProvider>,
  document.getElementById("root")
);

serviceWorker.unregister();
