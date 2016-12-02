# Constants
from pygame import Rect
from pygame.locals import *


SCREENSIZE = (1024, 768)

CENTER = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2)

''' viewspace TBD '''
VIEWWIDTH  = 500
VIEWHEIGHT = 600 

VIEWPORT = Rect(0, 0, VIEWWIDTH, VIEWHEIGHT)
VIEWPORT.center = CENTER

SHIPSIZE = VIEWWIDTH // 20
SHIPY = VIEWPORT.y + VIEWHEIGHT - SHIPSIZE
VIEWBOUNDS = (VIEWPORT.left + SHIPSIZE // 2, VIEWPORT.right - SHIPSIZE // 2) # the bounds within which the ship can move
MOVESTEP = SHIPSIZE // 5

BOLTLENGTH = SHIPSIZE // 2
BOLTWIDTH = 3
BOLTSPEED = MOVESTEP

SCOREBOARD = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
SCOREBOARD.midbottom = VIEWPORT.midtop
STATUSBOARD = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
STATUSBOARD.midtop = VIEWPORT.midbottom

NR_OF_STARS = 50






# key mapping. 
# how to check whether keyboard is azerty or qwerty?
LEFT_KEYS = [K_LEFT, K_q]
RIGHT_KEYS = [K_RIGHT, K_d]
FIRE_KEYS = [K_SPACE, K_j, K_UP]


# Colours
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREY  = ( 64,  64,  64)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)



# States
MOVING = 0
STATIC = 1
