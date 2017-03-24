import pyaudio 
import pygame
import time

import screen
import sound

from constants import *
from pygame.locals import *


def runGame():
    global level
    
    current_device_name = devices[0]["name"]
    
    audioInputText = font.render("[{}]".format(current_device_name), True, TEXTCOLOUR)
    txt_rect = audioInputText.get_rect()
    txt_rect.center = CENTER 
    
    level = screen.Level(4, surface)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        surface.fill(WHITE)
        
        #surface.blit(audioInputText, txt_rect)
        
        drawScreen()
        
        clock.tick(FPS)
        
        pygame.display.update()


def drawScreen():
    level.paint()
    

def endScreen():
    print('endScreen')
    
    
def settingsScreen():
    print('settingsScreen')
    

def openingScreen():
    image = pygame.image.load('title.png').convert_alpha()
    size = image.get_size()
    pos = CENTER[0] - size[0] // 2, CENTER[1] - size[1] // 2 
    
    pygame.mixer.music.load('intro.wav')
    pygame.mixer.music.play()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    pygame.mixer.music.fadeout(1000)
                    time.sleep(1)
                    return
                
        surface.fill(WHITE)
        surface.blit(image, pos)
        
        clock.tick(FPS)
        
        pygame.display.update()



def terminate():
    pygame.quit()
    pa.terminate()
    exit()


if __name__ == '__main__':
    pa = pyaudio.PyAudio()
    
    devices = {x: pa.get_device_info_by_index(x) for x in range(pa.get_device_count()) }
    print(devices)
     
    pygame.init()
    
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Pitch Perfect')
    
    font = pygame.font.SysFont("Arial", FONTSIZE)
    
    clock = pygame.time.Clock()
    
    #openingScreen()
    runGame()
    endScreen()
    
    terminate()
    