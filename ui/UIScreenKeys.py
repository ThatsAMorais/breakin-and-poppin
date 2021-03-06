#####	   File : UIScreenKeys.py
####	 Author : Alex Morais
### Description : 
###		 
##

from ui.Font import *
from managers.FontManager import *
from ui.UIObject import *

class UIScreenKeys(UIObject):

    def __init__( self, value="", pos=[0,0], font=None, scale=10):
	"""
	Init: (self, value="", pos=[0,0], font=None, scale=10)
	"""
	UIObject.__init__()

	self.pos = pos
	self.value = value
	# string or font object
	self.setFont( font )
	self.scale = scale
	self.fontMgr = None
	self.renderList = []


    def render( self, scrScroll=(0,0) ):
	"""
	"""
	if not self.visible:
	    return []

	if len(self.renderList) > 0:
	    return self.renderList
	
