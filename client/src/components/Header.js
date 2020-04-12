import React from "react";
import {
  Box,
  Button,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  Flex,
  Heading,
  Stack,
  useDisclosure,
} from "@chakra-ui/core";
import { PATHS } from "../constants";
import { useHistory } from "react-router-dom";
import { TokenManager } from "../storage";

export const Header = (props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  let history = useHistory();

  const logout = () => {
    TokenManager.clearTokenStorage();
    history.replace(PATHS.LANDING);
  };
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1.5rem"
      bg="teal.500"
      color="white"
      {...props}
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg" letterSpacing={"-.1rem"}>
          Opus
        </Heading>
      </Flex>

      <Box display={{ sm: "block", md: "none" }} onClick={onOpen}>
        <svg fill="white" width="20px" viewBox="0 0 20 20">
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
        </svg>
      </Box>

      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={btnRef}
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Menu</DrawerHeader>

          <DrawerBody>
            <Stack spacing="24px">
              <Box>
                <Button onClick={() => history.replace(PATHS.IDENTITY)}>
                  SSI
                </Button>
              </Box>

              <Box>
                <Button onClick={() => history.replace(PATHS.SERVICES)}>
                  SSO
                </Button>
              </Box>
            </Stack>
          </DrawerBody>
          <DrawerFooter>
            <Button variant="outline" mr={6} onClick={logout}>
              Logout
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </Flex>
  );
};

export default Header;
