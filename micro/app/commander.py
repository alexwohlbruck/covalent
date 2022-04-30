from app.config import reset_config
from machine import reset
from app.led import set_color, turn_off, set, get_color_gradient, rgb_to_hue, hex_to_rgb, polylinear_gradient, rgb_to_hex
from app.server import start_server

reading_light_on = False

server = None

def on_message(name, data):
	# TODO: Move this switch to a dict outside
	if name == 'GROUP_STATE_CHANGED':
		pulse_received(data)
	
	if name == 'FACTORY_RESET':
		factory_reset()
  	
def start_commander():
	global server
	server = start_server()
	server.subscribe(on_message)

def activate(color):
	if (server):
		server.send_lamp_command(rgb_to_hex(*color), True)

def deactivate(color=(0,0,0)):
	if (server):
		server.send_lamp_command(rgb_to_hex(*color), False)

def turn_on_reading_light():
	print('on')
	global reading_light_on
	reading_light_on = True
	set_color((255,255,255))

def turn_off_reading_light():
	print('off')
	global reading_light_on
	reading_light_on = False
	turn_off()

def toggle_reading_light():
	global reading_light_on
	if reading_light_on:
		turn_off_reading_light()
	else:
  		turn_on_reading_light()

def factory_reset():
	reset_config()
	reset()

def state_from_color_list(colors, brightness=None):
		if len(colors) == 1:
			colors = get_color_gradient(rgb_to_hue(*hex_to_rgb(colors[0])))
		else:
			colors = [hex_to_rgb(c) for c in colors]
  
		return polylinear_gradient(None, colors, brightness=brightness)
  	
def pulse_received(data):
	state = data.get('state', None)
	active = state.get('active', None)

	if state == None and active == None:
  		return
		  
	colors = state.get('colors')
	if active:
  		# effect = start_effect('rotate', colors=state.get('colors'))
		state = state_from_color_list(colors)
		set(state)

	else:
		# stop_effect(effect)
		global reading_light_on
		if reading_light_on:
  			turn_on_reading_light(colors)
		else:
			state = state_from_color_list(colors, .03)
			set(state)