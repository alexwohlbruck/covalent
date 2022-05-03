import network
from time import sleep
from app.config import load_config, get_config_item, add_config
from app.led import pulse, set_color

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
color = (255, 50, 0)

def scan_wifi():
    wifis = sta_if.scan()
    ssids = []

    for wifi in wifis:
        ssid = wifi[0].decode('utf-8')
        rssi = wifi[3]

        # Filter out hidden networks
        if len(ssid.strip()) > 0:
            ssids.append({
                'ssid': ssid,
                'rssi': rssi,
            })
    
    # Order by signal strength
    ssids.sort(key=lambda x: x['rssi'], reverse=True)
    
    print(ssids)
    return ssids


# Connect to wifi using existing config
# If no config exists, this returns False
# Otherwise, return if the connection was successful
def connect_wifi_from_config():

    wifis = get_config_item('wifi')

    if wifis is None:
        return False

    # If a network exists that is in the config, connect to it
    
    found_wifis = scan_wifi()

    # TODO: Order by signal strength
    for wifi in wifis:
        ssid = wifi.get('ssid', None)
        password = wifi.get('password', None)

        for found_wifi in found_wifis:
            if ssid == found_wifi.get('ssid', None):
                if ssid is None or password is None:
                    return False

                return connect_wifi(ssid, password)
    
    return False
    
# Connect to wifi using the given ssid and password
# Returns True if the connection was successful
def connect_wifi(ssid, password):
    print('Connecting to ' + ssid + '...')
    set_color(color)
    pulse()

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
        set_color(color)

        wifis = get_config_item('wifi')

        if wifis is None:
            wifis = []

        # Remove the ssid if it exists already
        wifis = [wifi for wifi in wifis if wifi.get('ssid', None) != ssid]
        
        wifis.append({
            'ssid': ssid,
            'password': password,
        })

        add_config('wifi', wifis)

        return True


def disconnect_wifi():
    print('Disconnecting from ' + sta_if.config('essid') + '...')
    sta_if.disconnect()
    print('Successfully disconnected from ' + sta_if.config('essid') + '\n')
