import React from "react";
import { Redirect, Route } from "react-router-dom";
import { TokenManager } from "../storage";

const ProtectedRoute = ({ component: RenderComponent, ...rest }) =>
  TokenManager.isAuthenticated() ? (
    <Route
      {...rest}
      render={(renderProps) => (
        <RenderComponent {...{ ...renderProps, ...rest }} />
      )}
    />
  ) : (
    <Redirect to="/" />
  );

export default ProtectedRoute;
