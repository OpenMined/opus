import React from "react";
import { useForm } from "react-hook-form";
import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
} from "@chakra-ui/core";

export default ({ onSubmit }) => {
  const { handleSubmit, errors, register, formState, watch } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormControl isInvalid={errors.email}>
        <FormLabel htmlFor="email">Email address</FormLabel>
        <Input
          name="email"
          placeholder="person@example.com"
          ref={register({
            required: "Email address is required",
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
              message: "Invalid email address",
            },
          })}
        />
        <FormErrorMessage>
          {errors.email && errors.email.message}
        </FormErrorMessage>
      </FormControl>
      <FormControl isInvalid={errors.password} mt={3}>
        <FormLabel htmlFor="password">Password</FormLabel>
        <Input
          name="password"
          type="password"
          placeholder="Password"
          ref={register({
            required: "Password is required",
            minLength: {
              value: 8,
              message: "Password must be at least 8 characters",
            },
          })}
        />
        <FormErrorMessage>
          {errors.password && errors.password.message}
        </FormErrorMessage>
      </FormControl>
      <FormControl isInvalid={errors.passwordMatch} mt={3}>
        <FormLabel htmlFor="passwordMatch">Password (again)</FormLabel>
        <Input
          name="passwordMatch"
          type="password"
          placeholder="Password"
          ref={register({
            required: "Password is required",
            validate: (val) =>
              val === watch("password") || "Passwords do not match",
          })}
        />
        <FormErrorMessage>
          {errors.passwordMatch && errors.passwordMatch.message}
        </FormErrorMessage>
      </FormControl>
      <Button
        mt={3}
        variantColor="blue"
        isLoading={formState.isSubmitting}
        type="submit"
      >
        Submit
      </Button>
    </form>
  );
};
