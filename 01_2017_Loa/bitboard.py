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
        #for idx in [37, 36]:            
            w |= 2 ** idx
        print(w)
        boards[WHITEVAL] = w
        
        self.rows = { x: self.makeMask('row', x) for x in range(8) }
        self.cols = { x: self.makeMask('col', x) for x in range(8) }
        self.ldiag = { x: self.makeMask('ldiag', x) for x in range(-7, 8) }
        self.rdiag = { x: self.makeMask('rdiag', x) for x in range(-7, 8) }
        
        self.min_sum_dist = { x: x - 1 if x <= 9 else x + (x - 10) 
                              for x in range(2, 13) }
        
        self.board_cat = { x: self.makeMask(MC[x]) for x in range(5)}
        
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
        #start = datetime.datetime.utcnow()
        
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

        #end = datetime.datetime.utcnow()
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
                
        row = 7 - fromPos // 8 
        col = 7 - fromPos % 8

        # horizontal
        count = gmpy2.popcount(self.rows[row] & fullst)
        if col - count >= 0:
            toPos = fromPos + count
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = (2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if col + count <= 7:
            toPos = fromPos - count
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = (2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # vertical
        count = gmpy2.popcount(self.cols[col] & fullst)
        if row - count >= 0:
            toPos = fromPos + count * 8
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)) & self.cols[col]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7:
            toPos = fromPos - count * 8
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)) & self.cols[col]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # \ diag
        idx = col - row
        count = gmpy2.popcount(self.ldiag[idx] & fullst)
        if row - count >= 0 and col - count >= 0:
            toPos = fromPos + count * 9
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** (toPos - 8) - 1) ^ (2 ** (fromPos + 1) - 1)) & self.ldiag[idx]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7 and col + count <= 7:
            toPos = fromPos - count * 9
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** (fromPos - 8) - 1) ^ (2 ** (toPos + 1) - 1)) & self.ldiag[idx]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        # / diag
        idx = 7 - col - row
        count = gmpy2.popcount(self.rdiag[idx] & fullst)
        if row - count >= 0 and col + count <= 7:
            toPos = fromPos + count * 7
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** toPos - 1) ^ (2 ** (fromPos + 1) - 1)) & self.rdiag[idx]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))
        if row + count <= 7 and col - count >= 0:
            toPos = fromPos - count * 7
            if st[p] & 2 ** toPos == 0 or st[-p] & 2 ** toPos == 1:
                mask = ((2 ** fromPos - 1) ^ (2 ** (toPos + 1) - 1)) & self.rdiag[idx]
                if gmpy2.popcount(mask & st[-p]) == 0:
                    av.append((fromPos, toPos))

        return av 


    def makeMask(self, mtype, idx=None):
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
            start = 63 - (7 - idx) if idx >= 0 else (8 + idx) * 8 - 8 
            end = -1 if idx < 0 else start - (8 - idx) * 7 
            for i in range(start, end, -7):
                mask |= 2 ** i  
        elif mtype == 'corners':
            for i in [63, 56, 7, 0]:
                mask |= 2 ** i
        elif mtype == '8x8':
            for i in [62, 61, 60, 59, 58, 57, 6, 5, 4, 3, 2, 1,
                      55, 48, 47, 40, 39, 32, 31, 24, 23, 16, 15, 8]:
                mask |= 2 ** i
        elif mtype == '6x6':
            for i in [54, 53, 52, 51, 50, 49, 46, 41, 38, 33,
                      30, 25, 22, 17, 14, 13, 12, 11, 10, 9]:
                mask |= 2 ** i
        elif mtype == '4x4':
            for i in [45, 44, 43, 42, 37, 34, 29, 26, 21, 20, 19, 18]:
                mask |= 2 ** i
        elif mtype == '2x2':
            for i in [36, 35, 28, 27]:
                mask |= 2 ** i
                   
        return mask
    
    def checkGroup(self, state=None, player=None):
        #print('begin checkGroup')
        #start = datetime.datetime.utcnow()
        
        if state is None:
            st = self.state
        else:
            st = state

        if player is None:
            p = self.currentPlayer
        else:
            p = player
            
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
        
        #end = datetime.datetime.utcnow()
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
        
        return { p: me , -p: you}
    
    
    def unmakeMove(self, move, state=None, player=None):
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player

        st[p] ^= 2 ** move[1]
        if self.stoneTaken:
            st[-p] ^= 2 ** move[1]
            self.stoneTaken = False             
        st[p] ^= 2 ** move[0]  
        
        return st    
    
    ''' heuristic evaluation function of the board'''
   
    ''' for the moment, this eval + cythonised gives 125 +- games per 5 secs'''
    def evaluate(self, state=None, player=None, move=None):
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player
        
        f1p, comp = self.f1_concentration(st[p]) 
        f1o, como = self.f1_concentration(st[-p])
        
        val = f1p - f1o
        val += self.f2_centralisation(st[p]) - self.f2_centralisation(st[-p])
        val += self.f3_centre_of_mass_pos(st[p], comp) - self.f3_centre_of_mass_pos(st[-p], como)
        
        if move:
            val += self.f5_mobility(st[p], move)
        
        # f9. player to move bonus
        if p == self.currentPlayer:
            val += .2
        
        return val    

    def f1_concentration(self, state):
        n = gmpy2.popcount(state)
        if n == 1:
            return 1.0
        
        # centre of mass
        rr, cc = 0, 0
        x = gmpy2.bit_scan1(state)
        p = []
        while x is not None:
            r, c = 7 - x // 8, 7 - x % 8
            p.append((r, c))
            rr += r
            cc += c
            #print(x, r, c, rr, cc)
            x = gmpy2.bit_scan1(state, x + 1)
        rr /= n
        rr = round(rr)
        cc /= n
        cc = round(cc)
        #print('centre of mass={}'.format((rr, cc)))
        
        # sum of distances
        dist = 0
        for r, c in p:
            dist += max(abs(r - rr), abs(c - cc))
        #print('sum of distances={}'.format(dist))
        
        # surplus of distances
        surplus = dist - self.min_sum_dist[n]
        #print('surplus={} -> return value={}'.format(surplus, 1 / surplus))
        
        return 1 / (surplus + 1), (rr, cc)

    
    def f2_centralisation(self, state): 
        n = gmpy2.popcount(state)
        x = gmpy2.bit_scan1(state)
        score = 0
        while x is not None:
            for i in range(5):
                if 2 ** x & self.board_cat[i]:
                    score += i - 2
                    break
            x = gmpy2.bit_scan1(state, x + 1)
        score /= n * 2
        #print('centralisation score: {}'.format(score))
        return score
    
    def f3_centre_of_mass_pos(self, state, com):
        pos = (7 - com[0]) * 8 + 7 - com[1]
        for i in range(4, -1, -1):
            if 2 ** pos & self.board_cat[i]:
                return 1 / (1 + i) 
            
    def f5_mobility(self, state, move):
        val = 1
        if self.stoneTaken:
            val *= 2
        if 2 ** move[1] & (self.board_cat[0] | self.board_cat[1]):
            val /= 2
            if 2 ** move[0] & (self.board_cat[0] | self.board_cat[1]):
                val /= 2          
        
        return val / 2

if __name__ == '__main__':
    bb = BitBoard()
    print('-----')    
    '''bb.f1_concentration(bb.state[1])
    bb.f2_concentration(bb.state[1])'''
    bb.evaluate()
    
   
