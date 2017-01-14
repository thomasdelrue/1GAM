'''
- mcts
- board object using numpy
- begin/end screen/gui
- persistence of AI?


- rekening houden met als er geen available moves zijn...
'''


import numpy as np
import random
import pprint
import pygame
import pygame.gfxdraw

from board import *
from constants import *
from pygame.locals import *
from sys import exit

import timeit

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
    availableMoves = [] # to do: change this to allAvailableMoves for player...
    
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
                            board.state[fromPos] = EMPTY
                            animateMove(fromPos, toPos)
                            board.state[toPos] = board.currentPlayer
                            board.changePlayer()
                        fromPos = None
                        toPos = None
                        
                    mouseClicked = False                        
        else:
            # computer
            aav = board.allAvailalbleMoves()
            move = random.choice(aav)
            if move:
                fromPos, toPos = move
                print('picked fromPos, movePos={}, {}'.format(fromPos, toPos))
                board.state[fromPos] = EMPTY
                animateMove(fromPos, toPos)
                board.state[toPos] = board.currentPlayer
                fromPos, toPos = None, None
            else:
                # pass
                pass # display 'Pass' on screen?
            board.changePlayer()

            
        
        timePassed = clock.tick(FPS) / 1000.0

        paintBoard()        
        pygame.display.update()


        
def checkForQuit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and 
                                  event.key == K_ESCAPE):
            exit()
        pygame.event.post(event)


def animateMove(origin, destination):
    startx, starty = getCoordFromPos(origin)
    endx, endy = getCoordFromPos(destination)
    
    speedRate = FPS // 2
    
    stepx = (endx - startx) // speedRate
    stepy = (endy - starty) // speedRate
    
    for i in range(speedRate):
        checkForQuit()
        paintBoard(moving=(startx + i * stepx, starty + i * stepy))    
        pygame.display.update()    
        clock.tick(FPS)   

    
def paintBoard(moving=None):
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
        pygame.gfxdraw.aacircle(screen, x, y, STONESIZE, BLACK)
        
    posrow, poscol = np.where(board.state == WHITEVAL)
    for pos in zip(posrow, poscol):
        x, y = getCoordFromPos(pos)
        pygame.gfxdraw.filled_circle(screen, x, y, STONESIZE, WHITE)
        pygame.gfxdraw.aacircle(screen, x, y, STONESIZE, BLACK)
        
    if moving:
        pygame.gfxdraw.filled_circle(screen, moving[0], moving[1], STONESIZE, PCOLOUR[board.currentPlayer])
        pygame.gfxdraw.aacircle(screen, moving[0], moving[1], STONESIZE, BLACK)
        
    else:
        # fromPos
        if fromPos is not None:
            x, y = getCoordFromPos(fromPos)
            pygame.gfxdraw.filled_circle(screen, x, y, 3, RED)
            pygame.gfxdraw.aacircle(screen, x, y, 3, RED)
            
            if len(availableMoves) > 0:
                for move in availableMoves:
                    x2, y2 = getCoordFromPos(move[1])
                    pygame.gfxdraw.aacircle(screen, x2, y2, 3, RED)
            
            if toPos is not None and fromPos != toPos:
                x2, y2 = getCoordFromPos(toPos)
                pygame.gfxdraw.line(screen, x, y, x2, y2, RED)
                pygame.gfxdraw.filled_circle(screen, x2, y2, 3, RED)
                pygame.gfxdraw.aacircle(screen, x2, y2, 3, RED)

                  
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