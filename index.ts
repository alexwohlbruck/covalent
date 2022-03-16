import dotenv from 'dotenv'
dotenv.config()
import express from 'express'
import expressWs from 'express-ws'
import cookieParser from 'cookie-parser'
import cors from 'cors'
import session from 'express-session'
import MongoStore from 'connect-mongo'
import passport from 'passport'
import path from 'path'
import history from 'connect-history-api-fallback'

import * as config from './server/config'
import './server/db' // Connect to database
import './server/models' // Register models

const PORT = process.env.PORT || 8080
const { app } = expressWs(express())

import routes from './server/routes'
import websockets from './server/websockets'

// Middleware
app.use(cookieParser())
app.use(cors({
  credentials: true,
  origin: config.clientUrl,
}))
app.use(express.json())
app.use(session({
  secret: config.sessionSecret,
  resave: false,
  saveUninitialized: false,
  store: MongoStore.create({
    mongoUrl: config.db.connectionString(),
  }),
}))
import './server/passport'
app.use(passport.initialize())
app.use(passport.session())
app.use(routes)
app.use(websockets)

// Serve static assets
app.use(history())
app.use(express.static(path.join(__dirname + '/client')))
app.get('*', (req, res) => {
  if (process.env.NODE_ENV === 'production') {
    res.sendFile(path.resolve(__dirname, 'index.html'))
  }
  else {
    res.redirect('localhost:8080')
  }
})


app.listen(PORT, () => {
  console.log(`listening on port ${PORT}`)
})
