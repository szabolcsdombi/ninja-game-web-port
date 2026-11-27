import sys

import pygame

sys.path.insert(0, '.')

from game import Game

pygame.init()
pygame.display.set_mode((320, 240))

game = Game()
