import datetime
import numpy as np

from constants import *


class Board(object):
    
    def __init__(self):
        self.state = self.newBoard()
        self.currentPlayer = -1
        
    def __repr__(self):
        return repr(self.state)
               
    def newBoard(self):
        b = np.zeros((8, 8), dtype=np.int8)
        b[0, 1:-1] = BLACKVAL
        b[-1,1:-1] = BLACKVAL
        b[1:-1, 0] = BLACKVAL #WHITEVAL
        b[1:-1,-1] = BLACKVAL #WHITEVAL
        
        
        b[1, 3] = WHITEVAL
        b[6, 4] = WHITEVAL
        b[4, 1] = WHITEVAL
        b[3, 6] = WHITEVAL
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
    
    def allAvailalbleMoves(self):
        start = datetime.datetime.utcnow()
         
        posrow, poscol = np.where(self.state == self.currentPlayer)
        aav = []
        for pos in zip(posrow, poscol):
            aav += self.availableMoves(pos)
        
        end = datetime.datetime.utcnow()
        print('aav time: {}'.format(end - start))
            
        return aav

    
    def availableMoves(self, fromPos):
        av = []
        
        # horizontal
        print('fromPos:', fromPos)
        print('H:', self.state[fromPos[0]])
        #print(np.where(self.state[fromPos[0]] != EMPTY)[0])
        count = len(np.where(self.state[fromPos[0]] != EMPTY)[0])
        print(count)
        if fromPos[1] - count >= 0:
            toPos = fromPos[0], fromPos[1] - count
            print('toPos', toPos)
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print(np.where(self.state[fromPos[0], toPos[1] + 1:fromPos[1]] == -self.currentPlayer))
                if len(np.where(self.state[fromPos[0], toPos[1] + 1:fromPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))
        if fromPos[1] + count <= 7:
            toPos = fromPos[0], fromPos[1] + count
            print('toPos', toPos)
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print(np.where(self.state[fromPos[0], fromPos[1] + 1:toPos[1]] == -self.currentPlayer))
                if len(np.where(self.state[fromPos[0], fromPos[1] + 1:toPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))
        
        # vertical
        print('-----')
        print('V:', np.where(self.state.T[fromPos[1]] != EMPTY))
        count = len(np.where(self.state.T[fromPos[1]] != EMPTY)[0])
        print(count)
        if fromPos[0] - count >= 0:
            toPos = fromPos[0] - count, fromPos[1]
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print(np.where(self.state[toPos[0] + 1:fromPos[0], fromPos[1]] == -self.currentPlayer))
                if len(np.where(self.state[toPos[0] + 1:fromPos[0], fromPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7:
            toPos = fromPos[0] + count, fromPos[1]
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print(np.where(self.state[fromPos[0] + 1:toPos[0], fromPos[1]] == -self.currentPlayer))
                if len(np.where(self.state[fromPos[0] + 1:toPos[0], fromPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))                    
                

        # diagonal
        print('-----')
        print('diag \\', self.state.diagonal(fromPos[1] - fromPos[0]))
        #print(np.where(self.state.diagonal(fromPos[1] - fromPos[0]) != EMPTY))
        count = len(np.where(self.state.diagonal(fromPos[1] - fromPos[0]) != EMPTY)[0])
        print(count)
        if fromPos[0] - count >= 0 and fromPos[1] - count >= 0:
            toPos = fromPos[0] - count, fromPos[1] - count
            print('toPos1', toPos, 'toPos[0] + 1', toPos[0] + 1, 'fromPos[0]', fromPos[0])
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                if fromPos[0] >= fromPos[1]:
                    start, end = toPos[1] + 1, fromPos[1]
                else:
                    start, end = toPos[0] + 1, fromPos[0]
                print('diag1', start, end, self.state.diagonal(fromPos[1] - fromPos[0])[start:end])
                if len(np.where(self.state.diagonal(fromPos[1] - fromPos[0])[start:end] == -self.currentPlayer)[0]) == 0:
                    print('added1')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7 and fromPos[1] + count <= 7:
            toPos = fromPos[0] + count, fromPos[1] + count
            print('toPos2', toPos, 'fromPos[1] + 1', fromPos[0] + 1, 'toPos[1]', toPos[0])
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                if fromPos[0] >= fromPos[1]:
                    start, end = fromPos[1] + 1, toPos[1]
                else:
                    start, end = fromPos[0] + 1, toPos[0]
                print('diag2', start, end, self.state.diagonal(fromPos[1] - fromPos[0])[start:end])
                if len(np.where(self.state.diagonal(fromPos[1] - fromPos[0])[start:end] == -self.currentPlayer)[0]) == 0:
                    print('added2')
                    av.append((fromPos, toPos))

        print('-----')
        flipped = np.fliplr(self.state)
        #import pprint
        #pprint.pprint(flipped)
        #print('fromPos[1] {} - fromPos[0] {} = {}'.format(fromPos[1], fromPos[0], fromPos[1] - fromPos[0]))
        print('diag /', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
        #print(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1]) != EMPTY))
        count = len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1]) != EMPTY)[0])
        print(count)
        if fromPos[0] - count >= 0 and fromPos[1] + count <= 7:
            toPos = fromPos[0] - count, fromPos[1] + count
            print('toPos1', toPos)
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print('diag1 whole', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
                if fromPos[0] + fromPos[1] <= 7:
                    start, end = toPos[0] + 1, fromPos[0]
                else:
                    start, end = 7 - toPos[1] + 1, 7 - fromPos[1]
                print('diag1 truncated', start, end, flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end])
                if len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end] == -self.currentPlayer)[0]) == 0:
                    print('added1')
                    av.append((fromPos, toPos))
        if fromPos[0] + count <= 7 and fromPos[1] - count >= 0:
            toPos = fromPos[0] + count, fromPos[1] - count
            print('toPos2', toPos)
            if self.state[toPos] in (EMPTY, -self.currentPlayer):
                print('diag2 whole', flipped.diagonal(7 - fromPos[0] - fromPos[1]))
                if fromPos[0] + fromPos[1] <= 7:
                    start, end = fromPos[0] + 1, toPos[0]
                else:
                    start, end = 7 - fromPos[1] + 1, 7 - toPos[1]
                print('diag2 truncated', start, end, flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end])
                if len(np.where(flipped.diagonal(7 - fromPos[0] - fromPos[1])[start:end] == -self.currentPlayer)[0]) == 0:
                    print('added2: {}-{}'.format(fromPos, toPos))
                    av.append((fromPos, toPos))
        
        
        print('----------\n----------')
        return av
    

    def changePlayer(self):
        self.currentPlayer = -self.currentPlayer

    def playMove(self, move):
        self.state[move[0]] = EMPTY
        self.state[move[1]] = self.currentPlayer
        
    def checkGroup(self):
        '''
        only check group for player that made the move, unless stone was taken, then check the other player as well
        '''
        '''
        
        0. check whether there's only one stone left -> is a group -> win condition
        1. add a random stone to checklist
        2. for each stone, check whether there's a neighbour who hasn't been visited yet, for the whole neighbourhood
        3. if so add neighbours to checklist, and add stone to visited...
        4. if there are still unvisited stones, and not on the checklist, then that means there's more than one group
        '''
        return False
    
        
if __name__ == '__main__':
    b = Board()
    import pprint
    pprint.pprint(b)
        
        