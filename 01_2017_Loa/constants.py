

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
SCREENSIZE = (WINDOWWIDTH, WINDOWHEIGHT)

BOXSIZE = 60
BOARDSIZE = 8
BOARDWIDTH = BOARDHEIGHT = BOXSIZE * BOARDSIZE
BOARDMARGIN = 10
XMARGIN = (WINDOWWIDTH - BOARDWIDTH) // 2 - BOARDMARGIN
YMARGIN = (WINDOWHEIGHT - BOARDHEIGHT) // 2 - BOARDMARGIN

STONESIZE = BOXSIZE // 5 * 2

FONTSIZE = 18
TEXTPOS = (WINDOWWIDTH // 2, WINDOWHEIGHT - YMARGIN // 2)

FPS = 30

BLACKVAL = -1
WHITEVAL = 1

PLAYER = 'Player'
COMPUTER = 'Computer'

WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
BGCOLOUR = (  0, 124, 255)
BOARDCOLOUR = (64, 192, 255)

P = { BLACKVAL: PLAYER, 
      WHITEVAL: COMPUTER }
PCOLOUR = { BLACKVAL: BLACK, 
            WHITEVAL: WHITE }

hourglass_strings_orig = (
  "oooooooooooooooo",
  " oo          oo ",
  " oo          oo ",
  " oo          oo ",
  "  oo        oo  ",
  "   oo      oo   ",
  "     oo  oo     ",
  "       oo       ",
  "       oo       ",
  "     oo  oo     ",
  "   oo      oo   ",
  "  oo        oo  ",
  " oo          oo ",
  " oo          oo ",
  " oo          oo ",
  "oooooooooooooooo",
)

hourglass_strings = (
  "............... ",
  ".XXXXXXXXXXXXX. ",
  " .X         X.  ",
  " .X         X.  ",
  "  .X X X X X.   ",
  "   .X X X X.    ",
  "    .X X X.     ",
  "      .X.       ",
  "    .X X X.     ",
  "   .X  X  X.    ",
  "  .X   X   X.   ",
  " .X   X X   X.  ",
  " .X XX X XX X.  ",
  ".XXXXXXXXXXXXX. ",
  "............... ",
  "                ",
)


import pygame
_hg_cursor, _hg_mask = pygame.cursors.compile(hourglass_strings)
computer_cursor = ((16, 16), (5, 1), _hg_cursor, _hg_mask)