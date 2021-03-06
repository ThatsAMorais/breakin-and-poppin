#####	   File : Level.py
####	 Author : Alex Morais
### Description : 
##

class Level():

    def __init__(self):
	"""
	The base-class for game level instances
	"""
	self.animSpeed = 1
	self.tick = 0
	self._step = 0
	self.numFrames = 1


    def update(self, elapsed):
	"""
	Updates the animation of the level (which all moves at the 
	same speed for now).
	"""

	self.tick += 1

	if self.tick/max(100-self.animSpeed, 1) == 1:
	    self.step()
	    self.tick = 0


    def step(self):
	"""
	Steps the animation index +1 or back to 0 to loop.
	"""
	self._step += 1

	if self._step >= self.numFrames:
	    self._step = 0


    def load(self):
	"""
	This does all necessary loading of resources and meta-data, but
	since this is a base class, this functionality will change dependent
	upon the class derived from it.
	"""
	print "BaseClass - Level - load() - Unimplemented"
	pass


    def collidePoint(self, pos=(0,0)):
	"""
	collision function which returns whether the point and a tile of 
	interest collides
	"""
	return False

    def render(self, scrScroll=(0,0)):
	"""
	"""
	print 'BaseClass - Level - render()'
	return []


