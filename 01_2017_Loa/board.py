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
        b[1:-1, 0] = WHITEVAL
        b[1:-1,-1] = WHITEVAL
        return b

    def availableMoves(self, fromPos):
        av = []
        
        # horizontal
        #print('H:', self.state[fromPos[0]])
        print(np.where(self.state[fromPos[0]] != EMPTY)[0])
        count = len(np.where(self.state[fromPos[0]] != EMPTY)[0])
        print(count)
        if fromPos[1] - count >= 0:
            toPos = fromPos[0], fromPos[1] - count
            #print('toPos', toPos)
            if self.state[toPos] in (EMPTY, self.currentPlayer):
                print(np.where(self.state[fromPos[0], toPos[1] + 1:fromPos[1]] == -self.currentPlayer))
                if len(np.where(self.state[fromPos[0], toPos[1] + 1:fromPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))
        if fromPos[1] + count <= 7:
            toPos = fromPos[0], fromPos[1] + count
            print('toPos', toPos)
            if self.state[toPos] in (EMPTY, self.currentPlayer):
                print(self.state[fromPos[0], fromPos[1] + 1:toPos[1]])
                if len(np.where(self.state[fromPos[0], fromPos[1] + 1:toPos[1]] == -self.currentPlayer)[0]) == 0:
                    print('added')
                    av.append((fromPos, toPos))
        
        # vertical
        #print(np.where(self.state.T[fromPos[1]] != EMPTY))
        count = len(np.where(self.state.T[fromPos[1]] != EMPTY)[0])
        #print(count)

        # diagonal
        #print(np.where(self.state.diagonal(fromPos[1] - fromPos[0]) != EMPTY))
        count = len(np.where(self.state.diagonal(fromPos[1] - fromPos[0]) != EMPTY)[0])
        #print(count)
        
        #print(np.where(self.state[::-1].diagonal(fromPos[0] - fromPos[1]) != EMPTY))
        count = len(np.where(self.state[::-1].diagonal(fromPos[0] - fromPos[1]) != EMPTY)[0])
        #print(count)
        
        return av

    def changePlayer(self):
        self.currentPlayer = -self.currentPlayer

    def playMove(self, move):
        self.state[move[0]] = EMPTY
        self.state[move[1]] = self.currentPlayer
        
    def checkGroup(self):
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
        
        