'''
Lines of Action
---------------

- not yet implemented: pass moves? probably bugs the ai too  
- bug: deciding winner...
- to do: gui, sound, smarten up ai

- saving winning moves?


'''

import mcts
import gmpy2
import random
import pprint
import pygame
import pygame.gfxdraw

from bitboard import *
from constants import *
from pygame.locals import *
from sys import exit


def mainGame():
    global screen, clock, board, fromPos, toPos, timePassed, availableMoves, basicFont, ai
    
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
    pygame.display.set_caption("Lines of Action")
    
    player_cursor = pygame.mouse.get_cursor()
    
    
    basicFont = pygame.font.SysFont("Arial", FONTSIZE)
    
    clock = pygame.time.Clock()
    
    board = BitBoard()
    ai = mcts.Mcts(board) 
    
    fromPos = None
    toPos = None
    
    mouseClicked = False
    availableMoves = board.allAvailableMoves()
    
    printText('Welcome to a game of Lines of Action', 2)
    
    toss = [BLACKVAL, WHITEVAL]
    random.shuffle(toss)
    print(toss)
    P[toss[0]] = PLAYER
    P[toss[1]] = COMPUTER
    printText("{} is black and {} is white. Black begins.".format(P[BLACKVAL], P[WHITEVAL]), 2)
    
    if P[board.currentPlayer] == COMPUTER:
        pygame.mouse.set_cursor(*computer_cursor) 
    
    gameOver = False
    
    while True:
        checkForQuit()

        
        ''' check whether Game Over, by checkGroup for both players?'''
        if not gameOver:
            # player's turn        
            if P[board.currentPlayer] == PLAYER:
                if len(availableMoves) == 0:
                    printText('{} needs to pass'.format(PLAYER), 1)                
                    board.changePlayer()
                    availableMoves = board.allAvailableMoves()
                 
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        #mousex, mousey = event.pos
                        #print(getPosFromCoord(*event.pos))
                        if mouseClicked and fromPos is not None:
                            toPos = getPosFromCoord(*event.pos)
                            #print('-toPos:', toPos)
                            
                    elif event.type == MOUSEBUTTONDOWN:
                        #mousex, mousey = event.pos
                        fromPos = None
                        pos = getPosFromCoord(*event.pos)
                        if pos and board.state[board.currentPlayer] & 2 ** pos:
                            fromPos = pos
                            #availableMoves = board.availableMoves(fromPos)
                        else:
                            #availableMoves = []
                            pass
                        mouseClicked = True
                    
                    elif event.type == MOUSEBUTTONUP:
                        if fromPos and toPos:
                            if (fromPos, toPos) in availableMoves:
                                # make move
                                board.state[board.currentPlayer] ^= 2 ** fromPos
                                animateMove(fromPos, toPos)
                                board.stoneTaken = (board.state[-board.currentPlayer] & 2 ** toPos)
                                if board.stoneTaken:
                                    board.state[-board.currentPlayer] ^= 2 ** toPos
                                board.state[board.currentPlayer] ^= 2 ** toPos
                                gameOver = board.isGameOver()
                                board.changePlayer()
                                availableMoves = board.allAvailableMoves()
                                pygame.mouse.set_cursor(*computer_cursor)
                            fromPos = None
                            toPos = None
                            
                        mouseClicked = False                        
            else:
                # computer
                if len(availableMoves) > 0:
                    #fromPos, toPos = random.choice(availableMoves)
                    
                    fromPos, toPos = ai.getPlay()
                    #print('picked fromPos, movePos={}, {}'.format(fromPos, toPos))
                    board.state[board.currentPlayer] ^= 2 ** fromPos
                    animateMove(fromPos, toPos)
                    board.stoneTaken = (board.state[-board.currentPlayer] & 2 ** toPos)
                    if board.stoneTaken:
                        board.state[-board.currentPlayer] ^= 2 ** toPos
                    board.state[board.currentPlayer] ^= 2 ** toPos
                    fromPos, toPos = None, None
                    gameOver = board.isGameOver()
                else:
                    printText('{} needs to pass'.format(COMPUTER), 1)
                board.changePlayer()
                availableMoves = board.allAvailableMoves()
                pygame.mouse.set_cursor(*player_cursor)
            
            ai.runSimulation()
            timePassed = clock.tick(FPS) / 1000.0
    
            paintBoard()        
            pygame.display.update()


        else: #game over
            pygame.mouse.set_cursor(*player_cursor)
            if board.winner:
                winTxt = '{} won.'.format(P[board.winner])
            else:
                winTxt = 'Draw.'
            printText('Game over. '+ winTxt, 3)
            
            

        
def checkForQuit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and 
                                  event.key == K_ESCAPE):
            ai.saveKnowledgeTree()
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
    pos = gmpy2.bit_scan1(board.state[BLACKVAL])
    while pos is not None:
        x, y = getCoordFromPos(pos)
        pygame.gfxdraw.filled_circle(screen, x, y, STONESIZE, BLACK)
        pygame.gfxdraw.aacircle(screen, x, y, STONESIZE, BLACK)
        pos = gmpy2.bit_scan1(board.state[BLACKVAL], pos + 1)

        
    pos = gmpy2.bit_scan1(board.state[WHITEVAL])
    while pos is not None:
        x, y = getCoordFromPos(pos)
        pygame.gfxdraw.filled_circle(screen, x, y, STONESIZE, WHITE)
        pygame.gfxdraw.aacircle(screen, x, y, STONESIZE, BLACK)
        pos = gmpy2.bit_scan1(board.state[WHITEVAL], pos + 1)
        
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
                #print('selected/availableMoves={}'.format(availableMoves))
                for move in availableMoves:
                    if fromPos == move[0]:
                        x2, y2 = getCoordFromPos(move[1])
                        pygame.gfxdraw.aacircle(screen, x2, y2, 3, RED)
            
            if toPos is not None and fromPos != toPos:
                x2, y2 = getCoordFromPos(toPos)
                pygame.gfxdraw.line(screen, x, y, x2, y2, RED)
                pygame.gfxdraw.filled_circle(screen, x2, y2, 3, RED)
                pygame.gfxdraw.aacircle(screen, x2, y2, 3, RED)

                  
''' x, y coord from a position (row, column)'''
def getCoordFromPos(pos):
    row = 7 - pos // 8 
    col = 7 - pos % 8
    return XMARGIN + BOARDMARGIN + col * BOXSIZE + BOXSIZE // 2, YMARGIN + BOARDMARGIN + row * BOXSIZE + BOXSIZE // 2
  

''' calculates the position on the board from a x, y coord'''
def getPosFromCoord(x, y):
    if (x < XMARGIN + BOARDMARGIN or x >= WINDOWWIDTH - XMARGIN - BOARDMARGIN or 
        y < YMARGIN + BOARDMARGIN or y >= WINDOWHEIGHT - YMARGIN - BOARDMARGIN):
        return None

    # calculates row, column from coordinates    
    pos = (y - YMARGIN - BOARDMARGIN) // BOXSIZE, (x - XMARGIN - BOARDMARGIN) // BOXSIZE
    #print('pos={}'.format(pos))
    
    # calculates pos number (63 - 0) from a row, column-pair
    newPos = 8 * (7 - pos[0]) + 7 - pos[1] 
    #print('newPos={}'.format(newPos))

    return newPos  

                      
''' prints Text, for an amount of time. timing in seconds '''
def printText(text, timing):
    textSurf = basicFont.render(text, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = TEXTPOS
    
    start = datetime.datetime.utcnow()
    
    while datetime.datetime.utcnow() - start <= datetime.timedelta(seconds=timing):
        paintBoard()    
        screen.blit(textSurf, textRect)
        pygame.display.update()
    


if __name__ == '__main__':
    mainGame()