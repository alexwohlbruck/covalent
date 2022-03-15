import axios from 'axios'
import { backendUrl } from './config'

const instance = axios.create({
  baseURL: backendUrl,
  withCredentials: true,
})

export default instance