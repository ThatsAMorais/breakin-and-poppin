#####	   File : CreateServerState.py
####	 Author : Alex Morais
### Description : 
##

from states.EngineState import *
from states.TitleScreenState import *
from states.ChoosePlayerState import *
from ui.Font import *
from ui.UIText import *
from ui.UIImage import *

class CreateServerState(EngineState):

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
	self.UI['title'] = UIText("Start a Server"\
		, pos=[res[0]*.01,res[1]*.10], font=self.font, scale=35)
	self.UI['server_name'] = UIText("Server Name"\
		, [res[0]*0.3, res[1]*0.2], self.font, 22)
	self.UI['text_entry'] = UIText("server_name"\
		, [res[0]*0.3, res[1]*0.4], self.font, 30)
	self.UI['backspace'] = UIText("BKSP"\
		, [res[0]*0.3, res[1]*0.50], self.font, 20)
	self.UI['space'] = UIText("SPACE"\
		, [res[0]*0.3, res[1]*0.7], self.font, 20)
	self.UI['back'] = UIText("Back"\
		, pos=[res[0]*0.15, res[1]*0.8], font=self.font, scale=20)
	self.UI['create'] = UIText("Create"\
		, pos=[res[0]*0.7, res[1]*0.8], font=self.font, scale=20)

	# Here, a hash is created containing a UIText for each letter in the alphabet.
	#   They are spaced and stacked on the screen so that they lie in 3 rows of 8,
	#   9, and 9 letters each.
	self.screenKeys = {}
	lettPos = [res[0]*0.20, res[1]*0.6]
	lettersToAdd = 8
	lettScale = 18
	for letter in map(chr, range(65, 91)):
	    
	    # add the letter to the hash
	    self.screenKeys[letter] = UIText(letter, [lettPos[0], lettPos[1]],
		    self.font, lettScale)

	    # This denotes that the last letter in the row has been added
	    #	
	    if lettersToAdd == 1:
		lettersToAdd = 9	    # the subsequent rows all have 9 letters
		lettPos[0] = res[0]*0.17    # reset the x pos (slightly less ^\ )
		lettPos[1] += lettScale+1   # increment the y pos
	    else:
		lettersToAdd -= 1	    # decrement the counter
		lettPos[0] += lettScale+1   # increment the x pos


    def renderFrame(self):
	""" RenderFrame - Base Class """

	#screen = Screen()

	for scrObj in self.UI.values():
	    Screen().drawThis( scrObj )

	for letter in self.screenKeys.values():
	    Screen().drawThis( letter )

	return self

    def on_key_press(self, key, x, y):
	"""
	On key press
	"""
	print key
	if key == '\x1b':
	    return TitleScreenState(self.engine)
	
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
	On mouse press
	"""
	if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
	    if self.UI['back'].CollidePoint((x,y)):
		return TitleScreenState(self.engine)

	    if self.UI['create'].CollidePoint((x,y)):
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

	    # test for user clicks on the screen keys
	    for letter in self.screenKeys:
		if self.screenKeys[letter].CollidePoint((x,y)):
		    self.UI['text_entry'].push( letter )

	    if self.UI['backspace'].CollidePoint((x,y)):
		self.UI['text_entry'].pop()

	    if self.UI['space'].CollidePoint((x,y)):
		self.UI['text_entry'].push(" ")
		    
		

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

