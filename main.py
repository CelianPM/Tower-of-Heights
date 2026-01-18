import pygame # Importer la bibliothèque
pygame.init() # Initialiser pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((40, 40, 55))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()
state = "menu_de_début"
player_speed = 5
GRAVITY = 0.5
velocity = 0
jump_power = -10
on_ground = False

# Créer les plateformes
plateforms = [
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

# Boutons écran de mort
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)

# Pour le texte
title_font = pygame.font.SysFont(None, 100)
text_font = pygame.font.SysFont(None, 40)
death_txt_font = pygame.font.SysFont("you-murderer.zip/youmurdererbb_reg.ttf", 64)

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))

running = True # Variable du jeu

# Boucle principale
while running:
    clock.tick(60) # FPS

    key = pygame.key.get_pressed() # Pour quand on appuie sur une touche

    # Pour sortir de la fenêtre de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]: running = False

        # Pour donner le choix de personnages sur la page menu de départ
        if state == "menu_de_début" and event.type == pygame.MOUSEBUTTONDOWN:
            if perso1_rect_menu.collidepoint(event.pos):
                selected_image = perso1_image
                selected_image_right = selected_image
                selected_image_left = pygame.transform.flip(selected_image, True, False)
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"

            if perso2_rect_menu.collidepoint(event.pos):
                selected_image = perso2_image
                selected_image_right = selected_image
                selected_image_left = pygame.transform.flip(selected_image, True, False)
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"
        
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

        pygame.display.flip() # Pour mettre la fenêtre à jour
        continue

    # Pour jouer
    if state == "game":

    # Pour bouger
        if key[pygame.K_LEFT]: # Aller à gauche
            perso_rect.x -= player_speed
            selected_image = selected_image_left
        if key[pygame.K_RIGHT]: # Aller à droite
            perso_rect.x += player_speed
            selected_image = selected_image_right
        if key[pygame.K_SPACE] and on_ground: # Saut
            velocity += jump_power
            on_ground = False

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
        continue


    screen.fill((40, 40, 55)) # Pour remplir la fenêtre
    for plateform in plateforms: pygame.draw.rect(screen, (120, 60, 60), plateform) # Pour générer les plateformes
    screen.blit(selected_image, perso_rect) # Pour générer le personnage
    pygame.display.flip() # Pour mettre l'ensemble de la fenêtre à jour


pygame.quit() # Pour arrêter le jeu
