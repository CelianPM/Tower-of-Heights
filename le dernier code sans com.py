import pygame
pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tower of Heights")
clock = pygame.time.Clock()

WIDTH = screen.get_width()
HEIGHT = screen.get_height()
state = "menu_de_début"
player_speed = 5
gravité = 0.5
velocité = 0
jump_power = -10
on_ground = False
plateformes = [
    pygame.Rect(0, HEIGHT - 25, WIDTH, 25),
    pygame.Rect(120, 450, 80, 25),
    pygame.Rect(260, 350, 80, 25),
    pygame.Rect(400, 250, 80, 25),
    pygame.Rect(550, 150, 80, 25),
]


perso1_image = pygame.image.load("silhouette_épéiste.png").convert_alpha()
perso2_image = pygame.image.load("épéiste_couleur.png").convert_alpha()


perso1_rect_menu = perso1_image.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
perso2_rect_menu = perso2_image.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))

selected_image = None
perso_rect = None


title_font = pygame.font.SysFont(None, 100)
text_font = pygame.font.SysFont(None, 40)

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))


running = True
while running:
    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False


        if state == "menu_de_début" and event.type == pygame.MOUSEBUTTONDOWN:
            if perso1_rect_menu.collidepoint(event.pos):
                selected_image = perso1_image
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"

            if perso2_rect_menu.collidepoint(event.pos):
                selected_image = perso2_image
                perso_rect = selected_image.get_rect(topleft=(200, 300))
                state = "game"


    if state == "menu_de_début":
        screen.fill((30, 30, 45))
        screen.blit(title_surface, title_rect)

        screen.blit(perso1_image, perso1_rect_menu)
        screen.blit(perso2_image, perso2_rect_menu)

        txt = text_font.render("Clique sur ton personnage", True, (200, 200, 200))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 120))

        pygame.display.flip()
        continue


    key = pygame.key.get_pressed()


    if key[pygame.K_LEFT]:
        perso_rect.x -= player_speed
        if not on_ground:
            perso_rect.x -= player_speed
    if key[pygame.K_RIGHT]:
        perso_rect.x += player_speed
        if not on_ground:
            perso_rect.x += player_speed
    if key[pygame.K_SPACE] and on_ground:
        velocité = jump_power
        on_ground = False
    if key[pygame.K_m]:
        state = "menu_de_début"


    velocité += gravité
    perso_rect.y += velocité


    on_ground = False
    for plateforme in plateformes:
        if perso_rect.colliderect(plateforme) and velocité > 0:
            perso_rect.bottom = plateforme.top
            velocité = 0
            on_ground = True

    
    screen.fill((40, 40, 55))

    for plateforme in plateformes:
        pygame.draw.rect(screen, (120, 60, 60), plateforme)

    screen.blit(selected_image, perso_rect)

    pygame.display.flip()

pygame.quit()
