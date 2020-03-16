import React from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button
} from '@chakra-ui/core';

export default ({ isOpen, onClose, title, onSubmit, children }) => (
  <Modal isOpen={isOpen} onClose={onClose}>
    <ModalOverlay />
    <ModalContent>
      <ModalHeader>{title}</ModalHeader>
      <ModalCloseButton />
      <ModalBody>{children}</ModalBody>
      <ModalFooter>
        <Button variant="blue" onClick={onSubmit}>
          Submit
        </Button>
      </ModalFooter>
    </ModalContent>
  </Modal>
);
