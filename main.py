import pygame # Importer la bibliothèque
import math
import functions
import globals
import classes

# Initialier pygame
pygame.init()        # Initialiser tous les modules de pygame
pygame.mixer.init()  # Initialiser le module de son de pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights" dans la barre de titre

# ================================
# VARIABLES GLOBALES
# ================================

# --- Pour les bruitages ---
    # Pour la musique de fond
pygame.mixer.music.load("MusiqueDeBase.mp3")  # Télécherger la musique de fond
pygame.mixer.music.set_volume(0.7)            # Régler le volume de la musique de fond à 70%

    # Pour le son du saut
jump_sound = pygame.mixer.Sound("Saut.wav")   # Son très moche qui va changer, mais qui est pour l'instant le son du saut
jump_sound.set_volume(1)                      # Régler le volume du son du saut à 100%

# --- Pour la fenêtre ---
    # L'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Definit la taille de la fenêtre (plein ecran)
screen.fill((40, 40, 55))                                    # Remplir la fenêtre avec une couleur de base

    # Le FPS
clock = pygame.time.Clock() # Variable de FPS

# --- Les couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# --- Constantes pour la fenêtre ---
WIDTH = screen.get_width()    # Largeur de l'ecran
HEIGHT = screen.get_height()  # Hauteur de l'ecran
camera_y = 0                  # Position verticale de la caméra, qui va suivre le joueur quand il monte
CAMERA_SMOOTH = 0.1           # Facteur de lissage pour le mouvement de la caméra, plus il est élevé, plus la caméra suit rapidement le joueur
state = "menu_de_debut" # Le jeu demarre sur la fenêtre de menu

# --- Variables de joueur ---
player_speed = 0     # vitesse du joueur
GRAVITY = 0.4        # vitesse de chute
velocity = 0         # variable = vitesse de saut - vitesse de chute
jump_power = -15     # puisssance de saut
on_ground = False    # contact avec le sol
attack = False       # le héro n'attaque pas encore
direction = "right"  # direction initiale
start_time = 0       # Lorsque le jeu commence, le temps de départ est à 0
attack_delay = 0  # le temps qu'il faut attendre avant de pouvoir rattaquer
max_life = 0             # Nombres de vies de départ
PUSHBACK = 100       # La distance de recul quand le joueur ou le monstre est touché
last_attack_time = 0
attack_animation_time = 0
can_attack = True
level = 0
point_attribut = 0
last_damage_time = 0
regenaration_time = 0
invincibility_time = 1000
degat = 0
puissance = 0

# --- Images et classes---
    # Heros
perso1_image = pygame.image.load("archer-attaque.png").convert_alpha()   # Charger l'image de l'archer
perso2_image = pygame.image.load("epeiste_couleur.png").convert_alpha()  # Charger l'image de l'épéiste

    # Fleche
arrow_img = pygame.image.load("fleche.png").convert_alpha()  # Charger l'image de la flèche
arrow_right = arrow_img                                      # Le profil droit de la flèche est l'image de base
arrow_left = pygame.transform.flip(arrow_img, True, False)   # Le profil gauche de la flèche est l'image de base retournée horizontalement

class Arrow:
    def __init__(self, x, y, direction):
        self.direction = direction  # La direction de la flèche est définie par la direction du joueur au moment du tir, et ne change pas après
        self.speed = 10             # La vitesse de la flèche, qui est constante et ne change pas selon la direction

        if direction == "right":
            self.image = arrow_right  # Le profil droit de la flèche est utilisé si la direction est à droite
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.image = arrow_left  # Le profil gauche de la flèche est utilisé si la direction est à gauche
            self.rect = self.image.get_rect(midright = (x, y))

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed  # La flèche se déplace vers la droite si sa direction est à droite
        else:
            self.rect.x -= self.speed  # La flèche se déplace vers la gauche si sa direction est à gauche
        if self.rect.right < 0 or self.rect.left > WIDTH:  # Si la flèche sort de l'écran, elle est retirée du jeu
            arrows.remove(self)
        for plateform in plateforms:
            if self.rect.colliderect(plateform):
                arrows.remove(self)
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Afficher la flèche à sa position actuelle sur l'écran

    # Monstre
monster_img = pygame.transform.scale(pygame.image.load("slug.png").convert_alpha(), (150, 112.5))  # Charger l'image du monstre et la redimensionner à une taille plus appropriée
monster_right = monster_img                                                                        # Le profil droit du monstre est l'image de base
monster_left = pygame.transform.flip(monster_img, True, False)                                     # Le profil gauche du monstre est l'image de base retournée horizontalement

class Monster:
    def __init__(self, x, y, image_right = None, life = 0, speed = 0, xp_reward = 10):
        self.spawn_x = x                                   # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.spawn_y = y                                   # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.image_right = image_right                   # Le profil droit du monstre est l'image du profil droit
        self.image_left = pygame.transform.flip(image_right, True, False) if image_right else None                     # Le profil gauche du monstre est l'image du profil gauche
        self.image = self.image_right                      # L'image de base du monstre est le profil droit
        self.rect = self.image.get_rect(topleft = (x, y)) if image_right else pygame.Rect(x, y, 50, 50)  # Le rectangle de collision du monstre est basé sur l'image du profil droit, et sa position est définie par les coordonnées x et y
        self.life = life                                      # Le monstre commence avec 3 vies
        self.max_life = life                                  # Le monstre a un maximum de 3 vies, et cette variable est utilisée pour réinitialiser la vie du monstre quand il meurt
        self.alive = True                                  # Le monstre est vivant au début du jeu, et cette variable est utilisée pour déterminer s'il doit être affiché et s'il peut interagir avec le joueur
        self.speed = speed                                     # La vitesse à laquelle le monstre suit le joueur, qui est constante et ne change pas selon la direction
        self.xp_reward = xp_reward                          # Quantité d'XP donnée quand ce monstre est vaincu
    def overlap(self, monsters, horizontal_only = False):
        for other in monsters:
            if other is self or not other.alive or other.__class__ is not self.__class__:
                continue
            if not self.rect.colliderect(other.rect):
                continue

            overlap_x = min(self.rect.right, other.rect.right) - max(self.rect.left, other.rect.left)
            overlap_y = min(self.rect.bottom, other.rect.bottom) - max(self.rect.top, other.rect.top)

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            if horizontal_only or overlap_x < overlap_y:
                push_x = math.ceil(overlap_x / 2)
                if self.rect.centerx < other.rect.centerx:
                    self.rect.x -= push_x
                else:
                    self.rect.x += push_x
            else:
                push_y = math.ceil(overlap_y / 2)
                if self.rect.centery < other.rect.centery:
                    self.rect.y -= push_y
                else:
                    self.rect.y += push_y

    def update(self, player_rect, monsters):
        if not self.alive:
            return                         # Si le monstre n'est pas vivant, il ne fait rien et ne suit pas le joueur
        if self.rect.x > player_rect.x :
            self.rect.x -= self.speed      # Le monstre se déplace vers la gauche si sa position x est plus grande que celle du joueur
            if self.image_left:
                self.image = self.image_left
        elif self.rect.x < player_rect.x:
            self.rect.x += self.speed      # Le monstre se déplace vers la droite si sa position x est plus petite que celle du joueur
            if self.image_right:
                self.image = self.image_right  # Le monstre affiche son profil droit pour se déplacer vers la droite
        
        self.overlap(monsters, horizontal_only = True)
    
    def reset(self):
        self.alive = True                                 # Quand le monstre est réinitialisé, il redevient vivant
        self.life = self.max_life                         # Quand le monstre est réinitialisé, il retrouve sa vie maximale (qui est de 3)
        self.rect.topleft = (self.spawn_x, self.spawn_y)  # Quand le monstre est réinitialisé, il retourne à sa position de spawn

    def draw(self, screen, camera_y = 0):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))  # Afficher le monstre à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra
    
slug_img = pygame.image.load("slug.png").convert_alpha()
slug_img = pygame.transform.scale(slug_img, (150, 112))
bat_img = pygame.image.load("bat.png").convert_alpha()
bat_img = pygame.transform.scale(bat_img, (60, 28))

class Slug(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, 
            y, 
            image_right=slug_img,  # Image spécifique
            life=1500,                # Vie spécifique du Slug
            speed=2,                # Vitesse spécifique du Slug
            xp_reward = 8
        )

class Bat(Monster):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            image_right=bat_img,  # Image spécifique
            life=300,               # Moins de vie qu'un slug
            speed=3,               # Plus rapide qu'un slug
            xp_reward = 2
        )
    def update(self, player_rect, monsters):
        if not self.alive:
            return

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery

        distance = math.sqrt(dx*dx + dy*dy)

        if distance != 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if dx < 0:
            self.image = self.image_left
        else:
            self.image = self.image_right
        
        self.overlap(monsters)

# --- Items / Inventaire ---
INVENTORY_SLOTS = 5
ITEM_USE_HOLD_MS = 1000
slot_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

fiole_vie_img = pygame.transform.scale(pygame.image.load("fiole_vie.png").convert_alpha(), (32, 32))
fiole_puissance_img = pygame.transform.scale(pygame.image.load("fiole_puissance.png").convert_alpha(), (32, 32))
fiole_vitesse_img = pygame.transform.scale(pygame.image.load("fiole_vitesse.png").convert_alpha(), (32, 32))
rune_vie_img = pygame.transform.scale(pygame.image.load("rune_vie.png").convert_alpha(), (32, 32))
rune_puissance_img = pygame.transform.scale(pygame.image.load("rune_puissance.png").convert_alpha(), (32, 32))
rune_vitesse_img = pygame.transform.scale(pygame.image.load("rune_vitesse.png").convert_alpha(), (32, 32))

class Item:
    def __init__(self, name, x, y, image, quantity=1, usable=False, heal_amount=0):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.quantity = quantity
        self.usable = usable
        self.heal_amount = heal_amount


    def draw(self, screen, camera_y=0):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))

# Liste des objets présents dans le monde
items = [
    Item("Potion_vie", 260, 320, fiole_vie_img, quantity=1, usable=True, heal_amount=1),
    Item("Potion_puissance", 550, 120, fiole_puissance_img, quantity=1, usable=True, heal_amount=1),
    Item("Potion_vitesse", 260, 320, fiole_vitesse_img, quantity=1, usable=True, heal_amount=1),
    Item("rune_vie", 550, 120, rune_vie_img, quantity=1, usable=False, heal_amount=0),
    Item("rune_puissance", 260, 320, rune_puissance_img, quantity=1, usable=False, heal_amount=0),
    Item("rune_vitesse", 550, 120, rune_vitesse_img, quantity=1, usable=False, heal_amount=0),
]

# Inventaire limité à 5 slots
inventory = [None] * INVENTORY_SLOTS
slot_hold_start = [None] * INVENTORY_SLOTS
slot_use_lock = [False] * INVENTORY_SLOTS
last_inventory_feedback = ""
last_inventory_feedback_time = 0

# --- Dictionnaires ---
    # Plateformes
plateforms = [
    pygame.Rect(0, HEIGHT - 25, WIDTH, 25),
    pygame.Rect(100, 950, 80, 25),
    pygame.Rect(100, 850, 80, 25),
    pygame.Rect(100, 700, 120, 25),
    pygame.Rect(100, 550, 80, 25),
    pygame.Rect(120, 450, 80, 25),
    pygame.Rect(260, 350, 80, 25),
    pygame.Rect(400, 250, 80, 25),
    pygame.Rect(550, 150, 80, 25),
]

    # Monstres
monsters = [
    Slug(1000, HEIGHT - 130),
    Slug(800, HEIGHT - 130),
    Bat(1000, HEIGHT - 250),
    Bat(1000, HEIGHT - 300)
]

    # Fleches
arrows = []

# --- Variables des personnages ---
perso1_rect_menu = perso1_image.get_rect(center = (WIDTH//2 - 150, HEIGHT//2))  # Rect de l'image de l'archer dans le menu de départ
perso2_rect_menu = perso2_image.get_rect(center = (WIDTH//2 + 150, HEIGHT//2))  # Rect de l'image de l'épéiste dans le menu de départ

selected_image = None         # Image selectionnée, non-definie pour l'instant
selected_image_left = None    # Profil gauche de l'image selectionnée, non-definie pour l'instant
selected_image_right = None   # Profil droit de l'image sélectionnée, non-definie pour l'instant
selected_attack = None        # Image de base de l'attaque, non-definie pour l'instant
selected_attack_left = None   # Profil gauche de l'image attaquant, non-definie pour l'instant
selected_attack_right = None  # Profil droit de l'image attaquant, non-definie pour l'instant
perso_rect = None             # Rect de l'image selectionnée, non-definie pour l'instant
player = None                 # Qui sera le héro, non-definie pour l'instant
hitbox = None                 # Hitbox du personnage ( pour les collisions), non-definie pour l'instant
xp = 0

# --- Polices de texte ---
title_font = pygame.font.SysFont(None, 100)                                         # Police du titre
text_font = pygame.font.SysFont(None, 40)                                           # Police du texte
death_txt_font = pygame.font.SysFont("you-murderer.zip/youmurdererbb_reg.ttf", 64)  # Police du texte de mort

# --- Boutons ---
    # Celui dans l'écran de mort pour recommencer
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

continue_rect = pygame.Rect(0, 255, 200, 60)
continue_rect.center = (WIDTH//2 - 150, HEIGHT//2)

speed_rect = pygame.Rect(0, 255, 300, 30)
speed_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 8)

vitality_rect = pygame.Rect(0, 255, 300, 30)
vitality_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 9)

puissance_rect = pygame.Rect(0, 255, 300, 30)
puissance_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 10)

attack_delay_rect = pygame.Rect(0,255, 300, 30)
attack_delay_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 11)

    # Celui dans l'écran de mort pour arrêter
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)

    # Ceux pour quand on pause le jeu
pause_box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)      # Rectangle dans lquel se situeront les boutons
continue_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 40, 180, 60)  # Celui pour continuer
quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 40, 180, 60)       # Celui pour arrêter

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))


# ===============================
# FONCTIONS
# ===============================

# --- Pour les boutons ---
    # Leur rect
pygame.draw.rect(screen, (200, 0, 0), continue_rect)                         # Dessiner un rectangle rouge pour le bouton de recommencer
pygame.draw.rect(screen, (0, 0, 200), speed_rect)                             # Dessiner un rectangle bleu pour le bouton d'arrêter
pygame.draw.rect(screen, (0, 0, 200), vitality_rect)
pygame.draw.rect(screen, (0, 0, 200), puissance_rect)
pygame.draw.rect(screen, (0, 0, 200), attack_delay_rect)


        # Leur texte
txt_continue = text_font.render("Continuer", True, WHITE)                            # Définir le texte du bouton pour recommencer
txt_speed = text_font.render("vitesse : " + str(player_speed), True, WHITE)                                # Définir le texte du bouton pour arrêter
txt_vitality = text_font.render("vie : " + str(max_life), True, WHITE)
txt_puissance = text_font.render("puissance : " + str(puissance*40//100), True, WHITE)
txt_attack_delay = text_font.render("vitesse d'attaque : " + str((1000 - attack_delay)/50), True, WHITE)

        # Les afficher
screen.blit(txt_continue, txt_continue.get_rect(center=continue_rect.center))  # Afficher le texte du bouton pour recommencer
screen.blit(txt_speed, txt_speed.get_rect(center=speed_rect.center))              # Afficher le texte du bouton pour arrêter
screen.blit(txt_vitality, txt_vitality.get_rect(center=vitality_rect.center))
screen.blit(txt_puissance, txt_puissance.get_rect(center=puissance_rect.center))
screen.blit(txt_attack_delay, txt_attack_delay.get_rect(center=attack_delay_rect.center))
    
pygame.display.flip()  # Tout générer sur la fenêtre

# ===============================
# BOUCLE PRINCIPALE
# ===============================

running = True # Variable du jeu

while running:
    clock.tick(60) # FPS
    time = pygame.time.get_ticks()  # pour relever le temps écoulé depuis le début du jeu (en millisecondes)

    key = pygame.key.get_pressed()  # Pour quand on appuie sur une touche

    for event in pygame.event.get():
        # --- Pour quitter le jeu ---
        if event.type == pygame.QUIT or (state != "game" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False             # Pour sortir du jeu si on clique sur la croix ou si on appuie sur ECHAPE dans les menus

        # --- Pour mettre le jeu en pause ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and state == "game":
            state = "paused"            # Si l'état est celui du jeu et que le joueur appuie sur la touche ECHAPE, alors définir l'état comme étant celui de pause
            pygame.mixer.music.pause()  # Arrêter la musique
        
        # --- Boutons de pause ---
        if state == "paused" and event.type == pygame.MOUSEBUTTONDOWN:
            state = functions.paused(state, event, continue_button, quit_button)  # Si le jeu est mis en pause, faire appel à la fonction paused() pour gérer les interactions avec les boutons de la fenêtre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, attack_delay, attack_animation_time, player_speed, max_life, life, regenaration_time, degat = functions.menu_de_debut(selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, perso1_rect_menu, perso2_rect_menu, perso1_image, perso2_image, event, attack_delay, attack_animation_time, player_speed, max_life, regenaration_time, degat)  # Appeler la fonction menu_de_debut() pour gérer les interactions avec les personnages sur la page du menu de départ, et récupérer les variables mises à jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state, xp, point_attribut, level, inventory, items = functions.death(state, event, restart_rect_death, end_rect_death, xp, point_attribut, level, inventory, items)  # Pour appeler la fonction death() pour gérer les interactions avec les boutons de l'écran de mort, et récupérer les variables mis à jour par cette fonction

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            level, state, player_speed, point_attribut, max_life, regenaration_time, attack_delay, puissance = functions.menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, level, player_speed, point_attribut, max_life, regenaration_time, attack_delay, puissance
)    
    # --- Pause ---
    if state == "paused":
        functions.paused2(screen, pause_box, text_font, continue_button, quit_button, WHITE, BLACK, GREEN, RED)  # Appeler la fonction paused2() pour afficher la fenêtre de pause
        continue
        
    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        functions.menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font, WIDTH, HEIGHT)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de départ
        continue

    # --- Pour jouer ---
    if state == "game":
        start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, camera_y, last_attack_time, last_damage_time, can_attack, xp, level, point_attribut, life, regenaration_time, degat, items, inventory, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time = functions.game(start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, player, monsters, arrows, GRAVITY, jump_power, player_speed, PUSHBACK, camera_y, HEIGHT, time, key, last_attack_time, last_damage_time, attack_delay, attack_animation_time, can_attack, xp, level, point_attribut, life, regenaration_time, degat, puissance, items, inventory, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time)  # Pour appeler la fonction game() pour gérer les mécaniques du jeu, et récupérer les variables mises à jour par cette fonction
    # --- Pour generer l'ecran de mort ---
    if state == "death":
        functions.death2(screen, WIDTH, HEIGHT, restart_rect_death, death_txt_font, WHITE, end_rect_death, monsters)  # Pour appeler la fonction death2() pour afficher l'écran de mort, et récupérer les variables mises à jour par cette fonction
        continue

    if state == "menu_attribut":
        functions.menu_attribut(screen, text_font, WIDTH, HEIGHT, RED, level, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player_speed, point_attribut, max_life, regenaration_time, attack_delay)
        continue

    if state == "end":
        running = functions.end(running, screen, text_font, WIDTH, HEIGHT, WHITE)  # Pour appeler la fonction end() pour afficher l'écran de fin, et récupérer les variables mises à jour par cette fonction
    if perso_rect is None:
        continue                                                         # Si le rect du personnage n'est pas encore défini (c'est-à-dire que le joueur n'a pas encore choisi son personnage), ne rien faire et continuer la boucle principale jusqu'à ce que le joueur choisisse son personnage pour que le rect du personnage soit défini et que le jeu puisse commencer

    # --- Synchronisation image avec la hitbox ---
    if direction == "right":
        perso_rect.x = hitbox.x - 20                                      # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    else:
        perso_rect.x = hitbox.x - (perso_rect.width - hitbox.width - 20)  # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    perso_rect.y = hitbox.y - 10                                          # Synchroniser la position y de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)

    # --- Caméra montante (lissée) + ne pas descendre sous le sol ---
    if hitbox.y >= HEIGHT//2:
        camera_y = 0                                            # Si le personnage est en dessous de la moitié de l'écran en hauteur, la caméra ne descend pas plus bas que le sol (camera_y = 0)
    else:
        target_camera = hitbox.y - HEIGHT//2                    # La position cible de la caméra est calculée pour que le personnage soit toujours à la moitié de l'écran en hauteur, sauf si le personnage est en dessous de cette moitié, auquel cas la caméra ne descend pas plus bas que le sol (camera_y = 0)
        camera_y += (target_camera - camera_y) * CAMERA_SMOOTH  # Pour faire en sorte que la caméra suive le joueur de manière lissée, on calcule la position cible de la caméra en fonction de la position du joueur, et on ajuste progressivement la position actuelle de la caméra vers cette position cible en utilisant un facteur de lissage (CAMERA_SMOOTH)
    
    if state == "game" :
        for arrow in arrows[:]: 
            arrow.update()  # Mettre à jour la position de chaque flèche en fonction de sa direction et de sa vitesse, et retirer les flèches qui sortent de l'écran pour éviter d'avoir trop de flèches inutiles dans la liste des flèches
    
    # --- Générer le jeu ---
    screen.fill((40, 40, 55))                                                                                              # Remplir l'écran avec une couleur de base pour le jeu
    for plateform in plateforms:
        pygame.draw.rect(screen, (120, 60, 60), (plateform.x, plateform.y - camera_y, plateform.width, plateform.height))  # Afficher les plateformes à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    screen.blit(selected_image, (perso_rect.x, perso_rect.y - camera_y))                                                   # Afficher l'image du personnage à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for monster in monsters:
        if monster.alive:
            screen.blit(monster.image, (monster.rect.x, monster.rect.y - camera_y))                                        # Afficher les monstres vivants à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for arrow in arrows:
        screen.blit(arrow.image, (arrow.rect.x, arrow.rect.y - camera_y))                                                  # Afficher les flèches à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    txt = text_font.render("Vie : " + str(life) + "/" + str(max_life), True, WHITE)
    screen.blit(txt, (20, 20))                                                                                                  # Tout générer sur la fenêtre
    for item in items:
        item.draw(screen, camera_y)

    functions.draw_inventory_hud(screen, inventory, slot_hold_start, slot_use_lock, time)
    if time - last_inventory_feedback_time <= 1400 and last_inventory_feedback:
        feedback_text = text_font.render(last_inventory_feedback, True, WHITE)
        screen.blit(feedback_text, (20, 150))

    pygame.display.flip()
pygame.quit()  # Arrêter Pygame et fermer la fenêtre du jeu




# Merci d'avoir lu notre code, nous espérons que vous avez apprécié le jeu et que vous avez trouvé notre code intéressant à lire


""" Tous droits réservés aux développeurs de ce jeu :
        - Célian
        - William
        - Samuel
"""
