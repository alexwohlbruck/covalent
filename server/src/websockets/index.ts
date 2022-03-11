import express from 'express'
import WebSocket, { WebSocketServer } from 'ws'

const router = express.Router()
const clients: WebSocket[] = []

export const broadcast = (data: { name: string, data: object }) => {
  clients.forEach((client) => {
    client.send(JSON.stringify(data))
  })
}

router.ws('/', (ws: WebSocket, req: express.Request) => {

  clients.push(ws)

  ws.on('message', (message: any) => {
    const { name, data } = JSON.parse(message)

    broadcast({
      name,
      data,
    })
  })
})

export default router