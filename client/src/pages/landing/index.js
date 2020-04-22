import { Box, Button, Stack, useDisclosure } from "@chakra-ui/core";
import Modal from "../../components/Modal";
import React, { useState } from "react";
import { useHistory, useLocation } from "react-router-dom";
import { apiClient, triggerSideEffect } from "../../api";
import QRcode from 'qrcode.react';

import { TokenManager } from "../../storage";
import SignupForm from "./SignupForm";
import LoginForm from "./LoginForm";

import poll from "./utils.js";

export function Landing({ onError }) {
  const [registrationQR, setRegistrationQR] = useState();
  const [loginQR, setLoginQR] = useState();
  const signupDisclosure = useDisclosure();
  const loginDisclosure = useDisclosure();
  const signupQRDisclosure = useDisclosure();
  const loginQRDisclosure = useDisclosure();
  let history = useHistory();
  let location = useLocation();
  let { from } = location.state || { from: { pathname: "/services" } };

  const signup = async (values) => {
    triggerSideEffect({
      apiCall: () => apiClient.register(values),
      onError,
      onSuccess: async (responseData) => {
        setRegistrationQR("https://web.cloud.streetcred.id/link/?c_i=" + responseData["inviteURL"]);
        signupDisclosure.onClose();
        signupQRDisclosure.onOpen();
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

    const getLoginQRCode = async () => {
      triggerSideEffect({
        apiCall: () => apiClient.getLoginQRCode(),
        onError,
        onSuccess: async (responseData) => {
          setLoginQR("https://web.cloud.streetcred.id/link/?c_i=" + responseData["verificationURL"]);
          loginQRDisclosure.onOpen();

          triggerSideEffect({
            apiCall: () => apiClient.qrLogin({verification_id: responseData["verificationId"]}),
            onError,
            onSuccess: async (responseData) => {
              console.log('Final response!!!!' + responseData);
              // This is the necessary login code below. 
              TokenManager.setSession(responseData);
              loginQRDisclosure.onClose();
              history.replace(from);
            }
          });

          poll(
            function () {
              console.log("Hello!")
            },
            function (err) {
              if (err) {

              }
              else {
                
              }
            },
          2000, 150);

          // Second API call to log the user in when the verification is validated.
          // Need to write a simple non-blocking polling function. 
          // Gives the user 30 seconds to respond, otherwise it times out.
          // poll(async (responseData) => {
          //   triggerSideEffect({
          //     apiCall: () => apiClient.qrLogin({verification_id: responseData["verificationId"]}),
          //     onError,
          //     onSuccess: async (responseData) => {
          //       console.log('Final response!!!!' + responseData);
          //       // This is the necessary login code below. 
          //       // TokenManager.setSession(responseData);
          //       // loginQRDisclosure.onClose();
          //       // history.replace(from);
          //     }
          //   })
          // }, 2000, 150);
        },
      });
    };

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
          <Button variantColor="blue" onClick={getLoginQRCode}>
            QR Code Login
          </Button>
        </Stack>
      </Box>
      <Modal {...signupDisclosure} title="Signup">
        <SignupForm onSubmit={signup} />
      </Modal>
      <Modal {...loginDisclosure} title="Login">
        <LoginForm onSubmit={login} />
      </Modal>
      <Modal {...signupQRDisclosure} title="Scan Me!">
          <QRcode size="200" value={registrationQR} style={{margin: "0 auto", padding: "10px"}} />
      </Modal>
      <Modal {...loginQRDisclosure}>
        Scan me!
        <QRcode size="200" value={loginQR} style={{margin: "0 auto", padding: "10px"}} />
      </Modal>
    </>
  );
}
