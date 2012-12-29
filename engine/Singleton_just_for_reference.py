#####	   File : ResourceManager.py
####	 Author : Alex Morais
### Description : 
##

import os, types
from PIL import Image

class TextureManager():
    """
    This is a singleton class that holds the 
    """

    __instances = {}

    def __init__( self, klass ):
        """ Create singleton instance """
        # Check whether we already have an instance
	if type(klass) in GetManager.__instances:
	    # Create and remember instance
            ResourceManager.__instance = GetManager.klass(args)

        # Store instance reference as the only member in the handle
        self.__dict__['_RsrcMgr__instance'] = ResourceManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


