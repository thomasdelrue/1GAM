import random
import pygame
import vector2

from constants import *
from vector2 import Vector2 
from bezier import *
from pygame import Rect, Surface



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

class Alien(pygame.sprite.Sprite):
	def __init__(self, alienType, currentPos, formPos, state=ENTERING):
		pygame.sprite.Sprite.__init__(self)
		
		self.alienType = alienType
		# current position on screen
		self.currentPos = currentPos
		# the previous position
		self.prevPos = currentPos
		# designated spot in the formation 
		self.formPos = formPos
		self.state = state
		self.trajectory = []
		# orientation
		self.heading = 0
		
		if self.alienType == GALAGA:
			self.lives = 2
			self.colour = BLUE
		else:
			self.lives = 1
			if self.alienType == BEE:
				self.colour = YELLOW
			elif self.alienType == BUTTERFLY:
				self.colour = RED
		
		# to do: use the Sprite class for the shape 
		#self.shape = Rect(0, 0, ALIENSIZE, ALIENSIZE)
		self.origShape = Surface((ALIENSIZE, ALIENSIZE))
		#self.shape.fill(self.colour)
		pygame.draw.rect(self.origShape, self.colour, (1, 1, ALIENSIZE - 1, ALIENSIZE - 1), 0)
		self.shape = self.origShape
		self.rect = self.shape.get_rect()
		#self.shape.center = self.currentPos
		self.rect.center = self.currentPos
		
		
	def getTrajectory(self, typeOfTrajectory, timePassed):
		# to do
		cp = BEZ_CP_SETS[typeOfTrajectory]

		'''TO DO: calculate the actual destination point for formPos, instead of the current one, since the formation shifts...'''
		cp.append(self.formation.formationCoord[self.formPos])
		path = BezierPath(cp)
		#path.getLength()
		print(path.controlPoints)
		self.trajectory = path.getDrawingPoints(timePassed)
		
	
	def move(self):
		if self.state == IN_FORMATION:
			# movement calculated in Formation
			
			if self.heading != 0:
				self.getHeading()
			
			pass
		elif self.state == ENTERING:
			if len(self.trajectory) > 0:
				self.oldPos = self.currentPos
				self.currentPos = self.trajectory.pop(0)
				
				self.getHeading()
				
				print('alien currentPost', self.currentPos)
				#self.shape.center = tuple(self.currentPos)
				self.rect.center = tuple(self.currentPos)
			else:
				self.state = IN_FORMATION
				
	def getHeading(self):
		self.heading += 5
		self.shape = pygame.transform.rotate(self.origShape, self.heading)
		self.rect = self.shape.get_rect()
				

# maybe make this a pygame.sprite.Group ?
class AlienCollection(object):
	def __init__(self):
		self.formRec = Rect(0, 0, (ALIENSIZE * 1.5) * 9 + ALIENSIZE, (ALIENSIZE * 1.5) * 4 + ALIENSIZE)
		self.formRec.midbottom = (VIEWWIDTH // 2, VIEWHEIGHT // 2)
		self.formationCoord = {(r, c): (int(self.formRec.left + ALIENSIZE * c * 1.5 + ALIENSIZE // 2), int(self.formRec.top + ALIENSIZE * r * 1.5 + ALIENSIZE // 2)) for r in range(5) for c in range(10) }
		
		self.state = FORMING
		
		self.aliens = []
		self.bolts = []
		
		self.step = 4
		self.directionStep = +1
		self.speedStep = .5
		self.timeSpent = .0

	def addAlien(self, alien):
		self.aliens.append(alien)
		alien.formation = self
		
	def removeAlien(self, alien):
		alien.formation = None
		self.aliens.remove(alien)
		
	def moveFormation(self, timePassed):
		if self.state == FORMATION_DONE:
			# expanding/contracting
			self.timeSpent += timePassed
			if self.timeSpent > self.speedStep:
				self.timeSpent -= self.speedStep
				self.step += 1
				
				self.formRec.left -= self.directionStep * 9
				self.formRec.width += self.directionStep * 18
				
				margin = (self.formRec.width - ALIENSIZE * 10) // 9
				for k in self.formationCoord:
					if not k[0] == 0:
						if k[0] == 1:
							print()
						self.formationCoord[k] = self.formRec.left + (ALIENSIZE + margin) * k[1], self.formationCoord[k][1]
						
				if self.step >= 8:
					self.step = 0
					self.directionStep *= -1


		elif self.state == FORMING or (self.state == FORMATION_DONE and self.step != 4):
			# ebb/flow/tide -- 8 stappen naar de ene kant, 8 naar de andere
			self.timeSpent += timePassed
			if self.timeSpent > self.speedStep:
				self.timeSpent -= self.speedStep
				self.step += 1
				
				self.formRec.left += self.directionStep * 10
				print('xbounds Rec, step {}: {} - {}'.format(self.step, self.formRec.left, self.formRec.right))
				for k in self.formationCoord:
					self.formationCoord[k] = self.formationCoord[k][0] + self.directionStep * 10, self.formationCoord[k][1]
				
				if self.step >= 8:
					self.step = 0
					self.directionStep *= -1
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
		self.state = MOVING
		
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
			
			
	
	
