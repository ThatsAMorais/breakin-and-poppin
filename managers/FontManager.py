#####	   File : FontManager.py
####	 Author : Alex Morais
### Description : The font manager manages all of the font objects
###		    created by the game.  If a font is loaded, that
###		    instance is used any time that font is requested.
###		    It does this by handling font loading.  All fonts are
###		    loaded through it.  The Singleton class is used to
###		    make sure only one of these exists.
##

from ui.Font import Font

class FontManager:
    """
    ### Description : The font manager manages all of the font objects
    ###		    created by the game.  If a font is loaded, that
    ###		    instance is used any time that font is requested.
    ###		    It does this by handling font loading.  All fonts are
    ###		    loaded through it.  The Singleton class is used to
    ###		    make sure only one of these exists.
    ##
    """

    class __impl:
	"""
	the font manager implementation
	"""

	def __init__(self):
	    self.fonts = {}
		
	def loadFont(self, fontName):

	    # if the font hasn't already been loaded
	    if not fontName in self.fonts:
		# make the font and store a ref in this mgr
		font = Font(fontName)
		self.fonts[fontName] = font
		
	    # return the font (ready or not)
	    return self.fonts[fontName]
	
    # storage for the instance reference
    __instance = None
    
    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if FontManager.__instance is None:
            # Create and remember instance
            FontManager.__instance = FontManager.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_FontMgr__instance'] = FontManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


