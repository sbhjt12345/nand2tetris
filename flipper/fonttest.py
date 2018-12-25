#!/usr/bin/python3


import pygame, sys, time
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (300, 280)
while True: # main game loop
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj,textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

# pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # pygame.draw.line(DISPLAYSURF, BLUE, (60,60), (120, 60), 4)
    # pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
    # pygame.draw.circle(DISPLAYSURF, BLUE, (300,50), 20, 5)
    #
    # pixObj = pygame.PixelArray(DISPLAYSURF)
    # pixObj[480][380] = BLACK
    # pixObj[482][382] = BLACK
    # pixObj[484][384] = BLACK
    # pixObj[486][386] = BLACK


# DISPLAYSURF.fill(WHITE)
# if direction == 'right':
#     girlx += 5
#     if girlx == 640:
#         direction = 'down'
# elif direction == 'down':
#     girly += 5
#     if girly == 260:
#         direction = 'left'
# elif direction == 'left':
#     girlx -= 5
#     if girlx == 120:
#         direction = 'up'
# elif direction == 'up':
#     girly -= 5
#     if girly == 120:
#         direction = 'right'