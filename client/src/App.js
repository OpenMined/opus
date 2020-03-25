import React, { useEffect, useState } from "react";
import { Box, Button, SimpleGrid, Stack, useDisclosure } from "@chakra-ui/core";

import services from "./services";
import { apiClient } from "./api";
import Modal from "./components/Modal";
import SignupForm from "./components/SignupForm";
import LoginForm from "./components/LoginForm";
import Service from "./components/Service";
import { TokenManager } from "./storage";

export default () => {
  const signupDisclosure = useDisclosure();
  const loginDisclosure = useDisclosure();

  const prepServices = () =>
    services.map((s) => {
      s.isConnected = false;
      return s;
    });

  const [currentUser, setCurrentUser] = useState(null);
  const [currentServices, setCurrentServices] = useState(null);

  const getCurrentUser = async () => {
    if (TokenManager.isAuthenticated()) {
      const providers = await apiClient.providers();
      setCurrentUser(TokenManager.getToken());
      setCurrentServices(
        services.map((s) => {
          if (providers.includes(s.name)) s.isConnected = true;
          return s;
        })
      );
    } else {
      setCurrentUser(null);
      setCurrentServices(prepServices());
    }
  };

  const signup = async (values) => {
    console.log("Do signup", values);

    signupDisclosure.onClose();

    const response = await apiClient.register(values);

    loginDisclosure.onOpen();
  };

  const login = async (values) => {
    const response = await apiClient.login(values);
    TokenManager.setSession(response);

    await getCurrentUser();

    loginDisclosure.onClose();
  };

  const logout = async () => {
    TokenManager.clearTokenStorage();
    await getCurrentUser();
  };

  useEffect(getCurrentUser, []);

  return (
    <Box mx="auto" width={["100%", null, 720, 960, 1200]} px={3} pb={6}>
      {!currentUser && (
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
      )}
      {currentUser && (
        <>
          <Box mx="auto" width={["100%", 200]} py={6}>
            <Button onClick={logout}>Logout</Button>
          </Box>
          <SimpleGrid columns={[1, null, 2, 3]} spacing={[3, null, 5]}>
            {currentServices.map((service) => (
              <Service key={service.name} {...service} />
            ))}
          </SimpleGrid>
        </>
      )}
    </Box>
  );
};
