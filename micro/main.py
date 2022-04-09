from app.startup import run_startup
import _thread as thread
from app.led import rainbow_cycle
from time import sleep, sleep_ms

from app.led import animate, start_effect, stop_effect, polylinear_gradient, led_count, hsl_to_rgb
import math

def main():
    run_startup()

if __name__ == "__main__":
    main()