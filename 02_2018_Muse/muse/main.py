from pygame.locals import *
from constants import *
from sheet import Sheet, Note, frere_jacques
from support import BeginScene, EndScene
import pygame
import pygame.midi
     
"""
next steps:
    - get music played in real/runtime, during runloop
    - animate the sheet scrolling
    - draw the notes
    - draw the cursor
    - write user input -> move the cursor
    - hit 'collision'...
    
    - responsiveness of user input: stepsize of player movement,
        buffer user input and make it additive? e.g. 2 'ups' make 1 up-move
        with stepsize 2?
    
questions:
    - if player misses the note, what happens?
        no sound, or maybe a muted sound (eg half or quarter the volume)    
    - levels? MIDI format?
    - only single notes at a time, or enable multiples notes?
""" 
        

def init():
    global screen, clock
    pygame.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption('Muse')
    
    clock = pygame.time.Clock()
    pygame.display.update()
    

def tearDown():
    pygame.quit()
    

class Game():
    def __init__(self):
        self.gameOver = False
        self.sheet = self.loadSheetMusic()
        self.timePassed = 0
        print(len(self.sheet))
        
        
    def loadSheetMusic(self):
        return frere_jacques()
        
        
    def run(self):
        import time
        
        pygame.midi.init()
        player = pygame.midi.Output(0)
        player.set_instrument(0)
        
        
        for n in self.sheet:
            player.note_on(n.pitch, 127)
            time.sleep(n.duration * 2)
            player.note_off(n.pitch, 127)
        
        del player
        pygame.midi.quit()
        
        while not self.gameOver:
            self.updateScreen()
            pygame.display.update()
            self.timePassed += clock.tick(FPS)
            print(self.timePassed)
            self.checkForQuit()

    
    def checkForQuit(self):
        if pygame.event.peek(QUIT):
            self.gameOver = True

        
    def updateScreen(self):
        screen.fill(BG_COLOR) 
        pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)


if __name__ == '__main__':
    init()
    BeginScene()
    game = Game()
    game.run()
    EndScene()
    tearDown()
