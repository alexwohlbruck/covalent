import network
from time import sleep
from app.config import add_config, load_config

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

def scan_wifi():
    wifis = sta_if.scan()
    ssids = []

    for wifi in wifis:
        ssid = wifi[0].decode('utf-8')

        # Filter out hidden networks
        if len(ssid.strip()) > 0:
            ssids.append({
                'ssid': ssid,
            })
    
    return ssids


# Connect to wifi using existing config
# If no config exists, this returns False
# Otherwise, return if the connection was successful
def connect_wifi_from_config():

    config = load_config()
    wifi = config.get('wifi', None)

    if wifi is None:
        return False
        
    ssid = wifi.get('ssid', None)
    password = wifi.get('password', None)

    if ssid is None or password is None:
        return False
    
    return connect_wifi(ssid, password)

    
# Connect to wifi using the given ssid and password
# Returns True if the connection was successful
def connect_wifi(ssid, password):
    print('Connecting to ' + ssid + '...')

    sta_if.connect(ssid, password)

    timeout = 10
    while not sta_if.isconnected() and timeout > 0:
        sleep(1)
        timeout -= 1
    
    if timeout == 0:
        print('Failed to connect to ' + ssid + '\n')
        disconnect_wifi()
        return False

    else:
        print('Successfully connected to ' + ssid + '\n')
        
        add_config('wifi', {
            'ssid': ssid,
            'password': password,
        })
        return True


def disconnect_wifi():
    print('Disconnecting from ' + sta_if.config('essid') + '...')
    sta_if.disconnect()
    print('Successfully disconnected from ' + sta_if.config('essid') + '\n')
