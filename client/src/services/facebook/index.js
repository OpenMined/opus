import icon from './logo.svg';

export default {
  name: 'Facebook',
  icon,
  description: 'The most popular social media networking website in the world.',
  onConnect: () => console.log('Do Facebook login'),
  onDisconnect: () => console.log('Do Facebook logout')
};
