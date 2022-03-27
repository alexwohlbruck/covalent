import machine, neopixel
import time
import _thread as thread

DEFAULT_BRIGHTNESS = .1
led_count = 72
pin = 14
np = neopixel.NeoPixel(machine.Pin(pin), led_count)

# Save state of LEDs in an array
def copy():
    state = [0] * led_count
    for i in range(led_count):
        state[i] = np[i]
    return state


# Turn off all LEDs and then fade them in
def flash():
    print('flashing')
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
def pulse(state=None):
    state = state or copy()
    thread.start_new_thread(pulse_thread, (state,))

def pulse_thread(state):
    while (True):
        # Fade in
        for i in range(20):
            for j in range(led_count):
                np[j] = tuple(int(p * (i / 20)) for p in state[j])
            np.write()
            time.sleep_ms(50)
        
        # Fade out
        for i in range(20):
            for j in range(led_count):
                np[j] = tuple(int(p * (1 - (i / 20))) for p in state[j])
            np.write()
            time.sleep_ms(50)


# TODO: Fade new color
def set_color(r, g, b, brightness=None):
    brightness = brightness or DEFAULT_BRIGHTNESS

    for i in range(led_count):
        np[i] = tuple(int(p * brightness) for p in (r, g, b))
    np.write()

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

def rainbow_cycle(wait, brightness=None):
    brightness = brightness or DEFAULT_BRIGHTNESS

    for j in range(255):
        for i in range(led_count):
            rc_index = (i * 256 // led_count) + j
            rgb = wheel(rc_index & 255)
            np[i] = tuple(int(p * brightness) for p in rgb)
        np.write()
        time.sleep_ms(wait)