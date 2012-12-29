##### File  : Mouse.py
#### Author : Alex Morais
### Description : Reads input from glut and moves a player accordingly
##

# TODO: import only what is used
from OpenGL.GLUT import *
from input.Controller import *
from managers.SettingsManager import *

class Mouse(Controller):
    """
    Reads input from glut and moves a player accordingly
    """

    def __init__(self, player=None):
	
	# Base-class constructor
	Controller.__init__(self, player)
    
	self.mousePos = (0,0)

	# grab the settings manager to get the screenRes
	screenRes = SettingsManager().screenRes
	# the center of the screen and tolerance area
	self.center = (screenRes[0]*0.5, screenRes[1]*0.5)
	# this tolerance is based on the resolution to produce a graded scale
	self.tolerance = (50,50)   # an absolute tolerance
	self.scrollAreaSize = ( screenRes[0] * (1-self.tolerance[0])
			    , screenRes[1] * (1-self.tolerance[1]) )

    def on_mouse(self, button, state, x, y):
	"""
	When a mouse button is pressed
	"""
	#if button == 1 and state == GLUT_DOWN:
	#    self.mousePos = (x,y)


    def on_mouse_motion(self, x, y):
	"""
	When the mouse moves
	"""
	self.mousePos = (x,y)


    def update(self, elapsed):

	# since the mouse has moved
	self.calcDeviationScroll( self.mousePos )


    # calcs the deviation of the mouse from the center of the screen
    def calcDeviationScroll(self, mousePos):
	devX = 0.0
	devY = 0.0
	
	# calc the x deviation
	if mousePos[0] > self.center[0] + self.tolerance[0]:
	    devX = mousePos[0] - (self.center[0] + self.tolerance[0])
	elif mousePos[0] < (self.center[0] - self.tolerance[0]):
	    devX = mousePos[0] - (self.center[0] - self.tolerance[0])

	# calc the y deviation
	if mousePos[1] > (self.center[1] + self.tolerance[1]):
		devY = mousePos[1] - (self.center[1] + self.tolerance[1])
	elif mousePos[1] < (self.center[1] - self.tolerance[1]):
		devY = mousePos[1] - (self.center[1] - self.tolerance[1])

	# scaling factor
	devX = devX*100
	devY = devY*100

	# the percentage of pixels between the mousePos and the tolerance area
	#   within the area outside the tolerance to the edge of the screen 
	offset = (-devX/self.scrollAreaSize[0]
		, -devY/self.scrollAreaSize[1] )

	#print 'Mouse : Calc Deviation scroll: offset =', offset
	# move the player by the offset
	self.player.move( offset )
	
	

