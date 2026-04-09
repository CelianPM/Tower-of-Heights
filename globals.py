import pygame


# =================================
# VARIABLES GLOBALES
# =================================

# --- Les couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# --- Pour les touches ---
key = None # initialisé plus tard


# --- Pour le FPS ---
clock = None  # Variable de FPS qui sera initialisé plus tard
FPS = 60      # Nombre de frames par seconde


# --- Pour la camera ---
screen = None        # Surface de rendu, initialisee au lancement du jeu
WIDTH = 0            # Largeur de l'ecran
HEIGHT = 0           # Hauteur de l'ecran
camera_y = 0         # Position verticale de la camera, qui va suivre le joueur quand il monte
CAMERA_SMOOTH = 0.1  # Facteur de lissage pour le mouvement de la camera, plus il est eleve, plus la camera suit rapidement le joueur


# --- Variables communes ---
GRAVITY = 0.4           # Vitesse de chute
velocity = 0            # Variable = vitesse de saut - vitesse de chute
on_ground = False       # Contact avec le sol
start_time = 0          # Lorsque le jeu commence, le temps de depart est a 0
PUSHBACK = 30           # La distance de recul quand le joueur ou le monstre est touche
hitbox_display = False  # Affiche les hitboxes des entites
music_muted = False     # Indique si la musique est mise en pause ou non
music_volume = 0.7      # Volume par defaut de la musique

# --- Items & Inventaire ---
INVENTORY_SLOTS = 5      # Nombre de slots d'inventaire disponibles pour le joueur
ITEM_USE_HOLD_MS = 1000  # Temps en millisecondes pour que l'utilisation d'un item soit considere comme un "hold" (maintenir la touche enfoncee)



# =================================
# LISTES GLOBALES
# =================================
platforms = []     # Liste de toutes les plateformes du jeu
traps = []         # Liste de toutes les plateforms traversables du jeu
monsters = []      # Liste de tous les monstres du jeu
items = []         # Liste de tous les items du jeu
rune_machines = [] # Liste de toutes les machines a runes du jeu
wall = []          # Liste de tous les murs du jeu
hazards = []       # Liste de tous les dangers du jeu
arrows = []        # Liste de toutes les fleches du jeu
shurikens = []     # Liste de tous les shurikens du jeu


# =================================
# INITIALISATION DES VARIABLES DE RUNTIME
# =================================

def initialize_runtime():
    """Initialise pygame et les objets runtime partages (ecran, clock, dimensions, clavier)."""
    global screen, WIDTH, HEIGHT, clock, key
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    key = pygame.key.get_pressed()


