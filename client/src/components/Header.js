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
import { MdMenu } from "react-icons/md";

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
      bg="blue.500"
      color="white"
      {...props}
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg" letterSpacing={"-.1rem"}>
          Opus
        </Heading>
      </Flex>

      {TokenManager.isAuthenticated() ? (
        <Flex align="right" mr={5}>
          <Box onClick={onOpen} as={MdMenu} size="32px" />
        </Flex>
      ) : (
        ""
      )}

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
            <Button onClick={logout} variantColor="blue">
              Logout
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </Flex>
  );
};

export default Header;
