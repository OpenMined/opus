import _ from "lodash";
import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  SimpleGrid,
  Stack,
  useDisclosure,
  useToast,
} from "@chakra-ui/core";
import services from "./services";
import { apiClient, triggerSideEffect } from "./api";
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

  const [currentUser, setCurrentUser] = useState({});
  const [currentServices, setCurrentServices] = useState([]);
  const toast = useToast();

  const onError = (res) => {
    return toast({
      title: "An error occurred",
      description: res.message,
      status: "error",
      position: "top-right",
      duration: 3000,
      isClosable: true,
    });
  };

  const getCurrentUser = async () => {
    if (!TokenManager.isAuthenticated()) {
      setCurrentUser(null);
      setCurrentServices(prepServices());
      return;
    }

    let providers =
      (await triggerSideEffect({
        apiCall: () => apiClient.providers(),
        onError,
      })) || [];
    setCurrentUser(TokenManager.getToken());
    setCurrentServices(
      services.map((s) => {
        s.isConnected = providers.includes(s.name.toLowerCase());
        return s;
      })
    );
  };

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
        await getCurrentUser();
        loginDisclosure.onClose();
      },
    });

  const logout = async () => {
    TokenManager.clearTokenStorage();
    await getCurrentUser();
  };

  useEffect(() => {
    getCurrentUser();
  }, []);

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
              <Service
                {...service}
                key={service.name}
                onDisconnect={() =>
                  service.onDisconnect(() => getCurrentUser(), onError)
                }
              />
            ))}
          </SimpleGrid>
        </>
      )}
    </Box>
  );
};
