import dotenv from 'dotenv'
dotenv.config()
import express from 'express'
import expressWs from 'express-ws'

import './db' // Connect to database
import './models' // Register models

const PORT = 3000
const { app } = expressWs(express())

import routes from './routes'
import websockets from './websockets'

// Middleware

app.use(express.json())
app.use(routes)
app.use(websockets)

app.listen(PORT, () => {
  console.log(`listening on port ${PORT}`)
})
