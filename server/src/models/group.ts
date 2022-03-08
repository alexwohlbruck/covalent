import { Schema, model } from 'mongoose'

export interface Group {
  _id: string;
  name: string;
  accessCode: string;
}

const GroupSchema = new Schema<Group>({
  name: {
    type: String,
    required: true,
  },
  accessCode: {
    type: String,
    required: true,
  },
}, {
  timestamps: true,
})

export const GroupModel = model<Group>('Group', GroupSchema)
