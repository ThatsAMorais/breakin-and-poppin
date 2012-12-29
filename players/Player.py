#####  File : Player.py
#### Author : Alex Morais
### Description : An entity controlled by the user.  This is a Base-
###		Class for the Cop and Robber classes.
##

from ui.Sprite import *
from collision.Collision import *

class Player( Sprite ):

    def __init__(self, filename):
        """
        An entity controlled by the user.  This is a base class for the Cop and Robber classes.
        """

	# call the Sprite ctor
	Sprite.__init__(self, filename)

	self.type = "Player : Base Class"	
	self.playerName = 'default-baseclass-player'
	self.pos = [50,50]	# current pos
	self.size = [2,2]
	self.halfSize = (1,1)
	self.center = None
	# walking speed (how big is offset += 1?)
	self.moveSpeed = (3, 3)

    def update(self, elapsed):
	"""
	This should be called by any derived classes that override it
	or much functionality will be lost!
	"""
	Sprite.update(self, elapsed)


    def setName( self, name ):
	"""
	sets this player's name
	"""
	self.playerName = name


    def getName( self ):
	return self.playerName


    def getType( self ):
	return self.type


    def getBBox( self ):
	"""
	Returns the player's bounding box based on its current pos.
	"""
	return [ self.pos[0], self.pos[1]
		, self.pos[0]+self.size[0]
		, self.pos[1]+self.size[1] ]


    def getCenterPos(self):
	"""
	Returns the center position of the robber
	"""
	return [ self.pos[0]+self.size[0]/2, self.pos[1]+self.size[1]/2 ]


    def setPos( self, pos=[0,0] ):
	"""
	Set the world position
	"""
	prevPos = list(self.pos)
	self.pos[0] = pos[0]
	self.pos[1] = pos[1]

    def move( self, offset ):
	"""
	Alter the position by an offset
	"""
	# Make sure that self.pos exists
	self.pos[0] += offset[0]*self.moveSpeed[0]
	self.pos[1] += offset[1]*self.moveSpeed[1]

	# The direction code was previously written like the following
	#   code block for both x and y separately...
	#
	#   # Determine horizontal facing direction 
	#   if self.pos > self.lastPos:
	#       self.facingDir = 1
	#   elif self.pos < self.lastPos:
	#       self.facingDir = -1
	#   else:
	#       self.facingDir = 0
	#
	# The implementation above made it so that the screen would
	#   not scroll when the mouse is inside the "tolerance
	#   area."  So, when the player is not moving(mouse inside
	#   tolerance area) and the screen edge has not become
	#   inert behind the player, it stops moving because the
	#   facing direction is [0,0].  The following is the new
	#   way.  It allows for movement while inside of the
	#   tolerance area because it doesn't allow the facing
	#   direction to be set to (0,0).

	# Determine horizontal facing direction 
	if self.pos[0] > self.lastPos[0]:
	    self.facingDir[0] = 1
	    # Determine vertical facing direction 
	    if self.pos[1] > self.lastPos[1]:
		self.facingDir[1] = 1
	    elif self.pos[1] < self.lastPos[1]:
		self.facingDir[1] = -1
	    else:
		self.facingDir[1] = 0
	elif self.pos[0] < self.lastPos[0]:
	    self.facingDir[0] = -1
	    # Determine vertical facing direction 
	    if self.pos[1] > self.lastPos[1]:
		self.facingDir[1] = 1
	    elif self.pos[1] < self.lastPos[1]:
		self.facingDir[1] = -1
	    else:
		self.facingDir[1] = 0
	else:
	    # Determine vertical facing direction 
	    if self.pos[1] > self.lastPos[1]:
		self.facingDir[0] = 0
		self.facingDir[1] = 1
	    elif self.pos[1] < self.lastPos[1]:
		self.facingDir[0] = 0
		self.facingDir[1] = -1

	self.lastPos[0] += offset[0]
	self.lastPos[1] += offset[1]

	# ensure that it is not less than 0
	self.lastPos[0] = max(0, self.lastPos[0])
	self.lastPos[1] = max(0, self.lastPos[1])


    def collidePoint(self, pos, type):
	"""
	Test if the point lies inside of the player's box
	"""
	print "Base Class - Player - collidePoint.  args=[", pos, type, ']'


    def scaleSize(self, scale=1):
	"""
	a go-through to the Sprite function
	"""
	Sprite.scaleSize( self, scale )

    def setSize( self, size ):
	"""
	a go-through to the Sprite function
	"""
	Sprite.setSize( self, size )



