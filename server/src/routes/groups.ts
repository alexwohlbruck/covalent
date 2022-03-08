import express from 'express'
import { Lamp, LampModel } from '../models/lamp'
import { Types } from 'mongoose'
import { User } from '../models/user'

const router = express.Router()

// Get a user's groups
router.get('/', async (req, res) => {
  try {
    const lamps = await LampModel.find({
      user: new Types.ObjectId((req.user as User)._id)
    })
    const groups = lamps.map((lamp: Lamp) => lamp.group)
    return res.status(200).json(groups)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

// Get a group
router.get('/:id', async (req, res) => {
  try {
    const lamp = await LampModel.findOne({
      user: new Types.ObjectId((req.user as User)._id),
      group: new Types.ObjectId(req.params.id)
    })

    if (lamp) {
      return res.status(200).json(lamp.group)
    }
    return res.status(404).json({ message: 'Group not found' })
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})


export default router