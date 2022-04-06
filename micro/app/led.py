import machine, neopixel
import time
import _thread as thread
import math
import random
import gc

DEFAULT_BRIGHTNESS = 1
led_count = 72
pin = 14
np = neopixel.NeoPixel(machine.Pin(pin), led_count)

refresh_rate = 30 # frames per second

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = time.ticks_us()
        result = f(*args, **kwargs)
        delta = time.ticks_diff(time.ticks_us(), t)
        print('{} took {} us'.format(myname, delta/1000))
        return result
    return new_func

# Current lamp statef

# List of effects that are currently running
effects = []

# List of keyframes that are currently being tweened
keyframes = {}
colors = [(128,0,15),(128, 15, 0),(128,0,0),(128,0,15)] # Gradient of current colors displayed
preview = None # Reserve a section of the LEDs for previewing a selected color from rotary input


def ease_in_cubic(t):
    return t**3

def ease_out_cubic(t):
    return (t-1)**3 + 1

def ease_in_out_cubic(t):
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

# Compute the intermediate value between two values given a percent
def tween(start, end, percent, ease=None):

    # If no ease function is specified, use linear
    if ease:
        function = globals().get(ease, None)
        if function:
            percent = function(percent)

    return start + (end - start) * percent

def tween_opacity(keyframe, current_fame):
    start = keyframe['start']
    end = keyframe['end']
    start_frame = keyframe['start_frame']
    duration = keyframe['duration']
    end_frame = start_frame + duration

    if current_fame >= start_frame and current_fame <= end_frame:
        progress = (current_fame - start_frame) / duration
        return tween(start['opacity'], end['opacity'], progress) # , ease=keyframe['ease']
    else:
        return None


# Overlay a color with a given opacity (color2, opacity) on top of another color (color1)
def overlay(color1, color2, opacity):
    return tuple(int(color1[i] * (1 - opacity) + color2[i] * opacity) for i in range(3))

# Start animation loop
'''
We have a list of effects and a list of keyframes
Both are a active list of currently running animations
Effects contain a state which is updated throughout the animation loop and an effect name that points to an effect function
Keyframes contain a start and end state, a duration, and an easing function for fading effects in and out
When a keyframe starts, it is tweened and the effects are overlapped
When a keyframe ends, it is removed
When an effect is animated to 0 opacity, it is removed
'''
def animate():

    # Open new thread
    def thread_animate():
        
        global keyframes
        global effects
        frame = 0

        while True:

            tstart = time.ticks_us()

            frame_state = [(0,0,0)] * led_count

            for effect_index, effect in enumerate(effects):
                
                effect_state = rotate(effect.get('state', copy()))
                effect['state'] = effect_state

                # Get current opacity for the current frame of the effect
                keyframe_queue = keyframes.get(effect['id'], None)
                opacity = effect.get('opacity', 1)

                if keyframe_queue:
                    keyframe = keyframe_queue[0]

                    if keyframe:

                        if not keyframe.get('start_frame', None):
                            keyframe['start_frame'] = frame

                        opacity = tween_opacity(keyframe, frame) or opacity
                        effect['opacity'] = opacity

                        start_opacity = keyframe['start']['opacity']
                        end_opacity = keyframe['end']['opacity']
                        start_frame = keyframe['start_frame']
                        duration = keyframe['duration']
                        end_frame = start_frame + duration

                        # If start opacity is 1, remove all other effects and unrelated keyframes
                        if frame == start_frame and start_opacity == 1:
                            print('start frame opacity 1, remove all other effects')
                            effects = [effect]
                            keyframes = {k: v for k, v in keyframes.items() if k == effect['id']}
                        
                        # If this keyframe is finished
                        if frame == end_frame:
                            print('keyframe finished')

                            # End opacity is one, remove all other effects and unrelated keyframes
                            if end_opacity == 1:
                                print('end opacity 1, remove all other effects')
                                effects = [effect]
                                keyframes = {k: v for k, v in keyframes.items() if k == effect['id']}


                            # If end opacity is 0, remove effect
                            if end_opacity == 0:
                                print('opacity is 0, remove ffect')
                                del effects[effect_index]

                            # Remove keyframe
                            print ('remove keyframe')
                            if len(keyframes[effect['id']]) > 1:
                                keyframes[effect['id']].pop(0)
                            else:
                                del keyframes[effect['id']]
                                


                # We layer the new effect with it's opacity on top of the existing frame_state
                for i in range(led_count):
                    frame_state[i] = overlay(frame_state[i], effect_state[i], opacity)

            
            set(frame_state)
            gc.collect()

            frame += 1

            tend = time.ticks_us()

            print((tend - tstart) / 1000, 'ms')

            time.sleep_ms(1)
    
    thread.start_new_thread(thread_animate, ())


def start_effect(name, initial_state=None, transition=20, ease='ease_in_out_cubic'):

    # If no initial state is given, use the current state
    if not initial_state:
        initial_state = copy()

    # If the effect is not running, add it to the effects list
    effect_id = math.floor(random.random() * 100000)

    fade = transition > 0

    effects.append({
        'id': effect_id,
        'effect': name,
        'state': initial_state,
        'opacity': 0 if fade else 1,
    })

    if fade:
        # Start a new keyframe
        keyframes[effect_id] = [{
            'duration': transition,
            'ease': ease,
            'start': {
                'opacity': 0,
            },
            'end': {
                'opacity': 1,
            },
        }]
    
    return effect_id


def stop_effect(effect_id, transition=30, ease='ease_in_out_cubic'):

    # If the effect is running, add a new keyframe to fade it out
    keyframe = {
        'duration': transition,
        'ease': ease,
        'start': {
            'opacity': 1,
        },
        'end': {
            'opacity': 0,
        },
    }

    if effect_id in keyframes:
        keyframes[effect_id].append(keyframe)
    else:
        keyframes[effect_id] = [keyframe]




EFFECT_PULSE = 1
EFFECT_RAINBOW_CYLCLE = 2
EFFECT_ROTATE = 3
EFFECT_TRANSITION = 4

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
    current_state = copy()
    new_state = polylinear_gradient(led_count, colors)
    set(new_state)

## Effects

# # TODO: Transition from state1 to state 2 with a smooth fade
# # state: list of rgb tuples [(R, G, B)]
# def transition(state1, state2, duration):
#     step_duration = 1 # duration of each step in ms
#     global effect
#     effect = EFFECT_TRANSITION
#     state1 = state1 or copy()
#     state2 = state2 or copy()

#     steps = int(duration * 1000 / step_duration)

#     for i in range(steps):
#         progress = i / steps
#         for j in range(led_count):
#             state1[j] = tuple(int(s1 + (s2 - s1) * progress) for s1, s2 in zip(state1[j], state2[j]))
#         set(state1)
#         time.sleep_ms(step_duration)
#     set(state2)
#     effect = None


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

def rotate(state, reverse=False):
    if reverse:
        # Shift state to the left by 1, wrapping around
        state = state[1:] + state[:1]
    else:
        # Shift state to the right by 1, wrapping around
        state = state[-1:] + state[:-1]

    return state
    

def rainbow_cycle(frame):
    state = [(0,0,0)] * led_count
    for i in range(led_count):
        rc_index = (i * 256 // led_count) + frame
        rgb = hsl_to_rgb(rc_index % 256, 1, .5)
        state[i] = tuple(int(p) for p in rgb)
        
    return state