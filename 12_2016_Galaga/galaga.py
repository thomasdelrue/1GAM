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
	global screen, clock, log, font, ship, aliens, backdrop, statusBar, \
		scoreBoard, gameScreen
	pygame.init()
	
	screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
	pygame.display.set_caption('Galaga')
	
	font = pygame.font.SysFont("arial", SHIPSIZE // 2)
	clock = pygame.time.Clock()
	
	# initialize world and objects
	log = Debug()
	
	log.message('start of debug session')
	
	ship = Ship()
	aliens = AlienCollection()
	backdrop = Backdrop()
	statusBar = StatusBar()
	scoreBoard = ScoreBoard()
	gameScreen = pygame.Surface((VIEWWIDTH, VIEWHEIGHT))
	
	
	'''for i in range(5):
		for j in range(10):
			aliens.addAlien(Alien(BEE, aliens.formation[(i, j)], (i, j), IN_FORMATION))'''
	'''aliens.state = FORMATION_DONE
	aliens.step = 0'''

	# move a tick, to set the pace... so we can have a timeframe for the aliens to move
	timePassed = clock.tick(FPS) / 1000.0
			
	alien = Alien(BEE, (0, 0), (4, 4))
	aliens.addAlien(alien)
	alien.getTrajectory(CURVE1_FROM_MIDTOPR, timePassed)
	
	alien = Alien(BUTTERFLY, (0, 0), (2, 4))
	aliens.addAlien(alien)
	alien.getTrajectory(CURVE1_FROM_MIDTOPL, timePassed)
	
	
	movex = 0
	
	screen.fill(BLACK)
	
	# game loop
	while True:
		
		# event loop
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			''' to do: change the key event handling with key.get_pressed()
				for a more intuitive right feel '''
			if ship.state != DEAD:
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

		backdrop.moveStars(timePassed)
				
		if movex:
			ship.move(movex * timePassed * MOVESPEED)
			
		ship.update()
		
		for bolt in ship.bolts:
			bolt.move(timePassed)

		aliens.moveFormation(timePassed)
		for alien in aliens.aliens:
			if alien.state == IN_FORMATION:
				if alien.heading % 360:
					alien.getHeading()				
				alien.currentPos = aliens.formationCoord[alien.formPos]
				alien.rect.center = alien.currentPos
				#alien.shape.center = alien.currentPos
			else:
				alien.move()

		# check for collisions?
		for bolt in ship.bolts:
			toRemove = False
			for alien in aliens.aliens:
				if bolt.shape.colliderect(alien.rect):
					log.message('HIT!!')
					aliens.removeAlien(alien)
					toRemove = True
			if toRemove:
				ship.removeBolt(bolt)
		
		# paint the new world
		paintWorld()		
		
		pygame.display.update()


def paintWorld():
	gameScreen.fill(BLACK)
	
	drawScoreBoard()
	drawStatusBar()
		
	# draw backdrop
	for n in backdrop.stars:
		
		pygame.draw.circle(gameScreen, backdrop.stars[n]['colour'], tuple(backdrop.stars[n]['pos']), 1, 1)
	
	# draw ship
	for b in ship.bolts:
		pygame.draw.rect(gameScreen, b.colour, b.shape, 0)

	ship.shape.center = ship.pos
	pygame.draw.rect(gameScreen, ship.colour, ship.shape, 0)
	
	
	# aliens
	pygame.draw.rect(gameScreen, RED, aliens.formRec, 1)
	
	for alien in aliens.aliens:
		gameScreen.blit(alien.shape, alien.rect)
		#pygame.draw.rect(gameScreen, alien.colour, alien.shape, 0)
	
	for coord in aliens.formationCoord:
		print(aliens.formationCoord[coord])
		gameScreen.set_at(aliens.formationCoord[coord], RED)
	
	screen.blit(gameScreen, VIEWPORT.topleft)


	# paint DEBUG window	
	log.paint()
	
	
def drawScoreBoard():
	# scoreBoard
	if scoreBoard.changed:
		log.message('scoreBoard changed')
		scoreBoardRect = scoreBoard.surface.get_rect()
		#pygame.draw.rect(scoreBoard.surface, GREEN, scoreBoardRect, 1)
		
		textSurface = font.render('HIGH SCORE', True, RED)
		textRect = textSurface.get_rect()
		textRect.midtop = scoreBoardRect.midtop
		scoreBoard.surface.blit(textSurface, textRect.topleft)

		textSurface = font.render('{}'.format(scoreBoard.hires), True, WHITE)
		textRect = textSurface.get_rect()
		textRect.midbottom = scoreBoardRect.midbottom
		scoreBoard.surface.blit(textSurface, textRect.topleft)

		textSurface = font.render('1UP', True, RED)
		textRect = textSurface.get_rect()
		textRect.topleft = scoreBoardRect.topleft
		scoreBoard.surface.blit(textSurface, textRect.topleft)

		textSurface = font.render('{}'.format(scoreBoard.score), True, WHITE)
		textRect = textSurface.get_rect()
		textRect.bottomleft = scoreBoardRect.bottomleft
		scoreBoard.surface.blit(textSurface, textRect.topleft)
		
		screen.blit(scoreBoard.surface, SCOREBOARD.topleft)
		scoreBoard.changed = False

	
def drawStatusBar():
	# statusBar
	if statusBar.changed:
		log.message('statusBar changed')
		#pygame.draw.rect(statusBar.surface, BLUE, statusBar.surface.get_rect(), 1)
		
		for i in range(ship.lives - 1):
			ship.shape.topleft = (SHIPSIZE * 1.5 * i + SHIPSIZE // 2, 0)
			pygame.draw.rect(statusBar.surface, ship.colour, ship.shape, 0)
			
		textSurface = font.render('Stage {}'.format(statusBar.stage), True, WHITE)
		textRect = textSurface.get_rect()
		textPos = (VIEWWIDTH - textRect.width, (SHIPSIZE - textRect.height) // 2)
		statusBar.surface.blit(textSurface, textPos)
		
		screen.blit(statusBar.surface, STATUSBAR.topleft)
		statusBar.changed = False	


class Debug(object):
	#global screen
	
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
	
