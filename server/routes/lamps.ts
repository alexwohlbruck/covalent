import express from 'express'
import { User } from '../models/user'
import {
  getLamps,
  getLamp,
  getLampConfig,
  updateLampConfig,
  createLamp,
  moveLampToGroup,
  sendCommand,
  deleteLamp,
  renameLamp,
} from '../services/lamps'
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
  const { name, groupId, deviceData, accessCode } = req.body

  const lamp = await createLamp(
    (req.user as User)._id,
    name,
    groupId,
    deviceData,
    accessCode,
  )

  return res.status(200).json(lamp)
})

router.get('/:id/config', isAuthenticated, async (req, res) => {
  const config = await getLampConfig(req.params.id)
  // const config = {"deviceId":"4091519b56b8","readingLightColorTemperature":2001,"nightMode":false,"minimumLightLevel":0.8,"wifi":[{"ssid":"asu-visitor","password":""}],"brightness":0.5,"lampId":"626df507d6756882f166942c"}
  return res.status(200).json(config)
})

router.patch('/:id/config', isAuthenticated, async (req, res) => {
  // TODO: Wait for successful response using pEvent
  updateLampConfig(req.params.id, req.body)
  const config = await getLampConfig(req.params.id)
  res.status(200).json(config)
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

router.put('/:id/name', isAuthenticated, async (req, res) => {
  const { name } = req.body

  const lamp = await renameLamp(
    (req.user as User)._id,
    req.params.id,
    name,
  )

  return res.status(200).json(lamp)
})

// Send a command to lamp
router.patch('/:id/state', isAuthenticated, async (req, res) => {
  const lamp = await sendCommand(
    // (req.user as User)._id,
    req.params.id,
    req.body
  )
  return res.status(200).json(lamp)
})

// Delete a lamp
router.delete('/:id', isAuthenticated, async (req, res) => {
  await await deleteLamp(req.params.id)
  return res.status(200).send()
})

export default router