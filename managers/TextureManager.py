#####	   File : TextureManager.py
####	 Author : Alex Morais
### Description : 
##

import os, types
from OpenGL.GL import *
from PIL import Image
from managers.SettingsManager import *

class TextureManager():
    """
    This is a singleton class that contains the texture manager
    """

    class __impl:
	""" The actual Texture Manager class"""
	
	def __init__(self):
	    # this is the image cache keyed by the path to the image
	    self.data = {}
	    self.textures = {}  # texture ids
	    self.sizeOf = {}    # { textureID : size, ... }

	    self.setsMgr = SettingsManager()

	def _makeTexture_(self, path):
	    """
	    makes a texture for the image passed in.  All images get one tex
	    that the requesting objects must themselves sub-divide and convey
	    to the screen object.
	    """
	    im = self.data[path]

	    # make sure we haven't already instantiated this images texture
	    if path in self.textures:
		return self.textures[path]

	    try:
		# get image meta-data (dimensions) and data
		width, height = im.size[0], im.size[1]
		sprite = im.tostring( "raw", "RGBA", 0, -1 )
	    except SystemError:
		# has no alpha channel, synthesize one, see the
		# texture module for more realistic handling
		width, height, sprite = im.size[0], im.size[1], im.tostring()

	    # enable the texture rect for indexing textures using pixels
	    glEnable( GL_TEXTURE_RECTANGLE_NV )

	    # Generate one texture ID
	    id = glGenTextures(1)
	    glBindTexture( GL_TEXTURE_RECTANGLE_NV, id )
	    
	    # Texture params(must have)
	    #glTexParameteri(GL_TEXTURE_RECTANGLE_NV, GL_TEXTURE_WRAP_S, GL_REPEAT)
	    #glTexParameteri(GL_TEXTURE_RECTANGLE_NV, GL_TEXTURE_WRAP_T, GL_REPEAT)
	    glTexParameteri(GL_TEXTURE_RECTANGLE_NV, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	    glTexParameteri(GL_TEXTURE_RECTANGLE_NV, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	    # this may still be necessary
	    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

	    try:
		#TODO: Fix the frequent crash on this statement ###
		# Write the 32-bit RGBA texture buffer to video memory
		glTexImage2D( GL_TEXTURE_RECTANGLE_NV, 0, GL_RGBA
			, width, height, 0, GL_RGBA
			, GL_UNSIGNED_BYTE, sprite )
	    except OpenGL.error.GLError:
		print 'OpenGL error!'

	    self.textures[path] = id
	    return id


	def load_image(self, path):
	    """
	    loads in image using PIL
	    """
	    # make sure the file hasn't already been loaded before
	    #   it is reopened.
	    if path not in self.data:
		fullPath = os.path.join( self.setsMgr.home_dir
					, self.setsMgr.media_home
					, path )
		#try: #but not until we actually encounter the
		#	error; don't want to cover it up
		self.data[path] = Image.open(fullPath)
		#except:
	
	    # make a texture for the image
	    id = self._makeTexture_( path )
	    
	    # save the texture id and image size
	    self.sizeOf[id] = self.data[path].size

	    # return this image
	    return self.data[path], id

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if TextureManager.__instance is None:
            # Create and remember instance
            TextureManager.__instance = TextureManager.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_TexMgr__instance'] = TextureManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)



