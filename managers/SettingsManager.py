#####	   File : SettingsManager.py
####	 Author : Alex Morais
### Description : 
##

import os
# this is for reading the configuration file
from ConfigParser\
	import SafeConfigParser\
	    , ParsingError\
	    , MissingSectionHeaderError\
	    , NoSectionError\
	    , NoOptionError

# Base Class
class SettingsManager():
    """
    a singleton manager that serves as an easily accessible repo
    for all of the engine's settings (i.e. game res, media directories)
    """

    class __impl:
	"""
	the actual settings manager implementation
	"""

	def __init__(self):

	    # the config file
	    self.config = None

	    # [video]
	    self.screenRes = (800, 600)
	    self.fullscreen = False

	    # [audio]

	    # [dirs]
	    self.home_dir = os.getcwd()
	    self.media_home = os.path.join(self.home_dir, 'data')
	    self.font_dir = os.path.join(self.media_home, 'font')
	    self.levels_dir = os.path.join(self.media_home, 'levels')
	    self.sprites_dir = os.path.join(self.media_home, 'sprites')
	    self.ui_dir = os.path.join(self.media_home, 'UI')
	    self.music_dir = os.path.join(self.media_home, 'music')
	    self.sounds_dir = os.path.join(self.media_home, 'sounds')

	    # [player]
	    self.player_name = "Player"
	    self.controller = "keyboard"

	    # attempt to open the settings.ini
	    self.loadSettings()

	def loadSettings( self, settingsFileName='settings' ):
	    """
	    Load the settings from the settings.ini.  The filename arg
	    shouldn't contain the extension (i.e. no '.ini' is needed).
	    Furthermore, your settings file should use .ini extension and
	    be placed in "GAMEFOLDER/data/" or it will not be found.
	    """
	    self.config = SafeConfigParser()

	    # open the font's info file
	    try:
		# attempt to open the input file name
		self.config.read( os.path.join(os.getcwd()
		    , 'data', settingsFileName+'.ini') )

	    except ( ParsingError, MissingSectionHeaderError ):

		print 'SettingsManager : Warning : loading default settings'

		# attempt to load the default settings
		try:
		    self.config.read(os.path.join(os.getcwd(),'data','settings.ini'))
		    print "Settings.ini found!"
		except ( ParsingError, MissingSectionHeaderError ):
		    print 'SettingsManager : Error : unable to open settings.ini'
		    # error reading the file
		    return # straight to your room w/o dessert
	    
	    ###################
	    ## Parse [video] ##
	    ###################
	    try: # ensure we have [video] or fail gracefully

		###########
		## 'res' ##
		###########
		try:
		    # store the plain-text name
		    self.screenRes = eval(self.config.get('video','res'),{},{})
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[video] section missing 'res'; defaulting to 800x600"

		##################
		## 'fullscreen' ##
		##################
		try:
		    # store the plain-text name
		    self.fullscreen = eval(self.config.get('video','fullscreen'),{},{})
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[video] section missing 'fullscreen'; defaulting to True"

	    except NoSectionError:
		print 'SettingsLoad:Error:', settingsFileName, ': .ini missing [video] section.'

	    ###################
	    ## Parse [audio] ##
	    ###################
	    #try: # ensure we have [video] or fail gracefully
	    #except NoSectionError:
	    #	print 'SettingsLoad:Error:', settingsFileName, ': .ini missing [audio] section.'

	    ##################
	    ## Parse [dirs] ##
	    ##################
	    try:

		################
		## 'home_dir' ##
		################
		try:
		    # get the value so we can check for -default-
		    home_dir_val = self.config.get('dirs','home_dir')

		    # if -default- use the cwd
		    if home_dir_val == '-default-':
			self.home_dir = os.getcwd()
		    else:
			# store the user's preference
			self.home_dir = home_dir_val
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'home_dir'; defaulting to cwd()"

		##################
		## 'media_home' ##
		##################
		try:
		    # store the plain-text name
		    self.media_home = self.config.get('dirs','media_home')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'media_home'; defaulting to 'media'"

		################
		## 'font_dir' ##
		################
		try:
		    # store the plain-text name
		    self.font_dir = self.config.get('dirs','font_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'font_dir'; defaulting to 'fonts'"

		##################
		## 'levels_dir' ##
		##################
		try:
		    # store the plain-text name
		    self.levels_dir = self.config.get('dirs','levels_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'levels_dir'; defaulting to 'levels'"

		###################
		## 'sprites_dir' ##
		###################
		try:
		    # store the plain-text name
		    self.sprites_dir = self.config.get('dirs','sprites_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'sprites_dir'; defaulting to 'sprites'"

		##############
		## 'ui_dir' ##
		##############
		try:
		    # store the plain-text name
		    self.ui_dir = self.config.get('dirs','ui_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'ui_dir'; defaulting to 'UI'"

		#################
		## 'music_dir' ##
		#################
		try:
		    # store the plain-text name
		    self.music_dir = self.config.get('dirs','music_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'music_dir'; defaulting to 'music'"

		##################
		## 'sounds_dir' ##
		##################
		try:
		    # store the plain-text name
		    self.sounds_dir = self.config.get('dirs','sounds_dir')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad:Warning:", settingsFileName\
			,":[dirs] section missing 'sounds_dir'; defaulting to 'sounds'"


	    except NoSectionError:
		print 'SettingsLoad:Error:', settingsFileName\
			, ': .ini missing [dirs] section.'

	    
	    ####################
	    ## Parse [player] ##
	    ####################
	    try:

		####################
		## 'player_name' ##
		####################
		try:
		    # store the plain-text name
		    self.player_name= self.config.get('player','player_name')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad : Warning :", settingsFileName\
			,":[player] section missing 'default_name'; defaulting to 'Player'"

		####################
		## 'controller' ##
		####################
		try:
		    # store the plain-text name
		    self.controller = self.config.get('player','controller')
		except NoOptionError:
		    # missing name is no big deal, but warn the user
		    print "SettingsLoad : Warning :", settingsFileName\
			,":[player] section missing 'controller'; defaulting to 'keyboard'"

	    except NoSectionError:
		print 'SettingsLoad:Error:', settingsFileName\
			, ': .ini missing [dirs] section.'

	def saveSettings( self ):
	    """
	    Outputs an .ini of the current settings so they can be
	    recalled on the next execution.
	    """
	    print "Settings saving is unimplemented for now"
	    pass

    # storage for the instance reference
    __instance = None
    
    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if SettingsManager.__instance is None:
            # Create and remember instance
            SettingsManager.__instance = SettingsManager.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_SetMgr__instance'] = SettingsManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)



