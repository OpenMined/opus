import icon from "./logo.svg";

export default {
  name: "Reddit",
  icon,
  description: "Where the world has conversations about esoteric stuff",
  onConnect: () => console.log("Do Reddit login"),
  onDisconnect: () => console.log("Do Reddit logout"),
};
