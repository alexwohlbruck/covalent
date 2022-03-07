// import { ObjectID } from 'mongodb'
import autopopulate from 'mongoose-autopopulate'
import { Schema, model, PopulatedDoc } from 'mongoose'
import { Group } from './group'
import { User } from './user'

export interface LampState {
  color: string;
  touching: boolean;
}

export interface Lamp {
  state: LampState,
  group: PopulatedDoc<Group>; // string | ObjectID | Group
  user: PopulatedDoc<User>; // string | ObjectID | User
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
}, {
  timestamps: true,
})

LampSchema.plugin(autopopulate)

export const LampModel = model<Lamp>('Lamp', LampSchema)
