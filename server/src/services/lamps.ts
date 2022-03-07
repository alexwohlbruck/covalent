import { convertToDotNotation } from '../helpers'
import { Lamp, LampModel, LampState } from '../models/lamp'

export const getMyLamps = async () => {

  // TODO: Return only the authed users lamps

  return LampModel.find()
}

export const getLamp = async (id: string) => {
  return LampModel.findById(id)
}

export const createLamp = async (lamp: Lamp) => {

  // TODO: Require group ID and access code and add the lamp to the group

  return LampModel.create(lamp)
}

export const changeGroup = async (id: string, groupId: string) => {

  // TODO: Require group ID and access code and add the lamp to the group

  return LampModel.findByIdAndUpdate(id, { group: groupId }, { new: true })
}

export const sendCommand = async (id: string, state: LampState) => {
  return LampModel.findByIdAndUpdate(id, {
    $set: convertToDotNotation({
      state,
    }),
  }, {
    new: true,
  })
}

export const deleteLamp = async (id: string) => {

  // TODO: Check if group is empty after removing, if so delete group

  return LampModel.findByIdAndRemove(id)
}