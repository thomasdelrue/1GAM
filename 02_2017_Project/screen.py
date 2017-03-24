'''module for ui components'''

from constants import *

import pygame
import pygame.gfxdraw
import random


class SoundButton(object):
    
    def __init__(self, colour, x, y, surface):
        self.colour = colour 
        self.x = x
        self.y = y
        self.surface = surface
        
    def paint(self):
        pygame.draw.circle(self.surface, self.colour, (self.x, self.y), BUTTONSIZE + 1, 0)
        pygame.gfxdraw.aacircle(self.surface, self.x, self.y, BUTTONSIZE, self.colour)
        pygame.gfxdraw.aacircle(self.surface, self.x, self.y, BUTTONSIZE + 1, self.colour)
    
    
class Level(object):
    def __init__(self, nr, surface):
        self.nr = nr 
        self.surface = surface
        self.pickColour = pickColour()
        self.soundButtons = []
        startx = CENTER[0] - (self.nr - 1) * (BUTTONSIZE + MARGIN // 2)
        for i in range(self.nr):
            x = startx + i * (BUTTONSIZE * 2 + MARGIN)  
            y = CENTER[1]
            self.soundButtons.append(SoundButton(next(self.pickColour), x, y, surface))
        
        
    def paint(self):
        for button in self.soundButtons:
            button.paint()
        
        pygame.draw.line(self.surface, RED, (CENTER[0], 0), (CENTER[0], WINDOWHEIGHT), 1)
        

def pickColour():
    colourList = []
    
    while True:
        if colourList == []:
            colourList = PASTELS.copy()
            random.shuffle(colourList)
        else:   
            yield colourList.pop(0)