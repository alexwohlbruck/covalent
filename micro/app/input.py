
from time import sleep_ms
from time import sleep, sleep_ms, ticks_ms
from machine import Pin, ADC
from app.rotary.rotary_irq_esp import RotaryIRQ
from app.led import set_color, rgb_to_hex, hsl_to_rgb, turn_off
from app.commander import activate, toggle_reading_light, deactivate, factory_reset, room_is_lit, motion_detected, user_is_interacting, MINIMUM_LIGHT_LEVEL

ROTARY_STEPS = 32
# LIGHT_SENSITIVITY = 3400
LIGHT_SENSITIVITY_MAX = 4095
LIGHT_SENSITIVITY_MIN = 100
SENSITIVITY_RANGE = 100
OUTLIER_RANGE = 35
DOUBLE_PRESS_WAIT = 350 # Usually 500, I like it a little quicker
HOLD_PRESS_WAIT = 5000 # Time to wait for factory reset
LOOP_WAIT = 5
LIGHT_WAIT = 2000 # How long to wait to register light change

pushbutton = Pin(27, Pin.IN, Pin.PULL_UP)
builtin = Pin(2, Pin.OUT)
motion_sensor = Pin(17, Pin.IN, Pin.PULL_UP)
light_sensor = ADC(Pin(33, Pin.IN, Pin.PULL_UP))
light_sensor.atten(ADC.ATTN_11DB)

r = RotaryIRQ(
    pin_num_clk=32, 
    pin_num_dt=25, 
    min_val=0, 
    max_val=(ROTARY_STEPS-1), 
    reverse=False, 
    range_mode=RotaryIRQ.RANGE_WRAP,
    pull_up=True
)

last_color = (255, 0, 0)

# Start watcher for input events
def input_watcher():

    global last_color

    # Pushbutton stuff
    pushbutton_old = pushbutton.value()
    pressed_time = ticks_ms()
    released_time = ticks_ms()
    press_count = 0
    holding = False
    
    # Other inputs
    rotary_old = r.value()
    motion_old = motion_sensor.value()
    light_old = light_sensor.read()
    reads_dark = False
    is_dark = False
    past_threshold = False
    light_time = ticks_ms() # Time since light threshold was crossed
    
    # Keep rolling average of last 50 light values
    light_values = []
    light_avg_max = 50

    while 1:

        pushbutton_new = pushbutton.value()
        rotary_new = r.value()
        motion_new = motion_sensor.value()
        light_new = light_sensor.read()

        # Pushbutton
        if pushbutton_new != pushbutton_old:
            user_is_interacting()
            if pushbutton_new == 0:
                # Pressed
                pressed_time = ticks_ms()
                press_count += 1
            else:
                # Released
                released_time = ticks_ms()
                
                if holding:
                    deactivate()
                    holding = False

                if press_count == 2:
                    toggle_reading_light()
        
        if press_count > 0:

            now = ticks_ms()

            # Reset press count if button is released for more than a fraction of a second
            if pushbutton_new == 1 and now - released_time > DOUBLE_PRESS_WAIT:
                press_count = 0

            # Send signal if single press is held for more than fraction of a second
            if not holding and press_count == 1 and pushbutton_new == 0 and now - pressed_time > DOUBLE_PRESS_WAIT:
                holding = True
                activate(last_color)

            # Check if user has held double press for a few seconds
            if press_count == 2 and pushbutton_new == 1 and now - pressed_time > HOLD_PRESS_WAIT:
                factory_reset()
                press_count = 0

        pushbutton_old = pushbutton_new

        # Rotary input
        if rotary_old != rotary_new:
            user_is_interacting()
            rotary_old = rotary_new
            val = int((rotary_new / ROTARY_STEPS) * 360)
            last_color = hsl_to_rgb(val, 1, 0.5)
            set_color(last_color, top=True)
            # print('result =', rotary_new)

        # Motion sensor
        if motion_old != motion_new:
            # print('motion =', motion_new)
            motion_old = motion_new
            motion_detected(motion_new == 1)
        
        # Light sensor
        light_values.append(light_new)
        # print(light_new)
        if len(light_values) > light_avg_max:
            light_values.pop(0)
        
        light_avg = sum(light_values) / len(light_values)

        # Ignore outliers
        if light_new <= light_avg + OUTLIER_RANGE and light_new >= light_avg - OUTLIER_RANGE:

            # # If light level passes sensitivity threshold, update reads_dark
            threshold = ((LIGHT_SENSITIVITY_MAX - LIGHT_SENSITIVITY_MIN) * MINIMUM_LIGHT_LEVEL) + LIGHT_SENSITIVITY_MIN

            if reads_dark and light_new > (threshold + SENSITIVITY_RANGE):
                reads_dark = False
                past_threshold = True

            elif not reads_dark and light_new < (threshold - SENSITIVITY_RANGE):
                reads_dark = True
                light_time = ticks_ms()
                past_threshold = True
            
            if past_threshold:

                now = ticks_ms()
                if now - light_time > LIGHT_WAIT:
                    if reads_dark != is_dark:
                        is_dark = reads_dark
                        room_is_lit(not is_dark)

                    past_threshold = False

        sleep_ms(LOOP_WAIT)