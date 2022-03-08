import { Schema, model } from 'mongoose'

export interface Group {
  _id: string;
  groupId: string;
  accessCode: string;
}

const GroupSchema = new Schema<Group>({
  groupId: {
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
