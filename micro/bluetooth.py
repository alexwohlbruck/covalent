from machine import Pin
from machine import Timer
from time import sleep_ms
import network
import ubluetooth
import json
from wifi import connect_wifi, scan_wifi
import ubinascii
import machine

DEVICE_DATA = 'DEVICE_DATA'
REQUEST_NETWORKS = 'REQUEST_NETWORKS'
CONNECT_NETWORK = 'CONNECT_NETWORK'
AVAILABLE_NETWORKS = 'AVAILABLE_NETWORKS'
CONNECTION_SUCCESS = 'CONNECTION_SUCCESS'
CONNECTION_FAILURE = 'CONNECTION_FAILURE'

def get_device_id():
  return ubinascii.hexlify(machine.unique_id()).decode('utf-8')

class ESP32_BLE():
  def __init__(self, name, callback):
    # Create internal objects for the onboard LED
    # blinking when no BLE device is connected
    # stable ON when connected
    self.led = Pin(2, Pin.OUT)
    self.timer1 = Timer(0)
    self.is_connected = False
    
    self.name = name
    self.ble = ubluetooth.BLE()
    self.ble.active(True)
    self.ble.config(mtu=512) # Max is 527
    self.disconnected()
    self.ble.irq(self.ble_irq)
    self.register()
    self.advertiser()
    self.callback = callback # When a message is received

  def connected(self):
    self.led.value(1)
    self.timer1.deinit()
    self.is_connected = True

  def disconnected(self):        
    self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
    self.is_connected = False

  def ble_irq(self, event, data):
      if event == 1: #_IRQ_CENTRAL_CONNECT:
                     # A central has connected to this peripheral
        self.connected()

      elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
                       # A central has disconnected from this peripheral.
        self.advertiser()
        self.disconnected()
    
      elif event == 3: #_IRQ_GATTS_WRITE:
                       # A client has written to this characteristic or descriptor.          
        buffer = self.ble.gatts_read(self.rx)
        msg = buffer.decode('UTF-8').strip()
        print('Received message: ' + msg)
        self.callback(msg)
          
  def register(self):        
    # Nordic UART Service (NUS)
    NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
    RX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
    TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        
    BLE_NUS = ubluetooth.UUID(NUS_UUID)
    BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
    BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        
    BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
    SERVICES = (BLE_UART, )
    ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)
    self.ble.gatts_set_buffer(self.rx, 1024, True)

  def send(self, data):
    data = json.dumps(data)
    print('Sending message: ' + data)
    self.ble.gatts_notify(0, self.tx, data + '\n')

  def advertiser(self):
    name = bytes(self.name, 'UTF-8')
    adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
    self.ble.gap_advertise(100, adv_data)

def run_ble():

  def on_message(payload):
    print(payload)
    payload = json.loads(payload)
    
    name = payload['name']
    data = payload['data']

    if name == REQUEST_NETWORKS:
      ble.send({
        'name': DEVICE_DATA,
        'data': {
          'deviceId': get_device_id(),
        }
      })
      networks = scan_wifi()
      ble.send({
        'name': AVAILABLE_NETWORKS,
        'data': {
          'networks': networks
        }
      })

    if name == CONNECT_NETWORK:
      ssid = data['ssid']
      password = data['password']

      if connect_wifi(ssid, password):
        ble.send({
          'name': CONNECTION_SUCCESS,
          'data': {
            'ssid': ssid,
            # TODO: Get IP address and strength
          },
        })
      else:
        ble.send({
          'name': CONNECTION_FAILURE,
          'data': {},
        })

  led = Pin(2, Pin.OUT)
  but = Pin(0, Pin.IN)

  device_name = 'Friendship Lamp - ' + get_device_id()[-6:]
  ble = ESP32_BLE(device_name, on_message)

  # def buttons_irq(pin):
  #   led.value(not led.value())
  #   ble.send('LED state will be toggled.')
  #   print('LED state will be toggled.')

  # but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

  count = 0
  while True:
    # if ble.ble_msg == 'read_LED':
    #   print(ble.ble_msg)
    #   ble.ble_msg = ""
    #   print('LED is ON.' if led.value() else 'LED is OFF')
    #   ble.send('LED is ON.' if led.value() else 'LED is OFF')
    if (ble.is_connected):
    #   ble.send('Test message ' + str(count))
      count += 1

    sleep_ms(1000)