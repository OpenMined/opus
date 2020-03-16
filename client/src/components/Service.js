import React from 'react';
import { Box, Heading, Text, Button } from '@chakra-ui/core';

export default ({ name, description, onClick }) => (
  <Box>
    <Heading>{name}</Heading>
    <Text>{description}</Text>
    <Button onClick={onClick}>Connect to {name}</Button>
  </Box>
);
