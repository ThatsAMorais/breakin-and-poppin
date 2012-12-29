#####	   File : Robber.py
####	 Author : Alex Morais
### Description : The robber player type.
##

from players.Player import *
from ui.Sprite import *
from managers.TextureManager import *
from engine.Screen import *

class Robber(Player):


    def __init__(self, name='default-robber'):
	"""
	A robber player type
	"""
	# initialize the base class
	Player.__init__(self, 'robber2')

	scrRes = Screen().getSize()
	
	# the player type for the purpose of introspection
	self.type = 'Robber'
	self.playerName = name
	self.size = [32,32]
	self.halfSize = (self.size[0]/2, self.size[1]/2)
	self.moveSpeed = (scrRes[0]*0.0125, scrRes[1]*0.0125)
	self.animSpeed = 40

	self.scale = [0.5, 0.5]
	self.scaleSize( self.scale )

    def render(self, scrScroll=(0,0)):
	"""
	Append some functionality to the base-class render method
	"""

	if not self.texID:
	    self.setSprite( 'robber2' )

	# call the base class's render (returning its result)
	return Player.render(self, scrScroll)


    def update(self, elapsed):
	"""
	update sprite and collision list
	"""
	Player.update(self, elapsed)


    def scaleSizeByTileSize(self, tileSize):
	"""
	Scales the cop based on the size of the tiles
	"""
	self.setSize( (tileSize[0]*0.5, tileSize[1]*0.5) )

