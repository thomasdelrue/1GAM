import random
import vector2

from constants import *
from vector2 import Vector2 
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
	def __init__(self, alienType, currentPos, formPos, state=None):
		self.alienType = alienType
		self.currentPos = currentPos
		self.formPos = formPos
		self.state = state
		self.trajectory = []
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
		
	def getTrajectory(self):
		# to do
		p0 = Vector2(*self.currentPos)
		p1 = Vector2(random.randint(0, 600), random.randint(0, 300))
		p2 = Vector2(random.randint(0, 600), random.randint(0, 300))
		self.trajectory = vector2.bezier2(p0, p1, p2)
	
	def move(self):
		if self.state == IN_FORMATION:
			# movement calculated in Formation
			pass
		else:
			if len(self.trajectory) > 0:
				self.currentPos = self.trajectory.pop(0)
				print('alien currentPost', self.currentPos)
				self.shape.topleft = tuple(self.currentPos)
			else:
				self.getTrajectory()
				self.move()

class AlienCollection(object):
	def __init__(self):
		self.formRec = Rect(0, 0, (ALIENSIZE * 1.5) * 9 + ALIENSIZE, (ALIENSIZE * 1.5) * 4 + ALIENSIZE)
		self.formRec.midbottom = (VIEWWIDTH // 2, VIEWHEIGHT // 2)
		self.formation = {(r, c): (self.formRec.left + ALIENSIZE * c * 1.5 , self.formRec.top + ALIENSIZE * r * 1.5) for r in range(5) for c in range(10) }
		
		self.state = FORMING
		
		self.aliens = []
		self.bolts = []
		
		self.step = 4
		self.directionStep = +1
		self.speedStep = .5
		self.timeSpent = .0

	def addAlien(self, alien):
		self.aliens.append(alien)
		
	def removeAlien(self, alien):
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
				for k in self.formation:
					if not k[0] == 0:
						if k[0] == 1:
							print()
						self.formation[k] = self.formRec.left + (ALIENSIZE + margin) * k[1], self.formation[k][1]
						
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
				for k in self.formation:
					self.formation[k] = self.formation[k][0] + self.directionStep * 10, self.formation[k][1]
				
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
			
			
	
	
