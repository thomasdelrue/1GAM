
from constants import *
from pygame import Rect


class Alien(object):
	def __init__(self):
		pass
		# type
		# lives
		# position
		# shape



class Bolt(object):
	def __init__(self, pos):
		self.pos = pos
		self.colour = WHITE
		self.shape = Rect(0, 0, BOLTWIDTH, BOLTLENGTH)
		self.shape.center = self.pos		
		
	def move(self):
		self.pos = self.pos[0], self.pos[1] - BOLTSPEED
		self.shape.center = self.pos		

		

class Ship(object):
	def __init__(self):
		self.lives = 3
		
		# position
		self.pos = (CENTER[0], SHIPY)
		
		# shape -- placeholder
		self.colour = WHITE

		
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

	def update(self):
		for bolt in self.bolts:
			if bolt.pos[1] - BOLTLENGTH < VIEWPORT.top:
				self.bolts.remove(bolt)
			
			
	
	
