#####	   File : EngineState.py
####	 Author : Alex Morais
### Description : The game determines what is happening on screen
###		 based on what state the GameEngine instance has.
##

import os, sys, time
from OpenGL.GLUT import glutTimerFunc
from subprocess import Popen
from platform import system
from ui.Font import *
from ui.UIText import *
from ui.UIImage import *
from managers.SettingsManager import *
from managers.FontManager import *
from engine.Screen import *
from level.PreBuiltLevel import *

class EngineState():

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	# the game engine that owns this state
	self.engine = engine # TRYING TO DEPRECATE
	self.screen = Screen()
	self.res = self.engine.setsMgr.screenRes
	res = self.res

	# get/load the font
	self.font = FontManager().loadFont( 'JohnDoe' )
	self.str_paused = UIText( "Paused", [res[0]*0.5, res[1]*0.5]
				, self.font, 35 )
	self.str_paused.setVisible(False)

	
	gameWorld = self.engine.gameWorld
	#gameWorld.setPlayerType( 'Cop' )
	gameWorld.setPlayerType( 'Robber' )
	#gameWorld.getPlayer().setName( "Alfonso" )

	# This is an optimization...
	# If using the Cop player type, use the smaller tiles
	if gameWorld.getPlayer().getType() == "Cop":
	    gameWorld.setLevelByName( 'Level1XS' )
	else:
	    gameWorld.setLevelByName( 'Level1L' )

	glutTimerFunc(50, self.engine.on_update, 50)

    def renderFrame(self):
	""" RenderFrame - Base Class """
	if not self.screen:
	    self.screen = Screen()

	self.screen.drawThis( self.str_paused )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == '\x1b':
	    return None

	# for now, this means to "spawn a server"
	if key == 'x':
	    if system() == "Linux" or system() == "Macintosh":
		Popen( [r'/usr/bin/python/python'
		    ,os.path.join( self.engine.setsMgr.home_dir
				    , 'StartServer.py' )] )
	    elif system() == "Windows":
		Popen([r'C:\Python25\python.exe'
		    ,os.path.join( self.engine.setsMgr.home_dir
				    , 'StartServer.py' )])
	    else:
	    	print "you are on an unsupported platform for spawning a server"
	    # declare that this game instance is the server owner
	    self.engine.serverOwner = True
	    
	# for now, its "connect"
	elif key == 'c':
	    self.engine.connect()

	elif key == 'v':
	    self.engine.disconnect()

	elif key == 'g':
	    self.str_paused.toggleVisible()
	    self.engine.gameWorld.pause()

	return self

    def on_key_release(self, key, x, y):
	"""
	On key release
	"""
	return self

    def on_specialkey_press(self, key, x, y):
	"""
	On special key press
	"""
	return self

    def on_specialkey_release(self, key, x, y):
	"""
	On special key release
	"""
	return self

    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	self.engine.gameWorld.startGame()
	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse
	"""
	return self

    def on_socket(self, packet):
	"""
	On socket
	"""
	self.gameTime = packet['time']
	return self

    def update(self, elapsed):
	"""
	switches the state based on 
	"""
	return self


