import _thread as thread
import json
from time import sleep_ms
import app.uwebsockets.client as wsclient
from app.config import get_device_id, reset_config
from machine import reset

# TODO: Move IO operations to a separate file
from machine import Pin, TouchPad
led = Pin(32, Pin.OUT)

class WebSocket():
    def __init__(self, uri, callback):
        print('Connecting to server')
        self.callback = callback
        self.websocket = wsclient.connect(uri)
        thread.start_new_thread(self.listen, ())
    
    def send(self, data):
        message = json.dumps(data)
        try:
            self.websocket.send(message)
        except:
            print('Failed to send data: {}'.format(message))

    def listen(self):
        while (True):
            message = self.websocket.recv()
            if message is None or len(message) == 0:
                return

            try:
                data = json.loads(message)
                print('Received data: {}'.format(data))
                self.callback(data)
            except ValueError:
                print('Received invalid JSON: "{}"'.format(message))
            sleep_ms(100)
    
    def stop(self):
        self.websocket.close()

# Main server class to send and receive messages
# TODO: Move event names to constants
class Server():
    def __init__(self, address, lamp_id):
        self.lamp_id = lamp_id
        self.device_id = get_device_id()
        
        uri = 'ws://' + address + '/?deviceId=' + self.device_id
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
        
        if name == 'FACTORY_RESET':
            self.ws.stop()
            reset_config()
            reset()
    
    def send_lamp_command(self, color, touching):

        # TODO: Auto resolve lamp id
        self.ws.send({
            'name': 'SEND_LAMP_COMMAND',
            'data': {
                'lampId': self.lamp_id,
                'state': {
                    'color': color,
                    'touching': touching,
                }
            }
        })
    