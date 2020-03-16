import React from 'react';
import { useForm } from 'react-hook-form';
import {
  FormErrorMessage,
  FormLabel,
  FormControl,
  Input,
  Button
} from '@chakra-ui/core';

export default function HookForm() {
  const { handleSubmit, errors, register, formState } = useForm();

  function validateName(value) {
    let error;
    if (!value) {
      error = 'Name is required';
    } else if (value !== 'Naruto') {
      error = "Jeez! You're not a fan 😱";
    }
    return error || true;
  }

  function onSubmit(values) {
    setTimeout(() => {
      alert(JSON.stringify(values, null, 2));
    }, 1000);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormControl isInvalid={errors.name}>
        <FormLabel htmlFor="name">First name</FormLabel>
        <Input
          name="name"
          placeholder="name"
          ref={register({ validate: validateName })}
        />
        <FormErrorMessage>
          {errors.name && errors.name.message}
        </FormErrorMessage>
      </FormControl>
      <Button
        mt={4}
        variantColor="teal"
        isLoading={formState.isSubmitting}
        type="submit"
      >
        Submit
      </Button>
    </form>
  );
}
