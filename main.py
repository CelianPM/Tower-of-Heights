import pygame # Importer la bibliothèque

# Initialier pygame
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"

# Pour le son de fond
pygame.mixer.music.load("MusiqueDeBase.mp3")
pygame.mixer.music.set_volume(0.5)
jump_sound = pygame.mixer.Sound("Saut.wav")#son très moche qui va changer
jump_sound.set_volume(1)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #definit la taille de la fenêtre (plein ecran)
screen.fill((40, 40, 55)) # Couleur de l'ecran 
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Constante pour la fenêtre
WIDTH = screen.get_width() #constante = largeur de l'ecran
HEIGHT = screen.get_height() #constante = hauteur de l'ecran
CAMERA_SMOOTH = 0.1
camera_y = 0

state = "menu_de_debut" #le jeu demare sur la fenêtre de menu

# Variables de mouvement
player_speed = 5 #vitesse du joueur
GRAVITY = 0.4 #vitesse de chute
velocity = 0 #variable = vitesse de saut - vitesse de chute
jump_power = -15 #puisssance de saut
on_ground = False #contact avec le sol
monster_speed = 2 #vitesse de deplacement des monstres
attack = False
direction = "right"
start_time = 0
attack_delay = 1000


life = 5 # Nombres de vies de départ
PUSHBACK = 100

# --- Plateformes ---
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

# --- Images ---

    # Heros
perso1_image = pygame.image.load("archer-attaque.png").convert_alpha()
perso2_image = pygame.image.load("épéiste_couleur.png").convert_alpha()

    # Monstre
monster = pygame.transform.scale(pygame.image.load("slug.png").convert_alpha(), (150, 112.5))
monster_right = monster
monster_left = pygame.transform.flip(monster, True, False)
monster_rect = monster.get_rect(topleft = (0, HEIGHT - 130))

# Prend le rect des images
perso1_rect_menu = perso1_image.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
perso2_rect_menu = perso2_image.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))

selected_image = None # Image selectionnée, non-definie pour l'instant
perso_rect = None # Rect de l'image selectionnée
image_rect_attaque = None

# --- Boutons écran de mort ---
    # Celui pour recommencer
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

    # Celui pour arrêter
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)

# --- Variables de texte ---
title_font = pygame.font.SysFont(None, 100) # Caracteristiques du titre
text_font = pygame.font.SysFont(None, 40) # Caracteristiques du texte
death_txt_font = pygame.font.SysFont("you-murderer.zip/youmurdererbb_reg.ttf", 64) # Caracteristiques du texte de mort

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240)) 
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))

# --- Lorsqu'échape est cliqué ---
pause_box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
continue_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 40, 180, 60)
quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 40, 180, 60)

running = True # Variable du jeu

def paused():
    global continue_button, state, quit_button, running, pause_box, txt, screen, GREEN, BLACK, continue_button, RED, quit_button
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"
        pygame.mixer.music.unpause() # Continuer la musique
    if quit_button.collidepoint(event.pos): # Si on appuie sur le bouton pour quitter
        running = False
def paused2():
# Dessiner le rectangle de pause
    pygame.draw.rect(screen, WHITE, pause_box)
    pygame.draw.rect(screen, BLACK, pause_box, 3)

# Pour poser la question
    txt = text_font.render("Que veux-tu faire ?", True, BLACK)
    screen.blit(txt, (pause_box.x + 100, pause_box.y + 40))

# Bouton pour continuer
    pygame.draw.rect(screen, GREEN, continue_button) # Pour dessiner un rectangle vert...
    pygame.draw.rect(screen, BLACK, continue_button, 2) # ...et sa bordure noire
    screen.blit(text_font.render("Continuer", True, BLACK), (continue_button.x + 20, continue_button.y + 15)) # Pour afficher le texte

# Bouton pour arrêter
    pygame.draw.rect(screen, RED, quit_button) # Pour dessiner un rectangle rouge...
    pygame.draw.rect(screen, BLACK, quit_button, 2) # ...et sa bordure noire
    screen.blit(text_font.render("Quitter", True, BLACK), (quit_button.x + 40, quit_button.y + 15)) # Pour afficher le texte

    pygame.display.flip()

def menu_de_debut():
    global perso1_rect_menu, selected_image, perso1_image, selected_image_right, selected_image_left, selected_attack, selected_attack_right, selected_attack_left, perso_rect, state
    if perso1_rect_menu.collidepoint(event.pos):
        selected_image = perso1_image
        selected_image_right = selected_image
        selected_image_left = pygame.transform.flip(selected_image, True, False)
        selected_attack = pygame.image.load("archer_post_attaque.png").convert_alpha()
        selected_attack_right = selected_attack
        selected_attack_left = pygame.transform.flip(selected_attack, True, False)
        perso_rect = selected_image.get_rect(topleft=(200, 300))
        image_rect_attaque = selected_attack.get_rect(topleft=(200, 300))
        state = "game"
        pygame.mixer.music.play(-1)
    if perso2_rect_menu.collidepoint(event.pos):
        selected_image = perso2_image
        selected_image_right = selected_image
        selected_image_left = pygame.transform.flip(selected_image, True, False)
        selected_attack = pygame.image.load("épéiste_attaque.png").convert_alpha()
        selected_attack_right = selected_attack
        selected_attack_left = pygame.transform.flip(selected_attack, True, False)
        perso_rect = selected_image.get_rect(topleft=(200, 300))
        image_rect_attaque = selected_attack.get_rect(topleft=(200, 300))
        state = "game"
        pygame.mixer.music.play(-1)
def death():
    global restart_rect_death, state, end_rect_death
    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"
    elif end_rect_death.collidepoint(event.pos):
        state = "end"
def menu_de_debut2():
    global screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_rect_menu, text, info, WIDTH, HEIGHT
    screen.fill((30, 30, 45))
    screen.blit(title_surface, title_rect)

    screen.blit(perso1_image, perso1_rect_menu)
    screen.blit(perso2_image, perso2_rect_menu)

    text = text_font.render("Clique sur ton personnage", True, (200, 200, 200))
    info = text_font.render("Appuie sur M pour revenir sur cette page", True, (200, 200, 200))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 120))
    screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT - 80))
    pygame.display.flip()
def game():
    global time, attack_delay, start_time, direction, attack, key, perso_rect, player_speed, selected_image, selected_image_right, selected_image_left, selected_attack_left, selected_attack_right, on_ground, jump_power, velocity, monster_rect, monster_speed, monster_left, monster_right, GRAVITY, plateforms, PUSHBACK, life, state, HEIGHT, monster
    
    if key[pygame.K_LEFT]:
        perso_rect.x -= player_speed
        if direction == "right":
            selected_image = selected_image_left
        direction = "left"

    if key[pygame.K_RIGHT]:
        perso_rect.x += player_speed
        if direction == "left":
            selected_image = selected_image_right
        direction = "right"
    
    if key[pygame.K_d] and time - start_time >= attack_delay:
        start_time = pygame.time.get_ticks()
        if direction == "left":
            selected_image = selected_attack_left
        else:
            selected_image = selected_attack_right
        attack = True
        
    if time - start_time >= 500:
        if direction == "left":
            selected_image = selected_image_left
        else:
            selected_image = selected_image_right
        attack = False


    if key[pygame.K_SPACE] and on_ground:
        velocity += jump_power
        on_ground = False
        jump_sound.play()

    if monster_rect.x > perso_rect.x:
        monster_rect.x -= monster_speed
        monster = monster_left
    if monster_rect.x < perso_rect.x:
        monster_rect.x += monster_speed
        monster = monster_right

    if not on_ground:
        velocity += GRAVITY

    for plateform in plateforms:
        if perso_rect.colliderect(plateform) and velocity > 0:
            perso_rect.bottom = plateform.top
            on_ground = True
            velocity = 0
            break

    if perso_rect.colliderect(monster_rect):
        if attack == True:
            if perso_rect.x < monster_rect.x:
                monster_rect.x += PUSHBACK
            elif perso_rect.x > monster_rect.x:
                monster_rect.x -= PUSHBACK
        else:
            life -= 1
            if perso_rect.x < monster_rect.x - 20:
                perso_rect.x -= PUSHBACK
            elif perso_rect.x > monster_rect.x + 20:
                perso_rect.x += PUSHBACK
            if perso_rect.y < monster_rect.y:
                velocity -= 2*velocity

    if life == 0:
        state = "death"

    if key[pygame.K_m]:
        state = "menu_de_debut"
        pygame.mixer.music.stop()

    perso_rect.y += velocity

    on_ground = False
    for plateform in plateforms:
        if perso_rect.colliderect(plateform) and velocity > 0:
            perso_rect.bottom = plateform.top
            on_ground = True
            velocity = 0
            break

    if perso_rect.top > HEIGHT:
        state = "death"
def death2():
    global screen, txt, WIDTH, HEIGHT, restart_rect_death, txt_end, txt_font, death_txt_font, txt_restart, WHITE, end_rect_death, life
    screen.fill((0, 0, 0))
    pygame.mixer.music.stop()

    txt = death_txt_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
    pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)
    txt_restart = text_font.render("Rejouer", True, WHITE)
    screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))
    pygame.draw.rect(screen, (0, 0, 200), end_rect_death)
    txt_end = text_font.render("Quitter", True, WHITE)
    screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))
    life = 5
    pygame.display.flip()
def end():
    global screen, txt, text_font, WHITE, WIDTH, HEIGHT, running
    screen.fill((0, 0, 100))
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, WHITE)
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.flip()
    pygame.time.wait(2500)
    running = False

# Boucle principale
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
        
    target_camera = perso_rect.y - HEIGHT // 2
    camera_y += (target_camera - camera_y) * CAMERA_SMOOTH
    if perso_rect.y > HEIGHT //2:
        camera_y = 0

    screen.fill((40, 40, 55))
    for plateform in plateforms:
        pygame.draw.rect(screen, (120, 60, 60),(plateform.x, plateform.y - camera_y, plateform.width, plateform.height))
    screen.blit(selected_image, (perso_rect.x, perso_rect.y - camera_y))
    screen.blit(monster, (monster_rect.x, monster_rect.y - camera_y))
    pygame.display.flip()

pygame.quit()
