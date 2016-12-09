import pygame
import random

from constants import *



# background, with stars, moving or static
class Backdrop(object):
	def __init__(self):
		self.state = STATIC
		self.stars = {x: ((random.randint(0, VIEWWIDTH), random.randint(0, VIEWHEIGHT)), GREY) for x in range(NR_OF_STARS)}


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
		
