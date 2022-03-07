import express from 'express'
import { User } from '../models'

const router = express.Router()

router.get('/', async (req, res) => {
  const users = await User.find()

  try {
    res.send(users)
  }
  catch (err) {
    res.status(500).send(err)
  }
})

export default router