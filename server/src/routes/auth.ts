import express from 'express'
import passport from 'passport'

const router = express.Router()

router.get('/me', (req, res) => {
  console.log(req.user)
  return res.status(req.user ? 200 : 401).json(req.user)
})

router.post('/login',
  passport.authenticate('google-id-token'),
  (req, res) => {
    return res.status(req.user ? 200 : 401).json(req.user)
  }
)

router.post('/logout', (req, res, next) => {
  req.logout()
  req.session.destroy(() => {
    res.status(200)
  })
})


export default router
