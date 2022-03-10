import { GroupModel } from '../models/group'
import { Lamp, LampModel } from '../models/lamp'
import { Types } from 'mongoose'
import { RequestException } from '../routes'

// List a user's groups
export const listGroups = async (userId: string) => {
  const lamps = await LampModel.find({
    user: new Types.ObjectId(userId)
  })
  const groups = lamps.map((lamp: Lamp) => lamp.group)

  return groups
}

export const getGroup = async (userId: string, groupId: string) => {

  const myGroups = await listGroups(userId)
  const group = myGroups.find((g: any) => g._id.toString() === groupId)

  if (!group) throw new RequestException(404, `Group id: ${groupId} not found.`)

  return group
}