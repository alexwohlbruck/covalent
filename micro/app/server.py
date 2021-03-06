import _thread as thread
import json
from time import sleep_ms
import app.uwebsockets.client as wsclient
from app.config import get_device_id, get_config_item, load_config
from app.wifi import disconnect_wifi
from app.led import set_color, pulse

MAX_RECONNECT_ATTEMPTS = 5
color = (0, 255, 0)

class WebSocket():
    def __init__(self, uri, callback):
        set_color(color)
        pulse()
        print('Connecting to server')
        self.uri = uri
        self.callback = callback
        self.reconnect_attempts = 0
        self.connect()
        set_color(color)

    def connect(self):
        self.websocket = wsclient.connect(self. uri)
        self.thread = thread.start_new_thread(self.listen, ())

    
    def send(self, data):
        message = json.dumps(data)
        try:
            self.websocket.send(message)
        except:
            print('Failed to send data: {}'.format(message))

    def listen(self):
        while (True):
            message = self.websocket.recv()

            if (not self.websocket.open):
                self.reconnect()
                return

            if message is None or len(message) == 0:
                return

            try:
                data = json.loads(message)
                # print('Received data: {}'.format(data))
                self.callback(data)
            except ValueError:
                print('Received invalid JSON: "{}"'.format(message))
            sleep_ms(100)
    
    def stop(self):
        self.websocket.close()

    # Attempt to reconnect, after a few attempts restart the device
    def reconnect(self):
        print(f'Reconnecting to server (Attempt { self.reconnect_attempts })')
        self.stop()

        if self.reconnect_attempts != 0 and self.reconnect_attempts != MAX_RECONNECT_ATTEMPTS:
            sleep(10)

        if self.reconnect_attempts > MAX_RECONNECT_ATTEMPTS:
            reset()
            return

        self.reconnect_attempts += 1
        self.connect()

# Main server class to send and receive messages
# TODO: Move event names to constants
class Server():
    def __init__(self, address, lamp_id):
        self.lamp_id = lamp_id
        self.device_id = get_device_id()
        
        uri = 'ws://' + address + '/?deviceId=' + self.device_id
        self.ws = WebSocket(uri, self.on_message)
        self.callbacks = []
    
    def on_message(self, message):
        name = message.get('name')
        data = message.get('data')

        print('Got ' + name)

        for callback in self.callbacks:
            callback(name, data)
    
    # Publish incoming messsages
    def subscribe(self, cb):
        self.callbacks.append(cb)
    
    def send_lamp_command(self, color, touching):
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

    def send_config(self):
        config = load_config()
        self.ws.send({
            'name': 'CONFIG',
            'data': config
        })
    
def start_server():
    try:
        lamp_id = get_config_item('lampId')
    except KeyError:
        print('no lamp id configured')
        disconnect_wifi()
        run_setup()
        # run_startup()

    return Server('www.projectcovalent.app', lamp_id)
    # return Server('192.168.1.17:3000', lamp_id)