#####	   File : Cop.py
####	 Author : Alex Morais
### Description : The cop player type.
##

from engine.Screen import *
from players.Player import *

class Cop(Player):

    def __init__(self, name="default-cop"):
	"""
	The cop player type.
	"""
	# initialize the base class (and its base class)
	Player.__init__(self, 'spotlight')

	scrSize = Screen().getSize()

	# the player type for the purpose of introspection
	self.type = 'Cop'
	self.playerName = name
	self.size = [scrSize[0]*0.11, scrSize[1]*0.11]
	self.halfSize = (self.size[0]/2, self.size[1]/2)
	self.radius = self.size[0] / 2
	self.moveSpeed = (scrSize[0]*0.007, scrSize[1]*0.007)

	self.scale = [1.18, 1.18]
	self.scaleSize( self.scale )

    def render(self, scrScroll=(0,0)):
	"""
	Append some functionality to the base-class render method
	"""

	if not self.texID:
	    self.setSprite( 'spotlight' )

	# call the base class's render
	return Player.render(self, scrScroll)

    def collidePoint(self, objPos):
	"""
	Returns True if the position arg is touching or within the cop.
	"""
	deltaX = (objPos[0] - self.pos[0]) 
	deltaY = (objPos[1] - self.pos[1]) 
	
	distance = (deltaX * deltaX + deltaY * deltaY) * 0.5
	
	#if Distance < self.radius:
	if distance < self.size[0]/2:
	    return True
	else:
	    return False

    def setSize( self, size ):
	"""
	"""
	Player.setSize(self, size)
	self.radius = size[0]

    def scaleSizeByTileSize(self, tileSize):
	"""
	Scales the cop based on the size of the tiles
	"""
	self.setSize( (tileSize[0]*5, tileSize[1]*5) )


    def getAreaUnder( self, scrScroll= [0,0] ):

	# adjust the sprite position on screen by the screen-scroll
	scrPos = ( self.pos[0]-scrScroll[0], self.pos[1]-scrScroll[1] )

	if scrPos[0] < 0 and scrPos[1] < 0:
	    # if the entity is out of the screen, don't try to render it
	    return [0,0,0,0]

	quad = [ scrPos[0]-self.size[0]
		, scrPos[1]-self.size[1]
		, scrPos[0]+self.size[0]
		, scrPos[1]+self.size[1] ]

	return quad


