#####	   File : AllStates.py
####	 Author : Alex Morais
### Description : I was getting a circular dependency issue having all of the
###		    following state classes in separate files, since it is
###		    highly likely that a state will import another state that
###		    imported it.  I had to copy them into this file.  This is
###		    why the codebase still includes the separated versions.
##

import os, sys, time
from subprocess import Popen
from platform import system
from OpenGL.GLUT import *

from states.EngineState import EngineState
from managers.SettingsManager import *
from managers.FontManager import *
from engine.Screen import *
from level.PreBuiltLevel import *
from ui.Font import *
from ui.UIText import *
from ui.UIImage import *


#####	   File : TitleScreenState.py
####	 Author : Alex Morais
### Description : 
##

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
	self.font = FontManager().loadFont( 'Basic' )

	# screen objects
	self.UI = {}
	self.UI['title'] = UIText("Breakin And Poppin"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=0.05)
	self.UI['start_server'] = UIText("Start a Server"\
		, pos=[res[0]*0.5, res[1]*0.42], font=self.font, scale=0.04)
	self.UI['start_server'].center()
	self.UI['join_server'] = UIText("Join a Server"\
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['join_server'].center()
	self.UI['quit'] = UIText("Quit"\
		, pos=[res[0]*0.5, res[1]*0.58], font=self.font, scale=0.04)
	self.UI['quit'].center()
	self.titleBGImg = UIImage("TitleScreenBG.png"\
		, pos=[0,0], size=res)

	self.selected = 'start_server'

    def renderFrame(self):
	if not self.screen:
	    self.screen = Screen()

	self.screen.drawThis( self.titleBGImg )

	selectionBox = UIImage("box.png",
				pos=self.UI[self.selected].pos,
				size=[(self.res[0]*0.05)*10, self.res[1]*0.05])
	selectionBox.center()
	self.screen.drawThis( selectionBox )

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

	elif key == chr(13):
	    if self.selected == "start_server":
		self.statePath = 'start'
		return CreateServerState(self.engine)
	    elif self.selected == "join_server":
		self.statePath = 'join'
		return JoinServerState(self.engine)
	    elif self.selected == "quit":
		return None

	elif key == 101:
	    if self.selected == "start_server":
		self.selected = "quit"
	    elif self.selected == "join_server":
		self.selected = "start_server"
	    elif self.selected == "quit":
		self.selected = "join_server"

	elif key == 103:
	    if self.selected == "start_server":
		self.selected = "join_server"
	    elif self.selected == "join_server":
		self.selected = "quit"
	    elif self.selected == "quit":
		self.selected = "start_server"

	return self


    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	# check the mouse pos against all the choices
	if self.UI['start_server'].CollidePoint( (x,y) ):
	    self.selected = "start_server"
	    
	elif self.UI['join_server'].CollidePoint( (x,y) ):
	    self.selected = "join_server"
	    
	elif self.UI['quit'].CollidePoint( (x,y) ):
	    self.selected = "quit"
    
	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse release
	"""
	if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
	    
	    # check the mouse pos against all the choices
	    if self.UI['start_server'].CollidePoint( (x,y) ):
		self.engine.statePath = 'start'
		return CreateServerState(self.engine)
		
	    if self.UI['join_server'].CollidePoint( (x,y) ):
		self.engine.statePath = 'join'
		return JoinServerState(self.engine)
		
	    if self.UI['quit'].CollidePoint( (x,y) ):
		return None

	return self


#####	   File : JoinServerState.py
####	 Author : Alex Morais
### Description : 
##

class JoinServerState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

	self.res = self.engine.setsMgr.screenRes
	res = self.res

	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )

	self.UI = {}
	self.UI['title'] = UIText("Join a Server"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=0.05)
	self.UI['back'] = UIText("Back"\
		, pos=[res[0]*0.1, res[1]*0.9], font=self.font, scale=0.03)
	self.UI['back'].center()
	self.UI['join'] = UIText("Join"\
		, pos=[res[0]*0.9, res[1]*0.9], font=self.font, scale=0.03)
	self.UI['join'].center()
	self.UI['backspace'] = UIText("BKSP"\
		, [res[0]*0.24, res[1]*0.65], self.font, 0.03)
	self.UI['space'] = UIText("SPACE"\
		, [res[0]*0.6, res[1]*0.65], self.font, 0.03)
	self.UI['ip_entry'] = UIText(self.engine.host\
		, [res[0]*0.5, res[1]*0.3], self.font, 0.03)
	self.UI['ip_entry'].center()
	
	self.selected = 'join'

	self.entryBox = UIImage("box.png",
				pos=[res[0]*0.5, res[1]*0.3],
				size=[(0.03*res[0])*12, 0.05*res[1]])
	self.entryBox.center()

	self.titleBGImg = UIImage("TitleScreenBG.png"\
		, pos=[0,0], size=res)

	# This is the text input that currently has focus; 
	#   the default is text_entry
	self.hasFocus = self.UI['ip_entry']

	# Here, a hash is created containing a UIText for each letter
	#   in the alphabet.
	# They are spaced and stacked on the screen so that they lie
	#   in 3 rows of 8, 9, and 9 letters each.

	self.screenKeys = {"." : UIText(".", 
				    [res[0]*0.5, res[1]*0.65],
				    self.font, 0.06) }
	self.screenKeys["."].center()
	self.screenKeys["localhost"] = UIText("localhost", 
						[res[0]*0.33, res[1]*0.48],
						self.font, 0.04)

	lettPos = [res[0]*0.3, res[1]*0.56]
	lettScale = 0.04
	for letter in map( str, range(10) ):
	    # add the letter to the hash
	    self.screenKeys[letter] = UIText(letter, 
					    [lettPos[0], lettPos[1]],
					    self.font, lettScale)
	    lettPos[0] += lettScale+(lettScale*res[0])  # increment the x pos

	self.keysBox = UIImage("box.png",
			    pos=list(self.screenKeys["5"].pos),
			    size=[ (lettScale*res[0])*15, (lettScale*res[1])*7 ] )
	self.keysBox.center()    


    def renderFrame(self):
	""" RenderFrame - Base Class """

	Screen().drawThis( self.titleBGImg )
	Screen().drawThis( self.entryBox )
	Screen().drawThis( self.keysBox )

	selectionBox = UIImage("box.png",
				pos=self.UI[self.selected].pos,
				size=[(self.res[0]*0.03)*5, (self.res[0]*0.03)*2])
	selectionBox.center()
	Screen().drawThis( selectionBox )

	for uiObj in self.UI.values():
	    # draw the background image firstly
	    Screen().drawThis( uiObj )

	for letter in self.screenKeys.values():
	    Screen().drawThis( letter )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""

	# Esc
	if key == chr(27):
	    return TitleScreenState(self.engine)

	# Enter
	elif key == chr(13):
	    if self.selected == "back":
		return TitleScreenState(self.engine)
	    elif self.selected == "join":
		self.engine.host = self.UI['ip_entry'].getText()
		return ChoosePlayerState(self.engine)

	elif key >= 100 and key <= 103:
	    if self.selected == "back":
		self.selected = "join"
	    elif self.selected == "join":
		self.selected = "back"

	elif self.hasFocus != None:
	    if key == chr(8) or key == chr(127):    # BS or Del
		if self.UI['ip_entry'].getText() == "localhost":
		    self.UI['ip_entry'].setText( "" )
		else:
		    self.hasFocus.pop()
	    elif key == ".":
		self.hasFocus.push(".")
	    elif key.isdigit():
		if len( self.UI['ip_entry'].getText() ) < 15:
		    if self.UI['ip_entry'].getText() == "localhost":
			self.UI['ip_entry'].setText( "" )
		    self.hasFocus.push(key)

	return self


    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	if self.UI['back'].CollidePoint( (x,y) ):
	    self.selected = "back"
	    
	elif self.UI['join'].CollidePoint( (x,y) ):
	    self.selected = "join"

	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse press
	"""
	if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
	    if self.UI['back'].CollidePoint((x,y)):
		return TitleScreenState(self.engine)

	    if self.UI['join'].CollidePoint((x,y)):
		self.engine.host = self.UI['ip_entry'].getText()
		return ChoosePlayerState(self.engine)

	    # test for user clicks on the screen keys
	    if len( self.UI['ip_entry'].getText() ) < 15:
		for letter in self.screenKeys:
		    if self.screenKeys[letter].CollidePoint((x,y)):
			if letter == "localhost":
			    self.UI['ip_entry'].setText("localhost")
			else:
			    if self.UI['ip_entry'].getText().isalpha():
				self.UI['ip_entry'].setText( "" )
			    self.UI['ip_entry'].push( letter )

	    if self.UI['backspace'].CollidePoint((x,y)):
		if self.UI['ip_entry'].getText() == "localhost":
		    self.UI['ip_entry'].setText( "" )
		else:
		    self.UI['ip_entry'].pop()

	    if self.UI['space'].CollidePoint((x,y)):
		self.UI['ip_entry'].push(" ")
		    

	return self




#####	   File : CreateServerState.py
####	 Author : Alex Morais
### Description : 
##

class CreateServerState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

	self.screen = Screen()
	self.res = self.engine.setsMgr.screenRes
	res = self.res # typing 'self.res' was making lines too long. :P
	
	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )

	# screen objects
	self.UI = {}
	self.UI['title'] = UIText("Start a Server"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=0.05)
	self.UI['server_name'] = UIText("Server Name"\
		, [res[0]*0.3, res[1]*0.2], self.font, 0.034)
	self.UI['text_entry'] = UIText(self.engine.serverName\
		, [res[0]*0.5, res[1]*0.3], self.font, 0.047)
	self.UI['text_entry'].center()
	self.UI['backspace'] = UIText("BKSP"\
		, [res[0]*0.24, res[1]*0.74], self.font, 0.031)
	self.UI['space'] = UIText("SPACE"\
		, [res[0]*0.6, res[1]*0.74], self.font, 0.031)
	self.UI['back'] = UIText("Back"\
		, pos=[res[0]*0.1, res[1]*0.9], font=self.font, scale=0.031)
	self.UI['back'].center()
	self.UI['create'] = UIText("Create"\
		, pos=[res[0]*0.9, res[1]*0.9], font=self.font, scale=0.031)
	self.UI['create'].center()
	
	self.selected = 'create'

	self.titleBGImg = UIImage("TitleScreenBG.png", pos=[0,0], size=res)
	
	self.entryBox = UIImage("box.png",
				pos=[res[0]*0.5, res[1]*0.3],
				size=[(0.03*res[0])*12, 0.05*res[1]])
	self.entryBox.center()

	# This is the text input that currently has focus; 
	#   the default is text_entry
	self.hasFocus = self.UI['text_entry']
	self.ServerNameMax = 12

	# Here, a hash is created containing a UIText for each letter
	#   in the alphabet.
	# They are spaced and stacked on the screen so that they lie
	#   in 3 rows of 8, 9, and 9 letters each.
	self.screenKeys = {}
	lettPos = [res[0]*0.32, res[1]*0.45]
	lettersToAdd = 8
	lettScale = 0.04
	for letter in map(chr, range(65, 91)):
	    
	    # add the letter to the hash
	    self.screenKeys[letter] = UIText(letter, [lettPos[0], lettPos[1]],
		    self.font, lettScale)

	    # This denotes that the last letter in the row has been added
	    #	
	    if lettersToAdd == 1:
		lettersToAdd = 9    # the subsequent rows all have 9 letters
		lettPos[0] = res[0]*0.3   # reset the x pos (slightly less ^\ )
		lettPos[1] += lettScale+(lettScale*res[0])  # increment the y pos
	    else:
		lettersToAdd -= 1	    # decrement the counter
		lettPos[0] += lettScale+(lettScale*res[0])  # increment the x pos

	self.keysBox = UIImage("box.png", pos=self.screenKeys['N'].pos\
		, size=[ (lettScale*res[0])*10, (lettScale*res[1])*6 ])
	self.keysBox.center()    


    def createServer( self ):
	"""
	for the sake of code reuse
	"""
	if system() == "Linux" or system() == "Macintosh":
	    Popen( [r'/usr/bin/python2.7'
		,os.path.join( self.engine.setsMgr.home_dir
				, 'StartServer.py' )] )
	elif system() == "Windows":
	    Popen([r'C:\Python27\python.exe'
		,os.path.join( self.engine.setsMgr.home_dir
				, 'StartServer.py' )])
	else:
	    print "you are on an unsupported platform for spawning a server"
	
	# declare that this game instance is the server owner
	self.engine.serverOwner = True
	self.engine.serverName = self.UI['text_entry'].getText()
	return ChoosePlayerState(self.engine)


    def renderFrame(self):
	""" RenderFrame - Base Class """

	#screen = Screen()

	Screen().drawThis( self.titleBGImg )
	Screen().drawThis( self.entryBox )
	Screen().drawThis( self.keysBox )

	selectionBox = UIImage("box.png",
				pos=self.UI[self.selected].pos,
				size=[(self.res[0]*0.03)*5, (self.res[0]*0.03)*2])
	selectionBox.center()
	Screen().drawThis( selectionBox )

	for scrObj in self.UI.values():
	    Screen().drawThis( scrObj )

	for letter in self.screenKeys.values():
	    Screen().drawThis( letter )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	# Esc
	if key == chr(27):			    # Escape
	    return TitleScreenState(self.engine)

	# Enter
	elif key == chr(13):
	    if self.selected == "back":
		return TitleScreenState(self.engine)
	    elif self.selected == "create":
		return self.createServer()

	# Arrow keys
	elif key >= 100 and key <= 103:
	    if self.selected == "back":
		self.selected = "create"
	    elif self.selected == "create":
		self.selected = "back"

	elif self.hasFocus != None:
	    if key == chr(32):			    # Space Bar
		if len(self.hasFocus.getText()) < self.ServerNameMax:
		    self.hasFocus.push(" ")
	    if key == chr(8) or key == chr(127):    # BS or Del
		self.hasFocus.pop()
	    if key.isalpha() or key.isdigit():	    # letter/numbers
		if len(self.hasFocus.getText()) < self.ServerNameMax:
		    self.hasFocus.push(key)

	return self


    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""
	if self.UI['back'].CollidePoint( (x,y) ):
	    self.selected = "back"
	    
	elif self.UI['create'].CollidePoint( (x,y) ):
	    self.selected = "create"

	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse press
	"""
	if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
	    if self.UI['back'].CollidePoint((x,y)):
		return TitleScreenState(self.engine)

	    if self.UI['create'].CollidePoint((x,y)):
		return self.createServer()

	    # test for user clicks on the screen keys
	    for letter in self.screenKeys:
		if self.screenKeys[letter].CollidePoint((x,y)):
		    if len(self.hasFocus.getText()) < self.ServerNameMax:
			self.UI['text_entry'].push( letter )

	    if self.UI['backspace'].CollidePoint((x,y)):
		self.UI['text_entry'].pop()

	    if self.UI['space'].CollidePoint((x,y)):
		if len(self.hasFocus.getText()) < self.ServerNameMax:
		    self.UI['text_entry'].push(" ")
		    
		

	return self





#####	   File : ChoosePlayerState.py
####	 Author : Alex Morais
### Description : 
##
class ChoosePlayerState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

	self.res = self.engine.setsMgr.screenRes
	res = self.res

	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )

	self.UI = {}
	self.UI['title'] = UIText("Choose a Player"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=0.05)
	self.UI['back'] = UIText("Back"\
		, pos=[res[0]*0.1, res[1]*0.9], font=self.font, scale=0.031)
	self.UI['back'].center()
	self.UI['ready'] = UIText("Ready"\
		, pos=[res[0]*0.8, res[1]*0.9], font=self.font, scale=0.031)
	self.UI['ready'].center()
	self.UI['cop_img'] = UIImage( "police_officer.png"\
		, pos=[res[0]*0.25, res[1]*0.5]
		, size= [res[0]*0.4, res[1]*0.4] )
	self.UI['cop_img'].center()
	self.UI['robb_img'] = UIImage( "cartoon_robber.png"\
		, pos=[res[0]*0.75, res[1]*0.5]
		, size= [res[0]*0.4, res[1]*0.4] )
	self.UI['robb_img'].center()
	self.titleBGImg = UIImage("TitleScreenBG.png"\
		, pos=[0,0], size=res)
	self.UI['server_connect_failed'] = UIText( "Connect Failed"\
		, [res[0]*0.3, res[1]*0.9], self.font, 0.031)
	self.UI['server_connect_failed'].setVisible(False)

	self.selected = 'ready'
	self.plChoice = 'cop_img'

    def playerReady(self):
	"""
	some reused code
	"""
	# set the player type in the game
	gW = self.engine.gameWorld
	peers = gW.peers

	if self.plChoice == "cop_img":
	    gW.setPlayerType( "Cop" )
	elif self.plChoice == "robb_img":
	    gW.setPlayerType( "Robber" )

	self.UI['server_connect_failed'].setVisible(False)
	self.engine.renderFrame()
	
	result = self.engine.connect()
	if result:
	    # go to the next state
	    if len( peers ) > 0:
		return GameState(self.engine)
	    else:
		return WaitingForPlayersState(self.engine)
	else:
	    self.UI['server_connect_failed'].setVisible()
	    return self

	    	

    def returnLastState(self):
	"""
	When needed, it determines which path through the interface
	screens the user chose from the title menu.

	This is used to determine where to go when the user wants
	to move 'back' to the previous screen, which could be the
	CreateServerState or JoinServerState
	"""
	if self.engine.statePath == 'start':
	    return CreateServerState(self.engine)
	elif self.engine.statePath == 'join':
	    return JoinServerState(self.engine)
	else:
	    return TitleScreenState(self.engine)

    def renderFrame(self):
	""" RenderFrame - Base Class """
	Screen().drawThis( self.titleBGImg )

	playerChoiceBox = UIImage( "box.png"\
				, pos=self.UI[self.plChoice].pos
				, size=[self.res[0]*0.42, self.res[1]*0.42] )
	playerChoiceBox.center()
	Screen().drawThis( playerChoiceBox )

	selectionBox = UIImage( "box.png"\
				, pos=self.UI[self.selected].pos
				, size=[(self.res[0]*0.03)*5, (self.res[0]*0.03)*2] )
	selectionBox.center()
	Screen().drawThis( selectionBox )

	for uiObj in self.UI.values():
	    Screen().drawThis( uiObj )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == chr(27):   # Escape
	    self.engine.disconnect()
	    return self.returnLastState()

	# Enter
	elif key == chr(13):
	    if self.selected == "back":
		return self.returnLastState()
	    elif self.selected == "ready":
		return self.playerReady()

	# Arrow keys
	elif key == 100 or key == 102:
	    if self.selected == "back":
		self.selected = "ready"
	    elif self.selected == "ready":
		self.selected = "back"
	    	
	elif key == 101 or key == 103:
	    if self.plChoice == "cop_img":
		self.plChoice = "robb_img"
	    elif self.plChoice == "robb_img":
		self.plChoice = "cop_img"

	return self

 

    def on_mouse_motion(self, x, y):
	"""
	On mouse motion
	"""

	if self.UI['back'].CollidePoint( (x,y) ):
	    self.selected = "back"
	    
	if self.UI['ready'].CollidePoint( (x,y) ):
	    self.selected = "ready"

	if self.UI['cop_img'].CollidePoint( (x,y) ):
	    self.plChoice = "cop_img"
	    
	if self.UI['robb_img'].CollidePoint( (x,y) ):
	    self.plChoice = "robb_img"

	return self

    def on_mouse(self, button, state, x, y):
	"""
	On mouse press
	"""

	if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
	    if self.UI['back'].CollidePoint((x,y)):
		return self.returnLastState()
	    if self.UI['ready'].CollidePoint((x,y)):
		return self.playerReady()

	    if self.UI['cop_img'].CollidePoint((x,y)):
		self.plChoice = "cop_img"
	    if self.UI['robb_img'].CollidePoint((x,y)):
		self.plChoice = "robb_img"
	
	return self





#####	   File : WaitingForPlayersState.py
####	 Author : Alex Morais
### Description : 
##
class WaitingForPlayersState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine

	self.res = self.engine.setsMgr.screenRes
	res = self.res

	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )
	self.UI = {}
	self.UI['waiting'] = UIText("Waiting"
		, pos=[res[0]*0.5, res[1]*0.3], font=self.font, scale=0.04)
	self.UI['waiting'].center()
	self.UI['for'] = UIText("For"
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['for'].center()
	self.UI['players'] = UIText("Players"
		, pos=[res[0]*0.5, res[1]*0.7], font=self.font, scale=0.04)
	self.UI['players'].center()
	self.UI['back'] = UIText("Back"\
		, pos=[res[0]*0.5, res[1]*0.9], font=self.font, scale=0.04)
	self.UI['back'].center()

	self.selectionBox = UIImage( "box.png"\
				, pos=self.UI['back'].pos
				, size=[(self.res[0]*0.03)*5, (self.res[0]*0.03)*2] )
	self.selectionBox.center()

	self.titleBGImg = UIImage("TitleScreenBG.png"\
		, pos=[0,0], size=res)


	glutTimerFunc(50, self.engine.on_update, 50)

    def renderFrame(self):
	""" RenderFrame - Base Class """
	
	Screen().drawThis( self.titleBGImg )
	
	Screen().drawThis( self.selectionBox )	

	for uiObj in self.UI.values():
	    Screen().drawThis( uiObj )

	return self

    def update(self, elapsed):
	"""
	"""
	# go to the next state
	if len( self.engine.gameWorld.peers ) > 0:
	    return GameState(self.engine)
	else:
	    return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == chr(27):   # Escape
	    return ChoosePlayerState(self.engine)
	return self


    def on_mouse(self, button, state, x, y):
	"""
	On mouse press/release
	"""
	if self.UI['back'].CollidePoint( (x,y) ):
	    return ChoosePlayerState(self.engine)
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



#####	   File : GameState.py
####	 Author : Alex Morais
### Description : 
##
class GameState(EngineState):

    def __init__(self, engine):
	"""
	The game determines what is happening on screen
	based on what state the GameEngine instance has.
	"""
	self.engine = engine
	self.res = self.engine.setsMgr.screenRes
	self.screen = None

	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )
	self.str_paused = UIText( "Paused",
		[self.res[0]*0.5, self.res[1]*0.5],
		self.font, 0.05 )
	self.str_paused.setVisible(False)

	engine.gameWorld.setLevelByName( 'Level1L' )
	engine.gameWorld.gameTime = 0.0

	engine.gameWorld.startGame()
	#glutTimerFunc(300, self.print_game_world, 300)

    def print_game_world(self, elapsed):
	gW = self.engine.gameWorld
	tileSize = gW.level.getTileSize()
	peerPos = gW.peers.values()[0].pos
	print ''
	print '--- Gameworld ---'
	print 'Player = {', gW.player.playerName, ":", gW.player.pos, "}"
	print 'mapPixelPos = ', gW.player.pos[0] + gW.scrScroll[0]\
				, gW.player.pos[1] + gW.scrScroll[1]
	print 'mapTilePos = ', gW.player.pos[0] / tileSize[0],\
				gW.player.pos[1] / tileSize[1]
	print 'renderPos = ', gW.player.pos[0] - gW.scrScroll[0]\
			    , gW.player.pos[1] - gW.scrScroll[1]
	print '  ------ ------ '
	print 'Peers = {', gW.peers.values()[0].playerName, ":", peerPos, "}" 
	print 'mapTilePos = ', peerPos[0] / tileSize[0],\
				peerPos[1] / tileSize[1]
	print 'renderPos = ', peerPos[0] - gW.scrScroll[0]\
			    , peerPos[1] - gW.scrScroll[1]
	print '  ------ ------ '
	print 'TileSize = ', tileSize
	print ''
	glutTimerFunc(300, self.print_game_world, 300)

    def renderFrame(self):
	""" RenderFrame - Base Class """
	if not self.screen:
	    self.screen = Screen()

	scrSize = self.screen.getSize()
	#self.engine.gameWorld.positionPlayer( [scrSize[0],scrSize[1]] )

	self.screen.drawThis( self.str_paused )
	
	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == chr(27):   # Escape
	    return ChoosePlayerState(self.engine)
	elif key == 'g':
	    self.str_paused.toggleVisible()
	    self.engine.gameWorld.pause()
	
	# controller
	self.engine.gameWorld.on_key_press(key, x, y)

	return self


    def on_key_release(self, key, x, y):
	"""On key release"""
	# controller	
	self.engine.gameWorld.on_key_release(key, x, y)
	return self


    def on_specialkey_press(self, key, x, y):
	"""On special key press"""
	# controller
	self.engine.gameWorld.on_specialkey_press(key, x, y)
	return self

    def on_specialkey_release(self, key, x, y):
	"""On special key release"""
	# controller
	self.engine.gameWorld.on_specialkey_release(key, x, y)
	return self

    def on_mouse_motion(self, x, y):
	"""On mouse motion"""
	# controller
	self.engine.gameWorld.on_mouse_motion(x, y)
	return self

    def on_mouse(self, button, state, x, y):
	"""On mouse press/release"""
	# controller
	self.engine.gameWorld.on_mouse(button, state, x, y)
	return self

    def update(self, elapsed):
	"""
	switches the state based on 
	"""
	if self.engine.gameWorld.gameStatus == "winner":
	    # Send a signal to the server that this player
	    #	seems to have won the game ( the server will
	    #	have to agree with our word )
	    
	    # Go to the appropriate engine-state screen
	    #self.engine.gameWorld = GameWorld()
	    print 'switching to winner state'
	    return WinnerState(self.engine)

	elif self.engine.gameWorld.gameStatus == "loser":
	    # Go to the appropriate engine-state screen
	    #self.engine.gameWorld = GameWorld()
	    return LoserState(self.engine)
	else:
	    return self



#####	   File : WinnerState.py
####	 Author : Alex Morais
### Description : 
##
class WinnerState(EngineState):

    def __init__(self, engine):
        """
	
	"""
	self.engine = engine
	self.res = self.engine.setsMgr.screenRes
	res = self.res
	self.screen = None

	# announce that the game is over
	#engine.announceGameOver( 'winner' )
	self.engine.gameWorld.status = 'winner'
	self.engine.gameWorld.stopGame()

	self.font = FontManager().loadFont( 'Basic' )
	self.UI = {}
	self.UI['nice_work'] = UIText("Nice Work!"
		, pos=[res[0]*0.5, res[1]*0.3], font=self.font, scale=0.047)
	self.UI['nice_work'].center()

	self.UI['cop_wins'] = UIText("You Caught The Robber!"
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['cop_wins'].center()

	self.UI['robber_wins'] = UIText("You made it home safe!"
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['robber_wins'].center()

    	self.UI['press_esc'] = UIText("Press escape to continue"
		, pos=[res[0]*0.5, res[1]*0.75], font=self.font, scale=0.04)
	self.UI['press_esc'].center()

	self.titleBGImg = UIImage("black_bg.png"\
		, pos=[0,0], size=res)

    def renderFrame(self):
	""" RenderFrame - Base Class """
	
	if not self.screen:
	    self.screen = Screen()

	self.screen.drawThis( self.titleBGImg )
	self.screen.drawThis( self.UI['nice_work'] )

	if self.engine.gameWorld.getPlayerType() == "Robber":
	    self.screen.drawThis( self.UI['robber_wins'] )
	elif self.engine.gameWorld.getPlayerType() == "Cop":
	    self.screen.drawThis( self.UI['cop_wins'] )

	self.screen.drawThis( self.UI['press_esc'] )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == chr(27):   # Escape
	    self.engine.disconnect()
	    return TitleScreenState(self.engine)
	else:
	    return self


    def on_mouse(self, button, state, x, y):
	"""
	On mouse press
	"""
	self.engine.disconnect()
	return TitleScreenState(self.engine)


#####	   File : LoserState.py
####	 Author : Alex Morais
### Description : 
##
class LoserState(EngineState):


    def __init__(self, engine):
        """
	
	"""
	self.engine = engine
	self.res = self.engine.setsMgr.screenRes
	res = self.res
	self.screen = None

	# announce that the game is over
	#engine.announceGameOver( 'loser' )
	self.engine.gameWorld.status = 'loser'
	self.engine.gameWorld.stopGame()

	self.font = FontManager().loadFont( 'Basic' )

	self.UI = {}
	self.UI['loser'] = UIText("Dont quit your day job!"
		, pos=[res[0]*0.5, res[1]*0.3], font=self.font, scale=0.04)
	self.UI['loser'].center()
	self.UI['cop_loses'] = UIText("You lost the thief!"
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['cop_loses'].center()
	self.UI['robber_loses'] = UIText("You got popped!"
		, pos=[res[0]*0.5, res[1]*0.5], font=self.font, scale=0.04)
	self.UI['robber_loses'].center()
	self.UI['press_esc'] = UIText("Press escape to continue"
		, pos=[res[0]*0.5, res[1]*0.75], font=self.font, scale=0.04)
	self.UI['press_esc'].center()

	self.titleBGImg = UIImage("black_bg.png"\
		, pos=[0,0], size=res)
    
    def renderFrame(self):
	""" RenderFrame - Base Class """
	
	if not self.screen:
	    self.screen = Screen()

	self.screen.drawThis( self.titleBGImg )

	self.screen.drawThis( self.UI['loser'] )

	if self.engine.gameWorld.getPlayerType() == "Robber":
	    self.screen.drawThis( self.UI['robber_loses'] )
	elif self.engine.gameWorld.getPlayerType() == "Cop":
	    self.screen.drawThis( self.UI['cop_loses'] )

	self.screen.drawThis( self.UI['press_esc'] )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	if key == chr(27):   # Escape
	    self.engine.disconnect()
	    return TitleScreenState(self.engine)
	return self


    def on_mouse(self, button, state, x, y):
	"""
	On mouse press
	"""
	self.engine.disconnect()
	return TitleScreenState(self.engine)



