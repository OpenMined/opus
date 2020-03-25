import icon from "./logo.svg";

export default {
  name: "Apple",
  icon,
  description: "Maker of the world's best computers",
  onConnect: () => console.log("Do Apple login"),
  onDisconnect: () => console.log("Do Apple logout"),
};
