import machine
import gc
from app.wifi import connect_wifi, disconnect_wifi, connect_wifi_from_config
from app.bluetooth import run_setup
from app.config import load_config, get_config_item
from app.server import Server
from app.ota.ota_updater import OTAUpdater
import app.input as inputio
from app.led import animate

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


def run_startup():
    wifi_success = connect_wifi_from_config()
    print('Wifi success: {}'.format(wifi_success))
    if not wifi_success:
        start_setup_mode()

    # Install updates if available
    check_update_and_install()

    try:
        lamp_id = get_config_item('lampId')
    except KeyError:
        print('no lamp id configured')
        disconnect_wifi()
        start_setup_mode()
        return run_startup()

    # Connect to server
    server = Server('project-covalent.herokuapp.com', lamp_id)

    # Run LED animation loop
    # animate()

    # Read hardware inputs
    inputio.input_watcher(server)
