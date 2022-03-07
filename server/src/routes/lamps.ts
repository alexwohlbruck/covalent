import express from 'express'
import { changeGroup, createLamp, deleteLamp, getLamp, getMyLamps, sendCommand } from '../services/lamps'

const router = express.Router()

// TODO: Validate input against mongoose models. If invalid, return 4XX

router.get('/', async (req, res) => {
  try {
    const lamps = await getMyLamps()
    return res.status(200).json(lamps)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.get('/:id', async (req, res) => {
  try {
    const lamp = await getLamp(req.params.id)
    return res.status(200).json(lamp)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.post('/', async (req, res) => {
  try {
    const lamp = await createLamp(req.body)
    return res.status(200).json(lamp)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.put('/:id/group', async (req, res) => {
  try {
    const lamp = await changeGroup(req.params.id, req.body.groupId)
    return res.status(200).json(lamp)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.patch('/:id/state', async (req, res) => {
  try {
    const lamp = await sendCommand(req.params.id, req.body)
    return res.status(200).json(lamp)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.delete('/:id', async (req, res) => {
  try {
    const lamp = await deleteLamp(req.params.id)
    return res.status(200).json(lamp)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

export default router