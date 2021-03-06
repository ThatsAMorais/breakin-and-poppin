#####	   File : UIText.py
####	 Author : Alex Morais
### Description : 
###		 
##

from types import *
from ui.Font import *
from managers.FontManager import *
from managers.SettingsManager import *
from ui.UIObject import *
from PIL import Image

class UIText(UIObject):

    def __init__( self, value="", pos=[0,0], font=None, scale=10):
	"""
	Init: (self, value="", pos=[0,0], font=None, scale=10)
	"""
	UIObject.__init__(self)
	self.setsMgr = None
	self.pos = pos
	self.value = value
	# string or font object
	self.setFont( font )
	self.setScale(scale)
	self.fontMgr = None
	self.renderList = []


    def render( self, scrScroll=(0,0) ):
	"""
	This is the function called by the screen on all renderable objects.
	"""

	if not self.visible:
	    return []

	# compile a list for each letter to be rendered
	#   ( id, texClipBox, pos, quadBox )

	# if nothing has changed in this object(as would be indicated
	#   by this list being empty) use the previous render list
	#   (this list is reset in "Set" accessors)
	if len(self.renderList) > 0:
	    return self.renderList

	id = self.font.getTexID()

	# the area covered by the string will depend on the length and scale
	self.calcSize()

	# adjust the pos by screen scroll
	pos = (self.pos[0]-scrScroll[0], self.pos[1]-scrScroll[1])
	if self.centerAround:
	    pos = (pos[0]-self.size[0]/2, pos[1]-self.size[1]/2)
	# init to the left pos of first letter
	horizPos = pos[0]

	# loop over all of letters in the text string
	for character in self.value:
	    # build a renderList-item that represents all that is needed
	    #	to put all or part of a texture into a quad of particular
	    #	size at some spot on the screen.
	    self.renderList.append (\
				(id
				, self.font.getCharBox(character)
				, (horizPos, pos[1]
				, horizPos+self.scale[0]
				, pos[1]+self.scale[1])))

	    horizPos = horizPos + self.scale[0]
	
	return self.renderList

    def calcSize( self ):
	"""
	This function calculates the area of this object
	"""
	self.size = [ len(self.value)*self.scale[0], self.scale[1] ]
	self.halfSize = [self.size[0]/2, self.size[1]/2 ]
	return self.size

    def getText( self ):
	"""
	returns the value of the string
	"""
	return self.value

    def setText( self, value="" ):
	"""
	Set the contents of this text object
	"""
	# ...
	self.value = value

	# clear this so it must be rebuilt
	self.renderList = []

	# calculate the size
	self.calcSize()

    def pop( self ):
	"""
	Takes a letter off of the end of the value string
	"""
	self.value = self.value[0:-1]
	# clear this so it must be rebuilt
	self.renderList = []

    def push( self, str ):
	"""
	Puts the input string at the end of the value string
	"""
	self.value += str
	# clear the renderList
	self.renderList = []


    def setFont( self, font=None ):
	"""
	Set the font in which to render this text
	"""
	if not font:
	    return

	elif isinstance( font, types.StringType ):

	    # get the font manager if we haven't already
	    if not self.fontMgr:
		self.fontMgr = FontManager()

	    # load the font into memory
	    self.font = self.fontMgr.loadFont( font )

	elif isinstance( font, Font ):
	    self.font = font

	# clear the letter render list so that it will be rebuilt
	self.renderList = []

    def setPos( self, pos=(0,0) ):
	UIObject.setPos(self, pos)
	# clear the letter render list so that it will be rebuilt
	self.renderList = []

    def setScale( self, factor=0.01 ):
	if not self.setsMgr:
	    self.setsMgr = SettingsManager()

	res = self.setsMgr.screenRes

	self.scale = [res[0]*factor, res[1]*factor]
	# clear the letter render list so that it will be rebuilt
	self.renderList = []


