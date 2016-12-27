# Constants
from pygame import Rect
from pygame.locals import *


DEBUG = True
FPS = 30


SCREENSIZE = (1024, 768)
CENTER = (SCREENSIZE[0] // 2, SCREENSIZE[1] // 2)

''' viewspace TBD '''
VIEWWIDTH  = 500
VIEWHEIGHT = 600 

VIEWPORT = Rect(0, 0, VIEWWIDTH, VIEWHEIGHT)
VIEWPORT.center = CENTER

ALIENSIZE = 24 #VIEWWIDTH // 20
ALIENSPEED = 300.

DISTANCE_BETWEEN = 1.75

SHIPSIZE = int(ALIENSIZE * 1.2) 

SHIPY = VIEWHEIGHT - SHIPSIZE
VIEWBOUNDS = (SHIPSIZE // 2, VIEWWIDTH - SHIPSIZE // 2) # the bounds within which the ship can move

SHIPSPEED = 200. # in pixels per second, how fast the backdrop moves
MOVESPEED = 500. # for the ship moving sideways

BOLTLENGTH = SHIPSIZE // 2
BOLTWIDTH = 3
BOLTSPEED = 600. # pixels per second

SCOREBOARD = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
SCOREBOARD.midbottom = VIEWPORT.midtop
STATUSBAR = Rect(0, 0, VIEWWIDTH, SHIPSIZE)
STATUSBAR.midtop = VIEWPORT.midbottom

DEBUGWINDOW = Rect(0, 0, (SCREENSIZE[0] - VIEWWIDTH) // 2, SCREENSIZE[1])
DEBUGWINDOW.bottomright = SCREENSIZE

NR_OF_STARS = 50

# at what score, the player receives an extra life
EXTRA_LIVES = [30000, 100000]



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
GAMEOVER = -1

MOVING = 1
STATIC = 2

FORMING        = 3
FORMATION_DONE = 4 

IN_FORMATION = 5
DEAD = 6

ENTERING = 7 
DIVING = 8

# Bezier curve datasets
CURVE1_FROM_MIDTOPR = 0
CURVE1_FROM_MIDTOPL = 1
CURVE1_FROM_LBOTTOM = 2
CURVE1_FROM_RBOTTOM = 3
BEE_DIVE_FROM_R = 4
BEE_DIVE_FROM_L = 5


BEZ_CP_SETS = [# CURVE1_FROM_MIDTOPR
               [(300, -50), (400, 125), (-50, 200), (50, 350), (100, 400), (226, 400), (226, 300)],
               # CURVE1_FROM_MIDTOPL
               [(200, -50), (100, 125), (550, 200), (450, 350), (400, 400), (274, 400), (274, 300)],
               # CURVE1_FROM_LBOTTOM
               [(-50, 500), (175, 525), (200, 410), (200, 300), (200, 180), (50, 180), (50, 300),
                (50, 420), (200, 420), (200, 250)],
               # CURVE1_FROM_RBOTTOM
               [(550, 500), (325, 525), (300, 410), (300, 300), (300, 180), (450, 180), (450, 300),
                (450, 420), (300, 420), (300, 250)],
               # BEE_DIVE_FROM_R
               [(402, 288), (402, 253), (462, 243), (452, 308), (432, 428), (212, 408), (222, 528),
                (232, 630), (362, 630), (352, 488)],
               # BEE_DIVE_FROM_L
               [(98, 288), (98, 253), (38, 243), (48, 308), (68, 428), (288, 408), (278, 528),
                (268, 630), (138, 630), (148, 488)],
              ]
