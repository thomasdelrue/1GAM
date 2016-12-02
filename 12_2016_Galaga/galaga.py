'''
1GAM december 2016
Thomas Delrue

Galaga-style clone
'''

import pygame
import sys

from constants import *
from objects import *
from pygame.locals import *


def mainGame():
	global world, SCREEN
	pygame.init()
	
	SCREEN = pygame.display.set_mode(SCREENSIZE, 0, 32)
	pygame.display.set_caption('Galaga')
	
	# initialize world and objects
	world = {}
	ship = Ship()
	world['ship'] = ship
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
					movex -= 1
				if event.key in RIGHT_KEYS:
					movex += 1
				if event.key in FIRE_KEYS:
					ship.fireBolt()
			if event.type == KEYUP:
				if event.key in LEFT_KEYS:
					movex = 0
				if event.key in RIGHT_KEYS:
					movex = 0
		
		# update states
		ship.pos = (ship.pos[0] + movex, ship.pos[1])
			
		paintWorld()		
		pygame.display.update()


def paintWorld():
	global world
	SCREEN.fill(BLACK)
	
	# draw ship
	ship = world['ship']
	shipForm = pygame.Rect(0, 0, SHIPSIZE, SHIPSIZE)
	shipForm.center = ship.pos
	pygame.draw.rect(SCREEN, ship.colour, shipForm, 0)
	

if __name__ == '__main__':
	mainGame()
	
