import icon from './logo.svg';

export default {
  name: 'Github',
  icon,
  description: 'Where the world hosts its code',
  onConnect: () => console.log('Do Github login'),
  onDisconnect: () => console.log('Do Github logout')
};
