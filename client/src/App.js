import React, { useState, useEffect } from 'react';
import { useDisclosure, Button, Stack, Box, SimpleGrid } from '@chakra-ui/core';

import services from './services';

import Modal from './components/Modal';
import SignupForm from './components/SignupForm';
import LoginForm from './components/LoginForm';
import Service from './components/Service';

export default () => {
  const signupDisclosure = useDisclosure();
  const loginDisclosure = useDisclosure();

  const prepServices = () =>
    services.map(s => {
      s.isConnected = false;
      return s;
    });

  const [currentUser, setCurrentUser] = useState(null);
  const [currentServices, setCurrentServices] = useState(null);

  const getCurrentUser = () => {
    console.log('Checking if a user is logged in');

    const localToken = JSON.parse(localStorage.getItem('token'));

    // TODO: Make fetch() request here to get user information
    // TODO: Make fetch() request here to get existing services

    if (localToken) {
      setCurrentUser(localToken.token);
      setCurrentServices(
        services.map(s => {
          if (localToken.services.includes(s.name)) s.isConnected = true;
          return s;
        })
      );
    } else {
      setCurrentUser(null);
      setCurrentServices(prepServices());
    }
  };

  const signup = values => {
    console.log('Do signup', values);

    signupDisclosure.onClose();

    // TODO: Make fetch() request here to signup
    fetch('http://localhost:5000/signup', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify(values)
    })
    .then(function (data) {
      console.log('Request succeeded with JSON response', data);
      loginDisclosure.onOpen();
    })
    .catch(function (error) {
      console.log('Request failed', error);
    });  
  };

  const login = values => {
    console.log('Do login', values);

    // TODO: Make fetch() request here to login
    fetch('http://localhost:5000/login', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify(values)
    })
    .then(function (data) {
      console.log('Request succeeded with JSON response', data);
    })
    .catch(function (error) {
      console.log('Request failed', error);
    });  

    localStorage.setItem(
      'token',
      JSON.stringify({
        token: 'my-special-auth-token',
        services: ['Facebook', 'Github']
      })
    );
    getCurrentUser();

    loginDisclosure.onClose();
  };

  const logout = () => {
    console.log('Do logout');

    localStorage.removeItem('token');
    getCurrentUser();
  };

  const toggleServiceConnection = name => {
    console.log('Toggling service', name);

    const token = JSON.parse(localStorage.getItem('token'));
    const tokenServiceIndex = token.services.indexOf(name);

    if (tokenServiceIndex === -1) token.services.push(name);
    else token.services.splice(tokenServiceIndex, 1);

    localStorage.setItem('token', JSON.stringify(token));

    const newServices = currentServices.map(s => {
      if (s.name === name) s.isConnected = !s.isConnected;
      return s;
    });

    setCurrentServices(newServices);
  };

  useEffect(getCurrentUser, []);

  return (
    <Box mx="auto" width={['100%', null, 720, 960, 1200]} px={3} pb={6}>
      {!currentUser && (
        <>
          <Box mx="auto" width={['100%', 200]} py={6}>
            <Stack spacing={4}>
              <Button variantColor="blue" onClick={signupDisclosure.onOpen}>
                Signup
              </Button>
              <Button variantColor="blue" onClick={loginDisclosure.onOpen}>
                Login
              </Button>
            </Stack>
          </Box>
          <Modal {...signupDisclosure} title="Signup">
            <SignupForm onSubmit={signup} />
          </Modal>
          <Modal {...loginDisclosure} title="Login">
            <LoginForm onSubmit={login} />
          </Modal>
        </>
      )}
      {currentUser && (
        <>
          <Box mx="auto" width={['100%', 200]} py={6}>
            <Button onClick={logout}>Logout</Button>
          </Box>
          <SimpleGrid columns={[1, null, 2, 3]} spacing={[3, null, 5]}>
            {currentServices.map(service => (
              <Service
                key={service.name}
                onToggle={toggleServiceConnection}
                {...service}
              />
            ))}
          </SimpleGrid>
        </>
      )}
    </Box>
  );
};
