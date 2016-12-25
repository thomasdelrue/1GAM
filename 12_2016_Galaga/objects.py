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
			self.colour = GREEN
			# TO DO: determine the score of a galaga...
			self.score = 0
		else:
			self.lives = 1
			if self.alienType == BEE:
				self.colour = YELLOW
				self.score = 50
			elif self.alienType == BUTTERFLY:
				self.colour = RED
				self.score = 80

		
		# to do: use the Sprite class for the shape 
		self.origShape = Surface((ALIENSIZE, ALIENSIZE))
		'''pygame.draw.rect(self.origShape, self.colour, (1, 1, ALIENSIZE - 1, ALIENSIZE - 1), 0)
		pygame.draw.circle(self.origShape, BLUE, (5, ALIENSIZE // 2), 3, 0)'''
		pygame.draw.aalines(self.origShape, self.colour, True, [(1, ALIENSIZE // 2), (ALIENSIZE - 2, 1), (ALIENSIZE - 2, ALIENSIZE - 2)])
		self.shape = self.origShape
		self.rect = self.shape.get_rect()
		self.rect.center = self.currentPos
		
		
	def getTrajectory(self, typeOfTrajectory, timePassed):
		# to do
		cp = BEZ_CP_SETS[typeOfTrajectory]
		
		# cp's are relative for these trajectories; they need adjusting from the 'constants' cp
		if typeOfTrajectory in (BEE_DIVE_FROM_R, BEE_DIVE_FROM_L):
			print('currentPos:', self.currentPos)
			print('cp[0]:', cp[0])
			offset = self.currentPos[0] - cp[0][0], self.currentPos[1] - cp[0][1]
			for i in range(len(cp)):
				cp[i] = cp[i][0] + offset[0], cp[i][1] + offset[1]

		#cp.append(self.formation.formationCoord[self.formPos])
		path = BezierPath(cp)
		#print(path.controlPoints)
		self.trajectory = path.getDrawingPoints(timePassed)
	
	
	def hit(self):
		self.lives -= 1
		if self.alienType == GALAGA and self.lives == 1:
			self.colour = BLUE
			pygame.draw.aalines(self.origShape, self.colour, True, [(1, ALIENSIZE // 2), (ALIENSIZE - 2, 1), (ALIENSIZE - 2, ALIENSIZE - 2)])
			self.shape = pygame.transform.rotate(self.origShape, self.heading)
		
		if self.lives == 0:
			if self.state != IN_FORMATION:
				self.score *= 2
			self.state = DEAD
			self.frame = 1
			self.shape = Surface((int(ALIENSIZE * 1.5), int(ALIENSIZE * 1.5)))
			self.rect = self.shape.get_rect()
			self.rect.center = tuple(self.currentPos)
			
			return self.score

		return 0		
	
	def move(self, timePassed):
		if self.state == IN_FORMATION:
			# movement calculated in Formation
			
			if self.heading != 270:
				self.setHeading(270)
			
			pass
		elif self.state in (ENTERING, DIVING):
			if len(self.trajectory) > 0:
				self.oldPos = self.currentPos
				self.currentPos = self.trajectory.pop(0)
				
				self.setHeading()
				
				#print('alien currentPost', self.currentPos)
			else:
				destPos = Vector2(*self.formation.formationCoord[self.formPos])
				diff = destPos - Vector2(*self.currentPos) 
				if diff.get_magnitude() < 10:
					self.state = IN_FORMATION
				else:
					self.oldPos = self.currentPos
					res = Vector2(*self.currentPos) + diff.normalize() * ALIENSPEED * timePassed
					self.currentPos = tuple(res) 
					self.setHeading()

			self.rect.center = tuple(self.currentPos)
		
			
				
	def setHeading(self, heading=None):
		if heading is None:
			self.heading = (Vector2(*self.currentPos) - Vector2(*self.oldPos)).getHeading()
		else:
			self.heading = heading
		self.shape = pygame.transform.rotate(self.origShape, self.heading)
		self.rect = self.shape.get_rect()
				



# maybe make this a pygame.sprite.Group ?
class AlienCollection(object):
	def __init__(self):
		self.formRec = Rect(0, 0, (ALIENSIZE * 1.5) * 9 + ALIENSIZE, (ALIENSIZE * 1.5) * 4 + ALIENSIZE)
		self.formRec.midbottom = (VIEWWIDTH // 2, VIEWHEIGHT // 2)
		self.formationCoord = {(r, c): (int(self.formRec.left + ALIENSIZE * c * 1.5 + ALIENSIZE // 2), int(self.formRec.top + ALIENSIZE * r * 1.5 + ALIENSIZE // 2)) for r in range(5) for c in range(10) }
		self.alienInFormaton = {}
		
		self.state = FORMING
		
		self.aliens = []
		self.bolts = []
		
		self.step = 4
		self.directionStep = +1
		self.speedStep = .5
		self.timeSpent = .0
		
		# when formation complete, these are the aliens that make dives
		self.attackers = []

	def addAlien(self, alien):
		self.aliens.append(alien)
		alien.formation = self
		self.alienInFormaton[alien.formPos] = alien
		
	def removeAlien(self, alien):
		alien.formation = None
		self.aliens.remove(alien)
		if alien in self.attackers:
			self.attackers.remove(alien)
		del self.alienInFormaton[alien.formPos]
		
		
	'''
	alienList: list of tuples: alienType, formPos
	'''
	def createSquadron(self, alienList, typeOfTrajectory, timePassed):
		firstAlien = Alien(alienList[0][0], (0, 0), alienList[0][1])
		self.addAlien(firstAlien)
		firstAlien.getTrajectory(typeOfTrajectory, timePassed)
		
		refPos = firstAlien.trajectory[0]
		#print('refPos:', refPos)
		offset = (refPos - firstAlien.trajectory[1]).normalize()
		#print('offset:', offset)
		#nextPos = refPos - offset * ALIENSIZE * 1.5
		#print('nextPos', nextPos)
		
		for i in range(1, len(alienList)):
			nextAlien = Alien(alienList[i][0], (0, 0), alienList[i][1])
			self.addAlien(nextAlien)
			nextAlien.getTrajectory(typeOfTrajectory, timePassed)
			
			startPos = refPos + offset * ALIENSIZE * DISTANCE_BETWEEN * i
			distance = (startPos - refPos).get_magnitude()
			nrSteps = int(distance / (timePassed * ALIENSPEED))
			extraLeg = bezier1(startPos, refPos, nrSteps)
			
			nextAlien.trajectory = extraLeg + nextAlien.trajectory
		
		
		
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
						self.formationCoord[k] = int(self.formRec.left + (ALIENSIZE + margin) * k[1] + ALIENSIZE // 2), self.formationCoord[k][1]
						
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
				#print('xbounds Rec, step {}: {} - {}'.format(self.step, self.formRec.left, self.formRec.right))
				for k in self.formationCoord:
					self.formationCoord[k] = self.formationCoord[k][0] + self.directionStep * 10, self.formationCoord[k][1]
				
				if self.step >= 8:
					self.step = 0
					self.directionStep *= -1
		else:
			pass


	def updateAliens(self, timePassed):
		for alien in self.aliens:
			if alien.state == DEAD:
				x, y = alien.shape.get_size()
				alien.shape.fill(BLACK)
				pygame.draw.circle(alien.shape, WHITE, (x // 2, y // 2), alien.frame, 1)
				alien.frame += 1
				if alien.frame >= ALIENSIZE // 2 * 1.5:
					self.removeAlien(alien)
		
		if self.state == FORMATION_DONE:
			# TO DO: decision rule whether an attacker will make a dive or not
			if len(self.attackers) == 0 and len(self.aliens) > 0:
				try:
					self.attackers.append(self.alienInFormaton[(random.randint(3, 4), random.randint(0, 9))])
				except KeyError:
					pass
				
				
			for alien in self.attackers:
				if alien.state == IN_FORMATION and random.random() < .2:
					alien.state = DIVING
					if alien.formPos[1] >= 5:
						alien.getTrajectory(BEE_DIVE_FROM_R, timePassed)
					else:
						alien.getTrajectory(BEE_DIVE_FROM_L, timePassed)

			
			
						


class Bolt(object):
	def __init__(self, pos):
		self.pos = pos
		self.colour = WHITE
		self.shape = Rect(0, 0, BOLTWIDTH, BOLTLENGTH)
		self.shape.center = self.pos		
		
	def move(self, timePassed):
		self.pos = self.pos[0], self.pos[1] - BOLTSPEED * timePassed
		self.shape.center = self.pos		

		

class Ship(pygame.sprite.Sprite):
	def __init__(self):
		self.lives = 3
		self.state = MOVING
		
		# position
		self.pos = (VIEWWIDTH // 2, SHIPY)
		
		# shape -- placeholder
		self.colour = WHITE
		self.origShape = Surface((SHIPSIZE, SHIPSIZE))
		self.origShape.fill(WHITE)
		self.shape = self.origShape.copy()
		self.rect = self.shape.get_rect()
		self.rect.center = self.pos
		
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

	def hit(self):
		self.lives -= 1
		self.state = DEAD
		self.frame = 1

	def update(self):
		for bolt in self.bolts:
			if bolt.pos[1] - BOLTLENGTH < 0:
				self.bolts.remove(bolt)
			
		if self.state == DEAD:
			self.shape.fill(BLACK)
			pygame.draw.circle(self.shape, WHITE, (SHIPSIZE // 2, SHIPSIZE // 2), self.frame, 1)
			self.frame += 2
			if self.frame > SHIPSIZE // 2:
				self.pos = (VIEWWIDTH // 2, SHIPY)
				if self.lives:
					self.shape = self.origShape.copy()
					self.state = MOVING
				else:
					self.shape.fill(BLACK)
					self.state = GAMEOVER
	
	
