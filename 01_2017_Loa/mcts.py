'''based on article'''

from constants import *

import datetime
import bitboard
import math
import random
import pprint

import pickle

'''
notes:
- keep in mind that it might be possible to pass: be sure to make that move also: i.e. save the nextState also,
  which will be identical to the current state
  
- 1100g in 6s random+cython tgo. ?g per 6s met eval+cython?
'''

class Mcts(object):
    def __init__(self, board):
        self.board = board
        self.plays = {}
        self.wins = {}
        self.maxMoves = 45
        self.maxDepth = 0
        self.calculationTime = 7.5
        self.C = 1.4
        
        self.totalSimulations = 0
        
        self._debug = False 
        
        self.loadKnowledgeTree()
        
        
    def loadKnowledgeTree(self):
        try:
            with open('plays.data', 'rb') as p:
                self.plays = pickle.load(p)
                print('\nloaded plays. {} entries'.format(len(self.plays)))
        except FileNotFoundError:
            print('\nno plays.data')
            
        try:
            with open('wins.data', 'rb') as w:
                self.wins = pickle.load(w)
                print('loaded wins. {} entries'.format(len(self.wins)))
        except FileNotFoundError:
            print('no wins.data\n')            
        
    
    def saveKnowledgeTree(self):
        savePlays = { k: self.plays[k] for k in self.plays if self.wins[k] != 0 }
        
        try:
            with open('plays.data', 'wb') as p:
                pickle.dump(savePlays, p)
                print('\nsaved plays. {} entries'.format(len(savePlays)))
        except:
            print('\ncould not save plays') 
    
        saveWins = { k: self.wins[k] for k in self.wins if self.wins[k] != 0 }
        
        try:
            with open('wins.data', 'wb') as w:
                pickle.dump(saveWins, w)
                print('saved wins. {} entries'.format(len(saveWins)))
        except:
            print('could not save wins') 
    
    
    def getPlay(self):
        self.maxDepth = 0
        state = self.board.state.copy()
        
        player = self.board.currentPlayer
        available = self.board.allAvailableMoves()
        random.shuffle(available)
        if self._debug:
            line = 'turn: %d player: %d state:\n %s' % (self.board.turnCount, player, str(state))
            print(line)
                
        if not available:
            return
        if len(available) == 1:
            return available[0]
        
        games = 0        
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < datetime.timedelta(seconds=self.calculationTime):
            self.runSimulation()
            games += 1
            
        if self._debug:
            line = '\ngames: %d time elapsed: %s' % (games, str(datetime.datetime.utcnow() - begin))
            print(line)
        
        # pick the move with the highest percentage of wins
        percentWins, move = max(
            (self.wins.get((player, state[-1], state[1], move), 0) /
             self.plays.get((player, state[-1], state[1], move), 1), move)
            for move in available
        )
        
        if self._debug:
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
        
        assert type(move) is tuple and len(move) == 2, '{} is not a valid move'.format(move)
        return move



    def runSimulation(self, eval=True):
        #start = datetime.datetime.utcnow()
        
        plays, wins = self.plays, self.wins
        state = self.board.state.copy()
        player = self.board.currentPlayer
        playerToMove = player

        visitedStates = set()
        
        expand = True
        scoreLoss, scoreWin = False, False
        
        for t in range(1, self.maxMoves + 1):
            available = self.board.allAvailableMoves(state, player)

            if len(available) > 0:
            
                if all(plays.get((player, state[-1], state[1], move)) for move in available):
                    # if we have stats on all of the legal moves here, use them.
                    log_total = math.log(sum(plays[(player, state[-1], state[1], move)] for move in available))
                    value, move = max(
                        ((wins[(player, state[-1], state[1], move)] / plays[(player, state[-1], state[1], move)]) +
                         self.C * math.sqrt(log_total / plays[(player, state[-1], state[1], move)]), move)
                        for move in available
                    )
                else:
                    if (t + 1) % 3 or not eval:
                        move = random.choice(available)
                    else:
                        value, move = max((self.board.evaluate(self.board.makeMove(move, state, player), player, move), move)
                                          for move in available
                        )
                
                nextState = self.board.makeMove(move, state, player)
            
            else:
                move = None
            
            ''' 'player' refers to player who moved
            into that particular state.'''
            if expand and (player, state[-1], state[1], move) not in plays:
                expand = False
                plays[(player, state[-1], state[1], move)] = 0
                wins[(player, state[-1], state[1], move)] = 0
                if t > self.maxDepth:
                    self.maxDepth = t
                    
                lookahead = self.board.allAvailableMoves(nextState, -player)
                if player != playerToMove:
                    for l in lookahead:
                        laState = self.board.makeMove(l, nextState, -player)
                        if self.board.isGameOver(laState, -player) and self.board.winner == -player:
                            scoreWin = True
                            break
                else:
                    for l in lookahead:
                        laState = self.board.makeMove(l, nextState, -player)
                        if self.board.isGameOver(laState, -player) and self.board.winner == player:
                            scoreLoss = True
                            break
            
            visitedStates.add((player, state[-1], state[1], move))
            
            if self.board.isGameOver(nextState, player) or scoreWin or scoreLoss:
                break
            
            player = -player
            state = nextState
            
        for player, state[-1], state[1], move in visitedStates:
            if (player, state[-1], state[1], move) not in plays:
                continue
            plays[(player, state[-1], state[1], move)] += 1

            if player == self.board.winner or scoreWin:
                wins[(player, state[-1], state[1], move)] += 1
            elif -player == self.board.winner or scoreLoss:
                wins[(player, state[-1], state[1], move)] -= 1
            
        self.totalSimulations += 1
        


def test(*args):
    b = bitboard.BitBoard()
    print(b)
    mcts = Mcts(b)
    mcts._debug = True
    if len(args) > 0 and type(args[0]) is int:
        print('set calculation time at {} seconds'.format(args[0]))
        mcts.calculationTime = args[0]

    
    while not b.isGameOver(player=-b.currentPlayer):
        move = mcts.getPlay()
        b.state = b.makeMove(move)
        print(b)
        b.changePlayer()
        
    print('winner: {}'.format(b.winner))
    
    mcts.saveKnowledgeTree()
    

    
if __name__ == '__main__':
    test()