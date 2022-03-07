import express from 'express'
import users from './users'
import auth from './auth'
import lamps from './lamps'
import groups from './groups'

const router = express.Router()

router.use('/users', users)
router.use('/auth', auth)
router.use('/lamps', lamps)
router.use('/groups', groups)

export default router