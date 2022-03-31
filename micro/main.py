from app.startup import run_startup
import _thread as thread
from app.led import rainbow_cycle
from time import sleep_ms

from app.led import rotate, set_color, set_color_gradient, rgb_to_hue, hex_to_rgb

def main():

    # rotate(reverse=True)

    # hue = rgb_to_hue(*hex_to_rgb('#003cff'))
    # set_color_gradient(hue)
    # rotate()

    # while (True):
    #     # print("rianbow")
    #     # rainbow_cycle(1, .5)
    #     sleep_ms(1000)

    # thread.start_new_thread(run_startup, ())
    run_startup()

if __name__ == "__main__":
    main()