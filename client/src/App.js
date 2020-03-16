import React, { useState, useEffect } from 'react';
import { useDisclosure, Button } from '@chakra-ui/core';

import Modal from './components/Modal';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';

export default () => {
  const loginDisclosure = useDisclosure();
  const signupDisclosure = useDisclosure();

  const [currentUser, setCurrentUser] = useState(null);

  const getCurrentUser = () => {
    console.log('Checking if a user is logged in');

    const localToken = localStorage.getItem('token');

    // TODO: Make fetch() request here to get user information

    if (localToken) setCurrentUser(localToken);
  };

  const signup = ({ email, password }) => {
    console.log('Do signup', email, password);

    // TODO: Make fetch() request here to signup

    signupDisclosure.onClose();
    loginDisclosure.onOpen();
  };

  const login = ({ email, password }) => {
    console.log('Do login', email, password);

    // TODO: Make fetch() request here to login

    localStorage.setItem('token', 'my-special-auth-token');

    loginDisclosure.onClose();
  };

  useEffect(getCurrentUser, []);

  console.log('Current user', currentUser);

  return (
    <div>
      {!currentUser && (
        <>
          <Button onClick={loginDisclosure.onOpen}>Open Login</Button>
          <Button onClick={signupDisclosure.onOpen}>Open Signup</Button>
          <Modal {...loginDisclosure} title="Login" onSubmit={login}>
            <LoginForm />
          </Modal>
          <Modal {...signupDisclosure} title="Signup" onSubmit={signup}>
            <SignupForm />
          </Modal>
        </>
      )}
      {currentUser && <div>ALL MY SERVICES</div>}
    </div>
  );
};
