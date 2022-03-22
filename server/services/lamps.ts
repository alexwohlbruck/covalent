import { Types } from 'mongoose'
import { RequestException } from '../routes'
import { toKebab } from '../helpers'
import { LampModel, LampState } from '../models/lamp'
import { GroupModel } from '../models/group'
import { updateGroupState } from './groups'
import { broadcast, broadcastToUsers } from '../websockets'

export const getLamps = async (options: {
  userId?: string;
  groupId?: string;
}) => {
  const query: any = {}

  if (options) {
    if (options.userId) query.user = new Types.ObjectId(options.userId)
    if (options.groupId) query.group = new Types.ObjectId(options.groupId)
  }

  return await LampModel.find(query).sort({ createdAt: -1 })
}

export const getLamp = async (id: string) => {
  const lamp = await LampModel.findById(id)
  if (!lamp) throw new RequestException(404, `Lamp id: ${id} not found.`)
  return lamp
}

export const createLamp = async (
  userId: string,
  name: string,
  groupId: string,
  deviceData: any,
  accessCode?: string
) => {

  // TODO: If a lamp with the existing device id exists, the user needs to relink the device
  // TODO: Delete the existing lamp and the group if it is the last lamp in the group

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
    const newAccessCode = String(Math.floor(Math.random() * 1000000).toFixed(0)).padStart(6, '0') // Generate 6 digit number string
    const newGroup = new GroupModel({
      groupId,
      accessCode: newAccessCode,
    })
    group = await newGroup.save()
  }

  const lamp = new LampModel({
    name,
    state: {
      color: '#ff0000',
      touching: false,
    },
    deviceData,
    group: new Types.ObjectId(group._id),
    user: new Types.ObjectId(userId),
  })

  await lamp.save()

  // Get populated lamp
  const res = await LampModel.findById(lamp._id)
  broadcastToUsers([userId], {
    name: 'ADD_LAMP',
    data: res,
  })

  return res
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

  const res = await LampModel.findByIdAndUpdate(id, { group: group._id }, { new: true })

  // TODO: Notify other users in group
  broadcastToUsers([lamp.user._id], {
    name: 'ADD_LAMP',
    data: res,
  })
  return res
}

export const renameLamp = async (userId: string, lampId: string, name: string) => {

  if (!name || !name.length) throw new RequestException(400, 'Name is required.')

  const lamp = await LampModel.findById(lampId)

  if (!lamp) throw new RequestException(404, `Lamp id: ${lampId} not found.`)
  if (lamp.user._id.toString() !== userId.toString())
    throw new RequestException(403, 'You do not own this lamp.')

  lamp.name = name

  await lamp.save()

  broadcastToUsers([userId], {
    name: 'ADD_LAMP',
    data: lamp,
  })

  return lamp
}

export const sendCommand = async (lampId: string, state: LampState) => {

  const lamp = await LampModel.findById(lampId)

  if (!lamp) throw new RequestException(404, `Lamp id: ${lampId} not found.`)

  // TODO: Check ownership without adding much latency
  // if (lamp.user._id.toString() !== userId.toString())
  //   throw new RequestException(403, 'You do not own this lamp.')

  state = {
    ...lamp.state,
    ...state,
  }

  const groupId = lamp.group._id

  const newState = await updateGroupState(groupId, lampId, state)

  const response = {
    groupId,
    state: newState,
  }

  // TODO: Broadcast lamp state update

  // TODO: Only broadcast to those in group
  broadcast({
    name: 'GROUP_STATE_CHANGED',
    data: response
  })

  await lamp.save() // Save in background

  return response
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