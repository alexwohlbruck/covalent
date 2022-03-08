import dotenv from 'dotenv'
dotenv.config()
import express from 'express'
import expressWs from 'express-ws'
import cookieParser from 'cookie-parser'
import cors from 'cors'
import session from 'express-session'
import MongoStore from 'connect-mongo'
import passport from 'passport'

import * as config from './config'
import './db' // Connect to database
import './models' // Register models

const PORT = 3000
const { app } = expressWs(express())

import routes from './routes'
import websockets from './websockets'

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
import './passport'
app.use(passport.initialize())
app.use(passport.session())
app.use(routes)
app.use(websockets)


app.listen(PORT, () => {
  console.log(`listening on port ${PORT}`)
})
