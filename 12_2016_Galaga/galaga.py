'''
1GAM december 2016
Thomas Delrue

Galaga-style clone
'''


'''
TO DO's:

- diving, first bees, butterflies, galagas (with/without escort butterflies)
- collision detection with aliens/ship
- aliens shooting... 

- scoring
-- make groups (state ENTERING), if last one of a group is hit, score bonus, display bonus on screen

- writing text to screen, 
-- static/moving backdrop

- if ship is DEAD, aliens returning to formation, READY, then continue...

- GAMEOVER

- sprites!

- galaga capturing

- begin screen: galaga logo
- end screen: hit/miss

- different levels

- challenging level 3

- new aliens: snakes, scorpions...

- sounds

- joystick

- refactor code!
-- make Vector2 subclass of tuple
-- AlienCollection.aliens dict instead of .aliens list + .alienInFormation dict 

'''

import pygame
import sys

from constants import *
from objects import *
from screen import *
from playbook import *
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
	playbook = Playbook(aliens, statusBar)
	playbook.log = log
	gameScreen = pygame.Surface((VIEWWIDTH, VIEWHEIGHT))
	
	
	'''for i in range(5):
		for j in range(10):
			aliens.addAlien(Alien(BEE, aliens.formation[(i, j)], (i, j), IN_FORMATION))'''
	'''aliens.state = FORMATION_DONE
	aliens.step = 0'''

	# move a tick, to set the pace... so we can have a timeframe for the aliens to move
	timePassed = clock.tick(FPS) / 1000.0
			
	'''alienList = [(BEE, (3, 4)), (BEE, (3, 5)), (BEE, (4, 4)), (BEE, (4, 5))]	
	aliens.createSquadron(alienList, CURVE1_FROM_MIDTOPR, timePassed)
	
	alienList = [(BUTTERFLY, (1, 4)), (BUTTERFLY, (1, 5)), (BUTTERFLY, (2, 4)), (BUTTERFLY, (2, 5))]	
	aliens.createSquadron(alienList, CURVE1_FROM_MIDTOPL, timePassed)'''
	
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
			if ship.state not in (DEAD, GAMEOVER):
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
		incrementScore = 0
		timePassed = clock.tick(FPS) / 1000.0
		
		playbook.check(timePassed)

		backdrop.moveStars(timePassed)
				
		if movex:
			ship.move(movex * timePassed * MOVESPEED)
			
		ship.update()
		
		for bolt in ship.bolts:
			bolt.move(timePassed)

		aliens.moveFormation(timePassed)
		for alien in aliens.aliens:
			if alien.state == IN_FORMATION:
				if alien.heading != 270:
					alien.setHeading(270)				
				alien.currentPos = aliens.formationCoord[alien.formPos]
				alien.rect.center = alien.currentPos
			else:
				alien.move(timePassed)
				
			if ship.state == MOVING and alien.state != DEAD:
				if alien.rect.colliderect(ship.rect):
					incrementScore += alien.hit()
					ship.hit()
					statusBar.changed = True

		# check for collisions?
		for bolt in ship.bolts:
			toRemove = False
			for alien in aliens.aliens:
				if bolt.shape.colliderect(alien.rect) and alien.state != DEAD:
					incrementScore += alien.hit()
					toRemove = True
			if toRemove:
				ship.removeBolt(bolt)
		
		aliens.updateAliens(timePassed)
		scoreBoard.addScore(incrementScore)
		
		# paint the new world
		paintWorld()
		
		if ship.state == GAMEOVER:
			# TO DO: gameover screen...
			textSurface = font.render('GAME OVER', True, RED)
			textRect = textSurface.get_rect()
			textRect.center = CENTER
			screen.blit(textSurface, textRect)
					
		
		pygame.display.update()


def paintWorld():
	gameScreen.fill(BLACK)
	
	drawScoreBoard()
	drawStatusBar()
		
	# draw backdrop
	for n in backdrop.stars:
		
		pygame.draw.circle(gameScreen, backdrop.stars[n]['colour'], tuple(backdrop.stars[n]['pos']), 1, 1)
	
	for b in ship.bolts:
		pygame.draw.rect(gameScreen, b.colour, b.shape, 0)

	
	# aliens
	#pygame.draw.rect(gameScreen, RED, aliens.formRec, 1)
	
	for alien in aliens.aliens:
		if alien.state != DEAD:
			gameScreen.blit(alien.shape, alien.rect)

	# draw ship
	ship.rect.center = ship.pos
	gameScreen.blit(ship.shape, ship.rect)
			
	
	# make sure explosions are at the foreground,
	# so that's why we first draw the living aliens, and secondly the exploding ones...
	for alien in aliens.aliens:
		if alien.state == DEAD:
			gameScreen.blit(alien.shape, alien.rect)
			
	
	screen.blit(gameScreen, VIEWPORT.topleft)


	# paint DEBUG window	
	log.paint()
	
	
def drawScoreBoard():
	# scoreBoard
	if scoreBoard.changed:
		log.message('scoreBoard changed')
		scoreBoard.surface.fill(BLACK)
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
		statusBar.surface.fill(BLACK)
		#pygame.draw.rect(statusBar.surface, BLUE, statusBar.surface.get_rect(), 1)
		
		for i in range(ship.lives - 1):
			ship.rect.topleft = (SHIPSIZE * 1.5 * i + SHIPSIZE // 2, 0)
			statusBar.surface.blit(ship.shape, ship.rect)
			#pygame.draw.rect(statusBar.surface, ship.colour, ship.shape, 0)
			
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
	
