import { Types } from 'mongoose'
import { RequestException } from '../routes'
import { convertToDotNotation, toKebab } from '../helpers'
import { Lamp, LampModel, LampState } from '../models/lamp'
import { GroupModel } from '../models/group'

export const getLamps = async (options: {
  userId?: string;
}) => {
  const query: any = {}

  if (options) {
    if (options.userId) query.user = new Types.ObjectId(options.userId)
  }

  return await LampModel.find(query)
}

export const getLamp = async (id: string) => {
  const lamp = await LampModel.findById(id)
  if (!lamp) throw new RequestException(404, `Lamp id: ${id} not found.`)
  return lamp
}

export const createLamp = async (
  userId: string,
  groupId: string,
  deviceData: any,
  accessCode?: string
) => {

  // TODO: Require group ID and access code and add the lamp to the group
  if (!groupId) throw new RequestException(400, 'Group ID is required.')
  if (!deviceData) throw new RequestException(400, 'Device data is required.')

  // We either create a new group or add the lamp to an existing group
  // This boolean tracks whether we are creating a new group or not
  const creatingGroup = accessCode ? false : true

  // Convert group ID to kebab case
  groupId = toKebab(groupId)

  let group = await GroupModel.findOne({
    groupId,
  })
  const groupExists = !!group

  // Creating a group that exists
  if (creatingGroup && groupExists) {
    throw new RequestException(400, 'Group already exists.')
  }

  // Joining a group that doesn't exist
  if (!creatingGroup && !groupExists) {
    throw new RequestException(400, 'Group does not exist.')
  }

  if (groupExists && group.accessCode !== accessCode) {
    throw new RequestException(400, 'Access code is incorrect.')
  }

  if (!groupExists) {
    const newAccessCode = Math.floor(Math.random() * 1000000).toString()
    const newGroup = new GroupModel({
      groupId,
      accessCode: newAccessCode,
    })
    group = await newGroup.save()
  }

  const lamp = new LampModel({
    state: {
      color: '#ff0000',
      touching: false,
    },
    group: new Types.ObjectId(group._id),
    user: new Types.ObjectId(userId),
  })

  await lamp.save()

  // Get populated lamp
  return LampModel.findById(lamp._id)
}

export const moveLampToGroup = async (id: string, groupId: string, accessCode: string) => {

  if (!id) throw new RequestException(400, 'Lamp ID is required.')
  if (!groupId) throw new RequestException(400, 'Group ID is required.')
  if (!accessCode) throw new RequestException(400, 'Access code is required.')

  const lamp: any = await LampModel.findById(id)
  if (!lamp) throw new RequestException(404, `Lamp id: ${id} not found.`)

  const group = await GroupModel.findOne({
    groupId,
  })
  if (!group) throw new RequestException(404, `Group id: ${groupId} not found.`)

  // Check new group access code
  if (accessCode !== group.accessCode) {
    throw new RequestException(400, 'Access code is incorrect.')
  }

  return await LampModel.findByIdAndUpdate(id, { group: group._id }, { new: true })
}

export const sendCommand = async (id: string, state: LampState) => {
  return await LampModel.findByIdAndUpdate(id, {
    $set: convertToDotNotation({
      state,
    }),
  }, {
    new: true,
  })
}

export const deleteLamp = async (id: string) => {

  const lamp = await LampModel.findById(id)

  if (!lamp) throw new RequestException(404, `Lamp id: ${id} not found.`)

  // Get lamps that are in the same group
  const lamps = await LampModel.find({
    group: new Types.ObjectId(lamp.group._id),
  })

  // If there are no other lamps in the group, delete the group
  if (lamps.length === 1) {
    await GroupModel.findByIdAndDelete(lamp.group._id)
  }

  return await LampModel.findByIdAndRemove(id)
}