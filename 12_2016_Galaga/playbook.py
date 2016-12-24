from constants import *

'''
idea of this file, is a playbook that has all the information
about the time development in the game, what the different 
stages are, and what happens in them...

the clock of the game should keep track of the time, and in
what play of the book we're currently in.

ie Challenging and Ready stage are allotted a certain amount of time,
other stages are not, and continue as long as there are aliens on screen
during that stage...

---
and yet, this idea of a playbook might be superfluous... we shall see
later in development...

'''

'''data = {1: # stage
		   [	# sequence of events
		    ['squad', ([(BEE, (3, 4)), (BEE, (3, 5)), (BEE, (4, 4)), (BEE, (4, 5))], CURVE1_FROM_MIDTOPR), 
			   		  ([(BUTTERFLY, (1, 4)), (BUTTERFLY, (1, 5)), (BUTTERFLY, (2, 4)), (BUTTERFLY, (2, 5))], CURVE1_FROM_MIDTOPL)],
			['formed']
		   ],
		2: [['nothing']
			]
	   }'''



data = {1: # stage
		   [	# sequence of events
		    ['squad', ([(BEE, (3, 4)), (BEE, (3, 5)), (BEE, (4, 4)), (BEE, (4, 5))], CURVE1_FROM_MIDTOPR), 
			   		  ([(BUTTERFLY, (1, 4)), (BUTTERFLY, (1, 5)), (BUTTERFLY, (2, 4)), (BUTTERFLY, (2, 5))], CURVE1_FROM_MIDTOPL)],
			['squad', ([(GALAGA, (0, 3)), (BUTTERFLY, (1, 3)), (GALAGA, (0, 4)), (BUTTERFLY, (1, 6)),
						(GALAGA, (0, 5)), (BUTTERFLY, (2, 3)), (GALAGA, (0, 6)), (BUTTERFLY, (2, 6))], CURVE1_FROM_LBOTTOM)],
			['squad', ([(BUTTERFLY, (1, 7)), (BUTTERFLY, (1, 1)), (BUTTERFLY, (1, 8)), (BUTTERFLY, (1, 2)),
						(BUTTERFLY, (2, 7)), (BUTTERFLY, (2, 1)), (BUTTERFLY, (2, 8)), (BUTTERFLY, (2, 2))], CURVE1_FROM_RBOTTOM)],
			['squad', ([(BEE, (3, 2)), (BEE, (3, 6)), (BEE, (3, 3)), (BEE, (3, 7)),
					    (BEE, (4, 2)), (BEE, (4, 6)), (BEE, (4, 3)), (BEE, (4, 7))], CURVE1_FROM_MIDTOPR)],
			['squad', ([(BEE, (3, 0)), (BEE, (3, 8)), (BEE, (3, 1)), (BEE, (3, 9)),
						    (BEE, (4, 0)), (BEE, (4, 8)), (BEE, (4, 1)), (BEE, (4, 9))], CURVE1_FROM_MIDTOPL)],
			['formed']
		   ],
		2: [
			['nothing', ]
		   ]
	   }

class Playbook(object):
	def __init__(self, aliens, statusBar):
		self.currentAction = None
		self.timer = 0
		self.cursor = -1
		self.aliens = aliens
		self.statusBar = statusBar
		self.dataset = data[self.statusBar.stage]

	
	def check(self, timePassed):
	
		if self.currentAction is None:
			# New action
			self.cursor += 1
			if self.cursor >= len(self.dataset):
				# finished the stage
				self.statusBar.stage += 1
				self.statusBar.changed = True
				if self.statusBar.stage in data:
					self.dataset = data[self.statusBar.stage]
					self.cursor = 0
				'''else:
					return'''
			
			self.currentAction = self.dataset[self.cursor][0]
			self.log.message('{}, {}'.format(self.statusBar.stage, self.currentAction))
			
			if self.currentAction == 'squad':
				for squad in self.dataset[self.cursor][1:]:
					alienList, typeOfTrajectory = squad	
					#print('alienList', alienList)
					#print('typeOfTrajectory', typeOfTrajectory)				
					self.aliens.createSquadron(alienList, typeOfTrajectory, timePassed)
					
			if self.currentAction == 'nothing':
				print('nothing 1!')
		else:
			# check status of the current action
			if self.currentAction == 'squad':
				# all aliens in formation?
				allInFormation = True
				for alien in reversed(self.aliens.aliens):
					if alien.state != IN_FORMATION:
						allInFormation = False
						break
				if allInFormation:
					self.currentAction = None
			
			elif self.currentAction == 'formed':
				if len(self.aliens.aliens) == 0:
					self.currentAction = None
					
			# temporary: loop back to beginning of playbook
			elif self.currentAction == 'nothing':
				self.currentAction = None
				self.statusBar.stage = 1
				self.dataset = data[self.statusBar.stage]
				self.cursor = -1
				
				print('nothing 2!')
		
		
		

if __name__ == '__main__':
	pb = Playbook()
	for k in data:
		print('key={}, value={}'.format(k, data[k]))