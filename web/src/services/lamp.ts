import Store from '@/store'
import router from '@/router'
import axios from '@/axios'
import { Lamp } from '@/types/Lamp'

export const getMyLamps = async() => {
  const { data } = await axios.get('/lamps/me')
  data.forEach((lamp: Lamp) => Store.commit('ADD_LAMP', lamp))
  return data
}

export const createLamp = async ({
  groupId, accessCode, deviceData
}: {
  groupId: string,
  accessCode: string,
  deviceData: any
}) => {
  try {
    const { data }: { data: Lamp } = await axios.post('/lamps', {
      groupId,
      deviceData,
      accessCode,
    })
    Store.commit('ADD_LAMP', data)
    router.push({name: 'lamps'})
    return data
  }
  catch (error: any) {
    Store.dispatch('error', error?.details?.message)
  }
}