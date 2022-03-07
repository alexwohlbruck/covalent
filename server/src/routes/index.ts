import express from 'express'
import users from './users'

const router = express.Router()

router.get('', (req, res) => {
  res.json({
    message: 'Hello World!'
  })
})

router.use('/users', users)

export default router