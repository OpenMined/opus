import React from "react";
import { Route, Redirect } from "react-router-dom";
import { TokenManager } from "../storage";

const ProtectedRoute = ({ component: RenderComponent, ...rest }) =>
  TokenManager.isAuthenticated() ? (
    <Route
      {...rest}
      render={(renderProps) => <RenderComponent {...renderProps} />}
    />
  ) : (
    <Redirect to="/" />
  );

export default ProtectedRoute;
