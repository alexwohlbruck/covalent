import firebase from 'firebase/compat/app'
import 'firebase/compat/database'
import 'firebase/compat/functions'
import 'firebase/compat/auth'

const firebaseConfig = {
  apiKey: 'AIzaSyDG6UdjzcKPb8AcKRM25eCESjZEIqm7fSg',
  authDomain: 'friendship-lamp-1ea8a.firebaseapp.com',
  databaseURL: 'https://friendship-lamp-1ea8a-default-rtdb.firebaseio.com',
  projectId: 'friendship-lamp-1ea8a',
  storageBucket: 'friendship-lamp-1ea8a.appspot.com',
  messagingSenderId: '821633514868',
  appId: '1:821633514868:web:03038031fb18f6b6db4021',
  measurementId: 'G-PK5MYM3RYT',
}

export const app = firebase.initializeApp(firebaseConfig)
export const functions = app.functions()
export const auth = app.auth()
// functions.useEmulator('localhost', 5001)
export const db = app.database()
