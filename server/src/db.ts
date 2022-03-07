
import mongoose, { ConnectOptions } from 'mongoose'
import { db as dbConfig } from './config'

mongoose.connect(dbConfig.connectionString(), {
  useNewUrlParser: true,
  useUnifiedTopology: true
} as ConnectOptions)

const db = mongoose.connection
db.on('error', console.error.bind(console, 'connection error:'))
db.once('open', () => {
  console.log('connected to database')
})
