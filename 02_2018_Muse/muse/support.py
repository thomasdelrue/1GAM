import pygame
from pygame.locals import *
from constants import *



class BeginScene():
    def __init__(self, screen):
        self.screen = screen
        self.run()
        
    def run(self):
        clock = pygame.time.Clock()
        pressed = False

        self.screen.fill(WHITE)
        self.screen.blit(*printText('-= M U S E =-'))
        pygame.display.update()

        
        while not pressed:
            clock.tick(FPS)
            if pygame.event.peek(QUIT) or pygame.event.peek(KEYDOWN):
                pygame.event.get()
                break    
    
class EndScene():
    def __init__(self, screen):
        self.screen = screen
        self.run()
        
    def run(self):
        clock = pygame.time.Clock()
        pressed = False

        self.screen.fill(WHITE)
        self.screen.blit(*printText('Thank you for playing'))
        pygame.display.update()

        
        while not pressed:
            clock.tick(FPS)
            if pygame.event.peek(QUIT) or pygame.event.peek(KEYDOWN):
                break
                

def printText(text):
    basicFont = pygame.font.SysFont("Arial", FONT_SIZE)
    textSurf = basicFont.render(text, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    return (textSurf, textRect)
    
    