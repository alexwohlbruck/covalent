from machine import Pin
from machine import Timer
from time import sleep_ms
import network
import ubluetooth
import json
from machine import Pin
from app.wifi import connect_wifi, scan_wifi
from app.config import get_device_id, add_config
from app.led import flash, pulse, set_color_gradient, rgb_to_hue

DEVICE_DATA = 'DEVICE_DATA'
REQUEST_NETWORKS = 'REQUEST_NETWORKS'
CONNECT_NETWORK = 'CONNECT_NETWORK'
AVAILABLE_NETWORKS = 'AVAILABLE_NETWORKS'
CONNECTION_SUCCESS = 'CONNECTION_SUCCESS'
CONNECTION_FAILURE = 'CONNECTION_FAILURE'
SET_LAMP_ID = 'SET_LAMP_ID'
ERROR = 'ERROR'


class ESP32_BLE():
    def __init__(self, name, callback):
        print('init')
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
        print('connected')
        self.led.value(1)
        self.timer1.deinit()
        self.is_connected = True
        flash()

    def disconnected(self):
        print('disconnected')
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
        self.is_connected = False

    def disconnect(self):
        self.ble.gap_disconnect(0)
        self.disconnected()

    def deinit(self):
        # Turn off bluetooth
        self.disconnect()
        self.ble.active(False)
        self.timer1.deinit()

    def ble_irq(self, event, data):
            print('BLE IRQ: ' + str(event))

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
        print('Registering service') 
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
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        print('Advertising')
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)

        # Set led to blue for pairing mode
        hue = rgb_to_hue(0, 0, 255)
        set_color_gradient(223)
        pulse()

def run_setup():

    setup_finished = False

    def on_message(payload):
        payload = json.loads(payload)
        
        name = payload['name']
        data = payload['data']

        # TODO: Move these checks out of the function in a dict
        if name == REQUEST_NETWORKS:
            print('Request networks')
            ble.send({
                'name': DEVICE_DATA,
                'data': {
                    'deviceId': get_device_id(),
                }
            })
            networks = scan_wifi()
            print(networks)

            # TODO: I only send the first 5 networks because of the packet size limit.
            # TODO: Make a recursive function to send all networks in chunks of 5.
            ble.send({
                'name': AVAILABLE_NETWORKS,
                'data': {
                    'networks': networks[0:5]
                }
            })

        if name == CONNECT_NETWORK:
            print('connect network')
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
        
        if name == SET_LAMP_ID:
            # Lamp created in DB, setup process finished, attempt to connect to server
            
            lamp_id = data.get('lampId', None)
            if (lamp_id):
                add_config('lampId', lamp_id)
                nonlocal setup_finished
                setup_finished = True
            else:
                ble.send({
                    'name': ERROR,
                    'data': {
                        'message': "Couldn't sync lamp ID to device."
                    }
                })
            

    led = Pin(2, Pin.OUT)
    but = Pin(0, Pin.IN)

    started = False
    device_name = 'Friendship Lamp' # - ' + get_device_id()[-6:]
    ble = ESP32_BLE(device_name, on_message)

    while not setup_finished:
        sleep_ms(1000)

    ble.deinit()
    print('Setup finished')