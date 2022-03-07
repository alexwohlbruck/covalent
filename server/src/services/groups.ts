import { GroupModel } from '../models/group'

export const listGroups = async () => {
  // TODO: Only return user's groups
  return await GroupModel.find()
}

export const getGroup = async (groupId: string) => {
  return await GroupModel.findById(groupId)
}