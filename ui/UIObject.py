#####	   File : UIObject.py
####	 Author : Alex Morais
### Description : Base class for the various ui objects
##

class UIObject():

    def __init__(self):
	"""
	Init: (self)
	"""
	self.pos = [0,0]
	self.size = [1,1]	
	# You probably don't want hidden objects automatically...
	self.visible = True
	self.centerAround = False

    def setPos( self, pos=[0,0] ):
	self.pos = list(pos)

    def center( self, center=True ):
	"""
	Centers this ui object around a position
	"""
	self.centerAround = center

    def CollidePoint(self, pos):

	if self.centerAround:
	    if ( pos[0] >= self.pos[0]-(self.size[0]/2)
		    and pos[0] < self.pos[0]+(self.size[0]/2)
		    and pos[1] >= self.pos[1]-(self.size[1]/2)
		    and pos[1] < self.pos[1]+(self.size[1]/2) ):
		return True
	    return False
	else:
	    if ( pos[0] >= self.pos[0] 
		    and pos[0] < self.pos[0]+self.size[0]
		    and pos[1] >= self.pos[1]
		    and pos[1] < self.pos[1]+self.size[1] ):
		return True
	    return False


    def setVisible( self, visibility=True):
	"""
	Show or hide this object
	"""
	self.visible = visibility


    def toggleVisible( self, value=0 ):
	if self.visible:
	    self.visible = False
	else:
	    self.visible = True

	# The 'value' arg is for compatibility with glutTimerFunc.
	#   In order to be able to call this function using (^), it
	#   has to have this argument.  This allows one to hide or
	#   show a UI object after some interval.

	return self.visible

    def getVisible( self ):
	return self.visible

