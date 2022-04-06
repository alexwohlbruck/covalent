from app.startup import run_startup
import _thread as thread
from app.led import rainbow_cycle
from time import sleep, sleep_ms

from app.led import animate, start_effect, stop_effect, polylinear_gradient, led_count

def main():

    animate()

    state1 = polylinear_gradient(led_count, [(255,0,0),(255,0,30),(255,0,0)])
    state2 = polylinear_gradient(led_count, [(0,0,255),(0,150,150),(0,0,255)])

    counter = 0
    while True:
        e = start_effect('rotate', initial_state=(state1 if counter % 2 == 0 else state2))
        counter+=1
        
        # while(True):
        #     sleep(1)

        sleep(1)

        stop_effect(e)

        sleep(6)




    # run_startup()

if __name__ == "__main__":
    main()