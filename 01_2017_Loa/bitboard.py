import datetime
import gmpy2

from constants import *


class BitBoard(object):
    def __init__(self):
        self.state = self.newBoard()
        self.currentPlayer = -1
        self.winner = None
        self.gameOver = False
        self.stoneTaken = False
        self.turnCount = 1
        
        self.mask64 = 2 ** 64 - 1
        
        
    def newBoard(self):
        boards = {}
        b = 0
        for idx in [62, 61, 60, 59, 58, 57, 6, 5, 4, 3, 2, 1]:
            b |= 2 ** idx
        print(b)
        boards[BLACKVAL] = b
        w = 0
        for idx in [55, 48, 47, 40, 39, 32, 31, 24, 23, 16, 15, 8]:
            w |= 2 ** idx
        print(w)
        boards[WHITEVAL] = w
        
        self.rows = { x: self.makeMask('row', x) for x in range(8) }
        self.cols = { x: self.makeMask('col', x) for x in range(8) }
        self.ldiag = { x: self.makeMask('ldiag', x) for x in range(-7, 8) }
        self.rdiag = { x: self.makeMask('rdiag', x) for x in range(-7, 8) }
        return boards
    
    
    def bitString(self, num):
        s = []
        for i in range(63, -1, -1):
            if (i + 1) % 8 == 0:
                s.append(' ')        
            if num & (2 ** i):
                s.append('1')
            else:
                s.append('0')
        return ''.join(s).strip() 
    
        
    def __str__(self):
        b = self.state[BLACKVAL]
        w = self.state[WHITEVAL]
        s = []
        for i in range(63, -1, -1):
            if (i + 1) % 8 == 0:
                s.append('\n')        
            if b & (2 ** i):
                s.append('x ')
            elif w & (2 ** i):
                s.append('o ')
            else:
                s.append('. ')
        return ''.join(s).strip()

    
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
        
        aav = []        

        n = gmpy2.bit_scan1(st[p])
        while n:
            aav += self.availableMoves(n, st, p)
            n = gmpy2.bit_scan1(st[p], n + 1)

        end = datetime.datetime.utcnow()
        #print('aav time: {}'.format(end - start))
            
        return aav
    
    
    
    ''' fromPos is a number from 63 to 0, representing the coord on the board'''
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
        
        fullst = st[p] | st[-p]
        #print(self.bitString(fullst))
                
        row = 7 - fromPos // 8 
        col = 7 - fromPos % 8
        #print(fromPos, row, col)

        # horizontal
        count = gmpy2.popcount(self.rows[row] & fullst)
        #print('H count={}'.format(count))
        if col - count >= 0:
            toPos = fromPos + count
            #print('H toPos1={}'.format(self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = (2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)
                #print('H mask1={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if col + count <= 7:
            toPos = fromPos - count
            #print('H toPos2={}'.format(self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = (2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)
                #print('H mask2={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # vertical
        count = gmpy2.popcount(self.cols[col] & fullst)
        #print('V count={}'.format(count))
        if row - count >= 0:
            toPos = fromPos + count * 8
            #print('V toPos1={}-{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)) & self.cols[col]
                #print('V mask1={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7:
            toPos = fromPos - count * 8
            #print('V toPos2={}-{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)) & self.cols[col]
                #print('V mask2={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # \ diag
        idx = col - row
        count = gmpy2.popcount(self.ldiag[idx] & fullst)
        #print('\ count={}'.format(count))
        if row - count >= 0 and col - count >= 0:
            toPos = fromPos + count * 9
            #print('\ toPos1={}/{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** (toPos - 8) - 1) ^ (2 ** (fromPos + 1) - 1)) & self.ldiag[idx]
                #print('\ mask1={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7 and col + count <= 7:
            toPos = fromPos - count * 9
            #print('\ toPos2={}/{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** (fromPos - 8) - 1) ^ (2 ** (toPos + 1) - 1)) & self.ldiag[idx]
                #print('\ mask2={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # / diag
        idx = 7 - col - row
        count = gmpy2.popcount(self.rdiag[idx] & fullst)
        #print('/ count={}'.format(count))
        if row - count >= 0 and col + count <= 7:
            toPos = fromPos + count * 7
            #print('/ toPos1={}/{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)) & self.rdiag[idx]
                #print('/ mask1={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7 and col - count >= 0:
            toPos = fromPos - count * 7
            #print('/ toPos2={}/{}'.format(toPos, self.bitString(2 ** toPos)))
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)) & self.rdiag[idx]
                #print('/ mask2={}'.format(self.bitString(mask)))
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))


        return av 


    def makeMask(self, mtype, idx):
        mask = 0
        if mtype == 'row':
            start = (8 - idx) * 8 - 1
            for i in range(start, start - 8, -1):
                mask |= 2 ** i    
        elif mtype == 'col':
            start = 63 - idx
            for i in range(start, -1, -8):
                mask |= 2 ** i 
        elif mtype == 'ldiag':
            start = 63 - idx if idx >= 0 else (8 + idx) * 8 - 1
            end = -1 if idx < 0 else start - (8 - idx) * 9 
            for i in range(start, end, -9):
                mask |= 2 ** i  
        elif mtype == 'rdiag':
            #print('rdiag')
            start = 63 - (7 - idx) if idx >= 0 else (8 + idx) * 8 - 8 
            end = -1 if idx < 0 else start - (8 - idx) * 7 
            #print(start, 'to', end)
            for i in range(start, end, -7):
                #print(i)
                mask |= 2 ** i  
                   
        return mask
    
    def checkGroup(self, state=None, player=None):
        #print('begin checkGroup')
        start = datetime.datetime.utcnow()
        
        if state is None:
            st = self.state
        else:
            st = state

        if player is None:
            p = self.currentPlayer
        else:
            p = player
            
        #print('state:', st[p])
        
        areGrouped = True
        
        if gmpy2.popcount(st[p]) == 1:
            areGrouped = True
        else:
            unvisited = st[p]
            checklist = 2 ** gmpy2.bit_scan1(unvisited)
            unvisited ^= checklist
            
            while gmpy2.popcount(checklist) > 0:
                current = gmpy2.bit_scan1(checklist)
                checklist ^= 2 ** current
                
                
                for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
                    if current <= 7 and i in [-7, -8, -9]:
                        continue
                    if current >= 56 and i in [7, 8, 9]:
                        continue
                    if current % 8 == 0 and i in [-9, -1, 7]:
                        continue
                    if (current + 1) % 8 == 0 and i in [9, 1, -7]:
                        continue                    
                    
                    
                    new = current + i
                    #print(new, current, i)

                    currentNeighbour = (2 ** new) & self.mask64
                    if currentNeighbour & unvisited:
                        unvisited ^= currentNeighbour
                        checklist |= currentNeighbour
                        
            if gmpy2.popcount(unvisited) > 0:
                areGrouped = False
        
        end = datetime.datetime.utcnow()
        #print('checkGroup time: {} areGrouped={}'.format(end - start, areGrouped))
                
        return areGrouped
    
    def changePlayer(self):
        self.currentPlayer = -self.currentPlayer
        self.turnCount += 1
        
    def isGameOver(self, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state
            
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

        
    def makeMove(self, move, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player
            
        me = st[p]
        you = st[-p]
        
        me ^= 2 ** move[0]  
        self.stoneTaken = bool(you & move[1])             
        me ^= 2 ** move[1]
        
        return { p: me, -p: you }
    
    
    def unmakeMove(self, move, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player
            
        '''print('st={}'.format(st))
        print('move[0]={}'.format(move[0]))'''

        st[p] ^= 2 ** move[1]
        self.stoneTaken = False             
        st[p] ^= 2 ** move[0]  
        
        return st    
    
    ''' heuristic evaluation function of the board'''
    def evaluate(self):
        pass
        

if __name__ == '__main__':
    bb = BitBoard()
    #print(bb.bitString(bb.state[BLACKVAL]))
    #print(bb.bitString(bb.state[WHITEVAL]))
    bb.currentPlayer = 1
    print(bb)
    
    
    #mask = bb.makeMask('row', 2)
    
    import pprint
    '''for r in bb.rows:
        print(bb.bitString(bb.rows[r]))
    for c in bb.cols:
        print(bb.bitString(bb.cols[c]))'''
    for ld in range(-7, 8):
        print(ld, ' --- ', bb.bitString(bb.ldiag[ld]))
    print('----')      
    for rd in range(7, -8, -1):
        print(rd,' --- ', bb.bitString(bb.rdiag[rd]))        
        
    '''print('----- check between 61 and 57')
    start = 2 ** 62 - 1
    end = 2 ** 57 - 1
    slice = start ^ end
    print(bb.bitString(slice))''' 
    
    bb.state[bb.currentPlayer] |= 2 ** 26
    av = bb.availableMoves(26)
    print('av={}'.format(av))
    
    
    bb.state[1] = 36452660924219712
    bb.currentPlayer = 1
    bb.checkGroup()
    
    print('-------')
    print(bb.allAvailableMoves())