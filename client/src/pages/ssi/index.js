import { Box, Button, Image, Input, Link, SimpleGrid } from "@chakra-ui/core";
import React, { useState } from "react";
import { apiClient, triggerSideEffect } from "../../api";

export function Identity({ onError }) {
  const [credentials, setCredentials] = useState(null);

  const copyInvitation = () => {
    navigator.clipboard.writeText(credentials.invitation_url);
  };

  const requestCredentials = () =>
    triggerSideEffect({
      apiCall: () => apiClient.requestSSICredentials(),
      onSuccess: (data) => {
        console.log("requestCredentials data");
        console.log(data);
        setCredentials(data);
      },
      onError,
    });
  const RenderCredentials = () => {
    if (!credentials) return "";
    return (
      <Box
        size="sm"
        isplay="grid"
        gridGap={2}
        gridAutoFlow="row dense"
        mx="auto"
      >
        <Image
          width="200"
          src={`data:image/png;base64, ${credentials.qr_png}`}
        />
        <Link href={credentials.streetcred_url} isExternal>
          Open in a Trusted Digital Wallet
        </Link>
        <Input
          type="text"
          readonly="readonly"
          value={credentials.invitation_url}
        />
        <Button my={2} onClick={copyInvitation} variantColor="blue">
          Copy
        </Button>
      </Box>
    );
  };

  return (
    <SimpleGrid columns={1} spacing={10}>
      <Box mx="auto" width={["100%", 200]} py={6}>
        <Button onClick={requestCredentials} variantColor="blue">
          Request Credentials
        </Button>
      </Box>
      <RenderCredentials />
    </SimpleGrid>
  );
}
