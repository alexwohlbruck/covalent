import Store from '@/store'
import axios from '@/axios'
import { Group } from '@/types/Group'

export const getGroup = async (id: string) => {
  const { data } = await axios.get<Group>(`/groups/${id}`)
  Store.commit('ADD_GROUP', data)
  return data
}
