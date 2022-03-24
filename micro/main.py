from app.startup import run_startup
import _thread as thread

def main():
    thread.start_new_thread(run_startup, ())

if __name__ == "__main__":
    main()