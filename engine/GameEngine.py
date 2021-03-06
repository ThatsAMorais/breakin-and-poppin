#####	   File : GameEngine.py
####	 Author : Alex Morais
### Description	: The main game client
##

import os, sys, socket
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from states.EngineState import *
from states.AllStates import TitleScreenState, WinnerState, LoserState

from managers.TextureManager import *
from managers.FontManager import *
from managers.SettingsManager import *
from engine.Screen import *
from engine.GameWorld import *
from input.Keyboard import *
from input.Mouse import *

# we're inheriting the client functionality for multiplayer use
from multiplayer.Client import *

class GameEngine(Client):
    """
    The main game client:
      The game engine sends GLUT events to a gamestate class that
      manages what is happening on the screen.  It also handles
      server communication.
    """

    def __init__(self):
	"""
	Initializes the game client
	"""
    
	# since our game client is a client...
	Client.__init__(self)

	self.setsMgr = SettingsManager()
	self.res = self.setsMgr.screenRes

	self._InitGLUT_()
	self._InitGL_()

	# Make a screen object - we want to make the first here
	#   so that we can ensure the size is set appropriately.
	#   All other objects using the screen-singleton will assume
	#   it is has already been sized and, thus, won't call setSize.
	self.screen = Screen()
	self.screen.setSize( self.res )

	# be the first entity to create the managers
	self.rsrcMgr = TextureManager()
	self.fontMgr = FontManager()

	self.connected = False
	self.serverOwner = False
	self.serverName = "default"

	# the gameworld is mostly undefined at this point
	self.gameWorld = GameWorld()
	
	# this variable denotes for certain game states whether
	#   the user 'start'-ed or 'join'-ed a server so they know
	#   which state to return to when the user pushes 'back'
	self.statePath = None
	# create the initial game state
	self.gState = TitleScreenState(self)
	#self.gState = EngineState(self)


    def _InitGLUT_(self):
	"""Initialize GLUT"""
	glutInit()
	#*# Create/Initialize the Window
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
	glutInitWindowPosition( 0,0 )
	glutInitWindowSize( self.res[0], self.res[1] )

	self.window = glutCreateWindow( "Breakin & Poppin" )

	#*# setup the event handlers
	glutDisplayFunc(self.renderFrame)
	glutIdleFunc(self.on_tick)
	#glutReshapeFunc(self.changeSize)
	# keyboard
	glutKeyboardFunc( self.on_key_press )
	glutKeyboardUpFunc( self.on_key_release )
	glutIgnoreKeyRepeat( 1 ) # !=0 disables key repeat callbacks
	glutSpecialFunc( self.on_specialkey_press )
	glutSpecialUpFunc( self.on_specialkey_release )
	glutMouseFunc( self.on_mouse )
	glutPassiveMotionFunc( self.on_mouse_motion )
	
	#glutFullScreen()


    def _InitGL_(self):
	"""Initialize GL"""
	# Set up the rendering environment

	# setup the orthographic projection (firstly)
	glMatrixMode( GL_MODELVIEW )
	glPushMatrix()
	glLoadIdentity()

	# Set up the orthographic projection
	glOrtho(0, self.res[0], 0, self.res[1], -1, 1)
	# invert the y axis, down is positive
	glScalef(1, -1, 1)
	# mover the origin from the bottom left corner
	# to the upper left corner
	glTranslatef(0, -self.res[1], 0)

	# turn off the lighting and depth testing
	glPushAttrib( GL_DEPTH_BUFFER_BIT | GL_LIGHTING_BIT )
	glDisable( GL_LIGHTING )
	glDisable( GL_DEPTH_TEST )
	glDisable( GL_DITHER )	

    def on_key_press(self, key, x, y):
	"""On key press"""
	if self.gState:
	    self.gState = self.gState.on_key_press(key, x, y)

    def on_key_release(self, key, x, y):
	"""On key release"""
	if self.gState:
	    self.gState = self.gState.on_key_release(key, x, y)
	
    def on_specialkey_press(self, key, x, y):
	"""On special key press"""
	# game state
	if self.gState:
	    self.gState = self.gState.on_key_press(key, x, y)

    def on_specialkey_release(self, key, x, y):
	"""On special key release"""
	# game state
	if self.gState:
	    self.gState = self.gState.on_key_release(key, x, y)	

    def on_mouse_motion(self, x, y):
	"""On mouse motion"""
	# game state 
	if self.gState:
	    self.gState = self.gState.on_mouse_motion(x, y)

    def on_mouse(self, button, state, x, y):
	"""On mouse press/release"""
	# game state
	if self.gState:
	    self.gState = self.gState.on_mouse(button, state, x, y)

    def on_update(self, elapsed):
	"""
	The function that updates every object's animation status (45ms)
	"""

	# update the game state
	if self.gState:
	    self.gState = self.gState.update(elapsed)

	# gameworld
	self.gameWorld.update(elapsed)

	# gamestate
	glutTimerFunc(50, self.on_update, 50)	

    def on_socket( self, elapsed):
	"""
	"""
	# call the base class version (returns the packet)
	packet = Client.on_socket(self, elapsed)

	if packet != None:
	    #print 'client - recv - got a packet'
	    self.readPacket( packet )	# the real meat of this
	else:
	    # Oh well, no packet for some reason
	    pass

	glutTimerFunc(20, self.on_socket, 20)
	
    ###
    def readPacket(self, packet):
	"""
	This interpets a packet sent by the server
	"""

	# This case is usually handled by the GameEngine side
	#   (But this class isn't supposed to know that. :P)
	if packet['type'] == 'update':
	    #print 'Client : Got an update : ', packet
	
	    if self.connected:

		if self.gState:
		    # let the game state handle some bih'ness
		    self.gState= self.gState.on_socket(packet)


		if self.gameWorld:
		    self.gameWorld.on_socket(packet)

		# if the level is different or non-existant, load it
		#if not self.gameWorld.getLevel() \
		#	    or (packet['level'] != self.gameWorld.getLevelName()):
		#	self.gameWorld.setLevelByName( packet['level'] )


	if packet['type'] == 'message':
	    #print 'Client : Got a message : ', packet

	    # Connection Reset by Peer
	    if 'CRbP' in packet:
		print 'Disconnected: The server connection is dead.'
		self.disconnect()

	    # The server is full
	    if 'ServerFull' in packet:
		print 'Disconnected: The server is full.'
		# this is just like getting CRbP for now
		#   but the response to the user should
		#   be different at some point.
		self.disconnect()

	    if 'CurrentLevel' in packet:
		#self.engine.gameWorld.setLevel( packet['CurrentLevel'] )
		print 'Current level is ', packet['CurrentLevel']
		self.gameWorld.setLevelByName(packet['CurrentLevel'])

	    if 'NextLevel' in packet:
		print 'Next Level is ', packet['NextLevel']
		
	    if 'GameStatus' in packet:
		self.gameWorld.stopGame()
		if packet['GameStatus'] == 'winner':
		    self.gState = LoserState(self)
		elif packet['GameStatus'] == 'loser':
		    self.gState = WinnerState(self)
		    
		
	    

    def on_tick(self):
	"""Timer event: on tick"""
	# kill the app if there is no state
	if not self.gState:
	    self.on_close()
	# render the scene
	glutPostRedisplay()


    def on_close(self):
	"""On close"""
        # leave the server
	self.disconnect()
	glutDestroyWindow(self.window)
	sys.exit()


    def renderFrame(self):
	"""The glut display function"""
	# clear the buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Draw the game world
	if self.gameWorld:
	    self.screen.drawThis( self.gameWorld )

	# Render if we have a state
	if self.gState:
	    # the state passes any objects the screen to be rendered
	    self.gState.renderFrame()

	# The screen draws all objects it has been passed
	self.screen.draw()

	# Dump the contents to the screen
	glutSwapBuffers()




if __name__ == '__main__':

    engine = GameEngine()

    while True:
	glutMainLoop()
	

