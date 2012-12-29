#####	   File : UIImage.py
####	 Author : Alex Morais
### Description : A screen object composed of a single image
###		 
##

from managers.TextureManager import *
from managers.SettingsManager import *
from ui.UIObject import *

class UIImage(UIObject):

    def __init__( self, imgName=None, pos=[0,0], size=[1,1]):
	"""
	An image on the screen for UI purposes (clickable or not)
	"""
	# Base class constructor
	UIObject.__init__(self)

	self.pos = pos
	self.size = size
	self.image = None   # the actual image file
	self.texID = None   # the texture id created for this image
	self.imgBox = None  # the bounding box (usually from 0 to size)
	self.quad = None    # the box repr the area and pos on the screen
	self.imgFileName = imgName
	self.texMgr = None
	self.setsMgr = SettingsManager()


	# if an image is specified, load it
	if self.imgFileName:
	    self.setImg( self.imgFileName )

    def setSize( self, size=(1,1) ):
	self.size = size

    def setPos( self, pos=[0,0] ):
	UIObject.setPos(self)

	self.quad = None

    def setImg( self, imgName=None ):

	if imgName:
	    if not self.texMgr:
		self.texMgr = TextureManager()

	    self.image, self.texID = self.texMgr.load_image(\
				os.path.join(self.setsMgr.ui_dir,imgName))

	else:
	    self.image = None
	    self.imgBox = None
	    self.quad = None

    def render( self, scrScroll=(0,0) ):
	"""
	Called by the screen on this object to retrieve all necessary info
	regarding the rendering of this object.  The name and arguments for
	this function should not be changed as it will not be known by the
	Screen class.
	"""

	# make sure an image has been loaded before we try and render
	if not self.image:
	    print "No image loaded"
	    return []

	if not self.visible:
	    return []

	# we want the whole image to show, so we provide the entire size as
	#   the texture coords
	if not self.imgBox:
	    self.imgBox = (0, self.image.size[1], self.image.size[0], 0)

	if not self.quad:
	    pos = ( self.pos[0]-scrScroll[0], self.pos[1]-scrScroll[1])

	    if self.centerAround:
		pos = (pos[0]-self.size[0]/2, pos[1]-self.size[1]/2)

	    self.quad = (pos[0], pos[1], pos[0]+self.size[0], pos[1]+self.size[1])

	# return this as a list with one object in it(because screen expects a
	#   list of renderable things from 
	return [ ( self.texID, self.imgBox, self.quad) ]



