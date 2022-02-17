import firebase from 'firebase/compat/app'
import 'firebase/compat/database'
import 'firebase/compat/functions'
import 'firebase/compat/auth'

const firebaseConfig = {
  apiKey: 'AIzaSyANs8iuTczWuRX0aR_lb52qGBxw77y0RcM',
  authDomain: 'project-friendship-lamp.firebaseapp.com',
  databaseURL: 'https://project-friendship-lamp-default-rtdb.firebaseio.com',
  projectId: 'project-friendship-lamp',
  storageBucket: 'project-friendship-lamp.appspot.com',
  messagingSenderId: '1067362191574',
  appId: '1:1067362191574:web:af19ed4c90c81f52676177',
  measurementId: 'G-K3WMSLK7B5',
}

export const app = firebase.initializeApp(firebaseConfig)
export const functions = app.functions()
export const auth = app.auth()
// functions.useEmulator('localhost', 5001)
export const db = app.database()
