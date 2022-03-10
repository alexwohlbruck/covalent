import express from 'express'
import { User } from '../models/user'
import { getLamps, getLamp, createLamp, moveLampToGroup, sendCommand, deleteLamp } from '../services/lamps'
import { isAuthenticated } from '../middleware'

const router = express.Router()

// Get the current user's lamps
router.get('/me', isAuthenticated, async (req, res) => {
  const lamps = await getLamps({
    userId: (req.user as User)._id,
  })
  return res.status(200).json(lamps)
})

// Get a lamp
router.get('/:id', isAuthenticated, async (req, res) => {

  // TODO: Ensure the user owns the lamp

  const lamp = await getLamp(req.params.id)
  return res.status(200).json(lamp)
})

// Create a lamp
router.post('/', isAuthenticated, async (req, res) => {
  const { groupId, deviceData, accessCode } = req.body

  const lamp = await createLamp(
    (req.user as User)._id,
    groupId,
    deviceData,
    accessCode,
  )

  return res.status(200).json(lamp)
})

// Move a lamp to another group
router.put('/:id/group', isAuthenticated, async (req, res) => {
  const { groupId, accessCode } = req.body

  const lamp = await moveLampToGroup(
    req.params.id,
    groupId,
    accessCode,
  )

  return res.status(200).json(lamp)
})

// Send a command to lamp
router.patch('/:id/state', isAuthenticated, async (req, res) => {
  const lamp = await sendCommand(req.params.id, req.body)
  return res.status(200).json(lamp)
})

// Delete a lamp
router.delete('/:id', isAuthenticated, async (req, res) => {
  await await deleteLamp(req.params.id)
  return res.status(200).send()
})

export default router