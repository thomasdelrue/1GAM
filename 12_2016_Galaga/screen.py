import pygame
import random

from constants import *
from vector2 import Vector2


# background, with stars, moving or static
class Backdrop(object):
	def __init__(self):
		self.state = MOVING
		'''to do: put in a blinking aspect... pulsing different shades of grey maybe?'''
		self.stars = {x: {'pos': Vector2(random.randint(0, VIEWWIDTH), random.randint(0, VIEWHEIGHT)),
						  'colour': random.choice(GREYS),
						  'speed': Vector2(0, random.randint(SHIPSPEED // 4, SHIPSPEED)) } 
						 for x in range(NR_OF_STARS)}
		
	def moveStars(self, timePassed):
		if self.state == MOVING:
			for n in self.stars:
				newpos = self.stars[n]['pos'] + self.stars[n]['speed'] * timePassed
				if newpos.y > VIEWHEIGHT:
					newpos.y -= VIEWHEIGHT
				self.stars[n]['pos'] = Vector2(int(newpos.x + .99), int(newpos.y + .99))


class ScoreBoard(object):
	def __init__(self):
		self.surface = pygame.Surface((VIEWWIDTH, SHIPSIZE))
		self.score = 0
		self.hires = 20000
		self.changed = True
		
	def addScore(points):
		self.score += points
		self.changed = True
		if self.hires < self.score:
			self.hires = self.score		
		


class StatusBar(object):
	def __init__(self):
		self.stage = 1
		self.surface = pygame.Surface((VIEWWIDTH, SHIPSIZE))
		self.changed = True
		
