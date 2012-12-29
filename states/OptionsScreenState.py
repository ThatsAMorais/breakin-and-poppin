#####	   File : OptionsScreenState.py
####	 Author : Alex Morais
### Description : 
##

from states.EngineState import *

class OptionsScreenState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

    def renderFrame(self):
	""" RenderFrame - Base Class """
	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	return self

    def on_key_release(self, key, x, y):
	"""
	On key release
	"""
	return self

    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	return self

    def on_mouse_press(self, button, state, x, y):
	"""
	On mouse press
	"""
	return self

    def on_mouse_release(self, button, state, x, y):
	"""
	On mouse release
	"""
	return self

    def on_socket(self, elapsed):
	"""
	On socket
	"""
	return self

    def Step(self):
	"""
	Step
	"""
	pass

