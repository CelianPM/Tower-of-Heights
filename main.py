import pygame # Importer la bibliothèque
pygame.init() # Initialiser pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((40, 40, 55))
clock = pygame.time.Clock()

player_speed = 5
GRAVITY = 0.5
velocity = 0
jump_power = -10
on_ground = True

# Créer les plateformes
plateformes = [pygame.Rect(0,1050,2000,25), pygame.Rect(120,450,60,25), pygame.Rect(230,375,50,40), pygame.Rect(345,250,80,25), pygame.Rect(460,150,30,25), pygame.Rect(0,0,10,2000),]

perso1_image = pygame.image.load(r"U:\Tower of Heights\épéiste_couleur.png").convert_alpha()
perso1_rect = perso1_image.get_rect(topleft=(200,300))

alive = True # Variable du jeu

# Boucle principale
while running == True:
    clock.tick(60) # FPS

    # Pour sortir de la fenêtre de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE: running = False
            
    key = pygame.key.get_pressed() # Pour quand on appuie sur une touche

    
    # Pour bouger
    if key[pygame.K_LEFT]:
        perso1_rect.x -= player_speed
    if key[pygame.K_RIGHT]:
        perso1_rect.x += player_speed

    # Pour sauter
    if key[pygame.K_SPACE] and on_ground:
        velocity += jump_power
        on_ground = False

    # Pour redecendre grâce à la gravity
    if not on_ground:
        velocity += gravity

    # Pour rester sur les plateformes
    for plateforme in plateformes:
        if perso1_rect.colliderect(plateforme) and velocity > 0:
            perso1_rect.bottom = plateforme.top
            on_ground = True
            velocity = 0


    perso1_rect.y += velocity



    screen.fill((40, 40, 55)) # Pour remplir la fenêtre

    # Pour générer les plateformes
    for plateforme in plateformes: pygame.draw.rect(screen,(50, 20, 20), (plateforme.x, plateforme.y, plateforme.width, plateforme.height))



    screen.blit(perso1_image, (perso1_rect.x, perso1_rect.y)) # Pour générer le personnage

    pygame.display.flip() # Pour mettre l'ensemble de la fenêtre à jour


pygame.quit() # Pour arrêter le jeu
