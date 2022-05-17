import { Schema, model } from 'mongoose'
import { Lamp } from './lamp'

export interface GroupState {
  colors: string[]
  active: boolean
}

export interface Group {
  _id: string
  groupId: string
  accessCode: string
  state: GroupState
  lamps?: Lamp[]
}

const GroupSchema = new Schema<Group>({
  groupId:    { type: String, required: true },
  accessCode: { type: String, required: true },
  state: {
    colors:   { type: [String], default: ['#ff0000'] },
    active:   { type: Boolean, default: false },
  },
}, {
  timestamps: true,
})

export const GroupModel = model<Group>('Group', GroupSchema)
