import pygame

from game import WINDOW_SIZE, Game

pygame.init()
pygame.display.set_caption('ninja game')
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
pygame.display.set_mode(WINDOW_SIZE, pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

game = Game()
clock = pygame.time.Clock()

while True:
    game.frame()
    game.draw()
    pygame.display.flip()
    clock.tick(60)
