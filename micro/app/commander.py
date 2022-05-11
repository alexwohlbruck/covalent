from app.config import reset_config, add_config, load_config
from machine import reset
from app.led import set_color, turn_off, transition_to, get_color_gradient, rgb_to_hue, hex_to_rgb, polylinear_gradient, rgb_to_hex, kelvin_to_rgb
from app.server import start_server
from time import sleep, ticks_ms

# User defined config variables
BRIGHTNESS = 1
NIGHT_MODE = True
MOTION_DETECTION = True
MINIMUM_LIGHT_LEVEL = 0.5
READING_LIGHT_COLOR_TEMPERATURE = 6000

server = None
last_active = False
last_colors = ['#ffffff']
reading_light_on = False

last_room_is_lit = True
last_motion_detected = True
time_since_interactive = ticks_ms()

message_queue = []

def on_message(name, data):
    # TODO: Move this switch to a dict outside
    if name == 'GROUP_STATE_CHANGED':
        pulse_received(data)
    
    if name == 'FACTORY_RESET':
        factory_reset()
    
    if name == 'REQUEST_CONFIG':
        server.send_config()

    if name == 'UPDATE_CONFIG':
        update_config(data)
      
def start_commander():
    global BRIGHTNESS
    global NIGHT_MODE
    global MOTION_DETECTION
    global MINIMUM_LIGHT_LEVEL
    global READING_LIGHT_COLOR_TEMPERATURE

    config = load_config()
    if config:
        BRIGHTNESS = config.get('brightness', BRIGHTNESS)
        NIGHT_MODE = config.get('nightMode', NIGHT_MODE)
        MOTION_DETECTION = config.get('motionDetection', MOTION_DETECTION)
        MINIMUM_LIGHT_LEVEL = config.get('minimumLightLevel', MINIMUM_LIGHT_LEVEL)
        READING_LIGHT_COLOR_TEMPERATURE = config.get('readingLightColorTemperature', READING_LIGHT_COLOR_TEMPERATURE)
          
    global server
    server = start_server()
    server.subscribe(on_message)


# Send activate command to server
def activate(color):
    if (server):
        active = True
        server.send_lamp_command(rgb_to_hex(*color), True)

# Send deactivate command to server
def deactivate(color=(0,0,0)):
    if (server):
        active = False
        server.send_lamp_command(rgb_to_hex(*color), False)

# Activate LEDs from last stored colors
def activate_local():
    global last_colors
    state = state_from_color_list(last_colors, brightness=BRIGHTNESS)
    # set(state)
    transition_to(state, 50)

# Deactivate LEDs from last stored colors
def deactivate_local():
    global last_colors
    global reading_light_on
    if reading_light_on:
        turn_on_reading_light()
    else:
        print(last_colors)
        state = state_from_color_list(last_colors, BRIGHTNESS * .05)
        # set(state)
        transition_to(state, 10)

def turn_on_reading_light():
    global READING_LIGHT_COLOR_TEMPERATURE
    print('on')
    global reading_light_on
    reading_light_on = True
    rgb = kelvin_to_rgb(READING_LIGHT_COLOR_TEMPERATURE)
    set_color(rgb, brightness=BRIGHTNESS)

def turn_off_reading_light():
    print('off')
    global reading_light_on
    reading_light_on = False
    deactivate_local()

def toggle_reading_light():
    global reading_light_on
    if reading_light_on:
        turn_off_reading_light()
    else:
        turn_on_reading_light()

# Triggered by input.py when the room becomes bright
def room_is_lit(val):
    global last_room_is_lit
    last_room_is_lit = val

    # If dark, turn off the light completely
    if not val:
        turn_off()
        return

    dequeue()

# Triggered by input.py when motion is detected
def motion_detected(val):
    global last_motion_detected
    last_motion_detected = val
    dequeue()

# Triggered by input.py when user is interacting with device
def user_is_interacting():
    global time_since_interactive
    time_since_interactive = ticks_ms()
    print('time since int:', time_since_interactive)

# If room is lid and motion detected, dequeue pending messages
def dequeue():
    global last_room_is_lit
    global last_motion_detected
    print(last_room_is_lit, last_motion_detected)

    if last_room_is_lit and last_motion_detected:
        # Wait 1 second between dequeuing
        while len(message_queue) > 0:
            message = message_queue.pop(0)
            pulse_received(message)
            sleep(1)
        
        # Deactivate after dequeuing
        deactivate_local()


def factory_reset():
    reset_config()
    reset()

def state_from_color_list(colors, brightness=None):
    if len(colors) == 1:
        colors = get_color_gradient(rgb_to_hue(*hex_to_rgb(colors[0])))
    else:
        colors = [hex_to_rgb(c) for c in colors]

    return polylinear_gradient(None, colors, brightness=brightness)
      
def pulse_received(data):
    state = data.get('state', None)
    active = state.get('active', None)

    if state == None and active == None:
        return

    global last_room_is_lit
    global last_motion_detected
    global time_since_interactive

    # Check if user has interacted with device in the last 30 seconds
    user_has_interacted = ticks_ms() - time_since_interactive < 30000

    # Don't light if user has not interacted recently or the room is dark
    if active and not user_has_interacted and (not last_room_is_lit):
        message_queue.append(data)
        return
          
    global last_active
    global last_colors
    last_active = active
    colors = state.get('colors')
    last_colors = colors

    if active:
        activate_local()
    else:
        deactivate_local()

def update_config(config):
    global BRIGHTNESS
    global NIGHT_MODE
    global MOTION_DETECTION
    global MINIMUM_LIGHT_LEVEL
    global READING_LIGHT_COLOR_TEMPERATURE
    
    brightness = config.get('brightness', None)
    night_mode = config.get('nightMode', None)
    motion_detection = config.get('motionDetection', None)
    minimum_light_level = config.get('minimumLightLevel', None)
    reading_light_color_temperature = config.get('readingLightColorTemperature', None)

    if brightness is not None:
        add_config('brightness', brightness)
        BRIGHTNESS = brightness

        global reading_light_on
        if reading_light_on:
            turn_on_reading_light()
        else:
            global last_active
            global last_colors

            if last_active:
                activate_local()
            else:
                deactivate_local()

    if night_mode is not None:
        add_config('nightMode', night_mode)
        NIGHT_MODE = night_mode
    
    if motion_detection is not None:
        add_config('motionDetection', motion_detection)
        MOTION_DETECTION = motion_detection

    if minimum_light_level is not None:
        add_config('minimumLightLevel', minimum_light_level)
        MINIMUM_LIGHT_LEVEL = minimum_light_level

    if reading_light_color_temperature is not None:
        add_config('readingLightColorTemperature', reading_light_color_temperature)
        READING_LIGHT_COLOR_TEMPERATURE = reading_light_color_temperature

        if reading_light_on:
            turn_on_reading_light()