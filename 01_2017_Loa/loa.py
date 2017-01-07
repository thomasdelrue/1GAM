'''
- mcts
- board object using numpy
- begin/end screen/gui
- persistence of AI?
'''


import numpy as np
import pprint
import pygame
import pygame.gfxdraw

from board import *
from constants import *
from pygame.locals import *
from sys import exit


def mainGame():
    global screen, clock, board, fromPos, toPos, timePassed, availableMoves
    
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
    pygame.display.set_caption("Lines of Action")
    
    clock = pygame.time.Clock()
    
    board = Board()
    
    fromPos = None
    toPos = None
    
    mouseClicked = False
    availableMoves = []
    
    while True:
        
        
        checkForQuit()

        # player's turn        
        if P[board.currentPlayer] == PLAYER: 
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    #mousex, mousey = event.pos
                    #print(getPosFromCoord(*event.pos))
                    if mouseClicked and fromPos is not None:
                        toPos = getPosFromCoord(*event.pos)
                        print('-toPos:', toPos)
                
                elif event.type == MOUSEBUTTONDOWN:
                    #mousex, mousey = event.pos
                    fromPos = None
                    pos = getPosFromCoord(*event.pos)
                    if pos and board.state[pos] == board.currentPlayer:
                        fromPos = pos
                        availableMoves = board.availableMoves(fromPos)
                    else:
                        availableMoves = []
                    mouseClicked = True
                
                elif event.type == MOUSEBUTTONUP:
                    if fromPos and toPos:
                        if (fromPos, toPos) in availableMoves:
                            # make move
                            board.playMove((fromPos, toPos))
                        fromPos = None
                        toPos = None
                        
                    mouseClicked = False                        
        
        
        timePassed = clock.tick(FPS) / 1000.0

        paintBoard()        
        pygame.display.update()
        
def checkForQuit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and 
                                  event.key == K_ESCAPE):
            exit()
        pygame.event.post(event)


    
def paintBoard():
    screen.fill(BGCOLOUR)
    
    pygame.draw.rect(screen, BOARDCOLOUR, (XMARGIN, YMARGIN, BOARDWIDTH + BOARDMARGIN * 2, BOARDHEIGHT + BOARDMARGIN * 2))
    
    # squares
    for i in range(9):
        pygame.draw.line(screen, BLACK, (XMARGIN + BOARDMARGIN + i * BOXSIZE, YMARGIN + BOARDMARGIN), 
                                        (XMARGIN + BOARDMARGIN + i * BOXSIZE, WINDOWHEIGHT - YMARGIN - BOARDMARGIN), 1)
        pygame.draw.line(screen, BLACK, (XMARGIN + BOARDMARGIN, YMARGIN + BOARDMARGIN + i * BOXSIZE), 
                                        (WINDOWWIDTH - XMARGIN - BOARDMARGIN, YMARGIN + BOARDMARGIN + i * BOXSIZE), 1)

    # stones
    posrow, poscol = np.where(board.state == BLACKVAL)
    for pos in zip(posrow, poscol):
        x, y = getCoordFromPos(pos)
        pygame.gfxdraw.filled_circle(screen, x, y, STONESIZE, BLACK)
        pygame.gfxdraw.circle(screen, x, y, STONESIZE, BLACK)
        
    posrow, poscol = np.where(board.state == WHITEVAL)
    for pos in zip(posrow, poscol):
        x, y = getCoordFromPos(pos)
        pygame.gfxdraw.filled_circle(screen, x, y, STONESIZE, WHITE)
        pygame.gfxdraw.circle(screen, x, y, STONESIZE, BLACK)
        

    # fromPos
    if fromPos is not None:
        x, y = getCoordFromPos(fromPos)
        pygame.gfxdraw.filled_circle(screen, x, y, 5, RED)
        
        if len(availableMoves) > 0:
            #print('show availableMoves', availableMoves)
            for move in availableMoves:
                x2, y2 = getCoordFromPos(move[1])
                pygame.gfxdraw.circle(screen, x2, y2, 5, RED)
        
        if toPos is not None and fromPos != toPos:
            x2, y2 = getCoordFromPos(toPos)
            pygame.draw.line(screen, RED, (x, y), (x2, y2), 5)
            pygame.gfxdraw.filled_circle(screen, x2, y2, 5, RED)

                  
''' x, y coord from a position (row, column)'''
def getCoordFromPos(pos):
    return XMARGIN + BOARDMARGIN + pos[1] * BOXSIZE + BOXSIZE // 2, YMARGIN + BOARDMARGIN + pos[0] * BOXSIZE + BOXSIZE // 2  


''' position (row, column) from a x, y coord'''
def getPosFromCoord(x, y):
    if (x < XMARGIN + BOARDMARGIN or x >= WINDOWWIDTH - XMARGIN - BOARDMARGIN or 
        y < YMARGIN + BOARDMARGIN or y >= WINDOWHEIGHT - YMARGIN - BOARDMARGIN):
        return None
    
    return (y - YMARGIN - BOARDMARGIN) // BOXSIZE, (x - XMARGIN - BOARDMARGIN) // BOXSIZE  
                      


if __name__ == '__main__':
    mainGame()