import pygame

pygame.init()


# =================================
# VARIABLES GLOBALES
# =================================

# --- Les couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# --- Pour les touches ---
key = pygame.key.get_pressed()  # Pour quand on appuie sur une touche


# --- Le FPS ---
clock = pygame.time.Clock() # Variable de FPS
FPS = 60                    # Nombre de frames par seconde

# --- Constantes pour la fenetre ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Definit la taille de la fenetre (plein ecran)
WIDTH = screen.get_width()                                   # Largeur de l'ecran
HEIGHT = screen.get_height()                                 # Hauteur de l'ecran
camera_y = 0                                                 # Position verticale de la camera, qui va suivre le joueur quand il monte
CAMERA_SMOOTH = 0.1                                          # Facteur de lissage pour le mouvement de la camera, plus il est eleve, plus la camera suit rapidement le joueur


# --- Variables communes ---
GRAVITY = 0.4      # Vitesse de chute
velocity = 0       # Variable = vitesse de saut - vitesse de chute
on_ground = False  # Contact avec le sol
start_time = 0     # Lorsque le jeu commence, le temps de depart est a 0
PUSHBACK = 30     # La distance de recul quand le joueur ou le monstre est touche
hitbox_display = False

# --- Items & Inventaire ---
INVENTORY_SLOTS = 5
ITEM_USE_HOLD_MS = 1000
