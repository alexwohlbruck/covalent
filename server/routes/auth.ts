import express from 'express'
import passport from 'passport'

const router = express.Router()

router.get('/me', (req, res) => {
  if (!req.user) {
    return res.status(204).send()
  }
  return res.status(200).json(req.user)
})

router.post('/login',
  passport.authenticate('google-id-token'),
  (req, res) => {
    return res.status(req.user ? 200 : 401).json(req.user)
  }
)

router.post('/logout', (req, res) => {
  req.logout()
  req.session.destroy(() => {
    res.status(200).send()
  })
})


export default router
