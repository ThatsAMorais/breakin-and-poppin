##### File  : Keyboard.py
#### Author : Alex Morais
### Description : Reads input from glut and moves a player accordingly
##

# TODO: import only what is used
from OpenGL.GLUT import *
from input.Controller import *

class Keyboard(Controller):
    """
    Reads input from glut and moves a player accordingly
    """

    def __init__(self, player=None):
	
	# Base-class constructor
	Controller.__init__(self, player)

	self.keys = { 'up'   : 'w'\
		    , 'down' : 's'\
		    , 'left' : 'a'\
		    , 'right': 'd'}

    def on_key_press(self, key, x, y):
	"""
	"""
	# Calculate the movement offset
	moveOffset = [0,0]
	if key == self.keys['up']:
	    moveOffset[1] -= 1
	elif key == self.keys['down']:
	    moveOffset[1] += 1
	elif key == self.keys['left']:
	    moveOffset[0] -= 1
	elif key == self.keys['right']:
	    moveOffset[0] += 1
	# Move the player
	self.player.move( moveOffset )


    def on_key_release(self, key, x, y):
	"""
	"""


    def on_specialkey_press(self, key, x, y):
	"""
	"""

    def on_specialkey_release(self, key, x, y):
	"""
	"""


