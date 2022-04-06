from app.startup import run_startup
import _thread as thread
from app.led import rainbow_cycle
from time import sleep, sleep_ms

from app.led import animate, start_effect, stop_effect, polylinear_gradient, led_count, hsl_to_rgb
import math

def generate_gradient(hue):
  
    radians = math.radians(hue)
    shift = int(-25 * math.cos(radians + (math.pi / 4)) + 30)

    upper = hsl_to_rgb((hue + shift) % 360, 1, .5)
    base = hsl_to_rgb(hue, 1, .5)
    lower = hsl_to_rgb((hue - shift) % 360, 1, .5)
    
    return [lower, base, upper, base, lower]

def main():

    animate()

    state1 = polylinear_gradient(led_count, generate_gradient(0))
    state2 = polylinear_gradient(led_count, generate_gradient(120))

    counter = 0
    while True:
        e1 = start_effect('rotate', initial_state=(state1 if counter % 2 == 0 else state2))

        sleep_ms(4000)

        # e2 = start_effect('rotate', initial_state=(state2 if counter % 2 == 0 else state1))
        
        # while(True):
        #     sleep(1)

        # sleep(1)

        # stop_effect(e1)
        # stop_effect(e2)

        # sleep(2)

        counter+=1



    # run_startup()

if __name__ == "__main__":
    main()