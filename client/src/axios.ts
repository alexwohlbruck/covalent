import axios, { AxiosRequestConfig } from 'axios'

const options: AxiosRequestConfig = {
  withCredentials: true,
}

if (process.env.NODE_ENV === 'development') {
  options.baseURL = 'http://localhost:3000'
}

const instance = axios.create(options)

export default instance