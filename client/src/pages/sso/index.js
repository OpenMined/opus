import { SimpleGrid } from "@chakra-ui/core";
import Service from "./Service";
import xss from "xss";
import React, { useEffect, useState } from "react";
import { TokenManager } from "../../storage";
import { apiClient, triggerSideEffect } from "../../api";
import services from "./providers";
import { useLocation } from "react-router-dom";

export function Services({ onError }) {
  const [currentServices, setCurrentServices] = useState([]);
  let location = useLocation();

  const prepServices = () =>
    services.map((s) => {
      s.isConnected = false;
      return s;
    });

  const displayErrorIfPresent = () => {
    const error = new URLSearchParams(location.search).get("error");
    if (error) {
      onError({ message: xss(error.replace(/"+/g, "").replace(/'+/g, "")) });
    }
  };

  const onLoad = async () => {
    await getUserServices();
    await displayErrorIfPresent();
  };

  const getUserServices = async () => {
    if (!TokenManager.isAuthenticated()) {
      setCurrentServices(prepServices());
      return;
    }

    let providers =
      (await triggerSideEffect({
        apiCall: () => apiClient.providers(),
        onError,
      })) || [];
    setCurrentServices(
      services.map((s) => {
        s.isConnected = providers.includes(s.name.toLowerCase());
        return s;
      })
    );
  };

  useEffect(() => {
    onLoad();
  }, []);

  return (
    <SimpleGrid columns={[1, null, 2, 3]} spacing={[3, null, 5]}>
      {currentServices.map((service) => (
        <Service
          {...service}
          key={service.name}
          onDisconnect={() =>
            service.onDisconnect(() => getUserServices(), onError)
          }
        />
      ))}
    </SimpleGrid>
  );
}
