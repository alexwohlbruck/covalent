import Store from '@/store'
import router from '@/router'
import axios from '@/axios'
import { Lamp } from '@/types/Lamp'
import { AVAILABLE_NETWORKS } from './bluetooth'

export const getMyLamps = async() => {
  const { data: lamps } = await axios.get<Lamp[]>('/lamps/me')
  lamps.forEach(lamp => Store.commit('ADD_LAMP', lamp))
  return lamps
}

export const getLamp = async(id: string) => {
  const { data: lamp } = await axios.get<Lamp>(`/lamps/${id}`)
  Store.commit('ADD_LAMP', lamp)
  return lamp
}

export const createLamp = async ({
  name, groupId, accessCode, deviceData
}: {
  name: string,
  groupId: string,
  accessCode: string,
  deviceData: any
}) => {
  try {
    const { data } = await axios.post<Lamp>('/lamps', {
      name,
      groupId,
      deviceData,
      accessCode,
    })
    Store.commit('ADD_LAMP', data)
    router.push({name: 'lamps'})
    return data
  }
  catch (error: any) {
    Store.dispatch('error', error.message)
  }
}

export const renameLamp = async (id: string, name: string) => {
  try {
    const { data } = await axios.put<Lamp>(`/lamps/${id}/name`, {
      name,
    })
    Store.commit('ADD_LAMP', data)
    return data
  }
  catch (error: any) {
    Store.dispatch('error', error.message)
  }
}

export const sendCommand = async ({
  lampId, color, touching
}: {
  lampId: string,
  color: string
  touching?: boolean
}) => {
  try {
    const { data } = await axios.patch<Lamp>(`/lamps/${lampId}/state`, {
      color,
      touching,
    })
    console.log(data)
    Store.commit('GROUP_STATE_CHANGED', data)
    return data
  }
  catch (error: any) {
    Store.dispatch('error', error.message)
  }
}

export const deleteLamp = async (id: string) => {
  const { data } = await axios.delete<Lamp>(`/lamps/${id}`)
  Store.commit('REMOVE_LAMP', {_id: id})
  return data
}