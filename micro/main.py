from machine import Pin
from time import sleep
import network
import sys

# led = Pin(2, Pin.OUT)

# while True:
#   led.value(not led.value())
#   sleep(0.5)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

def scan_wifi():
  print('Scanning for Wifi networks...')
  
  wifis = sta_if.scan()
  print('Found ' + str(len(wifis)) + ' networks:')

  for wifi in wifis:
    print('- ' + wifi[0].decode('utf-8'))
  
  print('\n')
  
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
  
def main():
  scan_wifi()

  # Take wifi credentials from user input
  input('') # The first one doesn't work for some reason
  ssid = input('Enter SSID: ')
  password = input('Enter password: ')

  connect_wifi(ssid, password)

  sleep(3)
  disconnect_wifi()

main()

# sta_if.connect("<AP_name>", "<password>") # Connect to an AP
# sta_if.isconnected()                      # Check for successful connection