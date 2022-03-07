import dotenv from 'dotenv'
dotenv.config()
import express from 'express'
import expressWs from 'express-ws'

import routes from './routes'
import './db' // Connect to database

const PORT = 3000

const { app } = expressWs(express())

// Middleware
app.use(express.json())
app.use(routes)

app.listen(PORT, () => {
  console.log(`listening on port ${PORT}`)
})
