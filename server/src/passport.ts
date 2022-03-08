import passport from 'passport'
import GoogleTokenStrategy from 'passport-google-id-token'
import { google } from './config'
import { User, UserModel } from './models/user'

passport.serializeUser((user: User, done: any) => {
  console.log('serialize', user._id.toString())
  done(null, user._id)
})

passport.deserializeUser(async (id: string, done: any) => {
  console.log('deserialize', id)
  try {
    const user = await UserModel.findById(id)
    done(null, user)
  }
  catch (err) {
    done(err)
  }
})

passport.use(new GoogleTokenStrategy(
  {
    clientID: google.clientId,
  },
  async (parsedToken: any, googleId: string, done: any) => {
    try {
      const { doc: user } = await (UserModel as any).findOrCreate({
        googleId,
        ...parsedToken.payload
      })
      return done(null, user)
    }
    catch (err) {
      return done(err)
    }
  }
))