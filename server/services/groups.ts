import { Lamp, LampModel, LampState } from '../models/lamp'
import { Types } from 'mongoose'
import { RequestException } from '../routes'
import { getLamps } from './lamps'
import { GroupModel } from '../models/group'
import { convertToDotNotation } from '../helpers'

// List a user's groups
export const listGroups = async (userId: string, includeLamps = false) => {
  const lamps = await LampModel.find({
    user: new Types.ObjectId(userId)
  })

  // Convert to plain JSON in order to append lamps results
  const groups = JSON.parse(JSON.stringify(
    lamps.map((lamp: Lamp) => lamp.group)
  ))

  if (includeLamps) {
    for (const group of groups) {
      group.lamps = await getLamps({
        groupId: group._id.toString(),
        autopopulate: false,
      })
    }
  }

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
export const updateGroupState = async (groupId: string, lampId: string, state: LampState) => {

  const lamp = await LampModel.findByIdAndUpdate(lampId, {
    $set: convertToDotNotation(state, {}, 'state.'),
  })

  if (!lamp) throw new RequestException(404, `Lamp id: ${lampId} not found.`)

  // Get lamps in the same group
  const lamps = await getLamps({ groupId })

  let active = true

  // Find colors of lamps that are active
  const colors = lamps
    .filter((l: Lamp) => {
      return l.state.touching
    })
    .map((l: Lamp) => {
      return l.state.color
    })

  if (colors.length === 0) active = false

  const query: any = {
    'state.active': active,
  }
  if (active) {
    query['state.colors'] = colors
  }

  const updated = await GroupModel.findByIdAndUpdate(groupId, {
    $set: query
  }, {
    new: true,
  })

  return updated.state
}