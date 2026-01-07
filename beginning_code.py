import pygame, sys
from pygame.locals import *
pygame.init()

# Colors
WHITE = (255, 255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Frames per Second
FPS = 45
fpsClock = pygame.time.Clock()

# Window setup
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tower Of Heights")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    WINDOW.fill(WHITE)
    pygame.display.update()
    fpsClock.tick(FPS)