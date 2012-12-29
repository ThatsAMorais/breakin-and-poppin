#####	   File : PreBuiltLevel.py
####	 Author : Alex Morais
### Description : 
##

import sys, os
from math import floor
from PIL import Image
from managers.TextureManager import TextureManager
from managers.SettingsManager import SettingsManager
from engine.Screen import Screen
from level.Level import *
from ConfigParser\
	import SafeConfigParser\
	    , ParsingError\
	    , MissingSectionHeaderError\
	    , NoSectionError\
	    , NoOptionError
from collision.Collision import *

class PreBuiltLevel(Level):

    def __init__(self):
        """
        Based on Level, this kind of level is drawn with a maptile image based on a map specification image and the tilekey image.
        The map spec has one pixel for every tile to be drawn.  Tiles are mapped by this class based on the color in the mapspec.  So, if pixel (x,y) = (r,g,b) then the pixel-index in the tilekey image corresponding to (r,g,b) is used to get the correct index from the maptile image to be blitted/collided at (x,y).
        """
	Level.__init__(self)
	# the name of the level repr. by this object
	self.lvlName = None
	self.displayName = "Undefined"

	# store the ref to the screen
	self.screen = Screen()

	# get the resource manager
	self.texMgr = TextureManager()
	self.setsMgr = SettingsManager()

	## level data ##
	# some things we'll be filling at load time
	self.spec, self.specTexID = (None, -1)
	self.tiles, self.tilesTexID = (None, -1)
	self.tileKey, self.keyTexID = (None, -1)
	self.tileSize = (0,0)
	self.tileScrSize = [4,4]
	self.tileHalfSize = [2,2]
	self.scrScroll = [0,0]
	self.mapSize = (0,0)
	self.mapSpec = []
	self.thiefInitPos = (1, 1)
	self.copInitPos = (1, 1)
	self.spriteKey = {}
	self.animSpeed = 20
	self.numTilesInView = [1,1]


    def load( self, lvlName ):
	"""
	Call this to load a level's resources and parse the necessary data
	"""
	self.lvlName = lvlName
	self.config = SafeConfigParser()

	numSprCols = 0
	numSprRows = 0

	try:
	    # attempt to open the input file name
	    successful = self.config.read(\
		os.path.join( self.setsMgr.home_dir
			    , self.setsMgr.media_home
			    , self.setsMgr.levels_dir
			    , self.lvlName
			    , 'info.ini' ))
	except ( ParsingError, MissingSectionHeaderError ):
	    print 'Error:Level:Could not read/find info file'
	    raise sys.exc_info()[1], None, sys.exc_info()[2]

	# The following try/except blocks are separated so that individual messages
	#   can be produced for each missing option
	try:
	    ###########
	    ## level ##
	    ###########
	    try:
	    	self.displayName = eval(self.config.get('level','displayName'))
	    except( NoOptionError ):
	    	pass

	    try:
		# Load the map-spec image
		self.spec, self.specTexID = self.texMgr.load_image(\
			os.path.join( self.setsMgr.levels_dir
				    , self.lvlName
				    , self.config.get('level','specImg')))
	    except( NoOptionError ):
		print 'Error : Level : No Map Spec img specified in info.ini'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    try:
		# Load the map tiles image
		self.tiles, self.tilesTexID = self.texMgr.load_image(\
			os.path.join( self.setsMgr.levels_dir
				    , self.lvlName
				    , self.config.get('level','tileImg')))

	    except( NoOptionError ):
		print 'Error : Level : No tile img specified in info.ini'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    try:
		# load the map-tile key image
		self.tileKey, self.keyTexID = self.texMgr.load_image(\
			os.path.join( self.setsMgr.levels_dir
				    , self.lvlName
				    , self.config.get('level','tileKeyImg')))
	    except( NoOptionError ):
		print 'Error : Level : Missing map-tile key from info.ini'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    ##########
	    ## tile ##
	    ##########
	    try:
		self.tileSize = eval(self.config.get('tile', 'tileSize'), {}, {})
	    except( NoOptionError ):
		print 'Error : Level : Missing tile size info : width, height'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    try:
		numSprCols = eval(self.config.get('tile', 'numCols'), {}, {})
		numSprRows = eval(self.config.get('tile', 'numRows'), {}, {})
	    except( NoOptionError ):
		print 'Error : Level : Missing numCols and Rows in tile image'
		raise sys.exc_info()[1], None, sys.exc_info()[2]

	    try:
		self.tileScrSize = eval(self.config.get('tile', 'scrSize'), {}, {})
	    except( NoOptionError ):
		print 'Warning : Level : Missing "scrSize" in "tile"; assuming the actual tile size.'
		self.tileScrSize = [self.tileSize[0], self.tileSize[1]]

	except( NoSectionError ):
	    print 'Error : Level : Missing section in info.ini', 
	    raise sys.exc_info()[1], None, sys.exc_info()[2]

	# store the map size for future use in a well-afforded place
	self.mapSize = self.spec.size

	# Produce boxes for each tile in the tile-set
	Sprs = []
	for y in range(0, numSprRows*self.tileSize[1], self.tileSize[1]):
	    for x in range(0, numSprCols*self.tileSize[0], self.tileSize[0]):
		Sprs.append( (x, y+self.tileSize[1], x+self.tileSize[0], y) )

	# a double-loop to map sprites to color keys
	for y in range(0, numSprRows):
	    for x in range(0, numSprCols):
		# get the tile-key color for this tile
		color = self.tileKey.getpixel( (x,numSprRows-y-1) )
		self.spriteKey[color] = Sprs[ x + (y*numSprCols) ]

	# convert the map spec from image to list( more efficient )
	#   Get pixel would be too expensive to do so often each frame
	self.mapSpec = self._readMapSpec_()


    def _readMapSpec_( self ):
        """
        Generate the list of colors from the map spec image that represent locations of tiles.
        """
	# the output list
	mapSpec = []

	for y in range( 0, self.mapSize[1] ):
	    for x in range( 0, self.mapSize[0] ):
		# Unpack Pixel Data
		pixel = self.spec.getpixel( (x,y) )

		# 1-1-0 is the Thief's initial position
		if pixel == (255,255,0):
		    self.setThiefMapCoord(x, y)
		    pixel = (255, 255, 255)
		if pixel == (0, 255, 255):
		    self.setCopMapCoord(x, y)
		    pixel = (255, 255, 255)

		# Look for the thief or spot pos
		#   The last one specified in the file is set.
		mapSpec.append( pixel )

	return mapSpec

    def setThiefMapCoord(self, x, y):
	self.thiefInitPos = (x, y)

    def setCopMapCoord(self, x, y):
	self.copInitPos = (x, y)

    def getThiefInitPos(self):
	"""
	Calculates and returns the most current pos based on the
	tileScrSize (player-dependent)
	"""
	return (self.thiefInitPos[0]*self.tileScrSize[0]
		, self.thiefInitPos[1]*self.tileScrSize[1])

    def getCopInitPos(self):
	"""
	Calculates and returns the most current pos based on the
	tileScrSize (player-dependent)
	"""
	return (self.copInitPos[0]*self.tileScrSize[0]
		, self.copInitPos[1]*self.tileScrSize[1])

    
    def setTileSize( self, size=(4,4) ):
	"""
	This sets how big the tile's will be on screen and is not
	related to the size in its texture
	"""
	self.tileScrSize[0] = size[0]
	self.tileScrSize[1] = size[1]
	self.tileHalfSize = [self.tileScrSize[0]/2, self.tileScrSize[1]/2]


    def setTilesPerView(self, numTiles=-1):
	"""
	Set the number of tiles that can be seen within the
	screen at one time
	"""

	# -1 means to show all tiles in the screen
	if numTiles == -1:
	    self.numTilesInView = [ self.mapSize[0]-1, self.mapSize[1]-1 ]
	else:
	    self.numTilesInView = [ numTiles[0], numTiles[1] ]
	
	# grab the screen if we must
	if not self.screen:
	    self.screen = Screen()

	self.setTileSize((1 + (self.screen.size[0] / self.numTilesInView[0])\
			,1 + (self.screen.size[1] / self.numTilesInView[1])))
	

    def getTileSize( self ):
	"""
	Returns the screen size of tiles on the screen
	"""
	return self.tileScrSize


    def render( self, scrScroll=(0,0), visibleArea=None ):
	"""
	Called by the screen object to draw the (visible portion of the) map
	"""
	if not self.screen:
	    self.screen = Screen() 

	if visibleArea:
	    visibleArea[0] = (visibleArea[0]+scrScroll[0]) / self.tileScrSize[0]
	    visibleArea[1] = (visibleArea[1]+scrScroll[1]) / self.tileScrSize[1]
	    visibleArea[2] = (visibleArea[2]+scrScroll[0]) / self.tileScrSize[0]
	    visibleArea[3] = (visibleArea[3]+scrScroll[1]) / self.tileScrSize[1]


	yOffset = scrScroll[1] % self.tileScrSize[1]
	xOffset = scrScroll[0] % self.tileScrSize[0]
	
	# The bounding box of the screen upon the map
	scrArea= [scrScroll[0] / self.tileScrSize[0]
		, scrScroll[1] / self.tileScrSize[1]
		,(scrScroll[0] + self.screen.size[0]) / self.tileScrSize[0]
		,(scrScroll[1] + self.screen.size[1]) / self.tileScrSize[1]]


	# Incr the tile count if there is one more tile to be rendered
	#   on the screen than was calculated, due to the offset
	if yOffset > 0 or self.screen.size[1] % self.tileScrSize[1] > 0:
	    scrArea[3] += 1
	if xOffset > 0 or self.screen.size[0] % self.tileScrSize[0] > 0:
	    scrArea[2] += 1

	renderList = []
	nextPixel = [-xOffset, -yOffset]

	# Loop through the scrArea (per tile)
	for y in range(scrArea[1], scrArea[3]):
	    
	    # skip the index if its out of range
	    if y > self.mapSize[1]:
		continue

	    for x in range(scrArea[0], scrArea[2]):
	    
		# skip the index if its out of range
		if x > self.mapSize[0]:
		    continue

		# Get the color from the mapSpec corresponding to tile[x,y]
		try:
		    #   The color indexes the tileBox array
		    color = self.mapSpec[ x + ( y * self.mapSize[0] ) ]
		except (IndexError):
		    # Index is out of range
		    #print 'Bad Index: ', x + ( y * self.mapSize[0] )
		    #raise sys.exc_info()[1], None, sys.exc_info()[2]
		    continue


		if visibleArea:
		    if x >= visibleArea[0] and x < visibleArea[2]\
			    and y >= visibleArea[1] and y < visibleArea[3]:
			# This quad is the position and area on screen where this
			#   tile will be drawn
			quad = ( nextPixel[0]
				, nextPixel[1]
				, nextPixel[0]+self.tileScrSize[0]
				, nextPixel[1]+self.tileScrSize[1] )
		    
			# add the tile to the list to be returned to the screen
			renderList.append( ( self.tilesTexID    # texture ID
					    , self.spriteKey[color] # tile's bbox
					    , quad ) )	# pos/area on screen
		else:
		    # This quad is the position and area on screen where this
		    #   tile will be drawn
		    quad = ( nextPixel[0]
			    , nextPixel[1]
			    , nextPixel[0]+self.tileScrSize[0]
			    , nextPixel[1]+self.tileScrSize[1] )
		    
		    # add the tile to the list to be returned to the screen
		    renderList.append( ( self.tilesTexID    # texture ID
					, self.spriteKey[color] # tile's bbox
					, quad ) )	# pos/area on screen

		# increment the pixel location
		nextPixel[0] += self.tileScrSize[0]
	
	    # reset the x pixel location
	    nextPixel[0] = -xOffset
	    # decrement the pixel location
	    nextPixel[1] += self.tileScrSize[1]

	return renderList


    def getTileAtPoint(self, pos):
	"""
	Returns the type of tile in which the given position(in map-space)
	resides, and the modulous of the tile division which shows where in
	the tile they are.
	"""

	# ... This is relevant because the specPos division
	# provides the floor.  This all goes back to the map being based on
	# a 1:1 pixel-to-tile mapping.  So, determining which tile is under
	# a position requires scaling down the position to the mapSpec
	# space and finding the tile at that pixel location.  since the
	# value is truncated, the collision was workin on one side, but not
	# for the other.  
	
	## Convert from tile to pixel coord
	specPos = [ int(floor(pos[0] / self.tileScrSize[0]))
		    , int(floor(pos[1] / self.tileScrSize[1])) ]
	
	modOfPos = [ (pos[0] % self.tileScrSize[0])
		    , (pos[1] % self.tileScrSize[1]) ]

	try:
	    ## Grab the color at specPos in the mapSpec
	    Red,Grn,Blu = self.mapSpec[specPos[0]+(specPos[1]*self.mapSize[0])]
	except:
	    print 'bad index'
	    return (None, None)

	box = [ specPos[0], specPos[1]
		, specPos[0]+self.tileScrSize[0]
		, specPos[1]+self.tileScrSize[1] ]

	## Look for particular Colors
	# Base : 1-0-0
	if Red==255 and Grn==0 and Blu==0:
	    return ('base', modOfPos)
	# Building : (0-0.2-0), (0-0.4-0), (0-0.6-0), (0-0.8-0), (0-1-0)
	elif Red==0 and Grn > 0 and Blu==0:
	    return ('building', modOfPos)
	# Drop Point : 0-0-1
	elif Red==0 and Grn==0 and Blu==255:
	    return ('drop-point', modOfPos)
	# X-X-X
	else:
	    return (None, None)







