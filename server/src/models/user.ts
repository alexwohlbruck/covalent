import { Schema, model } from 'mongoose'

export interface User {
  name: string;
  email?: string;
  photo?: string;
}

const UserSchema = new Schema<User>({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: false,
  },
  photo: {
    type: String,
    required: false,
  },
}, {
  timestamps: true,
})

export const UserModel = model<User>('User', UserSchema)
