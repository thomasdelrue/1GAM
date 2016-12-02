'''
1GAM december 2016
Thomas Delrue

Galaga-style clone
'''

import pygame
import sys

from constants import *
from objects import *
from screen import *
from pygame.locals import *


def mainGame():
	global world, SCREEN, clock
	pygame.init()
	
	SCREEN = pygame.display.set_mode(SCREENSIZE, 0, 32)
	pygame.display.set_caption('Galaga')
	
	
	# initialize world and objects
	world = {}
	ship = Ship()
	backdrop = Backdrop()
	world['ship'] = ship
	world['backdrop'] = backdrop
	movex = 0
	
	# game loop
	while True:
		
		# event loop
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key in LEFT_KEYS:
					movex -= MOVESTEP
				if event.key in RIGHT_KEYS:
					movex += MOVESTEP
				if event.key in FIRE_KEYS:
					ship.fireBolt()
			if event.type == KEYUP:
				if event.key in LEFT_KEYS:
					movex = 0
				if event.key in RIGHT_KEYS:
					movex = 0
		
		# update states
		if movex:
			ship.move(movex)
		ship.update()
		for bolt in ship.bolts:
			bolt.move()
			
		# check for collisions?
		pass
		
		# paint the new world
		paintWorld()		
		pygame.display.update()


def paintWorld():
	global world
	
	SCREEN.fill(BLACK)
	
	# draw screen
	pygame.draw.rect(SCREEN, RED, VIEWPORT, 1)
	pygame.draw.rect(SCREEN, GREEN, SCOREBOARD, 1)
	pygame.draw.rect(SCREEN, BLUE, STATUSBOARD, 1)
	
	# draw backdrop
	backdrop = world['backdrop']
	for k in backdrop.stars:
		pygame.draw.circle(SCREEN, backdrop.stars[k][1], backdrop.stars[k][0], 1, 1)
	
	# draw ship
	ship = world['ship']
	
	for b in ship.bolts:
		pygame.draw.rect(SCREEN, b.colour, b.shape, 0)
	
	shipForm = pygame.Rect(0, 0, SHIPSIZE, SHIPSIZE)
	shipForm.center = ship.pos
	pygame.draw.rect(SCREEN, ship.colour, shipForm, 0)
	

if __name__ == '__main__':
	mainGame()
	
