
import pygame # Importer la bibliothèque

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
    def __init__(self, x, y):
        self.spawn_x = x                                   # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.spawn_y = y                                   # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.image_right = monster_right                   # Le profil droit du monstre est l'image du profil droit
        self.image_left = monster_left                     # Le profil gauche du monstre est l'image du profil gauche
        self.image = self.image_right                      # L'image de base du monstre est le profil droit
        self.rect = self.image.get_rect(topleft = (x, y))  # Le rectangle de collision du monstre est basé sur l'image du profil droit, et sa position est définie par les coordonnées x et y
        self.life = 3                                      # Le monstre commence avec 3 vies
        self.max_life = 3                                  # Le monstre a un maximum de 3 vies, et cette variable est utilisée pour réinitialiser la vie du monstre quand il meurt
        self.alive = True                                  # Le monstre est vivant au début du jeu, et cette variable est utilisée pour déterminer s'il doit être affiché et s'il peut interagir avec le joueur
        self.speed = 2                                     # La vitesse à laquelle le monstre suit le joueur, qui est constante et ne change pas selon la direction

    def update(self, player_rect):
        if not self.alive:
            return                         # Si le monstre n'est pas vivant, il ne fait rien et ne suit pas le joueur
        if self.rect.x > player_rect.x :
            self.rect.x -= self.speed      # Le monstre se déplace vers la gauche si sa position x est plus grande que celle du joueur
            self.image = self.image_left   # Le monstre affiche son profil gauche pour se déplacer vers la gauche
        elif self.rect.x < player_rect.x:
            self.rect.x += self.speed      # Le monstre se déplace vers la droite si sa position x est plus petite que celle du joueur
            self.image = self.image_right  # Le monstre affiche son profil droit pour se déplacer vers la droite
    
    def reset(self):
        self.alive = True                                 # Quand le monstre est réinitialisé, il redevient vivant
        self.life = self.max_life                         # Quand le monstre est réinitialisé, il retrouve sa vie maximale (qui est de 3)
        self.rect.topleft = (self.spawn_x, self.spawn_y)  # Quand le monstre est réinitialisé, il retourne à sa position de spawn

    def draw(self, screen, camera_y):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))  # Afficher le monstre à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra


# --- Dictionnaires ---
    # Plateformes
plateforms = [
    pygame.Rect(0, HEIGHT - 25, WIDTH, 25),
    pygame.Rect(100, 950, 80, 25),
    pygame.Rect(100, 850, 80, 25),
    pygame.Rect(100, 700, 80, 25),
    pygame.Rect(100, 550, 80, 25),
    pygame.Rect(120, 450, 80, 25),
    pygame.Rect(260, 350, 80, 25),
    pygame.Rect(400, 250, 80, 25),
    pygame.Rect(550, 150, 80, 25),
]

    # Monstres
monsters = [
    Monster(0, HEIGHT - 130)
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

speed_rect = pygame.Rect(255, 0, 200, 30)
speed_rect.center = (WIDTH//2 + 150, HEIGHT//2)

vitality_rect = pygame.Rect(0, 0, 200, 30)
vitality_rect.center = (WIDTH//2 + 150, HEIGHT//8 * 5)

regenaration_time_rect = pygame.Rect(0, 0, 200, 30)
regenaration_time_rect.center = (WIDTH//2 + 150, HEIGHT//4 * 3)

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

def paused(state, event, continue_button, quit_button):
    """Ggère les clics sur les boutons affichés boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arrêter le jeu
    return state

def paused2(screen, pause_box, text_font, continue_button, quit_button, WHITE, BLACK, GREEN, RED):
    """Affiche les boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    # Dessiner le rectangle de pause avec la question
    pygame.draw.rect(screen, WHITE, pause_box)                                                                # Pour dessiner un rectangle blanc...
    pygame.draw.rect(screen, BLACK, pause_box, 3)                                                             # ...et sa bordure noire
    screen.blit(text_font.render("Que veux-tu faire ?", True, BLACK), (pause_box.x + 100, pause_box.y + 40))  # Pour afficher le texte

    # Bouton pour continuer
    pygame.draw.rect(screen, GREEN, continue_button)                                                           # Pour dessiner un rectangle vert...
    pygame.draw.rect(screen, BLACK, continue_button, 2)                                                        # ...et sa bordure noire
    screen.blit(text_font.render("Continuer", True, BLACK), (continue_button.x + 20, continue_button.y + 15))  # Pour afficher le texte

    # Bouton pour arrêter
    pygame.draw.rect(screen, RED, quit_button)                                                                 # Pour dessiner un rectangle rouge...
    pygame.draw.rect(screen, BLACK, quit_button, 2)                                                            # ...et sa bordure noire
    screen.blit(text_font.render("Quitter", True, BLACK), (quit_button.x + 40, quit_button.y + 15))            # Pour afficher le texte

    pygame.display.flip() # Pour charger la fenêtre

def menu_de_debut(selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, perso1_rect_menu, perso2_rect_menu, perso1_image, perso2_image, event, attack_delay, attack_animation_time, player_speed, max_life, regenaration_time):
    """Se charge de gérer les clics sur les personnages dans le menu de départ, et de définir les variables correspondantes en fonction du personnage choisi"""
    if perso1_rect_menu.collidepoint(event.pos):
        attack_delay = 800                                                                          # Définit le temps entre les attaques pour l'archer, pour qui c'est plus long
        attack_animation_time = 300
        player = "archer"                                                                            # Le joueur choisi est l'archer
        selected_image = perso1_image                                                                # L'image sélectionnée est celle de l'archer
        selected_image_right = selected_image                                                        # Profil droit de l'image sélectionnée
        selected_image_left = pygame.transform.flip(selected_image, True, False)                     # Profil gauche de l'image sélectionnée
        selected_attack = pygame.image.load("archer_post_attaque.png").convert_alpha()               # Télécharge l'image de l'attaque de l'archer
        player_speed = 3
        max_life = 5
        regenaration_time = 20000
    
    if perso2_rect_menu.collidepoint(event.pos):
        attack_delay = 300                                                                          # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
        attack_animation_time = 300
        player = "swordsman"                                                                         # Le joueur choisi est l'épéiste
        selected_image = perso2_image                                                                # L'image sélectionnée est celle de l'épéiste
        selected_image_right = selected_image                                                        # Profil droit de l'image sélectionnée
        selected_image_left = pygame.transform.flip(selected_image, True, False)                     # Profil gauche de l'image sélectionnée
        selected_attack = pygame.image.load("epeiste_attaque.png").convert_alpha()                   # Télécharge l'image de l'attaque de l'épéiste
        player_speed = 4
        max_life = 4
        regenaration_time = 25000

    
    if selected_attack is None:
        return (selected_image, hitbox, selected_image_left,
            selected_image_right, selected_attack_left,
            selected_attack_right, selected_attack,
            perso_rect, state, player,
            attack_delay, attack_animation_time,
            player_speed, max_life, max_life,
            regenaration_time)


    selected_attack_right = selected_attack                                                          # Profil droit de l'image attaquant
    selected_attack_left = pygame.transform.flip(selected_attack, True, False)                       # Profil gauche de l'image attaquant
    perso_rect = selected_image.get_rect(topleft=(200, 300))                                         # Rect de l'image
    hitbox = pygame.Rect(perso_rect.x, perso_rect.y, perso_rect.width - 60, perso_rect.height - 10)  # Hitbox du personnage
    pygame.mixer.music.play(-1)                                                                      # Lancer la musique de fond en boucle
    state = "game"                                                                                   # Passer au jeu
    life = max_life
    return selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, attack_delay, attack_animation_time, player_speed, max_life, life, regenaration_time

def menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font, WIDTH, HEIGHT):
    """Se charge d'afficher le menu de départ, avec les personnages à choisir et les instructions pour jouer"""
    # --- Remplir l'écran ---
        # Avec la couleur
    screen.fill((30, 30, 45))                                                                             # Remplir l'écran avec une couleur de base
    screen.blit(title_surface, title_rect)                                                                # Afficher le texte

        # Générer les personnages
    screen.blit(perso1_image, perso1_rect_menu)                                                           # Afficher l'image de l'archer
    screen.blit(perso2_image, perso2_rect_menu)                                                           # Afficher l'image de l'épéiste

        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                      # Pour définir le texte
    revenir_au_menu = text_font.render("Appuie sur M pour revenir sur cette page", True, (200, 200, 200)) # Pour définir le texte
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))         # Pour définir le texte
    screen.blit(selection, (WIDTH//2 - selection.get_width()//2, HEIGHT - 160))                           # Pour afficher le texte
    screen.blit(revenir_au_menu, (WIDTH//2 - revenir_au_menu.get_width()//2, HEIGHT - 110))               # Pour afficher le texte
    screen.blit(pour_pauser, (WIDTH//2 - pour_pauser.get_width()//2, HEIGHT - 60))                        # Pour afficher le texte
    pygame.display.flip()                                                                                 # Tout générer sur la fenêtre

def game(start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, player, monsters, arrows, GRAVITY, jump_power, player_speed, PUSHBACK, camera_y, HEIGHT, time, key, last_attack_time, last_damage_time, attack_delay, attack_animation_time, can_attack, xp, level, point_attribut, life, regenaration_time):
    """S'occupe de gérer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    # --- Mouvements du joueur ---
        # Gauche
    if key[pygame.K_LEFT]:                         # Si la touche de gauche est appuyée
        hitbox.x -= player_speed                   # Déplacer la hitbox vers la gauche en fonction de la vitesse du joueur
        if direction == "right":
            selected_image = selected_image_left   # Si la direction précédente était à droite, changer l'image sélectionnée par celle du profil gauche
        direction = "left"                         # Mettre à jour la direction comme étant la gauche gauche

        # Droite
    if key[pygame.K_RIGHT]:                        # Si la touche de droite est appuyée
        hitbox.x += player_speed                   # Déplacer la hitbox vers la droite en fonction de la vitesse du joueur
        if direction == "left":
            selected_image = selected_image_right  # Si la direction précédente était à gauche, changer l'image sélectionnée par celle du profil droit
        direction = "right"                        # Mettre à jour la direction comme étant la droite
    
        # Le saut
    if key[pygame.K_SPACE] and on_ground:          # Si la touche de saut est appuyée et que le joueur est au sol
        velocity += jump_power                     # Appliquer la puissance de saut à la variable de vitesse
        on_ground = False                          # Le joueur n'est plus au sol après avoir sauté
        jump_sound.play()                          # Jouer le son du saut

        # La gravité
    if not on_ground:
        velocity += GRAVITY                        # Appliquer la gravité à la variable de vitesse pour faire retomber le joueur quand il n'est pas sur le sol
    
    # --- Le joueur attaquant ---
        # Attaque
    if key[pygame.K_d] and not attack and can_attack and state == "game":         # Si la touche D est appuyée et que le joueur n'est pas déjà en train d'attaquer
        attack = True
        start_time = time        # Enregistrer le temps de début de l'attaque pour gérer le délai entre les attaques
        if direction == "left":
            selected_image = selected_attack_left   # Si la direction est à gauche, changer l'image sélectionnée par celle de l'attaque du profil gauche
        else:
            selected_image = selected_attack_right  # Si la direction est à droite, changer l'image sélectionnée par celle de l'attaque du profil droit
        
        # Tirer une flèche uniquement si le cooldown est terminé
        if player == "archer" and can_attack:
            arrows.append(Arrow(hitbox.centerx, hitbox.centery, direction))
            last_attack_time = time        
                
                # --- Gestion du cooldown de l'archer ---
        if player == "archer" and not can_attack:
            if time - last_attack_time >= attack_delay:
                can_attack = True
        can_attack = False
        # Délai avant la prochaine attaque
    if attack and time - start_time >= attack_animation_time:
        if direction == "left":
            selected_image = selected_image_left    # L'image revient à celle du profil gauche de l'image selectionnée
        else:
            selected_image = selected_image_right   # L'image revient à celle du profil droit de l'image selectionnée
        attack = False                              # Après le délai d'attaque, le joueur n'est plus en train d'attaquer, et son image revient à celle de base
    if time - start_time >= attack_animation_time + attack_delay:
        can_attack = True

        # --- Gestion du cooldown de l'archer ---
    if player == "archer" and not can_attack:
        if time - last_attack_time >= attack_delay:
            can_attack = True  # Cooldown terminé, le joueur peut tirer à nouveau

    # --- Collision avec les plateformes ---
    on_ground = False
    for plateform in plateforms:
        if hitbox.colliderect(plateform):                                   # Si la hitbox du personnage (et donc le personnage) est en collision avec une plateforme

        # Collisions de chaque côté de la plateforme
            if velocity > 0 and hitbox.bottom - velocity <= plateform.top:  # Si le joueur est en train de tomber et que sa hitbox est juste au-dessus de la plateforme
                hitbox.bottom = plateform.top                               # Aligner le bas de la hitbox avec le dessus de la plateforme pour que le joueur puisse marcher dessus
                on_ground = True                                            # Lorsqu'une plateforme est en dessous du joueur, il est au sol
                velocity = 0                                                # La vitesse de chute est réinitialiser à 0 quand le joueur touche une plateforme
            if velocity < 0 and hitbox.top - velocity >= plateform.bottom:  # Si le joueur est en train de sauter et que sa hitbox est juste en dessous de la plateforme
                hitbox.top = plateform.bottom                               # Aligner le haut de la hitbox avec le bas de la plateforme, de sorte à ce que cette plateforme crée un plafond que le joueur ne peut pas traverser en sautant
                velocity = 0                                                # La vitesse de saut est réinitialiser à 0 quand le joueur touche une plateforme par en dessous
            if hitbox.right - player_speed <= plateform.left:               # Si le joueur se déplace vers la droite et que sa hitbox est juste à gauche de la plateforme
                hitbox.right = plateform.left                               # Aligner le côté droit de la hitbox avec le côté gauche de la plateforme, de sorte à ce que cette plateforme crée un mur que le joueur ne peut pas traverser en se déplaçant vers la droite
            if hitbox.left + player_speed >= plateform.right:               # Si le joueur se déplace vers la gauche et que sa hitbox est juste à droite de la plateforme
                hitbox.left = plateform.right                               # Aligner le côté gauche de la hitbox avec le côté droit de la plateforme, de sorte à ce que cette plateforme crée un mur que le joueur ne peut pas traverser en se déplaçant vers la gauche
            

    # --- Monster movement ---
    for monster in monsters:
        if monster.alive:
            monster.update(hitbox)  # Si le monstre est vivant, il suit le joueur en fonction de la position de sa hitbox

    # --- Monster collision ---
    for monster in monsters[:]:
        if monster.alive and hitbox.colliderect(monster.rect):                           # Si le monstre est vivant et que sa hitbox est en collision avec celle du joueur

            if attack:
                if selected_image == selected_attack_left and player == "swordsman":     # Si le joueur attaque vers la gauche avec l'épée
                    if monster.rect.x < hitbox.x:                                        # Si le monstre est à gauche du joueur
                        monster.life -= 1                                                # Le monstre perd une vie
                        monster.rect.x -= PUSHBACK                                       # Le monstre recule
                elif selected_image == selected_attack_right and player == "swordsman":  # Si le joueur attaque vers la droite avec l'épée
                    if monster.rect.x > hitbox.x:                                        # Si le monstre est à droite du joueur
                        monster.life -= 1                                                # Le monstre perd une vie
                        monster.rect.x += PUSHBACK                                       # Le monstre recule
                else:
                    life -= 1                                                            # Si le joueur n'attaque pas du bon côté, le héro perd une vie
                    last_damage_time = time

                if monster.life <= 0:                                                    # Quand le monstre n'a plus de vies
                    monster.alive = False                                                # Il est retiré du jeu
                    xp += 10
                    if level<xp//10:
                        point_attribut += 5
            
            else:                                                                        # Si le joueur n'attaque pas
                life -= 1                                                                # Le héro perd une vie
                last_damage_time = time

                if hitbox.x < monster.rect.x:
                    hitbox.x -= PUSHBACK                                                 # Si le joueur est à gauche du monstre, il recule vers la gauche
                else:
                    hitbox.x += PUSHBACK                                                 # Si le joueur est à droite du monstre, il recule vers la droite
        
        for arrow in arrows[:]:
            if monster.alive and arrow.rect.colliderect(monster.rect):                   # Si la hitbox de la flèche est en collision avec celle du monstre
                monster.life -= 1                                                        # Le monstre perd une vie
                if arrow.direction == "right":
                    monster.rect.x += PUSHBACK                                           # Si la flèche va vers la droite, le monstre recule vers la droite
                else:
                    monster.rect.x -= PUSHBACK                                           # Si la flèche va vers la gauche, le monstre recule vers la gauche
                arrows.remove(arrow)                                                     # Retirer la flèche du jeu
                if monster.life <= 0:
                    monster.alive = False                                                # Quand le monstre n'a plus de vies, il est retiré du jeu
                    xp += 10
                    if level<xp//10:
                        point_attribut += 5
    
    # --- Lorsque le héro n'a plus de vies ---
    if life <= 0:
        state = "death"  # Passer à l'écran de mort

    if time - last_damage_time >= regenaration_time and life < max_life:
        life += 1
        last_damage_time = time

    # --- Pour retourner à la page du départ ---
    if key[pygame.K_m]:
        state = "menu_attribut"    # Passer à l'état correspondant à celui du menu de départ
        pygame.mixer.music.stop()  # Arrêter la musique de fond

    hitbox.y += velocity  # Appliquer la variable de vitesse à la position verticale de la hitbox pour faire sauter ou faire tomber le joueur

    # --- Mort si le personnage est en dehors de l'écran ---
    if hitbox.top > HEIGHT + camera_y:
        state = "death"  # Si le personnage tombe en dessous de l'écran, passer à l'écran de mort

    level = xp // 10

    txt = text_font.render(str(life), True, (250, 0, 0))
    screen.blit(txt, (20, 20))
    
    return start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, camera_y, last_attack_time, last_damage_time, can_attack, xp, level, point_attribut, life, regenaration_time, 

def death(state, event, restart_rect_death, end_rect_death):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
    elif end_rect_death.collidepoint(event.pos):
        state = "end"            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
    return state

def death2(screen, WIDTH, HEIGHT, restart_rect_death, death_txt_font, WHITE, end_rect_death, monsters):
    """S'occupe d'afficher l'écran de mort, avec les boutons pour recommencer ou arrêter le jeu, et de réinitialiser les variables du jeu pour pouvoir recommencer à zéro si le joueur choisit de rejouer"""
    screen.fill(BLACK)         # Remplir l'écran de noir pour l'écran de mort
    pygame.mixer.music.stop()  # Arrêter la musique de fond quand le joueur meurt

    txt = death_txt_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))  # Définir le texte de l'écran de mort
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))                    # Afficher le texte de l'écran de mort

    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)                         # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), end_rect_death)                             # Dessiner un rectangle bleu pour le bouton d'arrêter

        # Leur texte
    txt_restart = text_font.render("Rejouer", True, WHITE)                            # Définir le texte du bouton pour recommencer
    txt_end = text_font.render("Quitter", True, WHITE)                                # Définir le texte du bouton pour arrêter
    
        # Les afficher
    screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))  # Afficher le texte du bouton pour recommencer
    screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))              # Afficher le texte du bouton pour arrêter
    
    
    for monster in monsters:
        monster.reset()    # Faire recommencer à 0 les monstres avec les 3 vies de chaque monstre
    pygame.display.flip()  # Tout générer sur la fenêtre
    

def end(running, screen, text_font, WIDTH, HEIGHT, WHITE):
    """Se charge d'afficher l'écran de fin du jeu, avec un message de remerciement, et de fermer la fenêtre après quelques secondes"""
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base pour l'écran de fin
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, WHITE)  # Définir le texte de l'écran de fin
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//2)))                # Afficher le texte de l'écran de fin
    pygame.display.flip()                                                         # Tout générer sur la fenêtre
    pygame.time.wait(2500)                                                        # Attendre 2.5 secondes avant de fermer la fenêtre
    running = False                                                               # Sortir de la boucle principale
    return running

def menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, regenaration_time_rect, level, player_speed, point_attribut, max_life, regenaration_time):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    if continue_rect.collidepoint(event.pos):
        state = "game"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
        pygame.mixer.music.play()
    elif speed_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
            player_speed = (player_speed * 10 + 1) / 10
    elif vitality_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1
            max_life += 1
    elif regenaration_time_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1
            regenaration_time -= 500
    return level, state, player_speed, point_attribut, max_life, regenaration_time

def menu_attribut(screen, text_font, WIDTH, HEIGHT, RED, level, continue_rect, speed_rect, vitality_rect, regenaration_time_rect, player_speed, point_attribut, max_life, regenaration_time):
   
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base
    txt = text_font.render("ATTRIBUT", True, RED)                                 # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//5)))                # Afficher le texte de l'écran
    txt = text_font.render("level " + str(level), True, WHITE)                                    # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3, HEIGHT//4)))                # Afficher le texte de l'écran
    txt = text_font.render("point(s) d'attribut(s) " + str(point_attribut), True, WHITE)                                    # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3*2, HEIGHT//4)))                # Afficher le texte de l'écran


    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), continue_rect)                         # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), speed_rect)                             # Dessiner un rectangle bleu pour le bouton d'arrêter

        # Leur texte
    txt_continue = text_font.render("Continuer", True, WHITE)                            # Définir le texte du bouton pour recommencer
    txt_speed = text_font.render("vitesse : " + str(player_speed), True, WHITE)                                # Définir le texte du bouton pour arrêter
    txt_vitality = text_font.render("vie : " + str(max_life), True, WHITE)
    txt_regenaration_time = text_font.render("regéneration : " + str((30000 - regenaration_time)/500), True, WHITE)

        # Les afficher
    screen.blit(txt_continue, txt_continue.get_rect(center=continue_rect.center))  # Afficher le texte du bouton pour recommencer
    screen.blit(txt_speed, txt_speed.get_rect(center=speed_rect.center))              # Afficher le texte du bouton pour arrêter
    screen.blit(txt_vitality, txt_vitality.get_rect(center=vitality_rect.center))
    screen.blit(txt_regenaration_time, txt_regenaration_time.get_rect(center=regenaration_time_rect.center))
    
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
            state = paused(state, event, continue_button, quit_button)  # Si le jeu est mis en pause, faire appel à la fonction paused() pour gérer les interactions avec les boutons de la fenêtre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, attack_delay, attack_animation_time, player_speed, max_life, life, regenaration_time = menu_de_debut(selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, perso1_rect_menu, perso2_rect_menu, perso1_image, perso2_image, event, attack_delay, attack_animation_time, player_speed, max_life, regenaration_time)  # Appeler la fonction menu_de_debut() pour gérer les interactions avec les personnages sur la page du menu de départ, et récupérer les variables mises à jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state = death(state, event, restart_rect_death, end_rect_death)  # Pour appeler la fonction death() pour gérer les interactions avec les boutons de l'écran de mort, et récupérer les variables mis à jour par cette fonction

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            level, state, player_speed, point_attribut, max_life, regenaration_time = menu_attribut2(
                state, event,
                continue_rect, speed_rect, regenaration_time_rect, vitality_rect,
                level, player_speed, point_attribut, max_life, regenaration_time
                )
    
    # --- Pause ---
    if state == "paused":
        paused2(screen, pause_box, text_font, continue_button, quit_button, WHITE, BLACK, GREEN, RED)  # Appeler la fonction paused2() pour afficher la fenêtre de pause
        continue
        
    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font, WIDTH, HEIGHT)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de départ
        continue

    # --- Pour jouer ---
    if state == "game":
        start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, camera_y, last_attack_time, last_damage_time, can_attack, xp, level, point_attribut, life, regenaration_time = game(start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, player, monsters, arrows, GRAVITY, jump_power, player_speed, PUSHBACK, camera_y, HEIGHT, time, key, last_attack_time, last_damage_time, attack_delay, attack_animation_time, can_attack, xp, level, point_attribut, life, regenaration_time)  # Pour appeler la fonction game() pour gérer les mécaniques du jeu, et récupérer les variables mises à jour par cette fonction

    # --- Pour generer l'ecran de mort ---
    if state == "death":
        death2(screen, WIDTH, HEIGHT, restart_rect_death, death_txt_font, WHITE, end_rect_death, monsters)  # Pour appeler la fonction death2() pour afficher l'écran de mort, et récupérer les variables mises à jour par cette fonction
        continue

    if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
        if restart_rect_death.collidepoint(event.pos):
            state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
        elif end_rect_death.collidepoint(event.pos):
            state = "end"            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu

    if state == "menu_attribut":
            menu_attribut(screen, text_font, WIDTH, HEIGHT, RED, level, continue_rect, speed_rect, vitality_rect, regenaration_time_rect, player_speed, point_attribut, max_life, regenaration_time)
            continue
    
    if state == "end":
        running = end(running, screen, text_font, WIDTH, HEIGHT, WHITE)  # Pour appeler la fonction end() pour afficher l'écran de fin, et récupérer les variables mises à jour par cette fonction
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
    screen.blit(txt, (20, 20))
    pygame.display.flip()                                                                                                  # Tout générer sur la fenêtre

pygame.quit()  # Arrêter Pygame et fermer la fenêtre du jeu




# Merci d'avoir lu notre code, nous espérons que vous avez apprécié le jeu et que vous avez trouvé notre code intéressant à lire


""" Tous droits réservés aux développeurs de ce jeu :
        - Célian
        - William
        - Samuel
"""
