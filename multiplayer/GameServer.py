#####      File : GameServer.py
####	 Author : Alex Morais
### Description : A game server to which players can connect via
###		 the IP of the parent GameEngine instance.
##

import socket, time
from multiplayer.CommFunctions import *

BACKLOG = 25

class GameServer():

    def __init__(self):
	"""
	A server to which game clients can connect.  This
	is usually contained inside of another client that
	instantiated it in the process of Creating a Server.
	"""

	# the client that is the owner (honor system)
	self.owner = None
	# this variable will be set in the event that no client
	#   threads are in use by the server after one was alive
	# it can also be set by the Owner-client
	self.kill = False

	# the name of the server
	self.name = "TheServer"

	# the game time and 'active' flag
	self.gameTime = 0.0
	self.gameActive = False

	# these two hashes are both indexed by the client channel created
	#   on accept(), but they contain different data and are used
	#   in different contexts.
	self.maxPlayers = 1	## maximum number of clients that can connect
	self.clients = {}	## the client sockets
	self.playerData = {}	## the player data from received packets
	self.timeout = {}	## tracks the number of failed sends

	self.requestPackets = {} # a dict of packets to be sent to clients
				 #   that requested information
	# the server
	self.channel= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.port = 52850
	self.channel.bind(('', self.port))
	self.channel.listen(BACKLOG)

	# level-queue
	self.levelQueue = ['Level1L']
	self.levelIndex = 0	# current index in the queue
	self.levelVotes = {}	# votes for a level to be next
	self.currLevel = self.levelQueue[0] # the level currently in use
	self.nextLevel = None	# a special request
	self.roundStarted = False   # the game session is active


    def start(self):
	"""
	Begins the server accepting clients and serving game info.
	"""
	print "Server started"
	# loop until it should close
	acceptThread = None
	gotAClient = False

	while not self.kill and (len(self.clients) > 0 or not gotAClient):

	    # query the availability of the listen socket
	    ready_to_read, ready_to_write, in_error = select.select(
		    [self.channel], [], [self.channel], 0)
	    #
	    # accept clients - within the maxPlayers limit
	    #
	    if self.channel in ready_to_read:
		channel = None
		try:
		    channel, details = self.channel.accept()
		    gotAClient = True
		    self.clients[channel] = details
		except (socket.error, socket.herror):
		    print 'Server - socket error on accept'

		if len(self.clients) > self.maxPlayers:
		    # -allow the connection
		    # -send a message to the client
		    # -disconnect the client
		    sendData( channel, { 'type' : 'message'
					,'ServerFull' : None } )
		    del self.clients[channel]
		    pass
		else:
		    self.addRequest( channel, {'CurrentLevel':self.currLevel} )

	    if len(self.clients) > 0:
		# generate a client list for use in select
		#   (I was getting an error when I would try
		#   to make a list of the keys directly)
		clientLst = []
		for client in self.clients.keys():
		    clientLst.append(client)

		# query the availability of the sockets for reading only
		#	(incl the listen socket)
		ready_to_read, ready_to_write, in_error = select.select(
			clientLst, [], clientLst, 0)

		# address the sockets in the in_error list
		for client in self.clients.keys():
		    if client in in_error:
			# increment the timeout 
			self.timeout[client] = self.timeout[client] + 1
		    else:
			# clear the timeouts of the other client
			self.timeout[client] = 0

		#
		# recv from connected clients
		#
		for client in ready_to_read:
		    clientPacket = recvData( client )
		    if not clientPacket:
			try:
			    self.timeout[client] = self.timeout[client] + 1
			except KeyError:
			    self.timeout[client] = 1
		    else:
			self.readPacket( client, clientPacket )

		#time.sleep(.3)

		# process the 'client' information #
		#
		# #

		# check the availability of the client sockets for writing
		try:
		    ready_to_read, ready_to_write, in_error = select.select(
			    [], clientLst, clientLst, 0)
		    #
		    # send request packets to the respective clients
		    #
		    tempReqPack = dict(self.requestPackets)
		    for client in tempReqPack:
			# if there are any requests to pass
			if client in ready_to_write:
			    sendData(client, self.requestPackets[client])
			    del self.requestPackets[client]

		    # create a server packet
		    serverPacket = self.genUpdate()
		except:
		    pass

		
		# check the availability of the client sockets for writing
		ready_to_read, ready_to_write, in_error = select.select(
			[], clientLst, clientLst, 0)
		#
		# send outgoing data to clients
		#
		for client in ready_to_write:
		    sendData(client, serverPacket)


		for client in self.clients.keys():
		    try:
			if self.timeout[client] >= 10:
			    client.close()
			    del self.clients[client]
		    except KeyError:
			pass

	    # rest the process for a moment
	    time.sleep(.1)

	# close all connections
	for client in self.clients.keys():
	    client.close()

	# and close the socket
	self.channel.close()
	
	# and the server process closes
	print 'server closed'


    def genUpdate(self):
	"""
	This packet compiles the player/session data into a packet(dict)
	"""
	update = { 'type' :  'update'
		, 'players' : self.playerData.values()
		, 'time' : self.gameTime
		, 'level' : self.currLevel }
	#print 'SERVER - gen update :: ', update
	return update

    def addRequest(self, channel, request):
	"""
	Appends 'message' type packet requests for specific clients
	to a packet-dict which is later sent at first chance to the
	client channel.
	"""

	# make a packet if one doesn't already exist
	if channel not in self.requestPackets:
	    self.requestPackets[ channel ] = {'type' : 'message'}

	# loop through all requests provided
	for key in request.keys():
	    if key == 'type':
		print 'foolish..'
		continue
	    
	    # place the request into the request packet under
	    #	the same key (previous yet-unprocessed requests
	    #	with the same name will be over-written).
	    self.requestPackets[channel][key] = request[key]

    def readPacket(self, channel, packet):
	"""
	This function will read the packet(dict) received from a client
	"""
	try:
	    # if its a client packet, store it
	    if packet['type'] == 'update':
		# store the player's data
		self.playerData[channel] = {
			'position' : packet['position'],
			'name' : packet['name'],
			'pType' : packet['pType'],
			'GameStatus' : packet['GameStatus']}

		for client in self.clients:
		    if client == channel:
			continue
		    
		    if packet['GameStatus'] == 'winner':
			self.addRequest( client,
				    {'GameStatus' : 'winner'} )
		    elif packet['GameStatus'] == 'loser':
			self.addRequest( client,
				    {'GameStatus' : 'loser'} )
		    

	    # if its a command packet, check the packets keys
	    elif packet['type'] == 'message':
		if 'GameOver' in packet:
		    for client in self.clients:
			if client == channel:
			    continue
			else:
			    self.addRequest(client, {'GameOver':packet['GameOver']})

		# check for 'setOwner command
		if 'SetOwner' in packet:
		    # make sure we don't already have an owner
		    if self.owner == None:
			# otherwise, set this channel as the owner
			self.owner = channel
		    else:
			print 'the server already has an owner'

		if 'GetLevel' in packet:
		    self.addRequest(channel, {'CurrentLevel':self.currLevel})

		if 'GetNextLevel' in packet:
		    # add a request with the "next level" in it
		    self.addRequest(channel, {'NextLevel':self.getNextLevel()})

		# these cmds are only applicable to the server owner
		if self.owner == channel:
		    # check for 'kill' command
		    if 'Kill' in packet:
			print "Kill Server Received"
			self.kill = True
		    
		    # set the level/next-level
		    if 'NextLevel' in packet:
			self.nextLevel = packet['NextLevel']

		    if 'ChangeLevel' in packet:
			if packet['ChangeLevel'] == None:
			    if self.nextLevel:# != None
				self.level = self.nextLevel
				print 'Server has changed to the next level'
			else:
			    self.level = packet['ChangeLevel']
			    print 'Server level has been set to:', self.level
			# I may send a 'message' packet here to inform
			#   the players that the level has been changed
			#   so that the game engine can respond

		    if 'MaxPlayers' in packet:
			if packet['MaxPlayers'] >= 1:
			    self.maxPlayers = packet['MaxPlayers']
	
		    if 'ServerName' in packet:
			self.name = packet['ServerName']

		    if 'StartRound' in packet:
			#packet['StartRound']
			print 'Start Round'

		# Connection Reset by Peer
		if 'CRbP' in packet:
		    del self.clients[channel]

		# catch a client's vote for a level
		if 'VoteLevel' in packet:
		    # either incr a vote-counter or add a new
		    #   candidate to the hash (with a vote)
		    level = packet['VoteLevel']
		    if level in self.levelVotes:
			self.levelVotes[level] = self.levelVotes[level] + 1
		    else:
			self.levelVotes[level] = 1

		if 'LeaveServer' in packet:
		    del self.clients[channel]
		    channel.close()
		    # kill the server if the owner leaves
		    if self.owner == channel:
			self.owner = None
			self.kill = True

	# catch the dictionary key errors
	except KeyError:
	    print 'Key Error in ReadPacket()', sys.exc_info()


    def setLevelQueue(self, maps=[]):
	"""
	Sets which levels and in what order the server will set
	the map.
	"""
	self.levelQueue = maps

    def getNextLevel(self):
	"""
	Answers the question, .. who REALLY shot MLK...
	No, it returns what the next map will be.
	"""
	if len(self.levelQueue) < 1:
	    return None

	nextIndex = self.levelIndex + 1
	if nextIndex >= len(self.levelQueue):
	    nextIndex = 0

	return self.levelQueue[nextIndex]

    def nextLevel(self):
	"""
	This increments the server to the next level.  This message
	will eventually make it out to the clients in the next 'update'
	packet.
	"""
	# if there's a special request then use this next
	if self.nextLevel:
	    self.currLevel = str(self.nextLevel)
	    self.nextLevel = None
	else:
	    # if the level cue is empty
	    if len(self.levelQueue) < 1:
		self.currLevel = None
	    else:
		# get the next level in the queue
		self.levelIndex += 1
		
		# wrap the index if at the end
		if self.levelIndex >= len(self.levelQueue):
		    self.levelIndex == 0
		    
		# get the level at the index
		self.currLevel = self.levelQueue[self.levelIndex]

	# return the current level
	return self.currLevel


