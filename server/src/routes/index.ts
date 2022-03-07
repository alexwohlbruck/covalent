import express from 'express'
import users from './users'
import lamps from './lamps'
import groups from './groups'

const router = express.Router()

router.use('/users', users)
router.use('/lamps', lamps)
router.use('/groups', groups)

export default router