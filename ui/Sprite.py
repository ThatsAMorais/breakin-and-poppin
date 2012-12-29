##### File : Sprite.py
#### Author : Alex Morais
### Description : A visual representation of an object that supports
###		being animated by having defined several tiles to
###		be displayed corresponding with a particular anim step
###		or facing direction.  Given a filename, this class will
###		load the image and its corresponding .ini file and parse
###		the animation steps according to the file specifications.
##


import os, sys
# this is for reading font ini files
from ConfigParser\
	import SafeConfigParser\
	    , ParsingError\
	    , MissingSectionHeaderError\
	    , NoSectionError\
	    , NoOptionError
from PIL import Image
from managers.TextureManager import *
from managers.SettingsManager import *


class Sprite():
    
    def __init__(self, filename=None):

	self.size = [1,1]
	self.halfSize = [self.size[0]/2, self.size[1]/2]
	self.scale = (1,1)

	self.filename = filename
	self.directions = []
	self.numFrames = 0
	self.frameSize = [10,10]
	self.prevDir = 0	# last direction
	self.pos = [0,0]	# current pos
	self.lastPos = [0,0]	# previous pos
	self.facingDir = [1,1]	# the player's current facing direction

	# visibility
	self.visible = True

	# managers
	self.texMgr = None
	self.setsMgr = None

	# our image and corresponding texture id
	self.image, self.texID = None, -1
	self.sprBoxes = []
	self.UP = 0
	self.DOWN = 0
	self.LEFT = 0
	self.RIGHT = 0
	self.UL = 0
	self.UR = 0
	self.DL = 0
	self.DR = 0

	# animation related
	self.animSpeed = 1  # should be overridden by derived classes
	self.tick = 0	# the timer counting update ticks(see '.update')
	self._step = 0

	# the texture box
	self.image, self.texID = None, None
	self.textureBox = None
	self.lastTexBox = None

	# if we have the filename, load the sprite(hope it works)
	if filename:
	    self.setSprite( filename )
	

    def setSprite( self, filename ):
	"""
	Loads the ini file and image according to 'filename'.
	"""

	# grab this if we haven't already
	if not self.texMgr:
	    # We store it to be efficient about retrieving it
	    #	in case we need to use it later.
	    self.texMgr = TextureManager()
	if not self.setsMgr:
	    self.setsMgr = SettingsManager()

	self.config = SafeConfigParser()

	# open the font's info file
	try:
	    self.config.read(\
		    os.path.join( self.setsMgr.home_dir
			, self.setsMgr.media_home
			, self.setsMgr.sprites_dir, filename+'.ini'))
	except ( ParsingError, MissingSectionHeaderError ):
	    # error reading the file
	    raise sys.exc_info()[1], None, sys.exc_info()[2]
	

	#######################
	# Parse the meta-data #
	#######################
	try: # ensure we have 'details' or fail gracefully

	    #############
	    ## 'fname' ##
	    #############
	    try:
		# store the plain-text name
		self.filename = self.config.get('details', 'fname')
	    except NoOptionError:
		self.filename = filename+'.png'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    ##################
	    ## 'directions' ##
	    ##################
	    try:
		# store all of the supported directions
		self.directions= eval( self.config.get('details', 'directions'), {},{})

	    except NoOptionError:
		# missing 'sizes' means that we don't know what sizes
		#   are defined in the file (this parser will not infer
		#   any other sections on its own)
		print 'SpriteLoad:Warning:', fontName,\
			":[details] missing 'directions' list; one frame is assumed."


	    #################
	    ## 'numFrames' ##
	    #################
	    try:
		# this is the number of frames per direction
		self.numFrames = eval(self.config.get('details','numFrames'),{},{})
	    except NoOptionError:
		print 'SpriteLoad:Error:',filename,": [details] missing 'numFrames'"
		raise sys.exc_info()[1], None, sys.exc_info()[2]


	    #################
	    ## 'frameSize' ##
	    #################
	    try:
		# this is the size of each frame
		self.frameSize = eval(self.config.get('details','frameSize'),{},{})
	    except NoOptionError:
		print 'SpriteLoad : Error :', filename,": [details] missing 'frameSize'"
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	except NoSectionError:
	    print 'SpriteLoad:Error:', fontName, ': .ini missing [details] section.'
	    raise sys.exc_info()[1], None, sys.exc_info()[2]


	# load the image through the resource manager
	self.image, self.texID = self.texMgr.load_image(\
		os.path.join(self.setsMgr.sprites_dir, self.filename) )

	imSize = self.image.size
	self.tileWd = imSize[0]/self.numFrames
	
	if len(self.directions) > 0:
	    self.tileHt = imSize[1]/len(self.directions)
	else:
	    self.tileHt = imSize[1]
	
	dir = 0
	for y in range( 0, imSize[1], self.tileHt ):
	    for x in range( 0, imSize[0], self.tileWd):
		self.sprBoxes.append( (x, y+self.tileHt,
					x+self.tileWd, y) )
	
	# store direction offsets based on the order in
	#   self.directions
	offset = 0
	self.directions.reverse()
	for dir in self.directions:
	    if dir == 'U':
		self.UP = offset
	    elif dir == 'D':
		self.DOWN = offset
	    elif dir == 'L':
		self.LEFT = offset
	    elif dir == 'R':
		self.RIGHT = offset
	    elif dir == 'UL':
		self.UL = offset
	    elif dir == 'UR':
		self.UR = offset
	    elif dir == 'DL':
		self.DL = offset
	    elif dir == 'DR':
		self.DU = offset
	    else:
		print dir, ' SpriteLoad:Warning: Do not put things in the'\
			, ' directions list that are not'\
			, '[ U, D, L, R, UL, UR, DL, DR ].'
	    offset += self.numFrames

    def getFrame( self, (hDir, vDir) ):
	"""
	Returns the box of the frame corresponding to the direction
	implied by hDir and vDir and the current animation step.
	"""

	direction = 0

	# Facing Left
	if hDir < 0:
	    # Not facing up or down
	    if vDir == 0:
		direction = self.LEFT
	    # facing up
	    elif vDir < 0:
		direction = self.UL
	    # facing down
	    elif vDir > 0:
		direction = self.DL

	# Facing Right
	elif hDir > 0:
	    # Not facing up or down
	    if vDir == 0:
		direction = self.RIGHT
	    elif vDir < 0:
		direction = self.UR
	    elif vDir > 0:
		direction = self.DR

	# No horizontal movement
	elif hDir == 0:
	    if vDir == 0:
		### special case: 
		direction = self.prevDir
		###
	    elif vDir < 0:
		direction = self.UP
	    elif vDir > 0:
		direction = self.DOWN

	self.prevDir = direction

	# return the box of the frame in the dir and at the
	#   current step, 'self._step'
	return self.sprBoxes[self._step + direction]

    def update(self, elapsed):
	"""
	Updates the animation timer of the player.
	"""
	# This tick keeps track of how many times 'update' is called
	#   on this instance.
	self.tick += 1

	# The animation speed  is on a scale from 1 to 100.  In order
	#   to make speed an ascending scale I subtract the value from
	#   100 and threshold the value above 1.  I do not threshold
	#   to keep below 100 so that (-) speeds can be dynamically
	#   applied, increasing the denominator and lowering speed.
	#   1, on the other hand, is the fastest as it would tick at
	#   every update.
	if self.tick/max(50-self.animSpeed, 1) == 1:
	    self.step()
	    self.tick = 0

    def step( self ):

	# clear the current texture
	self.textureBox = None

	self._step += 1

	# reset the animation when necessary
	if self._step >= self.numFrames:
	    self._step = 0

	# convenience, but not used
	return self._step

    def getQuad( self, scrScroll=[0,0] ):
	"""
	returns the current quad describing their world position
	"""

	# adjust the sprite position on screen by the screen-scroll
	scrPos = ( self.pos[0]-scrScroll[0], self.pos[1]-scrScroll[1] )
	#scrPos = (self.pos)

	if scrPos[0] < 0 and scrPos[1] < 0:
	    # if the entity is out of the screen, don't try to render it
	    return [0,0,0,0]

	self.quad = [ scrPos[0]-self.halfSize[0]
		, scrPos[1]-self.halfSize[1]
		, scrPos[0]+self.halfSize[0]
		, scrPos[1]+self.halfSize[1] ]

	return self.quad
	


    def renderTest( self ):
	"""
	Returns the render-data that would show the sprite sheet on
	the screen in its natural size (possibly exceeding the screen
	extents).  This function must be used directly as Screen will
	not call this naturally.
	"""
	#!# Ignore the visibility for test render
	#if not self.visible:
	#    return []

	return [ (self.texID
		, (0,0,self.image.size[0], self.image.size[0])
		, (0,0,self.image.size[0], self.image.size[0])) ]



    def render(self, scrScroll=(0,0)):
	"""
	Draw the player to the screen
	"""

	# this sprite has been made invisible
	if not self.visible:
	    return []

	# this sprite has not been initialized yet
	if not self.texID:
	    return []

	#print self.facingDir
	textureBox = self.getFrame( self.facingDir )

	#if not self.quad:
	# adjust the sprite position on screen by the screen-scroll
	scrPos = (self.pos[0]-scrScroll[0], self.pos[1]-scrScroll[1])
    
	if scrPos[0] < 0 or scrPos[1] < 0:
	    # if the entity is out of the screen, don't try to render it
	    return []

	self.quad = ( scrPos[0]-self.halfSize[0]
		    , scrPos[1]-self.halfSize[1]
		    , scrPos[0]+self.halfSize[0]
		    , scrPos[1]+self.halfSize[1] )

	self.lastPos = [self.pos[0], self.pos[1]]

	return [ ( self.texID, textureBox, self.quad) ]
    
  
    def scaleSize(self, scale=(1,1)):

	if not scale:
	    scale = self.scale
	
	self.size = ( self.frameSize[0]*scale[0],
			self.frameSize[1]*scale[1] )
	self.halfSize = (self.size[0]/2, self.size[1]/2)


    def setSize( self, size ):
	"""
	Explicitly sets the size
	"""
	self.size = list(size)
	self.halfSize = (self.size[0]/2, self.size[1]/2)


