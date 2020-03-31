import icon from "./logo.svg";

export default {
  name: "Chase",
  icon,
  description: "A major banking network",
  onConnect: () => console.log("Do Chase login"),
  onDisconnect: () => console.log("Do Chase logout"),
};
