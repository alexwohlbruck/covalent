import { Lamp, LampModel } from '../models/lamp'
import { Types } from 'mongoose'
import { RequestException } from '../routes'
import { getLamps } from './lamps'
import { GroupModel } from '../models/group'

// List a user's groups
export const listGroups = async (userId: string) => {
  const lamps = await LampModel.find({
    user: new Types.ObjectId(userId)
  })
  const groups = lamps.map((lamp: Lamp) => lamp.group)

  return groups
}

export const getLampsInGroup = async (groupId: string) => {
  return await LampModel
    .find({
      group: new Types.ObjectId(groupId),
    }, {}, {
      autopopulate: false,
    })
    .populate('user')
}

export const getGroup = async (userId: string, groupId: string) => {

  const [ myGroups, lamps ] = await Promise.all([
    listGroups(userId),
    getLampsInGroup(groupId),
  ])

  const group = myGroups.find((g: any) => g._id.toString() === groupId)

  if (!group) throw new RequestException(404, `Group id: ${groupId} not found.`)

  return {
    ...JSON.parse(JSON.stringify(group)),
    lamps,
  }
}

// Recompute the colors and active state on a group and save in DB
export const updateGroupState = async (groupId: string) => {

  // Get lamps in group
  const lamps = await getLamps({ groupId })

  let active = true

  // Find colors of lamps that are active
  let colors = lamps
    .filter((lamp: Lamp) => {
      return lamp.state.touching
    })
    .map((lamp: Lamp) => {
      return lamp.state.color
    })

  // If no colors are active, use the last color
  if (colors.length === 0) {
    const defaultColor = lamps[0].state.color || '#ff0000'
    console.log('defaultColor', defaultColor)
    colors = [defaultColor]
    active = false
  }

  const updated = await GroupModel.findByIdAndUpdate(groupId, {
    $set: {
      'state.colors': colors,
      'state.active': active,
    }
  }, {
    new: true,
  })

  return updated
}