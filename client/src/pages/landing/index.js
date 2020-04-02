import { Box, Button, Stack, useDisclosure } from "@chakra-ui/core";
import Modal from "../../components/Modal";
import React from "react";
import { useHistory, useLocation } from "react-router-dom";
import { apiClient, triggerSideEffect } from "../../api";

import { TokenManager } from "../../storage";
import SignupForm from "./SignupForm";
import LoginForm from "./LoginForm";

export function Landing({ onError }) {
  const signupDisclosure = useDisclosure();
  const loginDisclosure = useDisclosure();
  let history = useHistory();
  let location = useLocation();
  let { from } = location.state || { from: { pathname: "/services" } };

  const signup = async (values) => {
    triggerSideEffect({
      apiCall: () => apiClient.register(values),
      onError,
      onSuccess: () => {
        signupDisclosure.onClose();
        loginDisclosure.onOpen();
      },
    });
  };

  const login = async (values) =>
    triggerSideEffect({
      apiCall: () => apiClient.login(values),
      onError,
      onSuccess: async (responseData) => {
        TokenManager.setSession(responseData);
        loginDisclosure.onClose();
        history.replace(from);
      },
    });

  return (
    <>
      <Box mx="auto" width={["100%", 200]} py={6}>
        <Stack spacing={4}>
          <Button variantColor="blue" onClick={signupDisclosure.onOpen}>
            Signup
          </Button>
          <Button variantColor="blue" onClick={loginDisclosure.onOpen}>
            Login
          </Button>
        </Stack>
      </Box>
      <Modal {...signupDisclosure} title="Signup">
        <SignupForm onSubmit={signup} />
      </Modal>
      <Modal {...loginDisclosure} title="Login">
        <LoginForm onSubmit={login} />
      </Modal>
    </>
  );
}
