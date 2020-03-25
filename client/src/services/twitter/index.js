import icon from "./logo.svg";

export default {
  name: "Twitter",
  icon,
  description: "Where the world has conversations.",
  onConnect: () => console.log("Do Twitter login"),
  onDisconnect: () => console.log("Do Twitter logout"),
};
