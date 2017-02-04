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
        boards[BLACKVAL] = b

        w = 0
        for idx in [55, 48, 47, 40, 39, 32, 31, 24, 23, 16, 15, 8]:
            w |= 2 ** idx
        boards[WHITEVAL] = w
        
        self.rows = { x: self.makeMask('row', x) for x in range(8) }
        self.cols = { x: self.makeMask('col', x) for x in range(8) }
        self.ldiag = { x: self.makeMask('ldiag', x) for x in range(-7, 8) }
        self.rdiag = { x: self.makeMask('rdiag', x) for x in range(-7, 8) }
        
        self.min_sum_dist = { x: x - 1 if x <= 9 else x + (x - 10) 
                              for x in range(2, 13) }
        
        self.board_cat = { x: self.makeMask(MC[x]) for x in range(5)}
        
        self.neighbourhood = { x: self.makeMask('neighbourhood', x) for x in range(64)}
        
        self.quads = { (r, c): self.makeMask('quads', (r, c)) for r in range(8) for c in range(8)}
        
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
        elif mtype == 'neighbourhood':
            for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
                if idx <= 7 and i in [-7, -8, -9]:
                    continue
                if idx >= 56 and i in [7, 8, 9]:
                    continue
                if idx % 8 == 0 and i in [-9, -1, 7]:
                    continue
                if (idx + 1) % 8 == 0 and i in [9, 1, -7]:
                    continue                    
                mask |= 2 ** (idx + i) 
        elif mtype == 'quads':
            mask = []
            rr = [r for r in range(idx[0] - 2, idx[0] + 2) if r >= 0 and r <= 6]
            cc = [c for c in range(idx[1] - 2, idx[1] + 2) if c >= 0 and c <= 6]
            for c in cc:
                for r in rr:
                    x = (7 - r) * 8 + (7 - c)
                    m = 0
                    for i in [x, x - 1, x - 8, x - 9]:
                        m |= 2 ** i
                    mask.append(m)
                   
        return mask
    
    def checkGroup(self, state=None, player=None):
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
                
                currentNeighbours = self.neighbourhood[current] & unvisited
                if currentNeighbours:
                    unvisited ^= currentNeighbours
                    checklist |= currentNeighbours
                
            if gmpy2.popcount(unvisited) > 0:
                areGrouped = False
        
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

        assert st[p] & st[-p] == 0, "overlapping states... {}, -1: {}, 1: {}".format(st[p] & st[-p], st[-1], st[1])

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
        self.stoneTaken = bool(you & 2 ** move[1])   
        if self.stoneTaken:
            you ^= 2 ** move[1]          
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
    def evaluate(self, state=None, player=None, move=None):
        if state is None:
            st = self.state
        else:
            st = state
            
        if player is None:
            p = self.currentPlayer
        else:
            p = player
        
        # the player        
        n = gmpy2.popcount(st[p])
        if n == 1:
            return 50
        
        nn = gmpy2.popcount(st[-p])
        if nn == 1:
            return -50
        
        x = gmpy2.bit_scan1(st[p])
        
        # centre of mass
        rr, cc = 0, 0
        pieces = []

        f2p = 0
        f7p = 0

        left = right = 7 - x % 8
        top = bottom = 7 - x // 8        
        while x is not None:
            r, c = 7 - x // 8, 7 - x % 8
            if r < top:
                top = r
            elif r > bottom:
                bottom = r
            if c < left:
                left = c
            elif c > right:
                right = c
            
            pieces.append((r, c))
            rr += r
            cc += c
            
            for i in range(5):
                if 2 ** x & self.board_cat[i]:
                    f2p += i - 2
                    break
            
            f7p += gmpy2.popcount(self.neighbourhood[x] & st[p])
            
            x = gmpy2.bit_scan1(st[p], x + 1)
        rr /= n
        rr = round(rr)
        cc /= n
        cc = round(cc)
        comp = (rr, cc)
        
        # sum of distances
        dist = 0
        for r, c in pieces:
            dist += max(abs(r - rr), abs(c - cc))
        
        # surplus of distances
        surplus = dist - self.min_sum_dist[n]
        
        f1p = 1 / (surplus + 1)
        
        f2p /= n * 2
        
        pos = (7 - rr) * 8 + 7 - cc
        for i in range(4, -1, -1):
            if 2 ** pos & self.board_cat[i]:
                f3p = 1 / (1 + i)
                break 

        f4p = 0
        for q in self.quads[comp]:
            if gmpy2.popcount(q & st[p]) == 3:
                f4p += 1
            elif gmpy2.popcount(q & st[p]) == 4:
                f4p += 2
        f4p /= len(self.quads[comp])

        f5p = 0        
        if move:
            f5p = .5
            if self.stoneTaken:
                f5p *= 2
            if 2 ** move[1] & (self.board_cat[0] | self.board_cat[1]):
                f5p /= 2
                if 2 ** move[0] & (self.board_cat[0] | self.board_cat[1]):
                    f5p /= 2          

        f7p /= n
        
        f8p = 1 / ((right - left + 1) * (bottom - top + 1))

        
        # the other

        x = gmpy2.bit_scan1(st[-p])
        
        # centre of mass
        rr, cc = 0, 0
        pieces = []
        
        f2o = 0
        f7o = 0

        left = right = 7 - x % 8
        top = bottom = 7 - x // 8        
        while x is not None:
            r, c = 7 - x // 8, 7 - x % 8
            if r < top:
                top = r
            elif r > bottom:
                bottom = r
            if c < left:
                left = c
            elif c > right:
                right = c
            
            pieces.append((r, c))
            rr += r
            cc += c
            
            for i in range(5):
                if 2 ** x & self.board_cat[i]:
                    f2o += i - 2
                    break

            f7o += gmpy2.popcount(self.neighbourhood[x] & st[-p])
            
            x = gmpy2.bit_scan1(st[-p], x + 1)
        rr /= nn
        rr = round(rr)
        cc /= nn
        cc = round(cc)
        como = (rr, cc)
        
        # sum of distances
        dist = 0
        for r, c in pieces:
            dist += max(abs(r - rr), abs(c - cc))
        
        # surplus of distances
        surplus = dist - self.min_sum_dist[nn]
        
        f1o = 1 / (surplus + 1)

        f2o /= nn * 2
        
        pos = (7 - rr) * 8 + 7 - cc
        for i in range(4, -1, -1):
            if 2 ** pos & self.board_cat[i]:
                f3o = 1 / (1 + i)
                break 

        f4o = 0
        for q in self.quads[como]:
            if gmpy2.popcount(q & st[-p]) == 3:
                f4o += 1
            elif gmpy2.popcount(q & st[-p]) == 4:
                f4o += 2
        f4o /= len(self.quads[como])


        f7o /= nn
        f8o = 1 / ((right - left + 1) * (bottom - top + 1))

        val = f1p - f1o + f2p - f2o + f3p - f3o + f4p - f4o + f5p + f7p - f7o + f8p - f8o
        
        # f9. player to move bonus
        if p == self.currentPlayer:
            val += .2

        return val   




if __name__ == '__main__':
    bb = BitBoard()
    print('-----')    
    '''bb.f1_concentration(bb.state[1])
    bb.f2_concentration(bb.state[1])'''
    
    ''' {1: 1152435641982976, -1: 9223442698233978892}'''
    
    '''print(bb.bitString(9007199254740992))''' 
    bb.state[-1] = 2 ** 55 | 2 ** 18 | 2 ** 17 | 2 ** 16
    bb.state[1] = 2 | 1 | 2 ** 10
    print(bb.bitString(bb.state[-1]))
    print(bb.bitString(bb.state[1]))
    
    '''bb.evaluate()'''
    
    #print(bb.f1_concentration(9007199254740992))
    print(bb.evaluate())
    print(bb.evaluate2())
    '''print('-------')
    for i in range(64):
        print(i, ':', bb.bitString(bb.neighbourhood[i]))'''
    
    '''for m in bb.quads[(4, 5)]:
        print(bb.bitString(m))'''
