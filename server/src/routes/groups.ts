import express from 'express'
import { getGroup, listGroups } from '../services/groups'

const router = express.Router()

router.get('/', async (req, res) => {
  try {
    const groups = await listGroups()
    return res.status(200).json(groups)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

router.get('/:id', async (req, res) => {
  try {
    const group = await getGroup(req.params.id)
    return res.status(200).json(group)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})


export default router