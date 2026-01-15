import pygame # Importer la bibliothèque
pygame.init() # Initialiser pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((40, 40, 55))
clock = pygame.time.Clock()

WIDTH = screen.get_width()
HEIGHT = screen.get_height()
state = "menu"
player_speed = 5
GRAVITY = 0.5
velocity = 0
jump_power = -10
on_ground = True

# Créer les plateformes
plateformes = [
    pygame.Rect(0, HEIGHT - 25, WIDTH, 25),
    pygame.Rect(120, 450, 80, 25),
    pygame.Rect(260, 350, 80, 25),
    pygame.Rect(400, 250, 80, 25),
    pygame.Rect(550, 150, 80, 25),
]

# Pour appeler les images
perso1_image = pygame.image.load("silhouette_épéiste.png").convert_alpha()
perso2_image = pygame.image.load("épéiste_couleur.png").convert_alpha()

perso1_rect_menu = perso1_image.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
perso2_rect_menu = perso2_image.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))

selected_image = None
perso_rect = None

# Pour le texte
title_font = pygame.font.SysFont(None, 100)
text_font = pygame.font.SysFont(None, 40)

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))

running = True # Variable du jeu

# Boucle principale
while running == True:
    clock.tick(60) # FPS

    # Pour sortir de la fenêtre de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE: running = False
            
    key = pygame.key.get_pressed() # Pour quand on appuie sur une touche

    # Pour donner le choix de personnages sur la page menu de départ
    if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if perso1_rect_menu.collidepoint(event.pos):
                selected_image = perso1_image
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"

            if perso2_rect_menu.collidepoint(event.pos):
                selected_image = perso2_image
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"

    # Pour créer la page menu de départ
    if state == "menu":
        screen.fill((30, 30, 45))
        screen.blit(title_surface, title_rect)

        screen.blit(perso1_image, perso1_rect_menu)
        screen.blit(perso2_image, perso2_rect_menu)

        txt = text_font.render("Clique sur ton personnage", True, (200, 200, 200))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 120))

        pygame.display.flip() # Pour mettre la fenêtre à jour
        continue
    
    # Pour bouger
    if key[pygame.K_LEFT]: # Aller à gauche
        perso_rect.x -= player_speed
    if key[pygame.K_RIGHT]: # Aller à droite
        perso_rect.x += player_speed
    if key[pygame.K_SPACE] and on_ground: # Saut
        velocity += jump_power
        on_ground = False

    # Pour redecendre grâce à la gravité
    if not on_ground:
        velocity += GRAVITY

    # Pour rester sur les plateformes
    for plateforme in plateformes:
        if perso_rect.colliderect(plateforme) and velocity > 0:
            perso_rect.bottom = plateforme.top
            on_ground = True
            velocity = 0


    perso_rect.y += velocity



    screen.fill((40, 40, 55)) # Pour remplir la fenêtre

    # Pour générer les plateformes
    for plateforme in plateformes: pygame.draw.rect(screen, (120, 60, 60), plateforme)



    screen.blit(selected_image, perso_rect) # Pour générer le personnage

    pygame.display.flip() # Pour mettre l'ensemble de la fenêtre à jour


pygame.quit() # Pour arrêter le jeu
