import { Lamp } from './Lamp'

export interface GroupState {
  colors: string[]
  active: boolean
}

export interface Group {
  _id: string
  groupId: string
  accessCode: string
  state: GroupState,
  lamps?: Lamp[],
  lampIds?: string[],
}