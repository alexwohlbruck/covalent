import express from 'express'
import WebSocket, { WebSocketServer } from 'ws'

const router = express.Router()
const clients: WebSocket[] = []

const broadcast = (data: string) => {
  clients.forEach((client) => {
    client.send(data)
  })
}

router.ws('/', (ws: WebSocket, req: express.Request) => {

  clients.push(ws)

  ws.on('message', (message: any) => {
    const { name, data } = JSON.parse(message)

    console.log(data)

    broadcast(JSON.stringify({
      name,
      data,
    }))
  })
})