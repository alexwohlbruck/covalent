import machine, neopixel
import time
import _thread as thread

EFFECT_PULSE = 1
EFFECT_RAINBOW_CYLCLE = 2

DEFAULT_BRIGHTNESS = 1
led_count = 72
pin = 14
np = neopixel.NeoPixel(machine.Pin(pin), led_count)

# Current lamp state
effect = None # Current animation effect
colors = [(255,0,255)] # Gradient of current colors displayed
preview = None # Reserve a section of the LEDs for previewing a selected color from rotary input

## Color helpers

def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

# Convert hex string #RRGGBB to (r, g, b)
def hex_to_rgb(str):
    return tuple(int(str[i:i+2], 16) for i in (1, 3, 5))

# Get a color out of the color wheel
def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def linear_gradient(n, start, finish):
    ''' Generate a gradient from two colors '''
    # Generate list of colors
    colors = []
    for i in range(n):
        colors.append(
            tuple(
                int(start[j] + (float(i)/(n-1))*(finish[j]-start[j]))
                for j in range(3)
            )
        )
    return colors

# Generate a gradient from a list of colors
def polylinear_gradient(n, colors):
    if len(colors) == 0:
        return [(0,0,0)] * n

    if len(colors) == 1:
        return [colors[0]] * n

    sections = len(colors) - 1
    section_length = n // sections

    state = [0] * n
    for i in range(sections):
        start_index = i * section_length
        end_index = start_index + section_length
        gradient = linear_gradient(section_length, colors[i], colors[i+1])
        for j in range(section_length):
            state[start_index + j] = gradient[j]

    return state
    

## Synchronous helpers

# Save state of LEDs in an array
def copy():
    state = [0] * led_count
    for i in range(led_count):
        state[i] = np[i]
    return state

# Set the LEDs to a state
def set(state):
    for i in range(led_count):
        np[i] = state[i]
    np.write()

# TODO: Fade new color
def set_color(color, brightness=None, top=False):
    global effect
    effect = None
    brightness = brightness or DEFAULT_BRIGHTNESS

    # if top is set, get top half of leds
    leds = range((led_count // 2) if top else 0, led_count)

    for i in leds:
        np[i] = tuple(int(p * brightness) for p in color)
    np.write()


# Set the lamp to the current colors list
def update_gradient():
    global colors
    state = polylinear_gradient(led_count, colors)
    set(state)


## Effects

# Turn off all LEDs and then fade them in
def flash(color=None):
    if color:
        set_color(color)

    global effect
    effect = None
    state = copy()

    # Turn off all LEDs
    for i in range(led_count):
        np[i] = (0, 0, 0)
    np.write()

    # Fade in
    for i in range(20):
        for j in range(led_count):
            np[j] = tuple(int(p * (i / 10)) for p in state[j])
        np.write()
        time.sleep_ms(50)

# Slowly pulse all LEDs
def pulse(color=None, state=None):
    if color:
        set_color(color)

    global effect
    effect = EFFECT_PULSE
    state = state or copy()
    thread.start_new_thread(pulse_thread, (state,))

def pulse_thread(state):
    while (effect == EFFECT_PULSE):
        # Fade out from 100% to 50%
        for i in range(20):
            for j in range(led_count):
                np[j] = tuple(int(p * (20 - i) / 20) for p in state[j])
            if effect != EFFECT_PULSE:
                return
            np.write()
            time.sleep_ms(15)
        
        # Fade out from 50% to 100%
        for i in range(20):
            for j in range(led_count):
                np[j] = tuple(int(p * (i + 1) / 20) for p in state[j])
            if effect != EFFECT_PULSE:
                return
            np.write()
            time.sleep_ms(15)

def rainbow_cycle(wait, brightness=None):
    global effect
    effect = EFFECT_RAINBOW_CYLCLE
    brightness = brightness or DEFAULT_BRIGHTNESS

    for j in range(255):
        for i in range(led_count):
            rc_index = (i * 256 // led_count) + j
            rgb = wheel(rc_index & 255)
            np[i] = tuple(int(p * brightness) for p in rgb)
        if effect != EFFECT_RAINBOW_CYLCLE:
            return
        np.write()
        time.sleep_ms(wait)