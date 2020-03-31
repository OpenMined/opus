import React from "react";
import { Box, useToast } from "@chakra-ui/core";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import { Services } from "./pages/sso";
import { Landing } from "./pages/landing";

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
      <Box mx="auto" width={["100%", null, 720, 960, 1200]} px={3} pb={6}>
        <Switch>
          <ProtectedRoute path="/services">
            <Services onError={onError} />
          </ProtectedRoute>
          <Route path="/">
            <Landing onError={onError} />
          </Route>
        </Switch>
      </Box>
    </Router>
  );
};
