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
    global screen, clock, pic, rect
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SRCALPHA, 32)
    pygame.display.set_caption('Digger clone')
    
    clock = pygame.time.Clock()
    
    
    pic = pygame.image.load("tools\\sprite.png").convert_alpha()
    rect = pic.get_rect()
    rect.center = (WIDTH // 2, HEIGHT // 2)
    
    
    drawScreen()
    
    while True:
        checkForQuit()
            
        drawScreen()
        
        clock.tick(FPS)
        pygame.display.update()
    


def drawScreen():
    
    def colour():
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
            pygame.draw.rect(screen, next(colour()), (i * 10, j * 10, 10, 10), 0)
            
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