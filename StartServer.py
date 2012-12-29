#! /usr/local/bin/python

#####      File : StartServer.py
####	 Author : Alex Morais
### Description : A script that is spawned by the game engine 
###		to start the server.
##

from multiplayer.GameServer import *

# instantiate a game server
gServer = GameServer()

# set the Server's map list
maps = ["Level1L"]
gServer.setLevelQueue( maps )

# begin the server
gServer.start()

print 'StartServer script complete'

