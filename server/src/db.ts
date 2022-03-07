
import mongoose, { ConnectOptions } from 'mongoose'
import { db as dbConfig } from './config'

console.log(dbConfig.connectionString())
mongoose.connect(dbConfig.connectionString(), {
  useNewUrlParser: true,
  useUnifiedTopology: true
} as ConnectOptions)

mongoose.connection.on('error', () => {
  console.error.bind(console, 'connection error:')
})

mongoose.connection.once('open', () => {
  console.log('connected to database')
})

export default mongoose.connection