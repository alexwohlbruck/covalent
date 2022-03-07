import express from 'express'
import { google } from '../config'
import { OAuth2Client } from 'google-auth-library'

const router = express.Router()
const client = new OAuth2Client(google.clientId)

router.post('/login', async (req, res) => {
  try {
    const ticket = await client.verifyIdToken({
      idToken: req.body.idToken,
      audience: google.clientId,
    })
    const payload = ticket.getPayload()
    const userid = payload.sub

    res.status(200).json(payload)
  }
  catch (error) {
    console.error(error)
    res.status(500).json({ message: error.message, error })
  }
})

export default router
