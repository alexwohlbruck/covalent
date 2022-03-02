import network
from time import sleep

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
  
def connect_wifi(ssid, password):
  print('Connecting to ' + ssid + '...')

  sta_if.connect(ssid, password)

  timeout = 10
  while not sta_if.isconnected() and timeout > 0:
    sleep(1)
    timeout -= 1
  
  if timeout == 0:
    print('Failed to connect to ' + ssid + '\n')
    return False
  else:
    print('Successfully connected to ' + ssid + '\n')
    return True

def disconnect_wifi():
  print('Disconnecting from ' + sta_if.config('essid') + '...')
  sta_if.disconnect()
  print('Successfully disconnected from ' + sta_if.config('essid') + '\n')

def prompt_wifi():
  scan_wifi()

  # Take wifi credentials from user input
  input('') # The first one doesn't work for some reason
  ssid = input('Enter SSID: ')
  password = input('Enter password: ')

  connect_wifi(ssid, password)