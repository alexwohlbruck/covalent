import { Types } from 'mongoose'
import { RequestException } from '../routes'
import { convertToDotNotation } from '../helpers'
import { Lamp, LampModel, LampState } from '../models/lamp'

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
  if (!lamp) throw new RequestException(404, `Lamp with id ${id} not found`)
  return lamp
}

export const createLamp = async (lamp: Lamp) => {

  // TODO: Require group ID and access code and add the lamp to the group

  return await LampModel.create(lamp)
}

export const moveLampToGroup = async (id: string, groupId: string) => {

  // TODO: Require group ID and access code and add the lamp to the group

  return await LampModel.findByIdAndUpdate(id, { group: groupId }, { new: true })
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

  // TODO: Check if group is empty after removing, if so delete group

  return await LampModel.findByIdAndRemove(id)
}