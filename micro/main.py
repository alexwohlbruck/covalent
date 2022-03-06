from time import sleep
from wifi import prompt_wifi, disconnect_wifi, connect_wifi
from bluetooth import run_ble
import json
from machine import Pin
import gc
import _thread as thread

builtin = Pin(2, Pin.OUT)
led = Pin(32, Pin.OUT)
button = Pin(27, Pin.IN, Pin.PULL_UP)

import uwebsockets.client


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


def main():
    connect_wifi('Night Owl', 'joeldrew swalonsky worst teacher batting average')

    def callback(message):
        name = message.get('name')
        data = message.get('data')
        if name == 'test':
            if (data):
                led.value(1)
            else:
                led.value(0)

    ws = WebSocket('ws://192.168.86.31:3000', callback)

    def button_pressed(pin):
        ws.send({
            'name': 'test',
            'data': True
        })
        button.irq(trigger = Pin.IRQ_RISING, handler = button_released)
    
    def button_released(pin):
        ws.send({
            'name': 'test',
            'data': False
        })
        button.irq(trigger = Pin.IRQ_FALLING, handler = button_pressed)

    button.irq(trigger = Pin.IRQ_FALLING, handler = button_pressed)
        
    

    
    # run_ble()
    # s.start()

    # prompt_wifi()
    # disconnect_wifi()

# 
main()
