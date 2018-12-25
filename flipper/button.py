#!/usr/bin/python3

import pygame

pygame.init()


class button():
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.ellipse(surface, outline, (self.x - 50, self.y - 23, self.width + 100, self.height + 40), 0)
        else:
            pygame.draw.ellipse(surface, self.color, (self.x - 50, self.y - 23, self.width + 100, self.height + 40), 0)

        if self.text != '':
            font = pygame.font.Font('fonts/07gothic.ttf', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text, (self.x + self.width / 2 - text.get_width() / 2,
                         self.y + self.height /2 - text.get_height() / 2))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                return True
        return False







