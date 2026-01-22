import pygame # Importer la bibliothèque
pygame.init() # Initialiser pygame
pygame.mixer.init()

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"
pygame.mixer.music.load("MusiqueDebase.mp3")
pygame.mixer.music.set_volume(1)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #définit la taille de la fenêtre (plein écran)
screen.fill((40, 40, 55)) #couleur de l'écran 
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

WIDTH = screen.get_width() #constante = largeur de l'écran
HEIGHT = screen.get_height() #constante = hauteur de l'écran
state = "menu_de_début" #le jeu démare sur la fenêtre de menu
player_speed = 5 #vitesse du joueur
GRAVITY = 0.4 #vitesse de chute
velocity = 0 #variable = vitesse de saut - vitesse de chute
jump_power = -15 #puisssance de saut
on_ground = False #contact avec le sol
monster_speed = 2 #vitesse de déplacement des monstres
life = 0
pushback = 50

# Créer les plateformes
plateforms = [
    pygame.Rect(0, HEIGHT - 25, WIDTH, 25),
    pygame.Rect(120, 450, 80, 25),
    pygame.Rect(260, 350, 80, 25),
    pygame.Rect(400, 250, 80, 25),
    pygame.Rect(550, 150, 80, 25),
]

# Pour appeler les images
    # Héros
perso1_image = pygame.image.load("silhouette_épéiste.png").convert_alpha()
perso2_image = pygame.image.load("épéiste_couleur.png").convert_alpha()
perso1_image_attaque = pygame.image.load("épéiste_attaque.png").convert_alpha()

    # Monstre
monster = pygame.transform.scale(pygame.image.load("slug.png").convert_alpha(), (150, 112.5))
monster_right = monster
monster_left = pygame.transform.flip(monster, True, False)
monster_rect = monster.get_rect(topleft = (0, HEIGHT - 130))

# Prend le rect des images
perso1_rect_menu = perso1_image.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
perso2_rect_menu = perso2_image.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))
perso1_attaque_rect = perso1_image_attaque.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))

selected_image = None #image sélectioné, non-définie pour l'instant
image_attack = perso1_image_attaque
image_rect_attack = perso1_rect_menu
perso_rect = None #rect de l'image sélectionné

# Boutons écran de mort
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)

# Pour le texte
title_font = pygame.font.SysFont(None, 100) #caractéristiques du titre
text_font = pygame.font.SysFont(None, 40) #caractéristiques du texte
death_txt_font = pygame.font.SysFont("youmurdererbb_reg.ttf", 64) #caractéristiques du texte de mort

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240)) 
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))

def menu_de_début():
    global state, perso1_rect_menu, perso1_image, selected_image, selected_image_left, selected_image_right, perso_rect, selected_attack_left,  selected_attack_right
    if event.type == pygame.MOUSEBUTTONDOWN:
        if perso1_rect_menu.collidepoint(event.pos):
            selected_image = perso1_image
            selected_image_right = selected_image
            selected_image_left = pygame.transform.flip(selected_image, True, False)
            selected_attack = pygame.image.load("épéiste_attaque.png").convert_alpha()
            selected_attack_right = selected_attack
            selected_attack_left = pygame.transform.flip(selected_attack, True, False)
            perso_rect = selected_image.get_rect(topleft=(200, 300))
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
            state = "game"
            pygame.mixer.music.play(-1)

running = True # Variable du jeu

# Boucle principale
while running:
    clock.tick(60) # FPS

    key = pygame.key.get_pressed() # Pour quand on appuie sur une touche

    # Pour sortir de la fenêtre de jeu
    for event in pygame.event.get():
        # Print text saying "do you want to stop?" then buttons with options yes and no
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]: running = False

        # Pour donner le choix de personnages sur la page menu de départ
        if state == "menu_de_début":
            menu_de_début()
        
        # Pour la page de mort
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect_death.collidepoint(event.pos):
                state = "menu_de_début"
            elif end_rect_death.collidepoint(event.pos):
                state = "end"

    # Pour créer la page du menu de départ
    if state == "menu_de_début":
        screen.fill((30, 30, 45))
        screen.blit(title_surface, title_rect)

        screen.blit(perso1_image, perso1_rect_menu)
        screen.blit(perso2_image, perso2_rect_menu)

        text = text_font.render("Clique sur ton personnage", True, (200, 200, 200))
        info = text_font.render("Appuie sur M pour revenir sur cette page", True, (200, 200, 200))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 120))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT - 80))
        life = 0
        pygame.display.flip() # Pour mettre la fenêtre à jour
        continue

    # Pour jouer
    if state == "game":
    # Pour bouger
        if key[pygame.K_LEFT]: # Aller à gauche
            perso_rect.x += -player_speed
            selected_image = selected_image_left

        if key[pygame.K_RIGHT]: # Aller à droite
            perso_rect.x += player_speed
            selected_image = selected_image_right

        if key[pygame.K_SPACE] and on_ground: # Saut
            velocity += jump_power
            on_ground = False

        if monster_rect.x > perso_rect.x:
            monster_rect.x -= monster_speed
            monster = monster_left
        if monster_rect.x < perso_rect.x:
            monster_rect.x += monster_speed
            monster = monster_right
        
        
        if key[pygame.K_d]:
            selected_image = image_attack

        # Pour redecendre grâce à la gravité
        if not on_ground:
            velocity += GRAVITY

        # Pour rester sur les plateformes
        for plateform in plateforms:
            if perso_rect.colliderect(plateform) and velocity > 0:
                perso_rect.bottom = plateform.top
                on_ground = True
                velocity = 0
                break
        if perso_rect.colliderect(monster_rect):
            life += 1
            if perso_rect.x < monster_rect.x - 20:
                perso_rect.x -= pushback
            elif perso_rect.x > monster_rect.x + 20:
                perso_rect.x += pushback
            if perso_rect.y < monster_rect.y:
                velocity -= 2*velocity
        if life > 5:
            state = "death"
        # Pour revenir au menu de départ
        if key[pygame.K_m]: state = "menu_de_début"

        velocity += GRAVITY
        perso_rect.y += velocity

        on_ground = False
        for plateform in plateforms:
            if perso_rect.colliderect(plateform) and velocity > 0:
                perso_rect.bottom = plateform.top
                on_ground = True
                velocity = 0
                break
        
        # Mort si chute hors écran
        if perso_rect.top > HEIGHT:
            state = "death"
    
    # Pour générer l'écran de mort
    if state == "death":
        screen.fill((0, 0, 0))
        pygame.mixer.music.stop()

        txt = death_txt_font.render("Bienvenue au Royaume des Défunts", True, (150, 20, 40))
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))

        # Bouton REJOUER
        pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)
        txt_restart = text_font.render("Rejouer", True, WHITE)
        screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))

        # Bouton QUITTER
        pygame.draw.rect(screen, (0, 0, 200), end_rect_death)
        txt_end = text_font.render("Quitter", True, WHITE)
        screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))
        life = 0
        pygame.display.flip()
        continue

    # Pour la page de mort
    if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
        if restart_rect_death.collidepoint(event.pos):
            state = "menu_de_début"
        elif end_rect_death.collidepoint(event.pos):
            state = "end"

    # END
    if state == "end":
        screen.fill((0, 0, 100))
        txt = text_font.render("Merci d'avoir joué à Tower Of Heights", True, WHITE)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        pygame. time. wait(3000)
        running = False


    screen.fill((40, 40, 55)) # Pour remplir la fenêtre
    for plateform in plateforms: pygame.draw.rect(screen, (120, 60, 60), plateform) # Pour générer les plateformes
    screen.blit(selected_image, perso_rect) # Pour générer le personnage
    screen.blit(monster, monster_rect)
    pygame.display.flip() # Pour mettre l'ensemble de la fenêtre à jour


pygame.quit() # Pour arrêter le jeu
