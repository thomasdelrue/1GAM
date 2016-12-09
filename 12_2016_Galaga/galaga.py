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
	
	font = pygame.font.SysFont("arial", SHIPSIZE / 2)
	clock = pygame.time.Clock()
	
	# initialize world and objects
	world = {}
	log = Debug()
	
	log.message('start of debug session')
	
	ship = Ship()
	aliens = AlienCollection()
	backdrop = Backdrop()
	statusBar = StatusBar()
	scoreBoard = ScoreBoard()
	gameScreen = pygame.Surface((VIEWWIDTH, VIEWHEIGHT))
	
	world['ship'] = ship
	world['backdrop'] = backdrop
	world['statusBar'] = statusBar
	world['scoreBoard'] = scoreBoard
	world['gameScreen'] = gameScreen
	world['aliens'] = aliens
	
	for i in range(5):
		for j in range(10):
			aliens.addAlien(Alien(BEE, aliens.formation[(i, j)], (i, j)))
	
	movex = 0
	
	log.message('formation: {}'.format(aliens.formation))
	
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
		timePassed = clock.tick(FPS) / 1000.0
		#log.message('timePassed = {}'.format(timePassed))
		
		if movex:
			ship.move(movex * timePassed * SHIPSPEED)
		ship.update()
		for bolt in ship.bolts:
			bolt.move(timePassed)

		aliens.shuffleMovement()

		# check for collisions?
		for bolt in ship.bolts:
			for alien in aliens.aliens:
				if bolt.shape.colliderect(alien.shape):
					log.message('HIT!!')
					aliens.removeAlien(alien)
					ship.removeBolt(bolt)
		
		# paint the new world
		paintWorld()		
		
		pygame.display.update()


def paintWorld():
	gameScreen = world['gameScreen']
	gameScreen.fill(BLACK)

	
	# scoreBoard
	scoreBoard = world['scoreBoard']
	if scoreBoard.changed:
		log.message('scoreBoard changed')
		scoreBoard.surface.fill(GREEN)
		screen.blit(scoreBoard.surface, SCOREBOARD.topleft)
		scoreBoard.changed = False
	
		
	
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
	
	
	# aliens
	aliens = world['aliens']
	#aliens.formRec.midbottom = gameScreen.get_rect().center
	pygame.draw.rect(gameScreen, RED, aliens.formRec, 1)
	
	for alien in aliens.aliens:
		pygame.draw.rect(gameScreen, alien.colour, alien.shape, 0)
	
	screen.blit(gameScreen, VIEWPORT.topleft)

	# statusBar
	statusBar = world['statusBar']
	if statusBar.changed:
		log.message('statusBar changed')
		statusBar.surface.fill(BLUE)
		
		for i in range(ship.lives - 1):
			shipForm.topleft = (SHIPSIZE * 1.5 * i + SHIPSIZE // 2, 0)
			pygame.draw.rect(statusBar.surface, ship.colour, shipForm, 0)
			
		textSurface = font.render('Stage {}'.format(statusBar.stage), True, WHITE)
		textRect = textSurface.get_rect()
		textPos = (VIEWWIDTH - textRect.width, (SHIPSIZE - textRect.height) // 2)
		statusBar.surface.blit(textSurface, textPos)
		
		screen.blit(statusBar.surface, STATUSBAR.topleft)
		statusBar.changed = False

	
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
			pygame.draw.rect(screen, PURPLE, DEBUGWINDOW, 0)
			y = 0
			for text in self.messages[-SCREENSIZE[1] // self.font_height:]:
				screen.blit(self.font.render(text, True, WHITE), (DEBUGWINDOW.left, y))
				y += self.font_height
			self.changed = False


if __name__ == '__main__':
	mainGame()
	
