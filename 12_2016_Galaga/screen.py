import random
from constants import *



# background, with stars, moving or static
class Backdrop(object):
	def __init__(self):
		self.state = STATIC
		self.stars = {x: ((random.randint(0, VIEWWIDTH) + VIEWPORT.left, random.randint(0, VIEWHEIGHT) + VIEWPORT.top), GREY) for x in range(NR_OF_STARS)}


class Scoreboard(object):
	def __init__(self):
		pass
