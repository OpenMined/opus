import icon from "./logo.svg";

export default {
  name: "Github",
  icon,
  description: "Where the world hosts its code",
  onConnect: () => {
    const url = `${process.env.BASE_URL || "http://localhost:5000"}/sso/github`;
    window.location.replace(url);
  },
  onDisconnect: () => console.log("Do Github logout"),
};
