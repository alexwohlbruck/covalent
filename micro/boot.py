from wifi import connect_wifi, connect_wifi_from_config
from bluetooth import run_ble
from config import load_config

# Debug print
debug = True
def dprint(str):
    if (debug):
        print(str)

def start_setup_mode():
    dprint('TODO: Start setup mode')
    run_ble()
    print('ble done')


def main():
    wifi_success = connect_wifi_from_config()
    if not wifi_success:
        start_setup_mode()
    
    # TODO: Connect to socket

    

if __name__ == '__main__':
    main()