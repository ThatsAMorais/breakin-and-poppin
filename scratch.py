#+# scratch #+#

		#overlap = self.collideObjs(playerBBox, tileBox)
		playerPos = self.player.pos
		playerBox = self.player.getBBox()
		
		# Determine if the position is closer to the left
		#   or right side of the box.
		# X axis #
		print "tile box = ", tileBox
		print "player pos = ", self.player.pos[0]
		print "player box = ", playerBox
		print "disp: ", playerPos[0]-tileBox[0], tileBox[2]-playerPos[0]

		if playerPos[0]-tileBox[0] < abs(tileBox[2]-playerPos[0]):
		    print 1, playerPos[0]-tileBox[0]
		    self.player.pos[0] -= playerPos[0]-tileBox[0]

		elif abs(tileBox[2]-playerPos[0]) < playerPos[0]-tileBox[0]:
		    print 2, tileBox[2]-playerPos[0]
		    self.player.pos[0] += tileBox[2]-playerPos[0]

		else:
		    print 3

		print "new player pos = ", self.player.pos[0]
		print "--"
		# Y axis #
		#if playerPos[1]-tileBox[1] > tileBox[3]-playerPos[1]:
		#    offset[1] = -(playerPos[1]-tileBox[1])
		#elif playerPos[1]-tileBox[1] < tileBox[3]-playerPos[1]:
		#    offset[1] = tileBox[3]-playerPos[1]
