export const backendUrl = process.env.NODE_ENV === 'production'
  ? process.env.VUE_APP_BACKEND_URL || 'https://project-covalent.herokuapp.com'
  : 'http://localhost:3000'