import 'express-async-errors'
import express from 'express'
import users from './users'
import auth from './auth'
import lamps from './lamps'
import groups from './groups'

export class RequestException extends Error {
  statusCode: number

  constructor(statusCode: number, message: string) {
    super(message)
    this.statusCode = statusCode
  }
}

const router = express.Router()

router.use('/users', users)
router.use('/auth', auth)
router.use('/lamps', lamps)
router.use('/groups', groups)

router.use((err: any, req: any, res: any, next: any) => {
  if (err instanceof RequestException) {
    return res.status(err.statusCode).json({ message: err.message })
  }
  return res.status(500).json({ message: err.message })
})

export default router