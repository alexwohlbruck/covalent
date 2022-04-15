import machine
import gc
from app.wifi import connect_wifi, connect_wifi_from_config
from app.bluetooth import run_setup
from app.config import load_config
from app.ota.ota_updater import OTAUpdater
import app.input as inputio
from app.led import animate
from app.commander import start_commander

def check_update_and_install():
    otaUpdater = OTAUpdater('https://github.com/alexwohlbruck/covalent', github_src_dir='micro', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()


def run_startup():
    wifi_success = connect_wifi_from_config()
    print('Wifi success: {}'.format(wifi_success))
    if not wifi_success:
        run_setup()

    # Install updates if available
    check_update_and_install()

    # Start commander service
    start_commander()

    # Run LED animation loop
    # animate()

    # Read hardware inputs
    inputio.input_watcher()
