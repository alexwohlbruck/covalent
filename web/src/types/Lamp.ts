import { Group } from './Group'
import { User } from './User'

export interface LampState {
  color: string;
  touching: boolean;
}

export interface Lamp {
  _id: string;
  state: LampState;
  group: Group;
  user: User;
  deviceData: any;
}