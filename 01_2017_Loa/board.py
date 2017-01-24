import datetime
import numpy as np
import random
import time

from constants import *


class Board(object):
    
    def __init__(self):
        self.state = self.newBoard()
        self.currentPlayer = -1
        self.winner = None
        self.gameOver = False
        self.stoneTaken = False
        self.turnCount = 1
        
    def __repr__(self):
        return ''.join([str(d) for d in self.state.flat])
    
    def __str__(self):
        return self.__repr__()
               
    def newBoard(self):
        b = np.zeros((8, 8), dtype=np.int64)
        b[0, 1:-1] = BLACKVAL
        b[-1,1:-1] = BLACKVAL
        b[1:-1, 0] = WHITEVAL
        b[1:-1,-1] = WHITEVAL
        
        
        ''''b[1, 3] = WHITEVAL
        b[6, 4] = WHITEVAL
        b[4, 1] = WHITEVAL
        b[3, 6] = WHITEVAL'''
        ''''b[2, 6] = BLACKVAL
        b[3, 5] = WHITEVAL
        b[2, 5] = WHITEVAL
        b[3, 6] = WHITEVAL
        '''
        
        ''''b[6, 2] = BLACKVAL
        b[6, 3] = WHITEVAL
        b[5, 3] = WHITEVAL
        b[5, 2] = WHITEVAL'''
        
        return b
    
    def allAvailableMoves(self, state=None, player=None):
        start = datetime.datetime.utcnow()
        
        if state is None:
            st = self.state
        else:
            st = state

        if player is None:
            p = self.currentPlayer
        else:
            p = player            
            
        posrow, poscol = np.where(st == p)
        aav = []
        for pos in zip(posrow, poscol):
            aav += self.availableMoves(pos, st, p)
        
        end = datetime.datetime.utcnow()
        #print('aav time: {}'.format(end - start))
            
        return aav

    
    def availableMoves(self, fromPos, state=None, player=None):
        av = []
        
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player                        
        
        # horizontal
        #print('fromPos:', fromPos)
        #print('H:', self.state[fromPos[0]])
        #print(np.where(self.state[fromPos[0]] != EMPTY)[0])
        count = len(np.where(st[fromPos[0]] != EMPTY)[0])
        #print(count)
        if fromPos[1] - count >= 0:
            toPos = fromPos[0], fromPos[1] - count
            #print('toPos', toPos)
            if st[toPos] in (EMPTY, -p):
                #print(np.where(st[fromPos[0], toPos[1] + 1:fromPos[1]] == -p))
                if len(np.where(st[fromPos[0], toPos[1] + 1:fromPos[1]] == -p)[0]) == 0:
                    #print('added')
                    av.append((fromPos, toPos))
        if fromPos[1] + count <= 7:
            toPos = fromPos[0], fromPos[1] + count
            #print('toPos', toPos)
            if st[toPos] in (EMPTY, -p):
                #print(np.where(st[fromPos[0], fromPos[1] + 1:toPos[1]] == -p))
                if len(np.where(st[fromPos[0], fromPos[1] + 1:toPos[1]] == -p)[0]) == 0:
                    #print('added')
                    av.append((fromPos, toPos))
        
        # vertical
        #print('-----')
        #print('V:', np.where(st.T[fromPos[1]] != EMPTY))
        count = len(np.where(st.T[fromPos[1]] != EMPTY)[0])
        #print(count)
        if fromPos[0] - count >= 0:
            toPos = fromPos[0] - count, fromPos[1]
            if st[toPos] in (EMPTY, -p):
                #print(np.where(st[toPos[0] + 1:fromPos[0], fromPos[1]] == -p))
                if len(np.where(st[toPos[0] + 1:fromPos[0], fromPos[1]] == -p)[0]) == 0:
                    #print('added')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7:
            toPos = fromPos[0] + count, fromPos[1]
            if st[toPos] in (EMPTY, -p):
                #print(np.where(st[fromPos[0] + 1:toPos[0], fromPos[1]] == -p))
                if len(np.where(st[fromPos[0] + 1:toPos[0], fromPos[1]] == -p)[0]) == 0:
                    #print('added')
                    av.append((fromPos, toPos))                    
                

        # diagonal
        #print('-----')
        #print('diag \\', st.diagonal(fromPos[1] - fromPos[0]))
        count = len(np.where(st.diagonal(fromPos[1] - fromPos[0]) != EMPTY)[0])
        #print(count)
        if fromPos[0] - count >= 0 and fromPos[1] - count >= 0:
            toPos = fromPos[0] - count, fromPos[1] - count
            #print('toPos1', toPos, 'toPos[0] + 1', toPos[0] + 1, 'fromPos[0]', fromPos[0])
            if st[toPos] in (EMPTY, -p):
                if fromPos[0] >= fromPos[1]:
                    start, end = toPos[1] + 1, fromPos[1]
                else:
                    start, end = toPos[0] + 1, fromPos[0]
                #print('diag1', start, end, st.diagonal(fromPos[1] - fromPos[0])[start:end])
                if len(np.where(st.diagonal(fromPos[1] - fromPos[0])[start:end] == -p)[0]) == 0:
                    #print('added1')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7 and fromPos[1] + count <= 7:
            toPos = fromPos[0] + count, fromPos[1] + count
            #print('toPos2', toPos, 'fromPos[1] + 1', fromPos[0] + 1, 'toPos[1]', toPos[0])
            if st[toPos] in (EMPTY, -p):
                if fromPos[0] >= fromPos[1]:
                    start, end = fromPos[1] + 1, toPos[1]
                else:
                    start, end = fromPos[0] + 1, toPos[0]
                #print('diag2', start, end, st.diagonal(fromPos[1] - fromPos[0])[start:end])
                if len(np.where(st.diagonal(fromPos[1] - fromPos[0])[start:end] == -p)[0]) == 0:
                    #print('added2')
                    av.append((fromPos, toPos))

        #print('-----')
        flipped = np.fliplr(st)
        #import pprint
        #pprint.pprint(flipped)
        #print('diag /', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
        #print(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1]) != EMPTY))
        count = len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1]) != EMPTY)[0])
        #print(count)
        if fromPos[0] - count >= 0 and fromPos[1] + count <= 7:
            toPos = fromPos[0] - count, fromPos[1] + count
            #print('toPos1', toPos)
            if st[toPos] in (EMPTY, -p):
                #print('diag1 whole', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
                if fromPos[0] + fromPos[1] <= 7:
                    start, end = toPos[0] + 1, fromPos[0]
                else:
                    start, end = 7 - toPos[1] + 1, 7 - fromPos[1]
                #print('diag1 truncated', start, end, flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end])
                if len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end] == -p)[0]) == 0:
                    #print('added1')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7 and fromPos[1] - count >= 0:
            toPos = fromPos[0] + count, fromPos[1] - count
            #print('toPos2', toPos)
            if st[toPos] in (EMPTY, -p):
                #print('diag2 whole', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
                if fromPos[0] + fromPos[1] <= 7:
                    start, end = fromPos[0] + 1, toPos[0]
                else:
                    start, end = 7 - fromPos[1] + 1, 7 - toPos[1]
                #print('diag2 truncated', start, end, flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end])
                if len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end] == -p)[0]) == 0:
                    #print('added2: {}-{}'.format(fromPos, toPos))
                    av.append((fromPos, toPos))
        
        
        #print('----------\n----------')
        return av
    

    def changePlayer(self):
        self.currentPlayer = -self.currentPlayer
        self.turnCount += 1


    def playMove(self, move, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state.copy()
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player
            
        '''print('st={}'.format(st))
        print('move[0]={}'.format(move[0]))'''
        
        st[move[0]] = EMPTY
        
        self.stoneTaken = (st[move[1]] == -p)             
        
        st[move[1]] = p
        
        return st
    
        
    def checkGroup(self, state=None, player=None):       
        start = datetime.datetime.utcnow()
        
        if state is None:
            st = self.state
        else:
            st = state

        if player is None:
            p = self.currentPlayer
        else:
            p = player
        
        areGrouped = True
       
        posrow, poscol = np.where(st == p)
        unvisited = [pos for pos in zip(posrow, poscol)]
        checklist = []
        
        if len(unvisited) == 1:
            #print('group of one')
            return True
        
        random.shuffle(unvisited)
        checklist.append(unvisited.pop())
        
        while len(checklist) > 0:
            current = checklist.pop()
            #print('current:', current)
            
            x, y = current
            neighbours = [(xx, yy) for xx in range(x - 1, x + 2) for yy in range(y - 1, y + 2) if (xx, yy) != (x, y) 
                                   and xx >= 0 and xx <= 7 and yy >= 0 and yy <= 7]
            #print('neighbours:', neighbours)
            
            while len(neighbours) > 0:
                currentNeighbour = neighbours.pop()
                if currentNeighbour in unvisited:
                    unvisited.remove(currentNeighbour)
                    checklist.append(currentNeighbour)
            
            
        if len(unvisited) > 0:
            areGrouped = False
            
        #print('checkGroup:', unvisited)        
        
        end = datetime.datetime.utcnow()
        #print('checkGroup time={} areGrouped={}'.format(end - start, areGrouped))
        
        return areGrouped
    
    
    def isGameOver(self, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state[:]
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player

        if self.checkGroup(st, p):
            self.winner = p
            return True
        
        if self.stoneTaken:
            if self.checkGroup(st, -p):
                self.winner = -p
                return True 
        
        self.winner = None    
        return False
        
        
if __name__ == '__main__':
    b = Board()
    import pprint
    pprint.pprint(b)
        
        