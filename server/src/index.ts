import WebSocket, { WebSocketServer } from 'ws'

const PORT = 3000
const wss = new WebSocketServer({
  port: PORT,
})

const clients: WebSocket[] = []

const broadcast = (data: string) => {
  clients.forEach((client) => {
    client.send(data)
  })
}

wss.on('connection', (ws: WebSocket) => {

  clients.push(ws)

  ws.on('message', (message: any) => {
    const { name, data } = JSON.parse(message)

    broadcast(JSON.stringify({
      name,
      data,
    }))
  })
})