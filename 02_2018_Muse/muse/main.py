from pygame.locals import *
from collections import deque
from constants import *
from sheet import Sheet, Note, frere_jacques
from support import BeginScene, EndScene
import pygame
import pygame.midi
     
"""
next steps:
    - animate the sheet scrolling (more or less... not exactly right)
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
        self.totalTimePassed = 0
        self.scroll = ScrollingSheet(self.sheet)
        print(len(self.sheet))
        
        
    def loadSheetMusic(self):
        return frere_jacques()
        
        
    def run(self):
        pygame.midi.init()
        player = pygame.midi.Output(0)
        player.set_instrument(0)
        
        
        i = 0 
        start, stop = self.sheet.note_times[i]
        #print(i, start, stop, self.timePassed)
       
        while not self.gameOver:
            if self.totalTimePassed >= len(self.sheet):
                self.gameOver = True
                
            
            elif self.totalTimePassed >= stop:
                player.note_off(self.sheet[i].pitch, 127)
                i += 1
                if i < len(self.sheet.note_times):
                    start, stop = self.sheet.note_times[i]
                else:
                    start = stop = len(self.sheet) + 1
                #print('stop', i, start, stop, self.timePassed)                    
            elif self.totalTimePassed >= start:
                player.note_on(self.sheet[i].pitch, 127)
                start = stop
                #print('start', i, start, stop, self.timePassed)                    
            else:
                #print('diff', i, start, stop, self.timePassed)                    
                pass
                    
            
            self.updateScreen()
            pygame.display.update()
            timePassed = clock.tick(FPS)
            self.totalTimePassed += timePassed
            step = int(SPEED * timePassed / 1000)
            #print(timePassed, step)
            self.scroll.updatePos(step)

            self.checkForQuit()
            


            
        del player
        pygame.midi.quit()
            

    
    def checkForQuit(self):
        if pygame.event.peek(QUIT):
            self.gameOver = True

        
    def updateScreen(self):
        screen.fill(BG_COLOR) 
        for i in range(-2, 3):
            pygame.draw.line(screen, BLACK, (self.scroll.pos['startx'], HEIGHT // 2 + i * BAR_HEIGHT), 
                             (min(self.scroll.pos['endx'], WIDTH - SCREEN_MARGIN), HEIGHT // 2 + i * BAR_HEIGHT), 1)
        pygame.draw.line(screen, RED, (SCREEN_MARGIN + PLAYER_X, 0), (SCREEN_MARGIN + PLAYER_X, HEIGHT), 1)            



class ScrollingSheet():
    def __init__(self, sheet):
        self.sheet = sheet
        self.pos = {'startx': SCREEN_MARGIN + PLAYER_X,
                    'endx': int(SCREEN_MARGIN + PLAYER_X + SPEED * len(self.sheet) / 1000)}
    
    def updatePos(self, step):
        for e in self.pos:
            self.pos[e] -= step
            if self.pos[e] < SCREEN_MARGIN:
                if e in ('startx', 'endx'):
                    self.pos[e] = SCREEN_MARGIN
                else:
                    del self.pos[e]
        



if __name__ == '__main__':
    init()
    BeginScene(screen)
    game = Game()
    game.run()
    EndScene(screen)
    tearDown()
