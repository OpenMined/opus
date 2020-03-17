import React from 'react';
import { Heading, Image, Text, Button, Flex } from '@chakra-ui/core';

export default ({
  name,
  icon,
  description,
  onConnect,
  onDisconnect,
  isConnected,
  onToggle
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

        // TODO: Maybe only fire onToggle() as the result of a promise?
        onToggle(name);
      }}
      variantColor={isConnected ? 'red' : 'blue'}
    >
      {isConnected ? `Disconnect to ${name}` : `Connect from ${name}`}
    </Button>
  </Flex>
);
