from time import sleep
from wifi import prompt_wifi, disconnect_wifi
from bluetooth import run_ble

def main():
  run_ble()

  # prompt_wifi()
  # sleep(1000)
  # disconnect_wifi()

main()
