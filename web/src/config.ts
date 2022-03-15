export const backendUrl = process.env.NODE_ENV === 'production'
  ? 'https://project-covalent.herokuapp.com'
  : 'http://192.168.86.34:3000'