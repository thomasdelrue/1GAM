'''based on article'''

from constants import *

import datetime
import bitboard
import math
import random
import pprint

'''
notes:
- keep in mind that it might be possible to pass: be sure to make that move also: i.e. save the nextState also,
  which will be identical to the current state
- first get a simple mcts going, then try to implement the ideas of the article...

- no copies in memory, make and UNMAKE the move...
'''

class Mcts(object):
    def __init__(self, board):
        self.board = board
        self.plays = {}
        self.wins = {}
        self.maxMoves = 45
        self.maxDepth = 0
        self.calculationTime = 5
        self.C = 1.4
        
        self.totalSimulations = 0
        
    
    def getPlay2(self):
        self.maxDepth = 0
        state = self.board.state.copy()
        
        '''print('beginning play...')
        print('-1: {}'.format(self.board.bitString(state[-1])))
        print('1: {}'.format(self.board.bitString(state[1])))'''
        
        player = self.board.currentPlayer
        available = self.board.allAvailableMoves()
        random.shuffle(available)
        line = 'turn: %d player: %d state:\n %s' % (self.board.turnCount, player, str(state))
        print(line)
                
        if not available:
            return
        if len(available) == 1:
            return available[0]
        
        games = 0        
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < datetime.timedelta(seconds=self.calculationTime):
            self.runSimulation2()
            games += 1
            
        #movesStates = [(p, stateState(self.board.playMove(p, state, player))) for p in available]
        
        line = '\ngames: %d time elapsed: %s' % (games, str(datetime.datetime.utcnow() - begin))
        print(line)
        
        '''print('after simulation...')
        for p, sb, sw, move in self.plays:
            print('{} {} {} {}'.format(p, self.board.bitString(sb), self.board.bitString(sw), move))
            
        print('-1: {}'.format(self.board.bitString(state[-1])))
        print('1: {}'.format(self.board.bitString(state[1])))'''
        
        # pick the move with the highest percentage of wins
        percentWins, move = max(
            (self.wins.get((player, state[-1], state[1], move), 0) /
             self.plays.get((player, state[-1], state[1], move), 1), move)
            for move in available
        )
        
        ''' indien een move nog geen 5 of meer plays gekregen heeft, werken met een evaluatie functie? '''
        
        line = "best move: %s %%chance of winning: %f" % (str(move), percentWins)
        print(line)
        
        # display stats for each possible play
        for x in sorted(((100 * self.wins.get((player, state[-1], state[1], move), 0) /
                         self.plays.get((player, state[-1], state[1], move), 1),
                         self.wins.get((player, state[-1], state[1], move), 0),
                         self.plays.get((player, state[-1], state[1], move), 0), move)
                        for move in available), reverse=True):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))
            
        print("Maximum depth searched: %d\n\n" % self.maxDepth)
        
        return move



    def runSimulation2(self):
        start = datetime.datetime.utcnow()
        
        plays, wins = self.plays, self.wins
        state = self.board.state.copy()
        player = self.board.currentPlayer
        visitedStates = set()
        
        expand = True
        
        for t in range(1, self.maxMoves + 1):
            #print('begin loop t{}'.format(t))
            available = self.board.allAvailableMoves(state, player)
            #print('all moves', available)

            if len(available) > 0:
                #movesStates = [(p, stateState(self.board.playMove(p, state, player))) for p in available]
                #line = ' ' * t +'%d: current: %s | moves: %s' % (t, stateState(state), str(movesStates[0]))
                #print(line)
            
            
                if all(plays.get((player, state[-1], state[1], move)) for move in available):
                    # if we have stats on all of the legal moves here, use them.
                    log_total = math.log(sum(plays[(player, state[-1], state[1], move)] for move in available))
                    value, move = max(
                        ((wins[(player, state[-1], state[1], move)] / plays[(player, state[-1], state[1], move)]) +
                         self.C * math.sqrt(log_total / plays[(player, state[-1], state[1], move)]), move)
                        for move in available
                    )
                    #line = ' ' * t +' val: %f, %s' % (value, str(move))
                    #print(line)
                else:
                    #move, _ = random.choice(movesStates)
                    
                    ''' wanneer expansion reeds gebeurd is, hier met een evaluatie functie werken? 
                    corrective strategy, greedy strategy...'''
                    
                    move = random.choice(available)
                    
                    #line = ' ' * t +' random: %s' % (str(move))
                    #print(line)
                
                nextState = self.board.makeMove(move, state, player)
                #self.board.unmakeMove(move, state, player)
            #statesCopy.append(state)
            
            ''' 'player' refers to player who moved
            into that particular state.'''
            if expand and (player, state[-1], state[1], move) not in plays:
                expand = False
                plays[(player, state[-1], state[1], move)] = 0
                wins[(player, state[-1], state[1], move)] = 0
                if t > self.maxDepth:
                    self.maxDepth = t
                    
                ''' hier 1-ply lookahead doen, op zoek naar een winner, indien winner(s?),
                backpropagation, en simulatie stoppen...                
                '''
            
            visitedStates.add((player, state[-1], state[1], move))
            
            if self.board.isGameOver(nextState, player):
                #line = ' ' * t + 'WINNER: %d\n' % (P[self.board.winner])
                #print(line)                
                break
            
            player = -player
            state = nextState
            
            #print('end loop t{}'.format(t))
            
        #pprint.pprint(visitedStates)
        for player, state[-1], state[1], move in visitedStates:
            if (player, state[-1], state[1], move) not in plays:
                continue
            plays[(player, state[-1], state[1], move)] += 1
            if self.board.winner is not None:
                if player == self.board.winner:
                    wins[(player, state[-1], state[1], move)] += 1
                else:
                    wins[(player, state[-1], state[1], move)] -= 1
            
        self.totalSimulations += 1
        end = datetime.datetime.utcnow()
        
        #print('runSimulation2: {}'.format(end - start))
        '''pprint.pprint(plays)'''


    
    
    
if __name__ == '__main__':
    b = bitboard.BitBoard()
    print(b)
    mcts = Mcts(b)
    
    #mcts.runSimulation2()
    #mcts.getPlay2()
    '''print('-------------')
    
    mcts.plays, mcts.wins = {}, {}
    mcts = Mcts(b)
    mcts.runSimulation2()'''
    
    while not b.isGameOver(player=-b.currentPlayer):
        move = mcts.getPlay2()
        b.state = b.makeMove(move)
        print(b)
        b.changePlayer()
        
    print('winner: {}'.format(b.winner))
