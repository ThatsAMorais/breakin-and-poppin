#####	   File : Client.py
####	 Author : Alex Morais
### Description : This base-class encapsulates the functionality of
###		being a client.
##

import os, sys, socket
from OpenGL.GLUT import glutTimerFunc
from multiplayer.CommFunctions import *

class Client():

    def __init__(self):
	"""init"""

	# these will be set later more properly
	self.host = 'localhost'
	self.port = 52850


    ###
    def on_socket(self, elapsed):
	"""Timer event: on socket"""

	if not self.connected:
	    return

	# the game engine handles all recv/send operations,
	#   but the game state has an opportunity to run
	#   code after this
	ready_to_read, ready_to_write, in_error = select.select(
		[self.channel], [self.channel], [self.channel], 0)

	if self.channel in in_error:
	    self.disconnect()

	playerPos = self.gameWorld.getPlayer().pos
	tileSize = self.gameWorld.level.getTileSize()
	# create a ClientPacket to be sent to the server
	packet = { 'type' : 'update'
		, 'name' : self.gameWorld.getPlayer().getName()
		, 'position' : [ playerPos[0]/tileSize[0]\
				, playerPos[1]/tileSize[1] ]
		, 'pType' : self.gameWorld.getPlayer().getType()
		, 'GameStatus' : self.gameWorld.status}

	if self.channel in ready_to_write:
	    sendData( self.channel, packet )
	    #print 'client - sent a packet'

	ready_to_read, ready_to_write, in_error = select.select(
		[self.channel], [self.channel], [self.channel], 0)

	serverPacket = None
	# recv data from the server
	if self.channel in ready_to_read:
	    serverPacket = recvData(self.channel)

	return serverPacket

    ###
    def connect(self):
	# Make a socket and set it up to look for the display wall
	self.channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	if not self.connected:# or not self.gameStarted :
	    try:
		self.channel.connect((self.host, self.port))
		self.connected = True
	    except (socket.error, socket.herror):
		print "client - Connection attempt to server failed."
		self.connected = False
		return False

	    #time.sleep(2)

	    if self.serverOwner:
		# send some initialization data to the server
		packet = {  'type' : 'message'
			, 'SetOwner' : None
			, 'MaxPlayers' : 5
			, 'ServerName' : self.serverName }
		
		sendData( self.channel, packet )
	    else:
		print 'client - not the server owner'

	    if self.connected:
		# start the socket event
		glutTimerFunc(20, self.on_socket, 20)
		print 'client - connected'

	if not self.gameWorld.getLevel(): 
	    ready_to_read, ready_to_write, in_error = select.select(
		    [self.channel], [self.channel], [self.channel], 0)

	    if self.channel in in_error:
		self.disconnect()

	    # create a request for the current level
	    packet = { 'type':'message', 'GetLevel':None }

	    if self.channel in ready_to_write:
		sendData( self.channel, packet )
		#print 'client - sent a packet'

	return True

    ###
    def disconnect(self):
	"""
	This sends the necessary cmd to leave a server
	"""
	if not self.connected:
	    return

	packet = {}
	if self.serverOwner:
	    # the server closes when the server owner leaves it
	    packet = {'type' : 'message'
		    , 'Kill' : None}
	else:
	    packet = {'type' : 'message'
		    , 'LeaveServer' : None}

	finished = False
	while not finished:
	    ready_to_read, ready_to_write, in_error = select.select(
		    [self.channel], [self.channel], [self.channel], 0)

	    if self.channel in ready_to_write:
		finished = True # If we get here its good enough to say
				#   we're finished regardless of the
				#   actual success of the send.
		sendData( self.channel, packet )

	    time.sleep(.8)
	
	self.connected = False
	self.serverOwner = False
	self.channel.close()
	print 'closing...'
	#time.sleep(1)


    ###
    def announceGameOver(self, result='winner'):
	"""
	This function will broadcast to the server that a winner or 
	loser has been decided.
	"""
	packet = {'type':'message', 'GameOver':result}
	finished = False
   
	while not finished:
	    ready_to_read, ready_to_write, in_error = select.select(
		    [self.channel], [self.channel], [self.channel], 0)

	    print 'announcing that the game is over'
	    print ready_to_write

	    if self.channel in ready_to_write:
		sendData( self.channel, packet )
		print self.gameWorld.player.playerName, "is the", result
		finished = True # If we get here its good enough to say
				#   we're finished regardless of the
				#   actual success of the send.

	    time.sleep(.8)



    ###
    def closeServer(self):
	"""
	This function closes the server by sending a Kill command
	"""
	packet = {'type' : 'message'
		, 'Kill' : True	    }

	print 'Killing the server'
	
	finished = False
	while not finished:
	    ready_to_read, ready_to_write, in_error = select.select(
		    [self.channel], [self.channel], [self.channel], 0)

	    if self.channel in ready_to_write:
		finished = True # If we get here its good enough to say
				#   we're finished regardless of the
				#   actual success of the send.
		try:
		    # this function returns (boolean, err)
		    sendData(self.channel, packet )
		except socket.error:
		    # ignore this because the server might already be gone
		    print 'client - the send thread did not make it'

	    time.sleep(.8)


