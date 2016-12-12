# Constants
from pygame import Rect
from pygame.locals import *


DEBUG = True
FPS = 60


SCREENSIZE = (1024, 768)
CENTER = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2)

''' viewspace TBD '''
VIEWWIDTH  = 500
VIEWHEIGHT = 600 

VIEWPORT = Rect(0, 0, VIEWWIDTH, VIEWHEIGHT)
VIEWPORT.center = CENTER

ALIENSIZE = 24 #VIEWWIDTH // 20
SHIPSIZE = int(ALIENSIZE * 1.2) 

SHIPY = VIEWHEIGHT - SHIPSIZE
VIEWBOUNDS = (SHIPSIZE // 2, VIEWWIDTH - SHIPSIZE // 2) # the bounds within which the ship can move

SHIPSPEED = 200. # in pixels per second, how fast the backdrop moves
MOVESPEED = 500. # for the ship moving sideways

BOLTLENGTH = SHIPSIZE // 2
BOLTWIDTH = 3
BOLTSPEED = 500. # pixels per second

SCOREBOARD = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
SCOREBOARD.midbottom = VIEWPORT.midtop
STATUSBAR = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
STATUSBAR.midtop = VIEWPORT.midbottom

DEBUGWINDOW = Rect(0, 0, (SCREENSIZE[0] - VIEWWIDTH) // 2, SCREENSIZE[1])
DEBUGWINDOW.bottomright = SCREENSIZE

NR_OF_STARS = 50






# key mapping. 
# how to check whether keyboard is azerty or qwerty?
LEFT_KEYS = [K_LEFT, K_q]
RIGHT_KEYS = [K_RIGHT, K_d]
FIRE_KEYS = [K_SPACE, K_j, K_UP]


# Colours
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
#GREY   = ( 64,  64,  64)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
PURPLE = (255,   0, 255)
YELLOW = (255, 255,   0)

GREYS = [(256 / 6 * i, 256 / 6 * i, 256 / 6 * i) for i in range(1, 6)]

# Alien Type
GALAGA    = 1
BEE	   	  = 2
BUTTERFLY = 3




# States
MOVING = 1
STATIC = 2

FORMING        = 3
FORMATION_DONE = 4 

IN_FORMATION = 5
DEAD = 6
