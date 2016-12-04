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
	global world, screen, clock, log, font
	pygame.init()
	
	screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
	pygame.display.set_caption('Galaga')
	
	font = pygame.font.SysFont("arial", 16)
	
	# initialize world and objects
	world = {}
	log = Debug()
	
	log.message('start of debug session')
	
	ship = Ship()
	backdrop = Backdrop()
	statusBar = StatusBar()
	gameScreen = pygame.Surface((VIEWWIDTH, VIEWHEIGHT))
	
	world['ship'] = ship
	world['backdrop'] = backdrop
	world['statusBar'] = statusBar
	world['gameScreen'] = gameScreen
	
	movex = 0
	
	
	screen.fill(BLACK)
	
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
	gameScreen = world['gameScreen']
	gameScreen.fill(BLACK)
	
	# draw screen
	
	# to do: refactor scoreboard to its own Surface, analogue to statusBar
	pygame.draw.rect(screen, GREEN, SCOREBOARD, 1)
	
	statusBar = world['statusBar']
	
	if statusBar.changed:
		log.message('statusBar changed')
		statusBar.surface.fill(BLUE)
		textSurface = font.render('Stage {}'.format(statusBar.stage), True, WHITE)
		textRect = textSurface.get_rect()
		textPos = (VIEWWIDTH - textRect.width, (SHIPSIZE - textRect.height) // 2)
		statusBar.surface.blit(textSurface, textPos)
		screen.blit(statusBar.surface, STATUSBAR.topleft)
		statusBar.changed = False
		
	
	# draw backdrop
	backdrop = world['backdrop']
	for k in backdrop.stars:
		pygame.draw.circle(gameScreen, backdrop.stars[k][1], backdrop.stars[k][0], 1, 1)
	
	# draw ship
	ship = world['ship']
	
	for b in ship.bolts:
		pygame.draw.rect(gameScreen, b.colour, b.shape, 0)
	
	shipForm = pygame.Rect(0, 0, SHIPSIZE, SHIPSIZE)
	shipForm.center = ship.pos
	pygame.draw.rect(gameScreen, ship.colour, shipForm, 0)

	
	screen.blit(gameScreen, VIEWPORT.topleft)
	
	log.paint()
	
	
	

class Debug(object):
	global screen
	
	def __init__(self):
		if DEBUG:
			self.messages = []
			self.font = pygame.font.SysFont("arial", 12)
			self.font_height = self.font.get_height()
		
	def message(self, str):
		if DEBUG:
			self.changed = True
			self.messages.append(str)

			
	def paint(self):
		if DEBUG and self.changed:
			pygame.draw.rect(screen, PURPLE, DEBUGWINDOW, 1)
			y = 0
			for text in self.messages[-SCREENSIZE[1] // self.font_height:]:
				screen.blit(self.font.render(text, True, WHITE), (DEBUGWINDOW.left, y))
				y += self.font_height
			self.changed = False


if __name__ == '__main__':
	mainGame()
	
