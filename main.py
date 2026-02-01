import pygame # Importer la bibliothèque

# Initialier pygame
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"

# --- Pour les bruitages ---
    # Pour la musique de fond
pygame.mixer.music.load("MusiqueDeBase.mp3")
pygame.mixer.music.set_volume(0.5)

    # Pour le son du saut
jump_sound = pygame.mixer.Sound("Saut.wav")#son très moche qui va changer
jump_sound.set_volume(1)

# --- Pour la fenêtre ---
    # L'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Definit la taille de la fenêtre (plein ecran)
screen.fill((40, 40, 55))

    # Le FPS
clock = pygame.time.Clock() # Variable de FPS

# --- Les couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Constantes pour la fenêtre
WIDTH = screen.get_width()    # Largeur de l'ecran
HEIGHT = screen.get_height()  # Hauteur de l'ecran
camera_y = 0
CAMERA_SMOOTH = 0.1

state = "menu_de_debut" # Le jeu demare sur la fenêtre de menu

# --- Variables de joueur ---
player_speed = 5     # vitesse du joueur
GRAVITY = 0.4        # vitesse de chute
velocity = 0         # variable = vitesse de saut - vitesse de chute
jump_power = -15     # puisssance de saut
on_ground = False    # contact avec le sol
attack = False       # le héro n'attaque pas encore
direction = "right"  # direction initiale
start_time = 0
attack_delay = 1000  # le temps qu'oil faut attendre avant de pouvoir rattaquer
life = 5             # Nombres de vies de départ
PUSHBACK = 100

# --- Images et classes---
    # Heros
perso1_image = pygame.image.load("archer-attaque.png").convert_alpha()
perso2_image = pygame.image.load("épéiste_couleur.png").convert_alpha()

    # Fleche
arrow_img = pygame.image.load("fleche.png").convert_alpha()
arrow_right = arrow_img
arrow_left = pygame.transform.flip(arrow_img, True, False)

class Arrow:
    def __init__(self, x, y, direction):
        self.direction = direction
        self.speed = 10

        if direction == "right":
            self.image = arrow_right
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.image = arrow_left
            self.rect = self.image.get_rect(midright = (x, y))

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Monstre
monster_img = pygame.transform.scale(pygame.image.load("slug.png").convert_alpha(), (150, 112.5))
monster_right = monster_img
monster_left = pygame.transform.flip(monster_img, True, False)

class Monster:
    def __init__(self, x, y):
        self.image_right = monster_right
        self.image_left = monster_left
        self.image = self.image_right
        self.rect = self.image.get_rect(topleft = (x, y))
        self.life = 3
        self.speed = 2
    
    def update(self, player_rect): # Le monstre suit le joueur
        if self.rect.x > player_rect.x :
            self.rect.x -= self.speed
            self.image = self.image_left
        elif self.rect.x < player_rect.x:
            self.rect.x += self.speed
            self.image = self.image_right
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

# Prend le rect des images
perso1_rect_menu = perso1_image.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
perso2_rect_menu = perso2_image.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))

selected_image = None         # Image selectionnée, non-definie pour l'instant
selected_image_left = None    # Profil gauche de l'image selectionnée, non-definie pour l'instant
selected_image_right = None   # Profil droit de l'image sélectionnée, non-definie pour l'instant
selected_attack_left = None   # Profil gauche de l'image attaquant, non-definie pour l'instant
selected_attack_right = None  # Profil droit de l'image attaquant, non-definie pour l'instant
perso_rect = None             # Rect de l'image selectionnée
player = None                 # Qui sera le héro, ce qui n'est pas encore défini

# Polices de texte
title_font = pygame.font.SysFont(None, 100)  # Police du titre
text_font = pygame.font.SysFont(None, 40)    # Police du texte
death_txt_font = pygame.font.SysFont("you-murderer.zip/youmurdererbb_reg.ttf", 64)  # Police du texte de mort

# --- Boutons écran de mort ---
    # Celui pour recommencer
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

    # Celui pour arrêter
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)


title_surface = title_font.render("Tower of Heights", True, (240, 240, 240)) 
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))

# Pour quand on pause le jeu
pause_box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
continue_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 40, 180, 60)
quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 40, 180, 60)


# ===============================
# FONCTIONS
# ===============================

def paused():
    global state
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if quit_button.collidepoint(event.pos): # Si on appuie sur le bouton pour quitter
        state = "end"                       # Arrêter le jeu

def paused2():
    # Dessiner le rectangle de pause avec la question
    pygame.draw.rect(screen, WHITE, pause_box)     # Pour dessiner un rectangle blanc...
    pygame.draw.rect(screen, BLACK, pause_box, 3)  # ...et sa bordure noire
    screen.blit(text_font.render("Que veux-tu faire ?", True, BLACK), (pause_box.x + 100, pause_box.y + 40)) # Pour afficher le texte

    # Bouton pour continuer
    pygame.draw.rect(screen, GREEN, continue_button)     # Pour dessiner un rectangle vert...
    pygame.draw.rect(screen, BLACK, continue_button, 2)  # ...et sa bordure noire
    screen.blit(text_font.render("Continuer", True, BLACK), (continue_button.x + 20, continue_button.y + 15)) # Pour afficher le texte

    # Bouton pour arrêter
    pygame.draw.rect(screen, RED, quit_button)       # Pour dessiner un rectangle rouge...
    pygame.draw.rect(screen, BLACK, quit_button, 2)  # ...et sa bordure noire
    screen.blit(text_font.render("Quitter", True, BLACK), (quit_button.x + 40, quit_button.y + 15)) # Pour afficher le texte

    pygame.display.flip() # Pour charger la fenêtre

def menu_de_debut():
    global selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, perso_rect, state, player
    
    if perso1_rect_menu.collidepoint(event.pos):
        player = "archer"
        selected_image = perso1_image
        selected_image_right = selected_image
        selected_image_left = pygame.transform.flip(selected_image, True, False)
        selected_attack = pygame.image.load("archer_post_attaque.png").convert_alpha()
        
    if perso2_rect_menu.collidepoint(event.pos):
        player = "swordsman"
        selected_image = perso2_image
        selected_image_right = selected_image
        selected_image_left = pygame.transform.flip(selected_image, True, False)
        selected_attack = pygame.image.load("épéiste_attaque.png").convert_alpha()

    selected_attack_right = selected_attack                                    # Profil droit de l'image attaquant
    selected_attack_left = pygame.transform.flip(selected_attack, True, False) # Profil gauche de l'image attaquant
    perso_rect = selected_image.get_rect(topleft=(200, 300))                   # Rect de l'image
    pygame.mixer.music.play(-1)
    state = "game" # Passer au jeu

def menu_de_debut2():
    
    # --- Remplir l'écran ---
        # Avec la couleur
    screen.fill((30, 30, 45))
    screen.blit(title_surface, title_rect)

        # Générer les personnages
    screen.blit(perso1_image, perso1_rect_menu)
    screen.blit(perso2_image, perso2_rect_menu)

        # Afficher le texte
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))
    revenir_au_menu = text_font.render("Appuie sur M pour revenir sur cette page", True, (200, 200, 200))
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))
    screen.blit(selection, (WIDTH//2 - selection.get_width()//2, HEIGHT - 160))
    screen.blit(revenir_au_menu, (WIDTH//2 - revenir_au_menu.get_width()//2, HEIGHT - 110))
    screen.blit(pour_pauser, (WIDTH//2 - pour_pauser.get_width()//2, HEIGHT - 60))
    pygame.display.flip()

def game():
    global start_time, direction, attack, on_ground, velocity, life, state, selected_image    

    # --- Mouvements du joueur ---
        # Gauche
    if key[pygame.K_LEFT]:
        perso_rect.x -= player_speed
        if direction == "right":
            selected_image = selected_image_left
        direction = "left"

        # Droite
    if key[pygame.K_RIGHT]:
        perso_rect.x += player_speed
        if direction == "left":
            selected_image = selected_image_right
        direction = "right"
    
        # Le saut
    if key[pygame.K_SPACE] and on_ground:
        velocity += jump_power
        on_ground = False
        jump_sound.play()

        # La gravité
    if not on_ground:
        velocity += GRAVITY
    
    # --- Le joueur attaquant ---
        # Attaque
    if key[pygame.K_d] and time - start_time >= attack_delay:
        start_time = pygame.time.get_ticks()
        if direction == "left":
            selected_image = selected_attack_left
        else:
            selected_image = selected_attack_right
        attack = True
        
        # Délai avant la prochaine attaque
    if time - start_time >= 500:
        if direction == "left":
            selected_image = selected_image_left
        else:
            selected_image = selected_image_right
        attack = False

    # --- Collision avec les plateformes ---
    on_ground = False
    for plateform in plateforms:
        if perso_rect.colliderect(plateform) and velocity > 0:
            perso_rect.bottom = plateform.top
            on_ground = True
            velocity = 0
            break

    # --- Monster movement ---
    for monster in monsters:
        monster.update(perso_rect)

    # --- Monster collision ---
    for monster in monsters[:]:
        if perso_rect.colliderect(monster.rect):

            if attack:
                monster.life -= 1

                if perso_rect.x < monster.rect.x:
                    monster.rect.x += PUSHBACK
                else:
                    monster.rect.x -= PUSHBACK

                if monster.life <= 0:
                    monsters.remove(monster)

            else:
                life -= 1

                if perso_rect.x < monster.rect.x:
                    perso_rect.x -= PUSHBACK
                else:
                    perso_rect.x += PUSHBACK

    if life <= 0:
        state = "death"

    if key[pygame.K_m]:
        state = "menu_de_debut"
        pygame.mixer.music.stop()

    perso_rect.y += velocity

    # Caméra montante
    if perso_rect.y < HEIGHT//2 :
        camera_y = HEIGHT//2 - perso_rect.y
    else:
        camera_y = 0

    # --- Death if outside of screen
    if perso_rect.top > HEIGHT:
        state = "death"

def death():
    global state
    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"
    elif end_rect_death.collidepoint(event.pos):
        state = "end"

def death2():
    global screen, txt, WIDTH, HEIGHT, restart_rect_death, txt_end, txt_font, death_txt_font, txt_restart, WHITE, end_rect_death, life
    screen.fill(BLACK)
    pygame.mixer.music.stop()

    txt = death_txt_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))

    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)
    pygame.draw.rect(screen, (0, 0, 200), end_rect_death)

        # Leur texte
    txt_restart = text_font.render("Rejouer", True, WHITE)
    txt_end = text_font.render("Quitter", True, WHITE)
    
        # Les afficher
    screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))
    screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))
    
    life = 5 # Recommencer à 0 avec les 5 vies
    pygame.display.flip() # Tout générer sur la fenêtre

def end():
    global running
    screen.fill((0, 0, 100))
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, WHITE)
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.flip() # Tout générer sur la fenêtre
    pygame.time.wait(2500) # Attendre 2.5 secondes avant de fermer la fenêtre
    running = False # Soritr de la boucle principale


# ===============================
# BOUCLE PRINCIPALE
# ===============================

running = True # Variable du jeu
while running:
    clock.tick(60) # FPS
    time = pygame.time.get_ticks()

    key = pygame.key.get_pressed() # Pour quand on appuie sur une touche

    # Pour sortir de la fenêtre de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT or state != "game" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and state == "game":
            state = "paused"
            pygame.mixer.music.pause() # Arrêter la musique
        
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_d and state == "game":
                if player == "archer":
                    arrows.append(Arrow(perso_rect.centerx, perso_rect.centery, direction))

        # --- Boutons de pause ---
        if state == "paused" and event.type == pygame.MOUSEBUTTONDOWN:
            paused()

        # Pour donner le choix de personnages sur la page menu de depart
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            menu_de_debut()

        # Pour la page de mort
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            death()

    # --- Pause ---
    if state == "paused":
        paused2()
        continue
        
    # Pour creer la page du menu de depart
    if state == "menu_de_debut":
        menu_de_debut2()
        continue

    # Pour jouer
    if state == "game":
        game()

    # Pour generer l'ecran de mort
    if state == "death":
        death2()
        continue

    if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
        if restart_rect_death.collidepoint(event.pos):
            state = "menu_de_debut"
        elif end_rect_death.collidepoint(event.pos):
            state = "end"

    if state == "end":
        end()
    if perso_rect is None:
        continue

    target_camera = perso_rect.y - HEIGHT//2
    camera_y += (target_camera - camera_y) * CAMERA_SMOOTH
    if perso_rect.y > HEIGHT//2 : 
        camera_y = 0
    
    if state == "game" :
        for arrow in arrows[:] : 
            arrow.update()
        
    screen.fill((40, 40, 55))
    for plateform in plateforms:
        pygame.draw.rect(screen, (120, 60, 60), (plateform.x, plateform.y - camera_y, plateform.width, plateform.height))
    screen.blit(selected_image, (perso_rect.x, perso_rect.y - camera_y))
    for monster in monsters:
        screen.blit(monster.image, (monster.rect.x, monster.rect.y - camera_y))
        for arrow in arrows:
            screen.blit(arrow.image, (arrow.rect.x, arrow.rect.y - camera_y))
    pygame.display.flip()

pygame.quit()
