from app.startup import run_startup
import _thread as thread
from app.led import rainbow_cycle
from time import sleep_ms

from app.led import update_gradient

def main():

    update_gradient()

    while (True):
        sleep_ms(1000)
        # rainbow_cycle(1)

    # thread.start_new_thread(run_startup, ())
    # run_startup()

if __name__ == "__main__":
    main()