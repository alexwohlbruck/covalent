import { Group } from './Group'
import { User } from './User'

export interface LampState {
  color: string;
  touching: boolean;
}

export interface Lamp {
  _id: string;
  name: string;
  state: LampState;
  group?: Group;
  groupId?: string;
  user?: User;
  userId?: string;
  deviceData: any;
}