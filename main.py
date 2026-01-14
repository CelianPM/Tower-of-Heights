import pygame, sys
from pygame.locals import *
pygame.init()


# Colors
WHITE = (255, 255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)


# Frames per Second
FPS = 45
fpsClock = pygame.time.Clock()

# Plateforms
plateforms = [pygame.Rect(0,1050,2000,25), pygame.Rect(120,450,60,25), pygame.Rect(230,375,50,40), pygame.Rect(345,250,80,25), pygame.Rect(460,150,30,25), pygame.Rect(0,0,10,2000)]

# Window setup
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tower Of Heights")


# Load the character and his information
heroX = 50
heroY = 300
HERO_WIDTH = 100
HERO_HEIGHT = 100
hero = pygame.transform.scale(pygame.image.load("Tower Of Heights\hero_with_sword.png").convert_alpha(), (HERO_WIDTH, HERO_HEIGHT)) # Load the image of the hero and change the image's size
hero_right = hero # Define the hero's right profile as the usual image
hero_left = pygame.transform.flip(hero, True, False) # Create the hero's other profile (the left one)
hero_rect = hero.get_rect(topleft=(200,300))

player_speed = 5
gravity = 0.5
velocity = 0
jump_power = -10
on_ground = True


loop_variable = True # game loop variable

# Main game loop
while loop_variable == True:

    pressed  = pygame.key.get_pressed() # To simplify when checking if a key is pressed

    # To quit the game
    for event in pygame.event.get():
        if event.type == QUIT or pressed[K_ESCAPE]:
            loop_variable = False

    # To move the square
    if pressed[K_LEFT]:
        hero_right = hero_left
        heroX -= 4.5
    if pressed[K_RIGHT]:
        hero_right = hero
        heroX += 4.5

    # Update position
    hero_rect.topleft = (heroX, heroY)

    # Celian's
    if pressed[K_SPACE] and on_ground:
        velocity += jump_power
        on_ground = False

    if not on_ground:
        velocity += gravity
    on_ground = False

    for plateform in plateforms:
        if hero_rect.colliderect(plateform) and velocity > 0:
            hero_rect.bottom = plateform.top
            on_ground = True
            velocity = 0
    heroY += velocity
        
    # To create walls
    if heroX < 0: heroX = 0 # Left wall
    if heroX > WINDOW_WIDTH - HERO_WIDTH: heroX = WINDOW_WIDTH - HERO_WIDTH # Right wall

    # To load and update the window, character, shapes and FPS
    WINDOW.fill(WHITE) # To load the window
    for plateform in plateforms:
        pygame.draw.rect(WINDOW,(50, 20, 20), (plateform.x, plateform.y, plateform.width, plateform.height))
    WINDOW.blit(hero_right, (heroX, heroY)) # Render the character image
    pygame.display.update() # To update the window
    fpsClock.tick(FPS) # To set the FPS

# To quit the game
pygame.quit()

sys.exit()
