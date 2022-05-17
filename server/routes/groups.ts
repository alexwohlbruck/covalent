import express from 'express'
import { User } from '../models/user'
import { isAuthenticated } from '../middleware'
import { getGroup, listGroups } from '../services/groups'

const router = express.Router()

// Get current user's groups
router.get('/me', isAuthenticated, async (req, res) => {
  try {
    const groups = await listGroups((req.user as User)._id, true)
    return res.status(200).json(groups)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

// Get a group
router.get('/:id', isAuthenticated, async (req, res) => {
  try {
    const group = await getGroup((req.user as User)._id, req.params.id)
    return res.status(200).json(group)
  }
  catch (err) {
    console.error(err)
    return res.status(500).json({ message: err.message })
  }
})

export default router