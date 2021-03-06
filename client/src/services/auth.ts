import axios from '@/axios'
import store from '@/store'
import router from '@/router'

declare global {
  interface Window { google: any }
}

window.onload = async () => {
  initializeGoogleOneTap()
  await getMe()
}

const initializeGoogleOneTap = () => {
  window.google.accounts.id.initialize({
    client_id: '1067362191574-44i4k8lk36kkub00gn77qiu8gff89c26.apps.googleusercontent.com',
    callback: handleCredentialResponse,
    auto_select: true,
  })
}

const promptGoogleOneTap = () => {
  window.google.accounts.id.prompt()
}

const handleCredentialResponse = (response: any) => {
  console.log("Encoded JWT ID token: " + response.credential)
  signIn(response.credential)
}

export const signIn = async (idToken: string) => {
  const { data: me } = await axios.post('/auth/login', {
    id_token: idToken,
  })
  store.commit('SET_ME', me)
  if (me) {
    router.push({ name: 'lamps' })
  }
}

export const signOut = async () => {
  await axios.post('/auth/logout')
  store.commit('RESET_STATE')
  router.push({ name: 'home' })
}

export const getMe = async () => {
  const { data: me } = await axios.get('/auth/me')
  store.commit('SET_ME', me)
  if (!me) {
    promptGoogleOneTap()
  }
}
