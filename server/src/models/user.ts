import { Schema, model } from 'mongoose'
import findOrCreate from 'mongoose-findorcreate'

export interface User {
  _id: string | Schema.Types.ObjectId,
  googleId: string;
  name: string;
  email?: string;
  picture?: string;
}

const UserSchema = new Schema<User>({
  googleId: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: false,
  },
  picture: {
    type: String,
    required: false,
  },
}, {
  timestamps: true,
})

UserSchema.plugin(findOrCreate)

export const UserModel = model<User>('User', UserSchema)
