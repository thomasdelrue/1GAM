# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 06:38:03 2017

@author: thomas

an attempt at making a sprite editor

to do:
    - rudimentary gui
    - make sprites
    - save sprites to file, load sprites from file
    - make spritesheets


    - use get_keypressed en get_mousepressed ipv huidig systeem
    voor betere inputafhandeling


    - show coordinate system... mousemotionover canvas displays coordinate in statusbar...

    - Make a spritesheet class...
    
    -- idee van active widget, de active highlighten...
    -- CLI toevoegen, misschien ipv StatusBar - widget, eerder een ConsoleWidget dus
    -- keystrokes contextgevoelig maken dus, met betrekking tot de actieve widget...

"""

from pygame.locals import *
import pygame


WIDTH = 1200
HEIGHT = 750

PIXEL_SIZE = 20
FONT_SIZE = 18

MARGIN = 20

SB_W = 400
SB_H = 20

P_W = PIXEL_SIZE * 2 + MARGIN * 2
P_H = PIXEL_SIZE * 2 + MARGIN * 2

C_SIZE = 16
C_W = C_SIZE * PIXEL_SIZE + MARGIN * 2
C_H = C_SIZE * PIXEL_SIZE + MARGIN * 2

PR_W = C_SIZE + MARGIN * 2
PR_H = C_SIZE + MARGIN * 2

FPS = 30

MB_LEFT = 1
MB_RIGHT = 3

WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
CYAN    = (  0, 160, 160)
MAGENTA = (160,   0, 160)

RED     = (255,   0,   0)
GREY    = (192, 192, 192)


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), SRCALPHA, 32);
        pygame.display.set_caption("Sprite Editor")

        self.clock = pygame.time.Clock()
        self.quitting = False
        
        self.widgets = []
        self.statusBar = StatusBar(SB_W, SB_H)    
        self.addWidget(self.statusBar, (MARGIN, HEIGHT - SB_H - MARGIN))
        
        self.palette = Palette(P_W, P_H)
        self.addWidget(self.palette, (0, HEIGHT - SB_H - MARGIN * 2 - P_H))
        
        self.canvas = Canvas(C_SIZE, C_W, C_H)
        self.addWidget(self.canvas, (MARGIN, MARGIN))
        self.canvas.setPalette(self.palette)

        self.preview = Preview(C_SIZE, PR_W, PR_H)
        self.addWidget(self.preview, (MARGIN, MARGIN * 2 + C_H))
        self.preview.setCanvas(self.canvas)
        
        
    def addWidget(self, widget, pos):
        rect = widget.get_rect()
        rect.topleft = pos
        self.widgets.append((widget, rect))
        self.screen.blit(widget, rect)               
        
        
    def checkForQuitting(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and 
                                      event.key == K_ESCAPE):
                self.quitting = True
            else:
                pygame.event.post(event)
            
        
    def drawScreen(self):
        self.screen.fill(BLACK)
        for w, r in self.widgets:
            w.draw()
            self.screen.blit(w, r)
        

    def run(self):
        mouseClicked = False
        mousePos = None
        mouseButton = None
        
        while not self.quitting:
            
            
            # event handling
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.statusBar.updateText("pos: {} button: {}".format(event.pos, event.button))
                    mouseClicked = True
                    mousePos = event.pos
                    mouseButton = event.button
                elif event.type == MOUSEBUTTONUP:
                    mouseClicked = False
                elif event.type == MOUSEMOTION:
                    mousePos = event.pos
                elif event.type == KEYDOWN:
                    self.statusBar.updateText("key pressed: {}".format(event.key));
                    if event.key == K_s:
                        self.saveImage()
                        self.statusBar.updateText("Image saved");
                    elif event.key == K_o:
                        self.loadImage()                                                
                        self.statusBar.updateText("Image loaded");                        
                    elif event.key == K_c:
                        self.canvas.clear()
                        self.statusBar.updateText("Cleared canvas");                        
                    elif event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                        self.canvas.moveCells(event.key)
                else:
                    pygame.event.post(event)
                    
            self.checkForQuitting()
            
        
            if mouseClicked:
                for w, r in self.widgets:
                    #print("mousePos", mousePos)
                    if r.collidepoint(mousePos):
                        #print("clicked in {}".format(w.__class__.__name__))
                        w.clicked((mousePos[0] - r.x, mousePos[1] - r.y), mouseButton)
                        break
        
            self.drawScreen()
            
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()
        exit()


    def loadImage(self):
        self.canvas.clear()
        
        img = pygame.image.load("sprite.png").convert_alpha()
        w, h = img.get_width(), img.get_height()
        for x in range(w):
            for y in range(h):
                rgba_val = img.get_at((x, y))
                if rgba_val[3] > 0:
                    self.canvas.cells[x][y] = rgba_val
        print("loaded")
                    
    
    
        
    def saveImage(self):
        pygame.image.save(self.preview.subsurface((MARGIN, MARGIN, C_SIZE, C_SIZE)), 
                          "sprite.png")
        print("saved")



class Widget(pygame.Surface):
    def __init__(self, w, h):
        pygame.Surface.__init__(self, (w, h), SRCALPHA)
        self.set_alpha(0)
    
    def clicked(self, pos, button):
        pass
    
    def draw(self):
        pass


class Palette(Widget):
    def __init__(self, w, h):
        Widget.__init__(self, w, h)
        self.colours = [[WHITE, MAGENTA], [CYAN, BLACK]]
        self.border = GREY
        self.highlight = RED
        self.margin = MARGIN
        self.selectedColour = WHITE
    
    def clicked(self, pos, _):
        if pos[0] < self.margin or pos[0] >= self.get_width() - self.margin or pos[1] < self.margin or pos[1] >= self.get_height() - self.margin:
                return
        self.selectedColour = self.colours[(pos[0] - self.margin) // PIXEL_SIZE][(pos[1] - self.margin) // PIXEL_SIZE]
    
    def draw(self):
        self.fill(BLACK)
        for i in range(2):
            for j in range(2):
                pygame.draw.rect(self, self.colours[i][j], 
                                 (self.margin + i * PIXEL_SIZE, self.margin + j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 0)
                pygame.draw.rect(self, self.border if self.selectedColour != self.colours[i][j] else self.highlight, 
                                 (self.margin + i * PIXEL_SIZE, self.margin + j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 
                                 1 if self.selectedColour != self.colours[i][j] else 3)
    
        
    
    
class Canvas(Widget):
    def __init__(self, size, w, h):
        self.size = size
        Widget.__init__(self, w, h)
        self.border = GREY
        self.cells = [[None for j in range(self.size)] for i in range(self.size)]        
        self.palette = None
        
    def clear(self):
        self.cells = [[None for j in range(self.size)] for i in range(self.size)]        

    def clicked(self, pos, button):
        if pos[0] < MARGIN or pos[0] >= self.get_width() - MARGIN or pos[1] < MARGIN or pos[1] >= self.get_height() - MARGIN:
            return
        x, y = (pos[0] - MARGIN) // PIXEL_SIZE, (pos[1] - MARGIN) // PIXEL_SIZE
        if button == MB_LEFT:
            self.cells[x][y] = self.palette.selectedColour
        elif button == MB_RIGHT:
            self.cells[x][y] = None
        
    
    def draw(self):
        self.fill(BLACK)
        pygame.draw.rect(self, self.border, (0, 0, self.get_width(), self.get_height()), 1)
        
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(self, self.border, (MARGIN + i * PIXEL_SIZE, MARGIN + j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 1)
                if self.cells[i][j]:
                    pygame.draw.rect(self, self.cells[i][j], (MARGIN + i * PIXEL_SIZE, MARGIN + j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 0)

    def moveCells(self, direction):
        if direction in (K_LEFT, K_UP):
            start, stop, step = 0, self.size - 1, 1
        else:
            start, stop, step = self.size - 1, 0, -1
        
        if direction in (K_LEFT, K_RIGHT):
            for y in range(self.size):
                for x in range(start, stop, step):
                    self.cells[x][y] = self.cells[x + step][y]
                self.cells[stop][y] = None
        else:
            for x in range(self.size):
                for y in range(start, stop, step):
                    self.cells[x][y] = self.cells[x][y + step]
                self.cells[x][stop] = None
        
                
    def setPalette(self, palette):
        self.palette = palette
        
        

class Preview(Widget):
    def __init__(self, size, w, h):
        self.size = size
        Widget.__init__(self, w, h)
        self.border = GREY
        self.canvas = None
        self.alpha_surface = pygame.Surface((self.get_width(), self.get_height()), SRCALPHA)

        
        
    def draw(self):
        self.fill((0, 0, 0, 0))
        self.alpha_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.alpha_surface, (*self.border, 255), (0, 0, self.get_width(), self.get_height()), 1)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.canvas.cells[i][j]:
                    pygame.Surface.set_at(self.alpha_surface, (MARGIN + i, MARGIN + j), self.canvas.cells[i][j])
        
        self.blit(self.alpha_surface, (0, 0))

    def setCanvas(self, canvas):
        self.canvas = canvas
        
    
class StatusBar(Widget):
    def __init__(self, w, h):
        Widget.__init__(self, w, h)
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.updateText("Hello")

    def draw(self):
        self.fill(BLACK)
        pygame.draw.line(self, RED, (0, 0), (self.get_width(), 0), 1)
        self.blit(self.textSurf, self.textRect)
        
        
    def updateText(self, text):
        self.textSurf = self.font.render(text, True, WHITE)
        self.textRect = self.textSurf.get_rect()
        self.textRect.bottomleft = (MARGIN, self.get_height())

        
        

if __name__ == '__main__':
    app = Application()
    app.run()