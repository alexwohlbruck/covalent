from app.config import reset_config, add_config, load_config
from machine import reset
from app.led import set_color, turn_off, set, get_color_gradient, rgb_to_hue, hex_to_rgb, polylinear_gradient, rgb_to_hex, kelvin_to_rgb
from app.server import start_server

BRIGHTNESS = 1
NIGHT_MODE = True
MINIMUM_LIGHT_LEVEL = 0.5
READING_LIGHT_COLOR_TEMPERATURE = 6000

server = None
reading_light_on = False

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
    global MINIMUM_LIGHT_LEVEL
    global READING_LIGHT_COLOR_TEMPERATURE

    config = load_config()
    if config:
        BRIGHTNESS = config.get('brightness', BRIGHTNESS)
        NIGHT_MODE = config.get('nightMode', NIGHT_MODE)
        MINIMUM_LIGHT_LEVEL = config.get('minimumLightLevel', MINIMUM_LIGHT_LEVEL)
        READING_LIGHT_COLOR_TEMPERATURE = config.get('readingLightColorTemperature', READING_LIGHT_COLOR_TEMPERATURE)
          
    global server
    server = start_server()
    server.subscribe(on_message)


def activate(color):
    if (server):
        server.send_lamp_command(rgb_to_hex(*color), True)

def deactivate(color=(0,0,0)):
    if (server):
        server.send_lamp_command(rgb_to_hex(*color), False)

def turn_on_reading_light():
    global READING_LIGHT_COLOR_TEMPERATURE
    print('on')
    global reading_light_on
    reading_light_on = True
    print(READING_LIGHT_COLOR_TEMPERATURE)
    print(kelvin_to_rgb(READING_LIGHT_COLOR_TEMPERATURE))
    set_color(kelvin_to_rgb(READING_LIGHT_COLOR_TEMPERATURE))

def turn_off_reading_light():
    print('off')
    global reading_light_on
    reading_light_on = False
    turn_off()

def toggle_reading_light():
    global reading_light_on
    if reading_light_on:
        turn_off_reading_light()
    else:
        turn_on_reading_light()

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
          
    colors = state.get('colors')
    if active:
        # effect = start_effect('rotate', colors=state.get('colors'))
        state = state_from_color_list(colors)
        set(state)

    else:
        # stop_effect(effect)
        global reading_light_on
        if reading_light_on:
            turn_on_reading_light(colors)
        else:
            state = state_from_color_list(colors, .03)
            set(state)

def update_config(config):
    global BRIGHTNESS
    global NIGHT_MODE
    global MINIMUM_LIGHT_LEVEL
    global READING_LIGHT_COLOR_TEMPERATURE
    
    brightness = config.get('brightness', None)
    night_mode = config.get('nightMode', None)
    minimum_light_level = config.get('minimumLightLevel', None)
    reading_light_color_temperature = config.get('readingLightColorTemperature', None)

    if brightness is not None:
        add_config('brightness', brightness)
        BRIGHTNESS = brightness

    if night_mode is not None:
        add_config('nightMode', night_mode)
        NIGHT_MODE = night_mode

    if minimum_light_level is not None:
        add_config('minimumLightLevel', minimum_light_level)
        MINIMUM_LIGHT_LEVEL = minimum_light_level

    if reading_light_color_temperature is not None:
        add_config('readingLightColorTemperature', reading_light_color_temperature)
        READING_LIGHT_COLOR_TEMPERATURE = reading_light_color_temperature

        if reading_light_on:
            turn_on_reading_light()