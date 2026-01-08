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

# Load the character and his information
heroX = 50
heroY = 350
hero = pygame.image.load("Tower Of Heights\pixil-frame-0.png").convert_alpha()

loopvar = True
# Main game loop
while loopvar == True:

    # To quite the game
    for event in pygame.event.get():
        if event.type == QUIT:
            loopvar = False

    # To move the square
    pressed  = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        heroX -= 3
    if pressed[K_RIGHT]:
        heroX += 3

    # Keep the rect object in sync with heroX/heroY
  #  hero.topleft = (heroX, heroY)

    # To create walls
    if heroX < 0: heroX = 0
    # if heroX > WINDOW_WIDTH - rect1Width: heroX = WINDOW_WIDTH - rect1Width

    WINDOW.fill(WHITE) # To load the window
    WINDOW.blit(hero, (heroX, heroY)) # Render the character image
    pygame.display.update()
    fpsClock.tick(FPS)

# To qiut the game
pygame.quit()
sys.exit()