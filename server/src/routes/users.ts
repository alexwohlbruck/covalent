import express from 'express'
import { isAuthenticated } from '../middleware'
import { UserModel } from '../models/user'

const router = express.Router()

router.get('/', isAuthenticated, async (req, res) => {
  const users = await UserModel.find()

  try {
    res.send(users)
  }
  catch (err) {
    res.status(500).send(err)
  }
})

export default router
