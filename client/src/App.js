import React from "react";
import { Box, useToast } from "@chakra-ui/core";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import { Services } from "./pages/sso";
import { Landing } from "./pages/landing";
import { PATHS } from "./constants";
import { Identity } from "./pages/ssi";
import DrawerMenu from "./components/Drawer";
import Header from "./components/Header";

export default () => {
  const toast = useToast();

  const onError = ({ message }) => {
    return toast({
      title: "An error occurred",
      description: message,
      status: "error",
      position: "top-right",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Router>
      <Header />
      <Box mx="auto" width={["100%", null, 720, 960, 1200]} px={3} pb={6}>
        <Switch>
          <ProtectedRoute path={PATHS.SERVICES}>
            <Services onError={onError} />
          </ProtectedRoute>
          <ProtectedRoute path={PATHS.IDENTITY}>
            <Identity onError={onError} />
          </ProtectedRoute>
          <Route path={PATHS.LANDING}>
            <Landing onError={onError} />
          </Route>
        </Switch>
      </Box>
    </Router>
  );
};
