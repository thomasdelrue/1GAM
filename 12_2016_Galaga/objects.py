
from constants import *


class Alien(object):
	def __init__(self):
		pass
		# type
		# lives
		# position
		# shape


class Bolt(object):
	def __init__(self):
		pass
		# position
		# shape
		

class Ship(object):
	def __init__(self):
		self.lives = 3
		
		# position
		self.pos = (CENTERX, SHIPY)
		
		# shape -- placeholder
		self.colour = WHITE
		
		# nr of bolts
		self.bolts = []
		
	def fireBolt(self):
		if length(self.bolts) >= 2:
			return
		# otherwise, create a bolt
		pass
	
