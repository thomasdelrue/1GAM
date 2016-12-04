import pygame
import random

from constants import *



# background, with stars, moving or static
class Backdrop(object):
	def __init__(self):
		self.state = STATIC
		self.stars = {x: ((random.randint(0, VIEWWIDTH), random.randint(0, VIEWHEIGHT)), GREY) for x in range(NR_OF_STARS)}


class Scoreboard(object):
	def __init__(self):
		pass


class StatusBar(object):
	def __init__(self):
		self.stage = 1
		self.surface = pygame.Surface((VIEWWIDTH, SHIPSIZE))
		self.changed = True
		
