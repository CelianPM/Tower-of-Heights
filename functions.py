import pygame
import globals, imports, buttons, inventory, classes
from math import floor

pygame.init()



# =================================
# PAUSE
# =================================

# --- Gere les boutons ---
def paused__buttons_manager(state, event, continue_button, quit_button, player):
    """Gere les clics sur les boutons affiches boutons pour continuer ou arreter le jeu lorsqu'il est mis en pause"""
    if buttons.continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        if globals.music_muted:                          # Si la musique est en mode muet, ne pas la reprendre    
            pygame.mixer.music.set_volume(0)              # S'assurer que le volume reste a 0
        else:
            pygame.mixer.music.unpause()            # Continuer la musique
    
    if buttons.quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arreter le jeu
    
    if buttons.pause_lower_speed_minus_rect.collidepoint(event.pos):
        player.speed = max(1, round(player.speed - 0.5, 2))

    if buttons.pause_lower_speed_plus_rect.collidepoint(event.pos):
        player.speed = min(12, round(player.speed + 0.5, 2))

    if buttons.pause_lower_speed_rect.collidepoint(event.pos):
        if player.speed_click == 0:
            player.last_player_speed = player.speed
            player.speed = 4
            player.speed_click = 1
        else:
            player.speed = player.last_player_speed
            player.speed_click = 0

    if buttons.pause_hitbox_display_rect.collidepoint(event.pos):
        globals.hitbox_display = not globals.hitbox_display

    if buttons.pause_music_toggle_rect.collidepoint(event.pos):
        globals.music_muted = not globals.music_muted
        pygame.mixer.music.set_volume(0 if globals.music_muted else 0.7)
    return state

# --- Affiche les boutons ---
def paused__buttons_displayer(screen, pause_box, text_font, continue_button, quit_button, player):
    """Affiche les boutons pour continuer ou arreter le jeu lorsqu'il est mis en pause"""
    pygame.draw.rect(globals.screen, (20, 20, 35), buttons.pause_box)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_box, 3)
    pygame.draw.rect(globals.screen, (35, 35, 60), buttons.pause_header_box)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_header_box, 2)
    globals.screen.blit(buttons.text_font.render("PAUSE - Parametres rapides", True, globals.WHITE), (buttons.pause_header_box.x + 130, buttons.pause_header_box.y + 20))

    pygame.draw.rect(globals.screen, (30, 30, 50), buttons.pause_info_box)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_info_box, 2)
    pygame.draw.rect(globals.screen, (30, 30, 50), buttons.pause_options_box)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_options_box, 2)
    pygame.draw.rect(globals.screen, (30, 30, 50), buttons.pause_actions_box)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_actions_box, 2)

    lines = [
        "Touches:",
        "Saut = SPACE",
        "Bouger = LEFT / RIGHT",
        "Attaque principale = D",
        "Ramasser objet = E",
        "Machine a runes = R",
        "Menu attributs = M",
        "Pause = ESC",
        "Objets: maintenir 1..5 = utiliser",
        "Shift + 1..5 = jeter",
    ]
    for i, text in enumerate(lines):
        globals.screen.blit(buttons.text_font.render(text, True, globals.WHITE), (buttons.pause_info_box.x + 20, buttons.pause_info_box.y + 20 + i * 30))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.pause_lower_speed_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_lower_speed_rect, 2)
    pygame.draw.rect(globals.screen, (120, 20, 20), buttons.pause_lower_speed_minus_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_lower_speed_minus_rect, 2)
    pygame.draw.rect(globals.screen, (20, 120, 20), buttons.pause_lower_speed_plus_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_lower_speed_plus_rect, 2)
    globals.screen.blit(buttons.text_font.render(f"Lower speed: {player.speed}", True, globals.WHITE), (buttons.pause_lower_speed_rect.x + 90, buttons.pause_lower_speed_rect.y + 15))
    globals.screen.blit(buttons.text_font.render("-", True, globals.WHITE), (buttons.pause_lower_speed_minus_rect.x + 22, buttons.pause_lower_speed_minus_rect.y + 15))
    globals.screen.blit(buttons.text_font.render("+", True, globals.WHITE), (buttons.pause_lower_speed_plus_rect.x + 19, buttons.pause_lower_speed_plus_rect.y + 14))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.pause_hitbox_display_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_hitbox_display_rect, 2)
    globals.screen.blit(buttons.text_font.render("Hitbox: ON" if globals.hitbox_display else "Hitbox: OFF", True, globals.WHITE), (buttons.pause_hitbox_display_rect.x + 20, buttons.pause_hitbox_display_rect.y + 15))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.pause_music_toggle_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_music_toggle_rect, 2)
    globals.screen.blit(buttons.text_font.render("Musique: OFF" if globals.music_muted else "Musique: ON", True, globals.WHITE), (buttons.pause_music_toggle_rect.x + 20, buttons.pause_music_toggle_rect.y + 15))

    pygame.draw.rect(globals.screen, globals.GREEN, buttons.continue_button)
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.continue_button, 2)
    globals.screen.blit(buttons.text_font.render("Continuer", True, globals.BLACK), (buttons.continue_button.x + 55, buttons.continue_button.y + 15))

    pygame.draw.rect(globals.screen, globals.RED, buttons.quit_button)
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.quit_button, 2)
    globals.screen.blit(buttons.text_font.render("Quitter", True, globals.BLACK), (buttons.quit_button.x + 80, buttons.quit_button.y + 15))
    pygame.display.flip() # Pour charger la fenetre


# =================================
# MACHINE A RUNES
# =================================
def rune_menu__displayer(screen, inventory_list, machine, rune_hold_start, rune_use_lock, current_time):
    box = pygame.Rect(globals.WIDTH//2 - 260, globals.HEIGHT//2 - 170, 520, 340)
    pygame.draw.rect(screen, globals.WHITE, box)
    pygame.draw.rect(screen, globals.BLACK, box, 3)

    title = buttons.text_font.render("Choisis une rune a utiliser", True, globals.BLACK)
    screen.blit(title, (box.x + 40, box.y + 30))

    counts = machine.available_runes(inventory_list) if machine else {
        "rune_vie": 0,
        "rune_vitesse": 0,
        "rune_puissance": 0,
    }
    lines = [
        (f"1 - Rune de vie ({counts['rune_vie']})", 0),
        (f"2 - Rune de vitesse ({counts['rune_vitesse']})", 1),
        (f"3 - Rune de puissance ({counts['rune_puissance']})", 2),
        ("ECHAP - fermer", None),
    ]

    for i, (text, rune_index) in enumerate(lines):
        line = buttons.text_font.render(text, True, globals.BLACK)
        screen.blit(line, (box.x + 40, box.y + 90 + i * 45))

        if rune_index is not None and rune_hold_start[rune_index] is not None and not rune_use_lock[rune_index]:
            progress = (current_time - rune_hold_start[rune_index]) / globals.ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(box.x + 360, box.y + 110 + i * 45, 120, 6)
            bar_fill = pygame.Rect(box.x + 360, box.y + 110 + i * 45, int(120 * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, globals.GREEN, bar_fill)

    pygame.display.flip()

def rune_menu__manager(state, event, inventory_list, player, machine, time, key, rune_hold_start, rune_use_lock):
    if event and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        for i in range(3):
            rune_hold_start[i] = None
            rune_use_lock[i] = False
        return "game", ""

    key_map = {
        0: (pygame.K_1, "rune_vie"),
        1: (pygame.K_2, "rune_vitesse"),
        2: (pygame.K_3, "rune_puissance"),
    }

    held_index = None
    for i, (key_code, _) in key_map.items():
        if key[key_code]:
            held_index = i
            break
    
    # Reset other holds
    for i in range(3):
        if i != held_index:
            rune_hold_start[i] = None
            rune_use_lock[i] = False
    
    if held_index is None:
        return state, ""
    
    key_code, rune_name = key_map[held_index]

    if rune_hold_start[held_index] is None:
        rune_hold_start[held_index] = time
        rune_use_lock[held_index] = False

    if not rune_use_lock[held_index] and (time - rune_hold_start[held_index] >= globals.ITEM_USE_HOLD_MS):
        if machine and machine.consume_rune(inventory_list, rune_name):
            player.apply_rune_effect(rune_name)
            rune_use_lock[held_index] = True
            print("game", f"{rune_name} utilise")

        rune_use_lock[held_index] = True
        return state, "Pas de rune a utiliser"

    return state, ""



# =================================
# MENU DE DEPART
# =================================

# --- Gere les boutons ---
def beginning_menu__manager(state, archer_menu_rect, swordsman_menu_rect, ninja_menu_rect, beggar_menu_rect, event, player, offset_x):
    """Se charge de gerer les clics sur les personnages dans le menu de depart, et de definir les variables correspondantes en fonction du personnage choisi"""
    if imports.archer_menu_rect.collidepoint(event.pos):
        player.hero = "archer"     # Le joueur choisi est l'archer
    
    if imports.swordsman_menu_rect.collidepoint(event.pos):
        player.hero = "swordsman"  # Le joueur choisi est l'epeiste
    
    if imports.ninja_menu_rect.collidepoint(event.pos):
        player.hero = "ninja"      # Le joueur choisi est le ninja

    if imports.beggar_menu_rect.collidepoint(event.pos):
        player.hero = "beggar"     # Le joueur choisi est le mendiant

    if player.hero is not None:
        player.select_the_player()

    if player.selected_attack is None:
        return state, player

    player.selected_attack_right = player.selected_attack                                                                               # Profil droit de l'image attaquant
    player.selected_attack_left = pygame.transform.flip(player.selected_attack, True, False)                                            # Profil gauche de l'image attaquant
    player.perso_rect = player.selected_image.get_rect(topleft=(200 + offset_x // 2, 300))                                                              # Rect de l'image
    player.hitbox = pygame.Rect(player.perso_rect.x, player.perso_rect.y, 32, 112)
    pygame.mixer.music.play(-1)                                                                                                         # Lancer la musique de fond en boucle
    state = "game"                                                                                                                      # Passer au jeu
    player.life = floor(player.max_life)
    player.velocity = 0
    return state, player

# --- Affiche les boutons ---
def beginning_menu__displayer(screen, title_surface, title_rect, archer_image, archer_menu_rect, swordsman_image, swordsman_menu_rect, ninja_image, ninja_menu_rect, text_font):
    """Se charge d'afficher le menu de depart, avec les personnages a choisir et les instructions pour jouer"""
    # --- Remplir l'ecran ---
        # Avec la couleur
    screen.fill((30, 30, 45))               # Remplir l'ecran avec une couleur de base
    screen.blit(title_surface, title_rect)  # Afficher le texte

        # Generer les personnages
    screen.blit(imports.archer_image, imports.archer_menu_rect)        # Afficher l'image de l'archer
    screen.blit(imports.swordsman_image, imports.swordsman_menu_rect)  # Afficher l'image de l'epeiste
    screen.blit(imports.ninja_image, imports.ninja_menu_rect)          # Afficher l'image du ninja
    screen.blit(imports.beggar_image, imports.beggar_menu_rect)
    
        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                # Pour definir le texte
    pour_pauser = text_font.render("Appuie sur ESC pour mettre le jeu en pause", True, (200, 200, 200))   # Pour definir le texte
    screen.blit(selection, (globals.WIDTH//2 - selection.get_width()//2, globals.HEIGHT - 160))     # Pour afficher le texte
    screen.blit(pour_pauser, (globals.WIDTH//2 - pour_pauser.get_width()//2, globals.HEIGHT - 60))  # Pour afficher le texte
    pygame.display.flip()                                                                           # Tout generer sur la fenetre



# =================================
# JEU
# =================================
def game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed, platforms, traps, shurikens, hazards):
    """S'occupe de gerer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    
    velocity, start_time = player.move(imports.jump_sound, state, time, key, velocity, start_time, arrows, shurikens)
    velocity = player.platform_collisions(platforms, traps, velocity)
    player.monster_collisions(monsters, time, arrows, platforms, shurikens)
    player.hazard_collisions(hazards, time)
    player.player_xp()
    items, inventory_list, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed = player.player_inventory(items, inventory_list, key, time, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed)
    state = player.player_death(time, camera_y,state)
    current_time = time

    # --- Gestion du cooldown de l'archer ---
    if player.hero in ("archer", "ninja") and not player.can_attack:
        if time - player.last_attack_time >= player.attack_delay:
            player.can_attack = True  # Cooldown termine, le joueur peut tirer a nouveau


    # --- Monster movement ---
    monster_platforms = platforms + traps + [hazard.rect for hazard in hazards]
    for monster in monsters:
        if monster.alive:
            monster.update(player.hitbox, monsters, monster_platforms)  # Si le monstre est vivant, il suit le joueur en fonction de la position de sa hitbox

    # --- Pour retourner a la page du depart ---
    if key[pygame.K_m]:
        state = "menu_attribut"    # Passer a l'etat correspondant a celui du menu de depart
        pygame.mixer.music.stop()  # Arreter la musique de fond
    
    
    # --- Utilisation des slots (maintenir 1..5 pendant 1s) ---
    for slot_index, key_code in enumerate(inventory.slot_keys):
        if globals.key[key_code]:
            if slot_hold_start[slot_index] is None:
                slot_hold_start[slot_index] = time
                slot_use_lock[slot_index] = False

            if not slot_use_lock[slot_index] and (time - slot_hold_start[slot_index] >= globals.ITEM_USE_HOLD_MS):
                last_inventory_feedback = inventory.use_inventory_slot(inventory_list, slot_index, player, current_time)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True
        else:
            slot_hold_start[slot_index] = None
            slot_use_lock[slot_index] = False

    # --- Jet d'objet (Shift + 1..5) ---
    if globals.key[pygame.K_LSHIFT] or globals.key[pygame.K_RSHIFT]:
        for slot_index, key_code in enumerate(inventory.slot_keys):
            if globals.key[key_code] and not slot_use_lock[slot_index]:
                dropped_x = player.hitbox.centerx + 25
                dropped_y = player.hitbox.bottom - 20
                last_inventory_feedback = inventory.drop_inventory_slot(inventory_list, slot_index, items, dropped_x, dropped_y)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True

    return velocity, state, player, start_time, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed


# --- Musique de fond ---
def background_music():
    pygame.mixer.music.load("Sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)



# =================================
# MORT DU JOUEUR
# =================================
def death__manager(state, event, restart_rect_death, end_rect_death, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, map_design, create_world_from_map):
    """Se charge de gerer les clics sur les boutons pour recommencer ou arreter le jeu lorsqu'on est sur l'ecran de mort"""

    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner a l'etat du menu de depart
    elif end_rect_death.collidepoint(event.pos):
        state = "end"            # Si le joueur clique sur le bouton pour arreter, passer a l'etat de fin du jeu
    player.xp = 0
    player.level = 0
    player.point_attribut = 0
    player.puissance = 0
    inventory_list = [None] * globals.INVENTORY_SLOTS
    slot_hold_start = [None] * globals.INVENTORY_SLOTS
    slot_use_lock = [False] * globals.INVENTORY_SLOTS
    last_inventory_feedback = ""
    last_inventory_feedback_time = 0
    player.speed_bonus = 0
    player.power_bonus = 0
    player.regeneration_bonus = False
    player.speed_effect_end_time = 0
    player.power_effect_end_time = 0
    player.regeneration_effect_end_time = 0
    player.attack = False
    player.can_attack = True
    globals.arrows.clear()
    globals.shurikens.clear()

    _, _, classes.monsters, items, classes.rune_machines, _, classes.hazards, _ = create_world_from_map(map_design)

    return state, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time

def death__displayer(screen, restart_rect_death, death_text_font, end_rect_death, monsters):
    """S'occupe d'afficher l'ecran de mort, avec les boutons pour recommencer ou arreter le jeu, et de reinitialiser les variables du jeu pour pouvoir recommencer a zero si le joueur choisit de rejouer"""
    globals.screen.fill(globals.BLACK)  # Remplir l'ecran de noir pour l'ecran de mort
    pygame.mixer.music.stop()           # Arreter la musique de fond quand le joueur meurt

    txt = buttons.death_text_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))  # Definir le texte de l'ecran de mort
    globals.screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//2 - 100)))   # Afficher le texte de l'ecran de mort

    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(globals.screen, (200, 0, 0), buttons.restart_rect_death)  # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.end_rect_death)      # Dessiner un rectangle bleu pour le bouton d'arreter

        # Leur texte
    txt_restart = buttons.text_font.render("Rejouer", True, globals.WHITE)  # Definir le texte du bouton pour recommencer
    txt_end = buttons.text_font.render("Quitter", True, globals.WHITE)      # Definir le texte du bouton pour arreter
    
        # Les afficher
    globals.screen.blit(txt_restart, txt_restart.get_rect(center = buttons.restart_rect_death.center))  # Afficher le texte du bouton pour recommencer
    globals.screen.blit(txt_end, txt_end.get_rect(center = buttons.end_rect_death.center))              # Afficher le texte du bouton pour arreter
    
    for monster in classes.monsters:
        monster.reset()    # Faire recommencer a 0 les monstres avec les 3 vies de chaque monstre
    pygame.display.flip()  # Tout generer sur la fenetre



# =================================
# MENU DES ATTRIBUTS
# =================================
def attributes_menu__displayer(screen, text_font, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
   
    globals.screen.fill((0, 0, 100))                                                                     # Remplir l'ecran d'une couleur de base
    txt = buttons.text_font.render("ATTRIBUT", True, globals.RED)                                                # Definir le texte de l'ecran
    globals.screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//5)))               # Afficher le texte de l'ecran
    txt = buttons.text_font.render("level " + str(player.level), True, globals.WHITE)                            # Definir le texte de l'ecran
    globals.screen.blit(txt, txt.get_rect(center = (globals.WIDTH//3, globals.HEIGHT//4)))               # Afficher le texte de l'ecran
    txt = buttons.text_font.render("point(s) d'attribut(s) " + str(player.point_attribut), True, globals.WHITE)  # Definir le texte de l'ecran
    globals.screen.blit(txt, txt.get_rect(center = (globals.WIDTH//3*2, globals.HEIGHT//4)))             # Afficher le texte de l'ecran


    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(globals.screen, (200, 0, 0), buttons.continue_rect)  # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.speed_rect)     # Dessiner un rectangle bleu pour le bouton d'arreter
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.vitality_rect)
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.puissance_rect)
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.attack_delay_rect)
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.lower_speed_rect)
    pygame.draw.rect(globals.screen, (0, 0, 200), buttons.hitbox_display_rect)

        # Leur texte
    txt_continue = buttons.text_font.render("Continuer", True, globals.WHITE)                    # Definir le texte du bouton pour recommencer
    txt_speed = buttons.text_font.render("vitesse : " + str(player.speed), True, globals.WHITE)  # Definir le texte du bouton pour arreter
    txt_vitality = buttons.text_font.render("vie : " + str(player.max_life*10//1/10), True, globals.WHITE)
    txt_puissance = buttons.text_font.render("puissance : " + str(player.puissance*40//100), True, globals.WHITE)
    txt_attack_delay = buttons.text_font.render("vitesse d'attaque : " + str((1000 - player.attack_delay)/50), True, globals.WHITE)
    txt_lower_speed = buttons.text_font.render("baisser la vitesse : " + "4", True, globals.WHITE)
    txt_hitbox_display = buttons.text_font.render("afficher la hitbox", True, globals.WHITE)
    
        # Les afficher
    globals.screen.blit(txt_continue, txt_continue.get_rect(center = buttons.continue_rect.center))  # Afficher le texte du bouton pour recommencer
    globals.screen.blit(txt_speed, txt_speed.get_rect(center = buttons.speed_rect.center))           # Afficher le texte du bouton pour arreter
    globals.screen.blit(txt_vitality, txt_vitality.get_rect(center = buttons.vitality_rect.center))
    globals.screen.blit(txt_puissance, txt_puissance.get_rect(center = buttons.puissance_rect.center))
    globals.screen.blit(txt_attack_delay, txt_attack_delay.get_rect(center = buttons.attack_delay_rect.center))
    globals.screen.blit(txt_lower_speed, txt_lower_speed.get_rect(center = buttons.lower_speed_rect.center))
    globals.screen.blit(txt_hitbox_display, txt_hitbox_display.get_rect(center = buttons.hitbox_display_rect.center))
    
    pygame.display.flip()  # Tout generer sur la fenetre

def attributes_menu__manager(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
    """Se charge de gerer les clics sur les boutons pour recommencer ou arreter le jeu lorsqu'on est sur l'ecran de mort"""
    hitbox_click = 0
    if continue_rect.collidepoint(event.pos):
        state = "game"  # Si le joueur clique sur le bouton pour recommencer, retourner a l'etat du menu de depart
        pygame.mixer.music.play()
    elif speed_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            if player.speed_click == 0:
                player.point_attribut -= 1            # Si le joueur clique sur le bouton pour arreter, passer a l'etat de fin du jeu
                player.speed = (player.speed * 20 + 1) / 20
                player.last_player_speed = (player.last_player_speed * 20 + 1) / 20
    elif vitality_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.max_life += 0.2
            player.regeneration_time -= 500
    elif puissance_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.puissance += player.degat//40
    elif attack_delay_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.attack_delay -= 10
    elif buttons.lower_speed_rect.collidepoint(event.pos) and player.speed_click == 0:
        player.last_player_speed = player.speed
        player.speed = 4
        player.speed_click = 1
    elif buttons.lower_speed_rect.collidepoint(event.pos) and player.speed_click == 1:
        player.speed = player.last_player_speed
        player.speed_click = 0
    elif buttons.hitbox_display_rect.collidepoint(event.pos) and hitbox_click == 0:
        globals.hitbox_display = not globals.hitbox_display

    return state, player



# =================================
# FIN DU JEU
# =================================
def end(running, screen, text_font):
    """Se charge d'afficher l'ecran de fin du jeu, avec un message de remerciement, et de fermer la fenetre apres quelques secondes"""
    screen.fill((0, 0, 100))                                                      # Remplir l'ecran d'une couleur de base pour l'ecran de fin
    txt = text_font.render("Merci d'avoir joue a Tower Of Heights", True, globals.WHITE)  # Definir le texte de l'ecran de fin
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//2)))                # Afficher le texte de l'ecran de fin
    pygame.display.flip()                                                         # Tout generer sur la fenetre
    pygame.time.wait(2500)                                                        # Attendre 2.5 secondes avant de fermer la fenetre
    running = False                                                               # Sortir de la boucle principale
    return running
