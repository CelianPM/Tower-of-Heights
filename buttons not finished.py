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
pause_box = pygame.Rect(globals.WIDTH // 2 - 620, globals.HEIGHT // 2 - 340, 1240, 680)
pause_header_box = pygame.Rect(pause_box.x + 30, pause_box.y + 20, pause_box.width - 60, 80)
pause_info_box = pygame.Rect(pause_box.x + 30, pause_box.y + 120, 560, 380)
pause_options_box = pygame.Rect(pause_box.x + 650, pause_box.y + 120, 560, 380)
pause_actions_box = pygame.Rect(pause_box.x + 30, pause_box.y + 520, pause_box.width - 60, 130)

pause_lower_speed_rect = pygame.Rect(pause_options_box.x + 80, pause_options_box.y + 90, 400, 60)
pause_lower_speed_minus_rect = pygame.Rect(pause_lower_speed_rect.x - 65, pause_lower_speed_rect.y, 55, 60)
pause_lower_speed_plus_rect = pygame.Rect(pause_lower_speed_rect.right + 10, pause_lower_speed_rect.y, 55, 60)
pause_hitbox_display_rect = pygame.Rect(pause_options_box.x + 80, pause_options_box.y + 185, 400, 60)
pause_music_toggle_rect = pygame.Rect(pause_options_box.x + 80, pause_options_box.y + 280, 400, 60)

continue_button = pygame.Rect(pause_actions_box.x + 220, pause_actions_box.y + 35, 260, 60)
quit_button = pygame.Rect(pause_actions_box.right - 480, pause_actions_box.y + 35, 260, 60)
