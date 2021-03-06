#####	   File : Screen.py
####	 Author : Alex Morais
### Description : 
###		 
##

from OpenGL.GLUT import *
from OpenGL.GL import *

class Screen:
    """
    The screen is responsible for drawing textures with OpenGL.  Anything\
 to be rendered to the screen must have a texture ID made by the screen.\
 A state, for example, would request that an image be rendered by calling\
 This and passing the texID returned by MakeTexture.  In other words, \
 the screen is also the texture manager.  No need for abstraction at the time.
    """

    class __impl:
	"""
	The Screen implementation inside of the singleton encapsulation
	"""

	def __init__( self, size=(1,1) ):
	    """
	    Que? ... Eeneet?  Si, esta el eeneet.
	    """
	    self.size = size
	    self.center = (size[0]*0.5, size[1]*0.5)
	    self.scrObjs = []   # objects to be drawn to the screen


	def setSize( self, size=(1,1) ):
	    """
	    Sets the size of the screen
	    """
	    self.size = size
	    self.center = (size[0]*0.5, size[1]*0.5)


	def getSize( self ):
	    return self.size


	def getCenter( self ):
	    return self.center


	#!# Not Being Used, Anymore #!#  (Thankfully)
	def _IntToFloatCoords_(self, intX, intY ):
	    """
	    Converts the two integer coordinates to their floating point
	    """
	    floatX = (intX - self.center[0]) / self.center[0]
	    floatY = (intY - self.center[1]) / self.center[1]	    
	    return (floatX,floatY)


	def drawThis( self, object ):
	    """
	    Adds an object to the screen's list of items to draw to the screen
	    """
	    self.scrObjs.append( object )


	def draw( self ):
	    """
	    The true, internal drawing function that draws the drawList
	    """
	    # loop over the screen objects,
	    #   rendering each in the order they were added.
	    for object in self.scrObjs:
		
		renderList = object.render()

		for item in renderList:
		    # decompose the list
		    id, texBox, quadBox = item
		    
		    # make sure the texture exists
		    self._draw_( id, texBox, quadBox )

	    # clear the list
	    self.scrObjs = []

	def _draw_( self, id, texBox, quadBox ):
	    """
	    Called on each object in the render list to draw it to the screen.
	    """

	    originCrd = (quadBox[0], quadBox[1])
	    extentCrd = (quadBox[2], quadBox[3])

	    # blend function for alpha support
	    glEnable( GL_BLEND )
	    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

	    # Bind to begin with texture number 'id'
	    glBindTexture (GL_TEXTURE_RECTANGLE_NV, id)
	    
	    #*#
	    glBegin( GL_QUADS )

	    ### TL
	    glTexCoord2i( texBox[0], texBox[3] )
	    #glTexCoord2f( 0, 0 )
	    glVertex2f( originCrd[0], extentCrd[1] )

	    ### TR
	    glTexCoord2i( texBox[2], texBox[3] )
	    #glTexCoord2f( 1, 0 )
	    glVertex2f( extentCrd[0], extentCrd[1] )

	    ### BR
	    glTexCoord2i( texBox[2], texBox[1] )
	    #glTexCoord2f( 1, 1 )
	    glVertex2f( extentCrd[0], originCrd[1] )

	    ### BL
	    glTexCoord2i( texBox[0], texBox[1] )
	    #glTexCoord2f( 0, 1 )
	    glVertex2f( originCrd[0], originCrd[1] )

	    glEnd()
	    #*#



    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Screen.__instance is None:
            # Create and remember instance
            Screen.__instance = Screen.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Screen__instance'] = Screen.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)



