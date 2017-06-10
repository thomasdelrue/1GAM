# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((250, 250), SRCALPHA, 32)


img = pygame.Surface((50, 50), SRCALPHA)
img.fill((0, 0, 0, 0))
pygame.draw.rect(img, (128, 64, 0), (10, 10, 30, 30), 0)
screen.blit(img, (0, 0))
pygame.display.update()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

pygame.image.save(img, "sprite.png")

pygame.quit()

