import express from 'express'
import { User, UserModel } from '../models/user'
import WebSocket, { WebSocketServer } from 'ws'
import { LampModel } from '../models/lamp'
import { sendCommand } from '../services/lamps'

const router = express.Router()

// Store socket connections from web app
const webClients: {
  [userId: string]: WebSocket,
} = {}

// Store socket connections from lamps
const deviceClients: {
  [deviceId: string]: WebSocket,
} = {}

interface WSPayload {
  name: string
  data: object
}

// Send a message to all connected clients (no auth)
export const broadcast = (data: WSPayload) => {
  const payload = JSON.stringify(data)

  Object.keys(webClients).forEach((userId) => {
    webClients[userId].send(payload)
  })

  Object.keys(deviceClients).forEach((deviceId) => {
    deviceClients[deviceId].send(payload)
  })
}

// Send a message to a user on the web app
export const broadcastToUsers = (userIds: string[], payload: WSPayload) => {
  userIds.forEach((userId) => {
    if (webClients[userId]) {
      webClients[userId].send(JSON.stringify(payload))
    }
  })
}

// Send a message to a device
export const broadcastToDevices = (deviceIds: string[], payload: WSPayload) => {
  deviceIds.forEach((deviceId) => {
    if (deviceClients[deviceId]) {
      deviceClients[deviceId].send(JSON.stringify(payload))
    }
  })
}

// Client to server events
const events = {
  SEND_LAMP_COMMAND: async (data: any) => {
    console.log('SEND_LAMP_COMMAND', data)
    const { lampId, state } = data
    if (lampId && state)
      await sendCommand(lampId, state)
  },
}

router.ws('/', async (ws: WebSocket, req: express.Request) => {

  const userId = (req?.user as User)?._id
  const deviceId = req.query?.deviceId as string

  console.log('New ws connection: ', userId, deviceId)

  if (!userId && !deviceId) {
    ws.send(JSON.stringify({
      name: 'ERROR',
      data: {
        message: 'You must be authenticated or pass device id in query string.',
      },
    }))
    return ws.close()
  }

  // Store socket connection
  if (userId)
    webClients[userId] = ws
  else
    deviceClients[deviceId] = ws


  // Handle incoming messages with event handlers
  ws.on('message', (message: any) => {
    const { name, data } = JSON.parse(message)
    const handler = (events as any)[name]

    if (handler) {
      handler(data)
    }
  })

})

export default router