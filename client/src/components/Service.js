import React from "react";
import { Heading, Image, Text, Button, Flex } from "@chakra-ui/core";

export default ({
  name,
  icon,
  description,
  onConnect,
  onDisconnect,
  isConnected,
}) => (
  <Flex
    flexDirection="column"
    p={4}
    backgroundColor="gray.50"
    borderRadius="md"
    boxShadow="sm"
  >
    <Flex alignItems="center">
      <Image src={icon} alt={name} size="36px" objectFit="contain" />
      <Heading as="h3" size="lg" ml={3}>
        {name}
      </Heading>
    </Flex>
    <Text color="gray.500" my={3}>
      {description}
    </Text>
    <Button
      mt="auto"
      alignSelf="flex-start"
      onClick={() => {
        if (isConnected) onDisconnect();
        else onConnect();
      }}
      variantColor={isConnected ? "red" : "blue"}
    >
      {isConnected ? `Disconnect from ${name}` : `Connect to ${name}`}
    </Button>
  </Flex>
);
