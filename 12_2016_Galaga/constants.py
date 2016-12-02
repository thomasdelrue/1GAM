# Constants
from pygame.locals import *


SCREENSIZE = (1024, 768)

''' viewspace TBD '''

CENTERX = SCREENSIZE[0] // 2
SHIPY = 700

SHIPSIZE = 30


# key mapping. 
# how to check whether keyboard is azerty or qwerty?
LEFT_KEYS = [K_LEFT, K_q]
RIGHT_KEYS = [K_RIGHT, K_d]
FIRE_KEYS = [K_SPACE, K_j]


# Colours
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)


# States
MOVING = 0
STATIC = 1
