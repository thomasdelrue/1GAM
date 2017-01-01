import math
import random
import pygame
import vector2

from constants import *
from vector2 import Vector2 
from bezier import *
from pygame import Rect, Surface



class Alien(object):
	def __init__(self, alienType, currentPos, formPos, state=ENTERING):
		pygame.sprite.Sprite.__init__(self)
		
		self.alienType = alienType
		# current position on screen
		self.currentPos = currentPos
		# the previous position
		self.oldPos = currentPos
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
			self.score = 200
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
		self.rect.center = tuple(self.currentPos)
		
	def __repr__(self):
		return str(self.formPos)
		
	def getTrajectory(self, typeOfTrajectory, timePassed):
		# to do
		cp = BEZ_CP_SETS[typeOfTrajectory]
		
		# cp's are relative for these trajectories; they need adjusting from the 'constants' cp
		if typeOfTrajectory in (BEE_DIVE_FROM_R, BEE_DIVE_FROM_L, BUTTERFLY_DIVE_FROM_R, BUTTERFLY_DIVE_FROM_L):
			offset = self.currentPos.x - cp[0][0], self.currentPos.y - cp[0][1]
			for i in range(len(cp)):
				cp[i] = cp[i][0] + offset[0], cp[i][1] + offset[1]

		path = BezierPath(cp)
		#print(path.controlPoints)
		#self.trajectory = path.getDrawingPoints(timePassed)
		self.trajectory = path.getDrawingPoints(1 / FPS)
	
	
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
		self.oldPos = self.currentPos
		if self.state == IN_FORMATION:
			# movement calculated in Formation
			
			pass
		elif self.state in (ENTERING, DIVING):
			if len(self.trajectory) > 0:
				self.currentPos = self.trajectory.pop(0)
				
				self.setHeading()
				
				#print('alien currentPost', self.currentPos)
			else:
				if self.alienType == BUTTERFLY and self.state == DIVING and self.currentPos.y > self.formation.formationCoord[self.formPos][1]:
					
					wander = random.randint(1, 2)
										
					if self.currentPos.y > VIEWHEIGHT + ALIENSIZE:
						self.currentPos = Vector2(self.formation.formationCoord[self.formPos][0], -ALIENSIZE)
					else:
						
						if wander == 1 or self.currentPos.x >= 500:
							nextPos = Vector2(self.currentPos.x - 50, self.currentPos.y + 80)
						else:  
							nextPos = Vector2(self.currentPos.x + 50, self.currentPos.y + 80)
						
						cp = [self.currentPos, Vector2(self.currentPos.x, nextPos.y - 40), Vector2(nextPos.x, self.currentPos.y + 40), nextPos]
						
						self.trajectory = BezierPath(cp).getDrawingPoints(timePassed)
						
						self.currentPos = self.trajectory.pop(0)

					
					self.setHeading(90)
				else:
					destPos = Vector2(*self.formation.formationCoord[self.formPos])
					diff = destPos - self.currentPos 
					if diff.get_magnitude() < 10:
						self.state = IN_FORMATION
					else:
						res = self.currentPos + diff.normalize() * ALIENSPEED * timePassed
						self.currentPos = res 
						self.setHeading()

			self.rect.center = tuple(self.currentPos)
		
			
				
	def setHeading(self, heading=None):
		if heading is None:
			self.heading = (self.currentPos - self.oldPos).getHeading()
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
		self.alienInFormation = {}
		
		self.state = FORMING
		
		self.aliens = []
		self.bolts = []
		
		self.step = 4
		self.directionStep = +1
		self.speedStep = .5
		self.timeSpent = .0
		
		# when formation complete, these are the aliens that make dives
		self.attackers = []
		self.outsiders = []
		self.getOutsiders = True
		
		self.chanceShooting = 0.04
		self.chanceDiving = 0.05

	def addAlien(self, alien):
		self.aliens.append(alien)
		alien.formation = self
		self.alienInFormation[alien.formPos] = alien
		
	def removeAlien(self, alien):
		alien.formation = None
		self.aliens.remove(alien)
		if alien in self.attackers:
			self.attackers.remove(alien)
		if alien in self.outsiders:
			self.outsiders.remove(alien)
			self.getOutsiders = True
		del self.alienInFormation[alien.formPos]

	def resetOriginalFormCoordinates(self):
		self.formRec = Rect(0, 0, (ALIENSIZE * 1.5) * 9 + ALIENSIZE, (ALIENSIZE * 1.5) * 4 + ALIENSIZE)
		self.formRec.midbottom = (VIEWWIDTH // 2, VIEWHEIGHT // 2)
		self.formationCoord = {(r, c): (int(self.formRec.left + ALIENSIZE * c * 1.5 + ALIENSIZE // 2), 
										int(self.formRec.top + ALIENSIZE * r * 1.5 + ALIENSIZE // 2)) for r in range(5) for c in range(10) }
		self.step = 4
		self.directionStep = +1
		self.speedStep = .5
		self.timeSpent = .0
		
		
	def checkAliensInFormation(self):
		allInFormation = True
		for alien in reversed(self.aliens):
			if alien.state != IN_FORMATION:
				allInFormation = False
				break
		return allInFormation
		
		
	'''
	alienList: list of tuples: alienType, formPos
	'''
	def createSquadron(self, alienList, typeOfTrajectory, timePassed):
		firstAlien = Alien(alienList[0][0], Vector2(0, 0), alienList[0][1])
		self.addAlien(firstAlien)
		firstAlien.getTrajectory(typeOfTrajectory, timePassed)
		
		refPos = firstAlien.trajectory[0]
		offset = (refPos - firstAlien.trajectory[1]).normalize()
		
		for i in range(1, len(alienList)):
			nextAlien = Alien(alienList[i][0], Vector2(0, 0), alienList[i][1])
			self.addAlien(nextAlien)
			nextAlien.getTrajectory(typeOfTrajectory, timePassed)
			
			startPos = refPos + offset * ALIENSIZE * DISTANCE_BETWEEN * i
			distance = (startPos - refPos).get_magnitude()
			nrSteps = int(distance / (timePassed * ALIENSPEED))
			extraLeg = bezier1(startPos, refPos, nrSteps)
			
			nextAlien.trajectory = extraLeg + nextAlien.trajectory
		
	
	def selectOutsiders(self):
		res = []
		
		for r, c in [(random.randint(3, 4), 0), (random.randint(1, 2), 1), (random.randint(3, 4), -9), (random.randint(1, 2), -8),
					(0, 3), (0, -6)]: 
			for i in range(10):
				alien = self.alienInFormation.get((r, abs(c + i)))
				if alien and alien not in res:
					if alien in self.outsiders:
						break
					res.append(alien)
					break
			 
		#print('res=', res)
		return res
	
		
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
				for k in self.formationCoord:
					self.formationCoord[k] = self.formationCoord[k][0] + self.directionStep * 10, self.formationCoord[k][1]
				
				if self.step >= 8:
					self.step = 0
					self.directionStep *= -1
		else:
			pass


	def updateAliens(self, timePassed, shipState):
		for alien in self.aliens:
			if alien.state == DEAD:
				x, y = alien.shape.get_size()
				alien.shape.fill(BLACK)
				pygame.draw.circle(alien.shape, WHITE, (x // 2, y // 2), alien.frame, 1)
				alien.frame += 1
				if alien.frame >= ALIENSIZE // 2 * 1.5:
					self.removeAlien(alien)
			
			elif alien.state == DIVING:
				if alien.heading >= 45 and alien.heading <= 135:
					if random.random() < 0.05 / len(self.attackers):
						self.bolts.append(Bolt(tuple(alien.currentPos), type=ALIENBOLT))
					
		for bolt in self.bolts:
			if bolt.pos[1] + BOLTLENGTH > VIEWHEIGHT:
				self.bolts.remove(bolt)
		
		if self.state == FORMATION_DONE:
			if len(self.attackers) < len(self.aliens):
				if self.getOutsiders:
					added = False
					selection = self.selectOutsiders()
					for i in range(len(selection)):
						if selection[i] not in self.outsiders:
							self.outsiders.append(selection[i])
							added = True
					
					if added:
						self.getOutsiders = False
				
				if len(self.attackers) <= len(self.outsiders):
					for i in range(len(self.outsiders)):
						if self.outsiders[i] not in self.attackers:
							self.attackers.append(self.outsiders[i])
			
			# TO DO: decision rule whether an attacker will make a dive or not	
			# print('attackers:', self.attackers)
			for alien in self.attackers:
				# hard-coded frequency... probably stage-dependent
				if alien.state == IN_FORMATION and random.random() < 0.05 / len(self.attackers) and shipState != DEAD:
					alien.state = DIVING
					if alien.alienType == BEE:
						if alien.formPos[1] >= 5:
							alien.getTrajectory(BEE_DIVE_FROM_R, timePassed)
						else:
							alien.getTrajectory(BEE_DIVE_FROM_L, timePassed)
					elif alien.alienType == BUTTERFLY:
						if alien.formPos[1] >= 5:
							alien.getTrajectory(BUTTERFLY_DIVE_FROM_R, timePassed)
						else:
							alien.getTrajectory(BUTTERFLY_DIVE_FROM_L, timePassed)							
					elif alien.alienType == GALAGA:
						if alien.formPos[1] >= 5:
							alien.getTrajectory(random.choice([BUTTERFLY_DIVE_FROM_R, BEE_DIVE_FROM_R]), timePassed)
						else:
							alien.getTrajectory(random.choice([BUTTERFLY_DIVE_FROM_L, BEE_DIVE_FROM_L]), timePassed)							
					break

			
			
						


class Bolt(object):
	def __init__(self, pos, dest=None, type=SHIPBOLT):
		self.pos = pos
		self.colour = WHITE
		self.type = type
		self.shape = Rect(0, 0, BOLTWIDTH, BOLTLENGTH)
		self.shape.center = self.pos
		# destination for ALIENBOLT
		self.destination = dest		
		
	def move(self, timePassed):
		if self.type == SHIPBOLT:
			direction = -1
		elif self.type == ALIENBOLT:
			direction = +1
		# to do: if alien bolt, move towards self.destination
		self.pos = self.pos[0], self.pos[1] + direction * BOLTSPEED * timePassed
		self.shape.center = self.pos		

		

class Ship(object):
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
		
	def readyNewShip(self):
		self.pos = (VIEWWIDTH // 2, SHIPY)
		self.shape = self.origShape.copy()
		self.state = MOVING
		
	def update(self, ready=None):
		for bolt in self.bolts:
			if bolt.pos[1] - BOLTLENGTH < 0:
				self.bolts.remove(bolt)
			
		if self.state == DEAD:
			if self.frame < SHIPSIZE // 2:
				self.shape.fill(BLACK)
				pygame.draw.circle(self.shape, WHITE, (SHIPSIZE // 2, SHIPSIZE // 2), self.frame, 1)
				self.frame += 2
			else:  
				self.pos = None
				if not self.lives:
					self.state = GAMEOVER
				elif ready:
					self.readyNewShip()
				
	
	
