import _thread as thread
import uwebsockets.client
from config import get_device_id

class WebSocket():
    def __init__(self, uri, callback):
        self.callback = callback
        self.websocket = uwebsockets.client.connect(uri)
        thread.start_new_thread(self.listen, ())
    
    def send(self, data):
        message = json.dumps(data)
        self.websocket.send(message)

    def listen(self):
        while (True):
            message = self.websocket.recv()
            print("< {}".format(message))
            data = json.loads(message)
            self.callback(data)
    
    def stop(self):
        self.websocket.close()

# Main server class to send and receive messages
class Server():
    def __init__(self):
        
        device_id = get_device_id()
        lamp_id = '6226fd0e8667493a669ba747'

        uri = 'ws://192.168.86.30:3000/?deviceId=' + device_id
        self.ws = WebSocket(uri, self.on_message)
    
    def on_message(self, message):
        name = message.get('name')
        data = message.get('data')
    
        # TODO: Move this switch to a dict outside
        if name == 'GROUP_STATE_CHANGED':
            state = data.get('state')
            active = state.get('active')
            if active:
                led.value(1)
            else:
                led.value(0)
    
    def send_lamp_command(lamp_id, color, touching):

        # TODO: Auto resolve lamp id
        self.ws.send({
            'name': 'SEND_LAMP_COMMAND',
            'data': {
                'lampId': lamp_id,
                'state': {
                    'color': color,
                    'touching': touching,
                }
            }
        })
    