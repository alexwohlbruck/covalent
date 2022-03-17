import machine
import gc
from app.wifi import connect_wifi, disconnect_wifi, connect_wifi_from_config
from app.bluetooth import run_setup
from app.config import load_config, get_config_item
from app.server import Server
from app.ota.ota_updater import OTAUpdater

def start_setup_mode():
    run_setup()

def check_update_and_install():
    otaUpdater = OTAUpdater('https://github.com/alexwohlbruck/covalent', github_src_dir='micro', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

from time import sleep, sleep_ms
from machine import Pin, TouchPad

# TODO: Move IO operations to a separate file 
builtin = Pin(2, Pin.OUT)
led = Pin(32, Pin.OUT)
touchpad = TouchPad(Pin(27, Pin.IN, Pin.PULL_UP))
touchpad.config(500)

def run_startup():
    wifi_success = connect_wifi_from_config()
    print('Wifi success: {}'.format(wifi_success))
    if not wifi_success:
        start_setup_mode()

    # Install updates if available
    check_update_and_install()

    print ('getting lamp id')
    
    # Internet successfully connected
    
    try:
        lamp_id = get_config_item('lampId')
    except KeyError:
        print('no lamp id configured')
        disconnect_wifi()
        start_setup_mode()
        return run_startup()

    # Connect to server
    server = Server('project-covalent.herokuapp.com', lamp_id)


    # IO operations here

    def button_pressed(pin):
        led.value(1)
        server.send_lamp_command('#00ff00', True)
    
    def button_released(pin):
        led.value(0)
        server.send_lamp_command('#00ff00', False)

    last_val = False
    while (True):
        sensor = touchpad.read()
        val = sensor < 250
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

