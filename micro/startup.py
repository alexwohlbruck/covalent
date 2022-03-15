from wifi import connect_wifi, disconnect_wifi, connect_wifi_from_config
from bluetooth import run_setup
from config import load_config, get_config_item
from server import Server

def start_setup_mode():
    run_setup()

from time import sleep, sleep_ms
from machine import Pin, TouchPad

# TODO: Move IO operations to a separate file 
builtin = Pin(2, Pin.OUT)
led = Pin(32, Pin.OUT)
touchpad = TouchPad(Pin(27, Pin.IN, Pin.PULL_UP))
touchpad.config(500)

def run_startup():
    wifi_success = connect_wifi_from_config()
    if not wifi_success:
        start_setup_mode()
    
    # Internet successfully connected
    
    try:
        lamp_id = get_config_item('lampId')
    except KeyError:
        disconnect_wifi()
        start_setup_mode()
        return run_startup()

    # Connect to server
    server = Server(lamp_id)


    # IO operations here

    def button_pressed(pin):
        led.value(1)
        server.send_lamp_command('#00ff00', True)
    
    def button_released(pin):
        led.value(0)
        server.send_lamp_command('#00ff00', False)

    last_val = False
    while (True):
        val = touchpad.read() < 250
        if val:
            if not last_val:
                button_pressed(None)
                sleep_ms(300)
        else:
            if last_val:
                button_released(None)
                sleep_ms(300)
        last_val = val
        sleep_ms(10)

