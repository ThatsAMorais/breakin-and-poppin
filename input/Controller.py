##### File  : Controller.py
#### Author : Alex Morais
### Description : Reads input from glut and moves a player accordingly
##

# TODO: import only what is used
from OpenGL.GLUT import *

class Controller():
    """
    Reads input from glut and moves a player accordingly
    """
    def __init__(self, player):
	self.player = player

    def setPlayer(self, player):
	self.player = player

    def update(self, elapsed):
	"""
	The mouse needs it, the keyboard doesn't; it doesn't hurt to include
	it in both to be general and accomodating.  This is called when everything
	else in the game engine is updated.
	"""
	pass

