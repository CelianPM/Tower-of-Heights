import pygame
import globals

pygame.init()


# =================================
# POLICES DE TEXTE
# =================================

title_font = pygame.font.SysFont(None, 100)                               # Police du titre
text_font = pygame.font.SysFont(None, 40)                                 # Police du texte
death_text_font = pygame.font.SysFont("Fonts/youmurdererbb_reg.ttf", 64)  # Police du texte de mort



# =================================
# BOUTONS
# =================================

# --- Celui dans l'ecran de mort pour recommencer ---
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (globals.WIDTH//2 - 150, globals.HEIGHT//2 + 120)


# --- Celui dans l'ecran de mort pour continuer ---
continue_rect = pygame.Rect(0, 255, 200, 60)
continue_rect.center = (globals.WIDTH//2 - 150, globals.HEIGHT//2)


# --- Ceux pour les ameliorations de statistiques ---
    # Vitesse
speed_rect = pygame.Rect(0, 255, 300, 30)
speed_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 8)

    # Vie
vitality_rect = pygame.Rect(0, 255, 300, 30)
vitality_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 9)

    # Puissance
puissance_rect = pygame.Rect(0, 255, 300, 30)
puissance_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 10)

    # Delai d'attaque
attack_delay_rect = pygame.Rect(0,255, 300, 30)
attack_delay_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 11)


# --- Celui dans l'ecran de mort pour arrêter ---
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (globals.WIDTH//2 + 150, globals.HEIGHT//2 + 120)


# --- Ceux pour quand on pause le jeu ---
    # Le rectangle de fond du menu de pause
pause_box = pygame.Rect(globals.WIDTH//2 - 250, globals.HEIGHT//2 - 150, 500, 300)
    
    # Celui pour continuer
continue_button = pygame.Rect(globals.WIDTH//2 - 200, globals.HEIGHT//2 + 40, 180, 60)
    
    # Celui pour arrêter
quit_button = pygame.Rect(globals.WIDTH//2 + 20, globals.HEIGHT//2 + 40, 180, 60)

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(globals.WIDTH//2, 120))