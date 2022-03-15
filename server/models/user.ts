import { Schema, model } from 'mongoose'
import findOrCreate from 'mongoose-findorcreate'

export interface User {
  _id: string,
  googleId: string;
  name: string;
  familyName: string;
  givenName: string;
  email?: string;
  picture?: string;
}

const UserSchema = new Schema<User>({
  googleId:   { type: String, required: true },
  name:       { type: String, required: true },
  familyName: { type: String, required: true },
  givenName:  { type: String, required: true },
  email:      { type: String, required: true },
  picture:    { type: String, required: true },
}, {
  timestamps: true,
})

UserSchema.plugin(findOrCreate)

export const UserModel = model<User>('User', UserSchema)
