#####	   File : TitleScreenState.py
####	 Author : Alex Morais
### Description : 
##

import os, sys, time
from subprocess import Popen
from platform import system

from states.EngineState import *
from states.CreateServerState import *
from states.FindServerState import *
from OpenGL.GLUT import *

class TitleScreenState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

	self.screen = Screen()
	self.res = self.engine.setsMgr.screenRes
	res = self.res # saying 'self.res' was making lines too long. :P
	
	# get/load the font
	self.font = FontManager().loadFont( 'JohnDoe' )

	# screen objects
	self.UI = {}
	self.UI['title'] = UIText("Breakin And Poppin"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=35)
	self.UI['start_server'] = UIText("Start a Server"\
		, pos=[res[0]*0.5, res[1]*0.45], font=self.font, scale=21)
	self.UI['find_server'] = UIText("Find a Server"\
		, pos=[res[0]*0.5, res[1]*0.51], font=self.font, scale=21)
	self.UI['quit'] = UIText("Quit"\
		, pos=[res[0]*0.5, res[1]*0.57], font=self.font, scale=21)
	self.UI['titleBGImg'] = UIImage("TitleScreenBG_trans.png"\
		, pos=[0,0], size=res)

    def renderFrame(self):
	if not self.screen:
	    self.screen = Screen()

	for uiObj in self.UI.values():
	    # draw the background image firstly
	    self.screen.drawThis( uiObj )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == '\x1b':
	    return None

	return self

    def on_key_release(self, key, x, y):
	"""
	On key release
	"""
	return self

    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse release
	"""
	if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
	    
	    # check the mouse pos against all the
	    if self.UI['start_server'].CollidePoint( (x,y) ):
		return CreateServerState(self.engine)
		
	    if self.UI['find_server'].CollidePoint( (x,y) ):
		return FindServerState(self.engine)
		
	    if self.UI['quit'].CollidePoint( (x,y) ):
		return None

	return self

    def on_socket(self, elapsed):
	"""
	On socket
	"""
	return self

    def Step(self):
	"""
	Step
	"""
	pass



