#####  File : Collision.py
#### Author : Alex Morais
### Description : An object repr. of a collision which clocks the time 
###		elapsed since the collision.  It is updated via
###		update() with the time since the previous update.
##

class Collision():

    # Supported types.  This is weakly abstracted, but this is an area of the
    #	game that is outside of the general framework.  In other words, if you
    #	want to reuse this, re-implement it.
    # player constants
    COP = 0
    ROBBER = 1
    # level constants
    BASE = 2
    BUILDING = 3
    DROP_POINT = 4
    # for use with pointing/clicking
    MOUSE = 5


    def __init__(self, type=[None,None]):
	"""
	Init: (self, type=[None,None])
	"""
	# start the clock
	self.timeSinceCollis = 0

	# a pair of bodies that have a collision
	self.type = list(type) # be sure and make a new copy

    def setType(self, type):
	"""
	set the collision type
	"""

    def getType(self):
	"""
	returns the tuple-pair as a type
	"""
	return self.type

    def update(self, elapsed):
	"""
	increment the clock since the initial collision.  Returns the time for
	convenience since it is likely to be retrieved soon after calling
	update, anyway.
	"""
	self.timeSinceCollis += elapsed
	return self.timeSinceCollis


    def getTime(self):
	"""
	returns the current time since the collision took place
	"""
	return self.timeSinceCollis


