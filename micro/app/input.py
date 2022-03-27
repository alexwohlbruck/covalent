
from time import sleep_ms
from time import sleep, sleep_ms
from machine import Pin, TouchPad, ADC
from app.rotary.rotary_irq_esp import RotaryIRQ
from app.led import wheel, set_color

server = None

ROTARY_STEPS = 32
LIGHT_SENSITIVITY = 3600
SENSITIVITY_RANGE = 300

builtin = Pin(2, Pin.OUT)
touchpad = TouchPad(Pin(27, Pin.IN, Pin.PULL_UP))
touchpad.config(500)
motion_sensor = Pin(17, Pin.IN, Pin.PULL_UP)
light_sensor = ADC(Pin(33, Pin.IN, Pin.PULL_UP))
light_sensor.atten(ADC.ATTN_11DB)

# a = Pin(25, Pin.IN)
# b = Pin(32, Pin.IN)
r = RotaryIRQ(
    pin_num_clk=32, 
    pin_num_dt=25, 
    min_val=0, 
    max_val=(ROTARY_STEPS-1), 
    reverse=False, 
    range_mode=RotaryIRQ.RANGE_WRAP,
    pull_up=True
)

def button_pressed(pin):
    # led.value(1)
    if (server):
        server.send_lamp_command('#00ff00', True)

def button_released(pin):
    # led.value(0)
    if (server):
        server.send_lamp_command('#00ff00', False)

# Start watcher for input events
def input_watcher(_server):
    global server
    server = _server

    rotary_old = r.value()
    motion_old = motion_sensor.value()
    touchpad_old = touchpad.read()
    is_dark = False
    
    while (True):

        rotary_new = r.value()
        motion_new = motion_sensor.value()
        touchpad_raw = touchpad.read()
        touchpad_new = touchpad_raw < 250
        light = light_sensor.read()
    
        if rotary_old != rotary_new:
            rotary_old = rotary_new

            set_color(*wheel(int((rotary_new / ROTARY_STEPS) * 255)))

            print('result =', rotary_new)

        if motion_old != motion_new:
            print('motion =', motion_new)
            motion_old = motion_new
        
        # If light level passes sensitivity threshold, update is_dark
        if is_dark and light > (LIGHT_SENSITIVITY + SENSITIVITY_RANGE):
            print(f'room is light ({light})')
            is_dark = False

        elif not is_dark and light < (LIGHT_SENSITIVITY - SENSITIVITY_RANGE):
            print(f'room is dark ({light})')
            is_dark = True

        if (touchpad_new != touchpad_old):
            if (touchpad_new):
                button_pressed(touchpad)
            else:
                button_released(touchpad)
            touchpad_old = touchpad_new


        # print('rotary_old: %d, rotary_new: %d' % (rotary_old, rotary_new))
        # print(str(light_sensor.read()) + ' ' + str(motion_sensor.value()))

        sleep_ms(5)