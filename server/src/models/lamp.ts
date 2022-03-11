// import { ObjectID } from 'mongodb'
import autopopulate from 'mongoose-autopopulate'
import { Schema, model, PopulatedDoc } from 'mongoose'
import { Group } from './group'
import { User } from './user'

export interface LampState {
  color: string
  touching: boolean
}

export interface Lamp {
  _id: string
  state: LampState
  group: Group
  user: User
  deviceData: any
}

const LampSchema = new Schema<Lamp>({
  state: {
    color: {
      type: String,
      required: true,
    },
    touching: {
      type: Boolean,
      required: true,
    },
  },
  group: {
    type: Schema.Types.ObjectId,
    ref: 'Group',
    required: true,
    autopopulate: true,
  },
  user: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    autopopulate: true,
  },
  deviceData: {
    type: Object,
  },
}, {
  timestamps: true,
})

LampSchema.plugin(autopopulate)

export const LampModel = model<Lamp>('Lamp', LampSchema)
