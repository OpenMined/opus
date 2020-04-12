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
  Stack,
  useDisclosure,
} from "@chakra-ui/core";
import { TokenManager } from "../storage";
import { useHistory } from "react-router-dom";
import { PATHS } from "../constants";

export default function DrawerMenu() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  let history = useHistory();

  const logout = () => {
    TokenManager.clearTokenStorage();
    history.replace(PATHS.LANDING);
  };

  return (
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
  );
}
