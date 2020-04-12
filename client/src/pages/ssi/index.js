import { Box, Button, SimpleGrid } from "@chakra-ui/core";
import React from "react";

export function Identity() {
  return (
    <>
      <Box mx="auto" width={["100%", 200]} py={6}>
        <Button>Logout</Button>
      </Box>
      <SimpleGrid columns={[1, null, 2, 3]} spacing={[3, null, 5]}>
        <p>Blah</p>
      </SimpleGrid>
    </>
  );
}
