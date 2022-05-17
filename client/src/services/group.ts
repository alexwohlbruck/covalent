import Store from '@/store'
import axios from '@/axios'
import { Group } from '@/types/Group'

export const getGroup = async (id: string) => {
  const { data } = await axios.get<Group>(`/groups/${id}`)
  Store.commit('ADD_GROUP', data)
  return data
}

export const getMyGroups = async () => {
  const { data } = await axios.get<Group[]>('/groups/me')

  data.forEach(group => {
    // Destructure lamps
    group.lamps?.forEach(lamp => {
      Store.commit('ADD_LAMP', lamp)
    })
    delete group.lamps

    Store.commit('ADD_GROUP', group)
  })

  return data

}