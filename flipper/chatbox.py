#!/usr/bin/python3

import pygame

pygame.init()

#
#
#
#
WHITE = (255, 255, 255)

CHATBOX_WIDTH = 1000
CHATBOX_HEIGHT = 200
def draw_chatbox(surface):
    s = pygame.Surface((CHATBOX_WIDTH, CHATBOX_WIDTH))
    s.set_alpha(128)
    s.fill((WHITE))
    surface.blit(s,(10,500))


