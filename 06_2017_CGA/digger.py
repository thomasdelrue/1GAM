# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:51:08 2017

@author: thomas


Digger clone?

-- POC... om van modes te switchen... <TAB> om tussen FULLSCREEN en windowed te togglen...
"""

from constants import *
from pygame.constants import *

import random
import pygame





def game():
    global screen, clock, pic, rect, screenFlags, tileSurf, tileRect
    
    screenFlags = SRCALPHA
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, screenFlags, 32)
    pygame.display.set_caption('Digger clone')
    
    clock = pygame.time.Clock()
    
    
    pic = pygame.image.load("tools\\digger1.png").convert_alpha()
    rect = pic.get_rect()
    rect.center = (WIDTH // 2, HEIGHT // 2)
    
    tileSurf = pygame.image.load("tools\\tile1.png").convert_alpha()
    tileRect = tileSurf.get_rect()
    
    drawScreen()
    
    while True:
        checkForQuit()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    toggleScreen()
            
        drawScreen()
        
        clock.tick(FPS)
        pygame.display.update()


def toggleScreen():
    global screenFlags
    screenFlags ^= FULLSCREEN
    screen = pygame.display.set_mode(SCREEN_SIZE, screenFlags, 32)
        


def drawScreen():
    
    '''def colour():
        colourList = []
        while True:
            if len(colourList) > 0:
                yield colourList.pop(0)
            else:
                colourList = [BLACK, WHITE, MAGENTA, CYAN]
                random.shuffle(colourList)
                continue
    
    for i in range(WIDTH // 10):
        for j in range(HEIGHT // 10):
            pygame.draw.rect(screen, next(colour()), (i * 10, j * 10, 10, 10), 0)'''
    
    for x in range(15):
        for y in range(10):
            tileRect.topleft = x * 16, y * 16
            screen.blit(tileSurf, tileRect)
    
    screen.blit(pic, rect)


def checkForQuit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and 
                                  event.key == K_ESCAPE):
            pygame.quit()
            exit()
            
        pygame.event.post(event)



if __name__ == '__main__':
    game()