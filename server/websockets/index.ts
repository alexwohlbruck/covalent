import express from 'express'
import { User, UserModel } from '../models/user'
import WebSocket, { WebSocketServer } from 'ws'
import { sendCommand } from '../services/lamps'

const router = express.Router()

// Store socket connections from web app
// keyed by userId
const webClients = new Map<string, WebSocket[]>()

// Store socket connections from lamps
// keyed by deviceId
const deviceClients = new Map<string, WebSocket[]>()

export interface WSPayload {
  name: string
  data: object
}

// Send a message to all connected clients (no auth)
export const broadcast = (data: WSPayload) => {
  const payload = JSON.stringify(data)

  webClients.forEach(clients => {
    clients.forEach(ws => ws.send(payload))
  })

  deviceClients.forEach(clients => {
    clients.forEach(ws => ws.send(payload))
  })
}

// Send a message to a user on the web app
export const broadcastToUsers = (userIds: string[], payload: WSPayload) => {
  userIds.forEach((userId) => {
    const clients = webClients.get(userId.toString())
    if (clients) {
      clients.forEach(ws => ws.send(JSON.stringify(payload)))
    }
  })
}

// Send a message to a device
export const broadcastToDevices = (deviceIds: string[], payload: WSPayload) => {
  deviceIds.forEach((deviceId) => {
    const clients = deviceClients.get(deviceId)
    if (clients) {
      clients.forEach(ws => ws.send(JSON.stringify(payload)))
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

// Ping clients on an interval
setInterval(() => {
  webClients.forEach(clients => clients.forEach(s => s.ping()))
  deviceClients.forEach(clients => clients.forEach(s => s.ping()))
}, 1000 * 5)

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
  if (userId) {
    if (webClients.has(userId.toString())){
      webClients.get(userId.toString()).push(ws)
    }
    else {
      webClients.set(userId.toString(), [ws])
    }
  }
  else {
    if (deviceClients.has(deviceId)) {
      deviceClients.get(deviceId).push(ws)
    }
    else {
      deviceClients.set(deviceId, [ws])
    }
  }

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