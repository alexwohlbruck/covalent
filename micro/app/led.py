import machine, neopixel
import time
import _thread as thread
import math

EFFECT_PULSE = 1
EFFECT_RAINBOW_CYLCLE = 2
EFFECT_ROTATE = 3
EFFECT_TRANSITION = 4

DEFAULT_BRIGHTNESS = 1
led_count = 72
pin = 14
np = neopixel.NeoPixel(machine.Pin(pin), led_count)

# Current lamp state
effect = None # Current animation effect
colors = [(128,0,15),(128, 15, 0),(128,0,0),(128,0,15)] # Gradient of current colors displayed
preview = None # Reserve a section of the LEDs for previewing a selected color from rotary input

## Color helpers

def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

# Convert hex string #RRGGBB to (r, g, b)
def hex_to_rgb(str):
    return tuple(int(str[i:i+2], 16) for i in (1, 3, 5))

# Convert rgb value into hue in degrees
def rgb_to_hue(r, g, b):
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    return int(h)


# Convert hsl values into rgb color
def hsl_to_rgb(h, s, l):    
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return tuple(int(255 * (r + m)) for r in (r, g, b))
    

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

    # if top is set, get top third of leds
    # leds = range((led_count // 3) if top else 0, led_count)
    # TODO: I reversed these because for the prototype the light strip is upside down
    leds = range(0, (led_count // 3) if top else led_count)

    for i in leds:
        np[i] = tuple(int(p * brightness) for p in color)
    np.write()


# Pass a color and create a slight gradient from it
def set_color_gradient(hue, brightness=None):

    # https://www.desmos.com/calculator/3q33srr3yw
    radians = math.radians(hue)
    shift = int(-25 * math.cos(radians + (math.pi / 4)) + 30)

    upper = hsl_to_rgb((hue + shift) % 360, 1, .5)
    base = hsl_to_rgb(hue, 1, .5)
    lower = hsl_to_rgb((hue - shift) % 360, 1, .5)
    
    set_gradient([lower, base, upper, base, lower])

# Set the gradient colors and update
def set_gradient(colors, fade=True):
    state = polylinear_gradient(led_count, colors)
    set(state)
    # thread.start_new_thread(set_gradient_thread, (colors, fade))

def set_gradient_thread(colors, fade):
    state = polylinear_gradient(led_count, colors)
    if fade:
        transition(copy(), state, .5)
    set(state)

## Effects

# Transition from state1 to state 2 with a smooth fade
def transition(state1, state2, duration):
    global effect
    effect = EFFECT_TRANSITION
    state1 = state1 or copy()
    state2 = state2 or copy()

    # TODO


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
        set_color_gradient(color)

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

# Rotate the current state along the light strip
def rotate(wait=20, reverse=False):
    global effect
    effect = EFFECT_ROTATE
    state = copy()
    
    thread.start_new_thread(rotate_thread, (state, wait, reverse))

def rotate_thread(state, wait, reverse):

    while (effect == EFFECT_ROTATE):
        if reverse:
            # Shift state to the left by 1, wrapping around
            state = state[1:] + state[:1]
        else:
            # Shift state to the right by 1, wrapping around
            state = state[-1:] + state[:-1]

        set(state)
        time.sleep_ms(wait)
    


def rainbow_cycle(wait=10, brightness=None):
    global effect
    effect = EFFECT_RAINBOW_CYLCLE
    brightness = brightness or DEFAULT_BRIGHTNESS

    for j in range(255):
        for i in range(led_count):
            rc_index = (i * 256 // led_count) + j
            rgb = hsl_to_rgb(rc_index & 255)
            np[i] = tuple(int(p * brightness) for p in rgb)
        if effect != EFFECT_RAINBOW_CYLCLE:
            return
        np.write()
        time.sleep_ms(wait)