from constants import *
from pygame import Rect




'''
Aliens should be finite-state machines...

Trajectory object...
either with fancy mathematical functions for the possible trajectory,
or rudimentary goniometrical trajectories... ie. plotted along a straight 
line, then along the perimeter of a circle... (tryout scripts...)

Formations object, 
that holds all the coordinates for the different positions of the formation,
whether the position is occupied by an alien or not...
having these coordinates, then it's easy to assign an alien that makes it's
entrance it's 'destination point' in the formation...
'''

class Alien(object):
	def __init__(self, alienType, currentPos, formPos):
		self.alienType = alienType
		self.currentPos = currentPos
		self.formPos = formPos
		if self.alienType == GALAGA:
			self.lives = 2
			self.colour = BLUE
		else:
			self.lives = 1
			if self.alienType == BEE:
				self.colour = YELLOW
			elif self.alienType == BUTTERFLY:
				self.colour = RED
		self.shape = Rect(0, 0, ALIENSIZE, ALIENSIZE)
		self.shape.topleft = self.currentPos
		


class AlienCollection(object):
	def __init__(self):
		self.formRec = Rect(0, 0, (ALIENSIZE * 1.5) * 9 + ALIENSIZE, (ALIENSIZE * 1.5) * 4 + ALIENSIZE)
		self.formRec.midbottom = (VIEWWIDTH // 2, VIEWHEIGHT // 2)
		self.formation = {(r, c): (self.formRec.left + ALIENSIZE * c * 1.5 , self.formRec.top + ALIENSIZE * r * 1.5) for r in range(5) for c in range(10) }
		
		self.state = FORMING
		
		self.aliens = []
		self.bolts = []
		

	def addAlien(self, alien):
		self.aliens.append(alien)
		
	def removeAlien(self, alien):
		self.aliens.remove(alien)
		
	def moveFormation(self):
		if self.state == FORMATION_DONE :
			# expanding/contracting
			pass
		elif self.state == FORMING:
			# ebb/flow/tide
			pass
		else:
			pass


class Bolt(object):
	def __init__(self, pos):
		self.pos = pos
		self.colour = WHITE
		self.shape = Rect(0, 0, BOLTWIDTH, BOLTLENGTH)
		self.shape.center = self.pos		
		
	def move(self, timePassed):
		self.pos = self.pos[0], self.pos[1] - BOLTSPEED * timePassed
		self.shape.center = self.pos		

		

class Ship(object):
	def __init__(self):
		self.lives = 3
		
		# position
		self.pos = (VIEWWIDTH // 2, SHIPY)
		
		# shape -- placeholder
		self.colour = WHITE
		self.shape = Rect(0, 0, SHIPSIZE, SHIPSIZE)
		self.shape.center = self.pos
		
		# nr of bolts
		self.bolts = []
		
	
	def move(self, movex):
		newx = self.pos[0] + movex
		if newx > VIEWBOUNDS[0] and newx < VIEWBOUNDS[1]:
			self.pos = (newx, self.pos[1])
	
	def fireBolt(self):
		if len(self.bolts) >= 2:
			return
		self.bolts.append(Bolt(self.pos))

	def removeBolt(self, bolt):
		self.bolts.remove(bolt)

	def update(self):
		for bolt in self.bolts:
			if bolt.pos[1] - BOLTLENGTH < 0:
				self.bolts.remove(bolt)
			
			
	
	
