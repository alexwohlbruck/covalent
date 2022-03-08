import express from 'express'
import { convertToDotNotation } from '../helpers'
import { LampModel } from '../models/lamp'
import { User } from '../models/user'
import { getLamps, getLamp, createLamp, moveLampToGroup, sendCommand, deleteLamp } from '../services/lamps'

const router = express.Router()

// Get the current user's lamps
router.get('/', async (req, res) => {
  const lamps = await getLamps({
    userId: (req.user as User)._id,
  })
  return res.status(200).json(lamps)
})

// Get a lamp
router.get('/:id', async (req, res) => {
  const lamp = await getLamp(req.params.id)
  return res.status(200).json(lamp)
})

// Create a lamp
router.post('/', async (req, res) => {
  const lamp = await createLamp(req.body)
  return res.status(200).json(lamp)
})

// Move a lamp to another group
router.put('/:id/group', async (req, res) => {
  const lamp = moveLampToGroup(req.params.id, req.body.groupId)
  return res.status(200).json(lamp)
})

// Send a command to lamp
router.patch('/:id/state', async (req, res) => {
  const lamp = sendCommand(req.params.id, req.body)
  return res.status(200).json(lamp)
})

// Delete a lamp
router.delete('/:id', async (req, res) => {
  await deleteLamp(req.params.id)
  return res.status(200).send()
})

export default router