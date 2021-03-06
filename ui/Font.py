#####	   File : Font.py
####	 Author : Alex Morais
### Description : This is the font class that is responsible for
###		parsing an ini file (currently using 'eval' which
###		loading an image of letters/numbers
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

class Font:
    """
    An encapsulation of a font to be used by UIText objects
    """

    def __init__( self, fontName=None ):
	"""
	This class represents a font to be rendered for UIText.
	"""
	# store the fontname for FYI's sake (might want to know this)
	self.fname = fontName
	self.letterSize = (1,1)
	self.tilesX = 0

	# get the singleton texture manager reference(see TextureManager)
	self.texMgr = TextureManager()
	self.setsMgr = SettingsManager()

	# font map image
	self.image = None
	self.imSize = (0,0)
	# font map texture id
	self.texID = None
	# an image returned if a letter/digit is not in the font
	self.NotDefined, self.NoDefID = self.texMgr.load_image(os.path.join('NotDefined.png'))
	
	### the following two lists are parallel
	#	-->	[<lower>,<upper>,<num>]
	# these bools tell what the font has defined(lowercase, uppercase, numbers)
	self.blockHt = {'lower':0, 'upper':0, 'digits':0}
	# the images corresponding to the respective letter and number
	self.alphabet = {}
	self.alphabetBox = {}

	# this determines if a font was loaded properly.
	self.ready = False
	self.config = None

	# process the font if it is provided
	if fontName:
	    self.setFont( fontName )
	# ...otherwise wait until defined


    # set and setup the visual representation of the font
    def setFont( self, fontName ):
	"""
	Sets the font represented by this class and loads it into
	the class by reading the font's respective <font-name>.ini
	and then cutting
	"""
	self.config = SafeConfigParser()
	self.ready = False

	# open the font's info file
	try:
	    self.config.read(os.path.join( self.setsMgr.home_dir, self.setsMgr.media_home
					, self.setsMgr.font_dir, fontName+'.ini'))
	except ( ParsingError, MissingSectionHeaderError ):
	    # error reading the file
	    return # straight to your room w/o dessert
	
	#######################
	# Parse the meta-data #
	#######################
	try: # ensure we have 'details' or fail gracefully

	    #############
	    ## 'fname' ##
	    #############
	    try:
		# store the plain-text name
		self.fname = self.config.get('details', 'fname')
	    except NoOptionError:
		# missing name is no big deal, but warn the user
		print "FontLoad:Warning:", fontName\
			,":[details] section missing 'fname'."


	    ############
	    ## 'size' ##
	    ############
	    try:
		# store all of the sizes available to this
		self.letterSize = eval( self.config.get('details', 'letterSize'), {},{})
	    except NoOptionError:
		# missing 'sizes' means that we don't know what sizes
		#   are defined in the file (this parser will not infer
		#   any other sections on its own)
		print 'FontLoad:Error:', fontName,\
			":[details] missing 'size' list"
		return # return failed


	    ################
	    ## 'tilesX/Y' ##
	    ################
	    try:
		self.tilesX = eval(self.config.get('details','tilesX'),{},{})
	    except NoOptionError:
		print 'FontLoad:Error:', fontName,": [details] missing 'tilesX'"
		return # return failed

	    ###################
	    ## block-heights ##
	    ###################
	    try:
		self.blockHt['lower'] = eval(self.config.get('details','htLower'),{},{})
	    except NoOptionError:
		# ignore quietly
		pass

	    try:
		self.blockHt['upper'] = eval(self.config.get('details','htUpper'),{},{})
	    except NoOptionError:
		# ignore quietly
		pass

	    try:
		self.blockHt['digits'] = eval(self.config.get('details','htNum'),{},{})
	    except NoOptionError:
		# ignore quietly
		pass

	    try:
		self.blockHt['symbols'] = eval(self.config.get('details','htSym'),{},{})
		self.suppSyms = eval( self.config.get('details', 'symbols'), {}, {} )
	    except NoOptionError:
		# clear what might have been done
		self.blockHt['symbols'] = 0
		self.suppSyms = []
		print 'Warning : Font : symbols load failed'
		# and ignore quietly... just waaalk away, .. nice and slow now.... nothing to see heere..
		pass

	    # validate that this font defines at least one of the four
	    if self.blockHt['lower']+self.blockHt['upper']+\
		    self.blockHt['digits']+self.blockHt['symbols'] == 0:
		print 'FontLoad:Error:', fontName,\
			":[details] must specify block ht for all letter/number sets in image"
		return # the font must specify 

	except NoSectionError:
	    print 'FontLoad:Error:', fontName, ': .ini missing [details] section.'
	    return # a font requires this section, return unsuccessfully

	########################
	# Load/Parse the image #
	########################
	#self.NotDefined, self.NoDefID = self.texMgr.load_image(os.path.join('fonts','NotDefined.png'))

	# load the image through the resource manager
	self.image, self.texID = self.texMgr.load_image( os.path.join(self.setsMgr.font_dir, self.fname) )

	if not self.image:
	    print 'FontLoad:Error:', fontName,\
		    ":Image load was unsuccessful with path,",\
		    os.path.join(self.setsMgr.home_dir, self.setsMgr.media_home
				, self.setsMgr.font_dir, self.fname)
	    return # image load failed

	E = []
	if self.blockHt['lower'] > 0:
	    # the following extensions are ordered deliberately
	    E.extend( map(chr, range(97, 123)) )
	    # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
	    #, 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	if self.blockHt['upper'] > 0:
	    E.extend( map(chr, range(65, 91)) )
	    # ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'
	    #, 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	if self.blockHt['digits'] > 0:
	    E.extend( map(str, range(0, 10)) )
	    # [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
	if self.blockHt['symbols'] > 0:
	    E.extend( self.suppSyms )	# include the supported symbols acc. to the .ini
	
	x, y = (0, 0)

	# might be useful later
	self.imSize = self.image.size

	# loop over image calculating boxes
	for letter in E:
	    # the area of the image containing 'this' letter
	    box = ( x, self.imSize[1]-y, x+self.letterSize[0]
		    , self.imSize[1] - (y+self.letterSize[1]) )
	    # throw it onto the list
	    self.alphabet[letter] = self.image.crop( box )
	    self.alphabetBox[letter] = box

	    #print letter, x, y

	    # increment the x forward
	    x = x + self.letterSize[0]
	    # check if at z
	    if letter == 'z' or letter == 'Z' or letter == '9' or letter == ' ':
		x = 0
		y = y + self.letterSize[1]
	    elif x/self.letterSize[0] >= self.tilesX:
		x = 0
		y = y + self.letterSize[1]
	
	# this is only set in the event that this function completed
	#   all necessary actions and is ready for use.
	self.ready = True
	return


    # gets a letter/digit image from the font at destSize
    #	DEPRECATED: its inefficient to chop up the image into separate textures
    #		    as opposed to indexing boxes into a single one (see getCharBox)
    def getChar( self, character, destSize ):

	# this is for transforming the image to the desired size
	data = ( 0, 0, self.letterSize[0], self.letterSize[1] )

	if character in self.alphabet:
	    return self.alphabet[character].transform(destSize, Image.EXTENT, data)
	elif character.swapcase() in self.alphabet:
	    return self.alphabet[character.swapcase()].transform(destSize, Image.EXTENT, data)

	# the letter is not defined (return the empty image)
	return self.NotDefined.transform(destSize,Image.EXTENT,data)


    # Returns the box of a character in the font
    def getCharBox( self, character ):
	"""
	Returns the box of a character in the font
	"""
	# get the character from the alphabet
	if character in self.alphabetBox:
	    #print character, self.alphabetBox[character]
	    return self.alphabetBox[character]
	elif character.swapcase() in self.alphabetBox:
	    #print character, self.alphabetBox[character.swapcase()]
	    return self.alphabetBox[character.swapcase()]

	print 'Bad Character:', character
	# return the NoDef image
	return (0, 0, self.NotDefined.size[0], self.NotDefined.size[1])

    # Returns the font's texture id
    def getTexID( self ):
	"""
	Returns the font's texture id
	"""
	return self.texID

    # This is the function called by the screen on all renderable objects.
    def render( self, scrScroll=(0,0) ):
	"""
	This is a test function and not intended for use in the game, but
	who am I to judge what's in a game..
	"""
	setMgr = SettingsManager()
	# returns the id, texBox, position, and a quadBox in pixel coords
	return [ (self.texID
		, ( 0, self.image.size[1], self.image.size[0], 0 )
		, ( 0, 0, setMgr.screenRes[0], setMgr.screenRes[1] )) ]

    
