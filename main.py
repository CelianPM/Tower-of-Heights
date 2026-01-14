import pygame, sys
from pygame.locals import *
pygame.init()

HeroVelocity = -21
HeroStrength = 20
# Colors
WHITE = (255, 255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)

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
heroY = 300
hero = pygame.transform.scale(pygame.image.load("Tower Of Heights\hero_with_sword.png").convert_alpha(), (100, 100)) # Load the image of the hero and change the image's size
hero_right = hero # Define the hero's right profile as the usual image
hero_left = pygame.transform.flip(hero, True, False) # Create the hero's othr profile (ht eleft one)

loop_variable = True # game loop variable

# Main game loop
while loop_variable == True:

    pressed  = pygame.key.get_pressed() # To check which key is pressed

    # To quit the game
    
    for event in pygame.event.get():
        if event.type == QUIT or pressed[K_ESCAPE]:
            loop_variable = False

    # To move the square
    if pressed[K_LEFT]:
        hero_right = hero_left
        heroX -= 3
    if pressed[K_RIGHT]:
        hero_right = hero
        heroX += 3
        
    # Jump
    if (pressed[K_SPACE] and HeroVelocity < -HeroStrength) :
      HeroVelocity = HeroStrength
    if HeroVelocity >= -HeroStrength :
          heroY -= HeroVelocity
          HeroVelocity -= 1
        
    # To create walls
    if heroX < 0: heroX = 0
    if heroX > WINDOW_WIDTH: heroX = WINDOW_WIDTH

    WINDOW.fill(WHITE) # To load the window
    WINDOW.blit(hero_right, (heroX, heroY)) # Render the character image
    pygame.display.update()
    fpsClock.tick(FPS)

# To quit the game
pygame.quit()

sys.exit()



