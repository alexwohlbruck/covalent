import machine
import gc
from app.wifi import connect_wifi, connect_wifi_from_config
from app.bluetooth import run_setup
from app.config import load_config
from app.ota.ota_updater import OTAUpdater
import app.input as inputio
from app.led import animate
from app.commander import start_commander
import app.mcron as mcron
import app.mcron.decorators

def check_update_and_install():
    otaUpdater = OTAUpdater('https://github.com/alexwohlbruck/covalent', github_src_dir='micro', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def counter(callback_id, current_time, callback_memory):
    check_update_and_install()
    
def start_updater_chron():
    mcron.init_timer()
    mcron.insert(15 * 60 * 1000, {0}, '15m', counter) # Check update every 15 minutes
    
def my_exception_processor(e):
    print(e)

mcron.callback_exception_processors.append(my_exception_processor)

def run_startup():
    wifi_success = connect_wifi_from_config()
    print('Wifi success: {}'.format(wifi_success))
    if not wifi_success:
        run_setup()

    # Install updates if available
    check_update_and_install()

    # Start commander service
    start_commander()
    start_updater_chron()

    # Run LED animation loop
    # animate()

    # Read hardware inputs
    inputio.input_watcher()
