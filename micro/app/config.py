import json
import ubinascii
from machine import unique_id
from ubinascii import hexlify

def get_device_id():
  return hexlify(unique_id()).decode('utf-8')

config_filename = 'config.json'
default_config = {
  'deviceId': get_device_id(),
  'wifi': [],
  'brightness': 1,
  'nightMode': True,
  'minimumLightLevel': 0.5,
  'readingLightColorTemperature': 6000
}

def load_config():
  
  # If file exists, load it
  try:
    f = open(config_filename, 'r')
    config = json.load(f)
    f.close()

    # If any config options are missing, add them
    found_new = False
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
        found_new = True

    if found_new:
      write_config(config)

    return config
  
  # If file doesn't exist, create it
  except OSError:
    config = default_config
    f = open(config_filename, 'w')
    json.dump(config, f)
    f.close()
    return config

# Overwrite config options
def write_config(config):
  f = open(config_filename, 'w')
  json.dump(config, f)
  f.close()

# Append a config option
def add_config(key, value):
  config = load_config()
  config[key] = value
  write_config(config)

def get_config_item(key):
  config = load_config()
  return config.get(key, default_config.get(key, None))

def reset_config():
  write_config(default_config)