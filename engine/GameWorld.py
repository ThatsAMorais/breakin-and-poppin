#####	   File : GameWorld.py
####	 Author : Alex Morais
### Description : This object encapsulates game objects so that the
###		engine state only has to call render on this object
###		and it serves to encapsulate all objects to be 
###		rendered with respect to world coords as opposed to
###		screen coords. Any renderable object can be added to
###		the GameWorld, but it is intended to contain objects
###		positioned in world space.
##

from managers.SettingsManager import *
from managers.FontManager import *
from level.PreBuiltLevel import *
from players.Robber import *
from players.Cop import *
from engine.Screen import *
from input.Keyboard import *
from input.Mouse import *
from ui.Font import *
from ui.UIText import *
from OpenGL.GLUT import glutTimerFunc


class GameWorld():
    """
    A class to encapsulate all objects in the world-space of the 'game'.
    """

    def __init__(self):
	"""
	Init: (self)
	"""

	# grab the settings manager cause we need it here
	self.setsMgr = SettingsManager()

	# all things in the world scene (except the level and the player)
	self.objects = []
	self.collisions = {}
	self.prevCols = {}
	# store this separately so we know where it is
	self.levelName = ""
	self.level = PreBuiltLevel()
	# the user's player object
	self.player = None
	# the peer players on other computers in the network
	self.peers = {}
	# the player's controller (set to settings-default)
	self.controller = None
	self.setControllerType( self.setsMgr.controller )

	# the screen object
	self.screen = Screen()
	# the screen's position in world space
	self.scrScroll = [0,0]
	self.scrSize = self.screen.getSize()
	scrMiddle = (self.scrSize[0]/2, self.scrSize[1]/2)
	#self.sideBuf = ( self.scrSize[0]*0.4, self.scrSize[1]*0.4 )
	self.sideBuf = ( 100, 100 )
	# the max deviation that the player 
	self.maxDevi = ( self.scrSize[0]/2 - self.sideBuf[0]
			, self.scrSize[1]/2 - self.sideBuf[1] )
	self.scrSpeed = (0,0)

	self.status = "undecided"

	self.active = False # This is the 'pause' flag.
	self.gameTime = 0.0
	self.gameStatus = 'unresolved'
	# Denotes whether the Robber has touched the drop point
	self.drop_point_hit = False	# for the 'Robber' only

	# A few messages for indicating to the user
	# get/load the font
	self.font = FontManager().loadFont( 'Basic' )

	# a text objects for der screenzimmer
	self.txtObjs = []   # this will make rendering easy
	self.cops_got_ya = UIText("The Cops got ya!!",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.cops_got_ya )

	self.robber_detained = UIText("The Robber has been detained.",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.robber_detained )

	self.lose_the_cops = UIText("Ya gotta lose the cops first!",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.lose_the_cops )

	self.go_to_base = UIText("Ya already dropped off the loot.",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.go_to_base )

	self.go_to_drop = UIText("Go to the Drop Point first.",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.go_to_drop )

	self.safe_at_base = UIText("Ya made it!  Great job.",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.safe_at_base )

	self.dropped_loot = UIText("Good, now head to the Base",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.dropped_loot )

	self.robber_eluded = UIText("The robber eluded us.",
		pos=scrMiddle, font=self.font, scale=0.025)
	self.txtObjs.append( self.robber_eluded )

	for txtObj in self.txtObjs:
	    txtObj.setVisible( False )
	    txtObj.center()


    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # World control
    def pause(self):
	"""
	Pause/Unpause the gameworld
	"""
	if self.active == True:
	    self.active = False
	else:
	    self.active = True
	return self.active



    def startGame(self):
	"""
	Explicitly sets a game to active
	"""
	self.active = True


    def stopGame(self):
	"""
	Explicitly stops the game
	"""
	self.active = False


    def on_socket( self, packet ):
	"""
	receives the 'update' packet and reads it
	"""
	#process the packet
	try:
	    for plData in packet['players']:
		self.updatePeer( plData )
	except KeyError:
	    print "GameWorld -` on_socket - Missing 'players' in update packet"
	    pass



    def update( self, elapsed ):
	"""
	Call the update function of all objects in the gameworld.
	"""

	# don't update if the gameworld is inactive
	if not self.active:
	    # either the game is paused or the game hasn't started yet
	    return

	# update the controller
	#   (as it might be necessary depending on the type)
	self.controller.update(elapsed)

	# Update collisions first(to hopefully achieve greater accuracy)
	for coll in self.collisions.values():
	    coll.update(elapsed)

	# send the elapsed time to the player (for whatever it needs to do)
	if self.player:
	    # update the player animation
	    self.player.update(elapsed)

	self.ensureWithinLevel()

	# update the screen pos based on the character 
	#   pos and facing direction
	self.scrollScreen()

	if self.level:
	    # update the level
	    self.level.update(elapsed)

	# update the peer avatars
	for peer in self.peers.values():
	    peer.update(elapsed)

	# all world objects
	for obj in self.objects:
	    obj.update(elapsed)

	#/\/\/\# Collision #/\/\/\#
	# copy the old collisions to another list
	self.prevCols = dict(self.collisions)
	self.collisions = {}
	## Player-to-Level
	if self.player.getType() == "Robber":

	    tileType, offset = self.level.getTileAtPoint(self.player.pos)

	    if not tileType:
		pass

	    elif tileType == 'base':
		self.addCollision(Collision.ROBBER, Collision.BASE)

	    elif tileType == 'building':
		posAdjust = [0,0]

		if offset[0] < self.level.tileHalfSize[0]:
		    posAdjust[0] = offset[0] * -1
		elif offset[0] >= self.level.tileHalfSize[0]:
		    posAdjust[0] = (self.level.tileScrSize[0]-offset[0])
		    
		if offset[1] < self.level.tileHalfSize[1]:
		    posAdjust[1] = offset[1] * -1
		elif offset[1] >= self.level.tileHalfSize[1]:
		    posAdjust[1] = (self.level.tileScrSize[1]-offset[1])

		self.player.pos[0] += posAdjust[0]
		self.player.pos[1] += posAdjust[1]

	    elif tileType == 'drop-point':
		self.addCollision(Collision.ROBBER, Collision.DROP_POINT)

	
	for peer in self.peers.values():
	    # player's of the same type do not collide (for now)
	    if peer.getType() != self.player.getType():
		if self.player.getType() == "Cop":
		    # collide the peer(a robber) with the player's spotlight
		    if self.player.collidePoint( peer.pos  ):
			self.addCollision( Collision.ROBBER, Collision.COP )

		elif self.player.getType() == "Robber":
		    # collide the peer's spotlight with the player(a robber)
		    if peer.collidePoint( self.player.pos ):
			self.addCollision( Collision.ROBBER, Collision.COP )
		    
	# This is not in use for now #	
	## Player-to-Objects
	#for obj in self.objects:
	#    #collide the object box with the robber pos only
	#    if self.player.getType() == "Robber":
	#	print 'object'

	
	#/\/\/\# Collision Response #/\/\/\#

	cop_robber_coll = False
	try:
	    # First, determine if there is a cop-to-robber collision as
	    #   this will be relevant to the effect of other collisions
	    # This collision depends on the player type
	    if self.collisions[(Collision.ROBBER, Collision.COP)].getTime() > 3000:
		if self.player.getType() == "Robber":
		    #self.cops_got_ya.setPos(\
		    #	    ( self.player.pos[0], self.player.pos[1]+10 ) )
		    self.cops_got_ya.setVisible(True)
		    glutTimerFunc( 2000, self.cops_got_ya.toggleVisible, 0 )
		    self.gameStatus = "loser"

		elif self.player.getType() == "Cop":
		    #self.robber_detained.setPos(\
		    #	    ( self.player.pos[0], self.player.pos[1]+10 ))
		    self.robber_detained.setVisible(True)
		    glutTimerFunc( 2000, self.robber_detained.toggleVisible, 0 )
		    self.gameStatus = "winner"
		self.active = True
	except KeyError:
	    # the collision is not present (saved myself a few 'if'-stmts, above)
	    pass

	try:
	    # We can assume the next two can only occur when the player is a "Robber"
	    if (Collision.ROBBER, Collision.DROP_POINT) in self.collisions:
		if cop_robber_coll == True:
		    #self.lose_the_cops.setPos(\
		    #	    (self.player.pos[0], self.player.pos[1]+10) )
		    self.lose_the_cops.setVisible(True)
		    glutTimerFunc( 2000, self.lose_the_cops.toggleVisible, 0 )
		#elif self.drop_point_hit == True:
		#    #self.go_to_base.centerAround( self.player.pos )
		#    self.go_to_base.setVisible(True)
		#    glutTimerFunc( 2000, self.go_to_base.toggleVisible, 0 )

		elif self.collisions[(Collision.ROBBER, Collision.DROP_POINT)].getTime() > 3000:
		    self.drop_point_hit = True
		    #self.dropped_loot.setPos(\
		    #	    ( self.player.pos[0], self.player.pos[1]+10 ))
		    self.dropped_loot.setVisible(True)
		    glutTimerFunc( 2000, self.dropped_loot.toggleVisible, 0 )

	except KeyError:
	    # the collision is not present (saved myself a few 'if'-stmts, above)
	    pass

	try:
	    if (Collision.ROBBER, Collision.BASE) in self.collisions:
		if cop_robber_coll == True:
		    #self.lose_the_cops.setPos(\
		    #	    ( self.player.pos[0], self.player.pos[1]+10 ))
		    self.lose_the_cops.setVisible(True)
		    glutTimerFunc( 2000, self.lose_the_cops.toggleVisible, 0 )
		elif self.drop_point_hit == False:
		    self.go_to_drop.setVisible(True)
		    glutTimerFunc( 2000, self.go_to_drop.toggleVisible, 0 )

		elif self.collisions[(Collision.ROBBER, Collision.BASE)].getTime() > 3000:
		    self.gameStatus = "winner"
		    self.active = False
		    #self.safe_at_base.setPos(\
		    #	    ( self.player.pos[0], self.player.pos[1]+10 ))
		    self.safe_at_base.setVisible(True)
		    glutTimerFunc( 2000, self.safe_at_base.toggleVisible, 0 )
	except KeyError:
	    # the collision is not present (saved myself a few 'if'-stmts, above)
	    pass



    def addCollision(self, type1, type2):
	"""
	This function determines whether to add a new collision or
	to transfer an existing one to the new list.
	"""
	if (type1, type2) in self.prevCols:
	    self.collisions[(type1, type2)] = self.prevCols[(type1, type2)]
	else:
	    self.collisions[(type1, type2)] = Collision((type1, type2))




    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # Player setup/control
    def setPlayer( self, player ):
	"""
	Set the player by object
	"""
	self.player = player
	#self.player.setName( self.setsMgr.player_name )

	if self.controller:
	    self.controller.setPlayer( self.player )




    def setPlayerType( self, type ):
	"""
	Set the player by type-str
	"""
	if type == 'Robber':
	    self.setPlayer( Robber() )
	    #self.player.setName( self.setsMgr.player_name )
	    
	    if self.level:
		self.level.setTilesPerView( [15,15] )
	    	self.player.setPos(self.level.getThiefInitPos())
		self.player.scaleSizeByTileSize( self.level.getTileSize() )

	elif type == 'Cop':
	    self.setPlayer( Cop() )
	    #self.player.setName( self.setsMgr.player_name )
	    
	    if self.level:
		self.level.setTilesPerView( -1 )
	    	self.player.setPos( self.level.getCopInitPos() )
		self.player.scaleSizeByTileSize( self.level.getTileSize() )

	else:
	    print type, ' is not an acceptable argument to setPlayer()'

	if self.controller:
	    self.controller.setPlayer( self.player )

	self.scrSpeed = ( int(self.player.moveSpeed[0]),
			    int(self.player.moveSpeed[1]) )
	self.centerScreenAroundPlayer()


    def getPlayer( self ):
	return self.player



    def getPlayerType( self ):
	if self.player:
	    return self.player.getType()
	else:
	    return None


    def movePlayer( self, offset=(0,0) ):
	"""
	Simply calls the position func of the player
	"""
	self.player.move( offset )


    def positionPlayer( self, pos=(1,1) ):
	"""
	Place the player at some particular spot
	"""
	self.player.setPos( pos )


    def ensureWithinLevel( self ):
	"""
	checks the player's position is within the level area
	"""

	mapSize = self.level.mapSize
	tileSize = self.level.tileScrSize
	playerPos = self.player.pos

	# check that PosX > left_edgeTileWidth
	if playerPos[0] < 0:
	    self.positionPlayer([0, playerPos[1]])

	# check that PosY > top_edgeTileHeight
	if playerPos[1] < 0:
	    self.positionPlayer([playerPos[0], 0])

	# check that PosX < right_EdgeTileWidths
	if playerPos[0] > mapSize[0]*tileSize[0]:
	    self.positionPlayer( [(mapSize[0]*tileSize[0]), playerPos[1]] )
	
	# check that PosY < bottom_EdgeTileWidth
	if playerPos[1] > mapSize[1]*tileSize[1]:
	    self.positionPlayer( [playerPos[0], (mapSize[1]*tileSize[1])] )
	    



    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # Controller Setup
    def setController( self, controller ):
	"""
	Set the controller by passing a derived Controller class
	"""
	self.controller = controller
	self.controller.setPlayer( self.player )



    def setControllerType( self, type ):
	"""
	Sets the controller by passing either "keyboard" or "mouse"
	"""
	# determine which type of controller to create
	if type.lower() == "keyboard":
	    self.controller = Keyboard()
	elif type.lower() == "mouse":
	    self.controller = Mouse()
	else:
	    print "Set Controller Failed with type: ", type
	    return

	# set the player of the controller
	self.controller.setPlayer(self.player)



    def getController( self ):
	return self.controller



    def centerScreenAroundPlayer(self):
	"""
	As the name suggests, it centers the screen as best it can
	around the player.
	"""
	self.positionScreen( [self.player.pos[0]-(self.scrSize[0]/2),
			   self.player.pos[1]-(self.scrSize[1]/2) ] )
	# this will check the screen to make sure it is within the bounds
	#   of the level
	self.moveScreen( [0,0] )


    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # Level setup
    def setLevelByName( self, level=None ):
	"""
	Set the level by name
	"""
	if level:
	    self.levelName = level
	    self.level.load( level )

	    if self.player:
		if self.player.type == 'Robber':
		    self.level.setTilesPerView( [15,15] )
		    self.player.setPos( self.level.getThiefInitPos() )
		    self.player.scaleSizeByTileSize( self.level.getTileSize() )
		elif self.player.type == 'Cop':
		    self.level.setTilesPerView( -1 )
		    self.player.setPos( self.level.getCopInitPos() )
		    self.player.scaleSizeByTileSize( self.level.getTileSize() )

	    self.centerScreenAroundPlayer()
	else:
	    self.level = None


    def setLevel( self, level=None ):
	"""
	Set the level with an instance
	"""
	self.level = level
	
	if self.player and self.level:
	    self.levelName = self.level.lvlName
	    if self.player.type == 'Robber':
		self.level.setTilesPerView( [15,15] )
		self.player.setPos( self.level.getThiefInitPos() )
		self.player.scaleSizeByTileSize( self.level.getTileSize() )
	    elif self.player.type == 'Cop':
		self.level.setTilesPerView( -1 )
		self.player.setPos( self.level.getCopInitPos() )
		self.player.scaleSizeByTileSize( self.level.getTileSize() )

	    self.centerScreenAroundPlayer()


    def getLevel( self ):
	return self.level



    def getLevelName( self ):
	return self.level.lvlName



    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # Drawing
    def render( self ):
	"""
	Called by the screen class; this function will call render()
	of all entities in self.objects and return the compiled list
	"""

	renderList = []

	# don't update if paused
	if not self.active:
	    return renderList

	# render order is relevant in this function esp. wrt the level and
	#   the player.
	if self.level:
	    if self.player.type == 'Robber':
		renderList.extend(self.level.render(self.scrScroll))
	    elif self.player.type == 'Cop':
		quad = self.player.getQuad( self.scrScroll )
		renderList.extend(self.level.render(self.scrScroll, quad))
	
	if self.player:
	    renderList.extend( self.player.render(self.scrScroll) )

	for object in self.objects:
	    renderList.extend( object.render(self.scrScroll) )

	for peer in self.peers.values():
	    if self.player.type == "Cop":
	    	quad = self.player.getAreaUnder( self.scrScroll )

	    	if peer.pos[0] > quad[0] and peer.pos[0] < quad[2] \
	    	    and peer.pos[1] > quad[1] and peer.pos[1] < quad[3]:
	    		renderList.extend( peer.render(self.scrScroll) )
	    else:
		renderList.extend( peer.render(self.scrScroll) )


	for txt in self.txtObjs:
	    #renderList.extend( txt.render(self.scrScroll) )
	    renderList.extend( txt.render() )

	return renderList


    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # Screen control
    def moveScreen( self, offset=[0,0] ):
	"""
	Moves the screen in world coords offset from its current
	position.
	"""
	if not self.screen:
	    self.screen = Screen()
	
	# validate the upper and left extent
	self.scrScroll[0] = max( self.scrScroll[0]+offset[0], 0 )
	self.scrScroll[1] = max( self.scrScroll[1]+offset[1], 0 )

	tileSize = self.level.tileScrSize
	scrSize = self.screen.size
	mapSize = self.level.mapSize

	self.scrScroll[0] = min( self.scrScroll[0]
				, (mapSize[0]*tileSize[0]) - scrSize[0] )
	self.scrScroll[1] = min( self.scrScroll[1]
			    , (mapSize[1]*tileSize[1]) - scrSize[1] )


    def positionScreen( self, pos=[0,0] ):
	"""
	Put the screen at a specific position
	"""
	self.scrScroll[0] = pos[0]
	self.scrScroll[1] = pos[1]
    

    def scrollScreen(self):
	
	dir = self.player.facingDir
	#playerPos = list(self.player.getCenterPos())
	playerPos = list(self.player.pos)

	if not self.screen:
	    self.screen = Screen()

	screenRes = self.screen.size

	# the extent from the side-buffer(above)
	scrExtent = ( self.scrScroll[0] + screenRes[0]
		    , self.scrScroll[1] + screenRes[1] )

	# The current screen scroll + the side buffer offset
	#   and the size 
	# The order of the "walls" indicated within are
	#   West, North, East, South
	scrEdge = ( self.scrScroll[0] + self.sideBuf[0]
		    , self.scrScroll[1] + self.sideBuf[1]
		    , scrExtent[0] - self.sideBuf[0]
		    , scrExtent[1] - self.sideBuf[1] )

	# the screen movement based on its current position
	offset = [0,0]

	# Horizontal, player is within the area
	if playerPos[0] > scrEdge[0] and dir[0] > 0:
	    if abs(playerPos[0] - scrEdge[0]) >= self.scrSpeed[0]:
		offset[0] = self.scrSpeed[0]
	    else:
		offset[0] = int(playerPos[0] - scrEdge[0])

	if playerPos[0] < scrEdge[2] and dir[0] < 0:
	    if abs(playerPos[0] - scrEdge[2]) >= self.scrSpeed[0]:
		offset[0] = -self.scrSpeed[0]
	    else:
		# ..subtracted in this order, (pos - scrEdge) is already negative..
		offset[0] = int(playerPos[0] - scrEdge[2])

	# Vertical
	if playerPos[1] > scrEdge[1] and dir[1] > 0:
	    if abs(playerPos[1] - scrEdge[1]) >= self.scrSpeed[1]:
		offset[1] = self.scrSpeed[1]
	    else:
		offset[1] = int(playerPos[1] - scrEdge[1])

	if playerPos[1] < scrEdge[3] and dir[1] < 0:
	    if abs(playerPos[1] - scrEdge[3]) >= self.scrSpeed[1]:
		offset[1] = -self.scrSpeed[1]
	    else:
		offset[1] = int(playerPos[1] - scrEdge[3])

	
	# move the screen by the ofset
	self.moveScreen( offset )


    #\\\\\\\\\\\\\\\\\\\\\\\\\\#
    # World-object stuff
    def addObject( self, newObj ):
	"""
	Appends an object to the game world(as long as it can be rendered)
	"""

	if 'render' in dir( newObj ):
	    self.objects.append( newObj )
	else:
	    print 'Warning : GameWorld : newObj does not have a "render" function; it was not added to the render list.'


    def updatePeer( self, update ):
	"""
	update (or add) a peer to the game world
	"""
	if update['name'] == self.player.getName():
	    # ignore this packet because it is the player packet
	    return

	if update['name'] not in self.peers:
	    # Make a player object of the type in the packet
	    if update['pType'] == 'Robber':
		newPlayer = Robber()
		newPlayer.setPos( self.scalePos(update['position']) )
		newPlayer.setSize( self.getPeerSize( "Robber") )
		self.peers[ update['name'] ] = newPlayer
	    if update['pType'] == 'Cop':
		newPlayer = Cop()
		newPlayer.setPos( self.scalePos(update['position']) )
		newPlayer.setSize( self.getPeerSize( "Cop") )
		self.peers[ update['name'] ] = newPlayer
	else:
	    self.peers[ update['name'] ].setPos(\
		    self.scalePos(update['position']))

    def scalePos(self, pos):
	"""
	scales the peer's map pos to tile coords
	"""
	tileSize = self.level.getTileSize()
	return [ pos[0]*tileSize[0], pos[1]*tileSize[1] ]

    def getPeerSize(self, type):
	"""
	Calculates and returns the size of a peer based on its type
	and the playyer's type.
	"""
	size = None
	tileSize = self.level.getTileSize()

	if self.player.type == type:
	    pass
	elif self.player.type == "Robber":
	    # then peer-type == "Cop"
	    size = [tileSize[0]*5, tileSize[1]*5]
	elif self.player.type == "Cop":
	    # then peer-type == "Robber"
	    size = [tileSize[0]*0.5, tileSize[1]*0.5]

	return size


    def on_key_press(self, key, x, y):
	"""On key press"""
	if self.active:
	    if self.controller and isinstance( self.controller, Keyboard ):
		self.controller.on_key_press(key, x, y)



    def on_key_release(self, key, x, y):
	"""On key release"""
	if self.active:
	    if self.controller and isinstance( self.controller, Keyboard ):
		self.controller.on_key_release(key, x, y)



    def on_specialkey_press(self, key, x, y):
	"""On special key press"""
	if self.active:
	    if self.controller and isinstance( self.controller, Keyboard ):
		self.controller.on_specialkey_press(key, x, y)




    def on_specialkey_release(self, key, x, y):
	"""On special key release"""
	if self.active:
	    if self.controller and isinstance( self.controller, Keyboard ):
		self.controller.on_specialkey_release(key, x, y)




    def on_mouse_motion(self, x, y):
	"""On mouse motion"""
	if self.active:
	    if self.controller and isinstance( self.controller, Mouse ):
		self.controller.on_mouse_motion(x, y)




    def on_mouse(self, button, state, x, y):
	"""On mouse press/release"""
	if self.active:
	    if self.controller and isinstance( self.controller, Mouse ):
		self.controller.on_mouse(button, state, x, y)


    
