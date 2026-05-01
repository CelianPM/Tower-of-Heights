import pygame
from math import floor
import globals, imports, buttons, inventory, classes

MUSIC_TRACKS = {
    "game": "Sounds/background_music.mp3",
    "boss": "Sounds/musique_de_boss.mp3",
    "menu": "Sounds/musique_de_menu.mp3",
}
_current_music_track = None


def play_music(music_name):
    """Charge et joue une musique en boucle"""
    global _current_music_track
    if music_name not in MUSIC_TRACKS:
        return
    target_file = MUSIC_TRACKS[music_name]
    if _current_music_track == target_file and pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(0 if globals.music_muted else globals.music_volume)
        return
    pygame.mixer.music.load(target_file)
    _current_music_track = target_file
    pygame.mixer.music.set_volume(0 if globals.music_muted else globals.music_volume)
    pygame.mixer.music.play(-1)

def update_music_for_state(state, monsters, player = None):
    """Choisit automatiquement la bonne musique selon l'etat du jeu (menu, jeu, boss)."""
    menu_states = {"menu_de_debut", "menu_attribut", "paused", "rune_menu", "death", "end"}
    if state in menu_states:
        play_music("menu")
        return
    if state == "game":
        boss_alive = [monster for monster in monsters if isinstance(monster, classes.Boss) and monster.alive]
        if not boss_alive or player is None:
            play_music("game")
            return

        player_center_y = player.hitbox.centery
        in_boss_room = any(
            abs(player_center_y - boss.rect.centery) <= 280
            for boss in boss_alive
        )
        play_music("boss" if in_boss_room else "game")



# =================================
# PAUSE
# =================================

def paused_buttons_manager(state, event, continue_button, quit_button, player):
    """Gere les clics sur les boutons affiches boutons pour continuer ou arreter le jeu lorsqu'il est mis en pause"""
    if buttons.continue_button.collidepoint(event.pos):
        state = "game"                                  # Si on appuie sur le bouton pour continuer, continuer le jeu
        if globals.music_muted:
            pygame.mixer.music.set_volume(0)            # Si la musique est en mode muet, ne pas la reprendre et s'assurer que le volume reste a 0
        else:
            pygame.mixer.music.unpause()                # Sinon, continuer la musique
    
    if buttons.quit_button.collidepoint(event.pos):
        state = "end"                                   # Si on appuie sur le bouton pour quitter, arreter le jeu

    if buttons.restart_button.collidepoint(event.pos):
        state = "death"
        if globals.music_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.unpause()
    
    if buttons.lower_speed_minus_rect.collidepoint(event.pos):
        player.speed = max(1, round(player.speed - 0.5, 2))  # Limiter la vitesse minimale a 1 pour eviter les bugs de mouvement, et arrondir a 2 decimales pour eviter les valeurs bizarres

    if buttons.lower_speed_plus_rect.collidepoint(event.pos) and player.speed < player.max_speed:
        player.speed = min(player.max_speed, round(player.speed + 0.5, 2))  # Limiter la vitesse maximale a la vitesse de base du personnage pour eviter les bugs de mouvement, et arrondir a 2 decimales pour eviter les valeurs bizarres

    if buttons.lower_speed_rect.collidepoint(event.pos):
        if player.speed_click == 0:
            """Enregistrer la vitesse actuelle du joueur avant de la modifier, pour pouvoir la restaurer ensuite quand on reclique sur le bouton. Si le bouton est clique une premiere fois, baisser la vitesse du joueur a 4. Si le bouton est clique une deuxieme fois, restaurer la vitesse originale du joueur."""
            player.last_player_speed = player.speed
            player.speed = 4
            player.speed_click = 1
        else:
            """Si le bouton est clique une deuxieme fois, restaurer la vitesse originale du joueur."""
            player.speed = player.last_player_speed
            player.speed_click = 0

    if buttons.hitbox_display_rect.collidepoint(event.pos):
        globals.hitbox_display = not globals.hitbox_display  # Basculer l'affichage des hitboxes des entites

    if buttons.music_toggle_rect.collidepoint(event.pos):
        globals.music_muted = not globals.music_muted                     # Si on clique sur le bouton pour basculer la musique, basculer le mode muet
        pygame.mixer.music.set_volume(0 if globals.music_muted else globals.music_volume)  # Et ajuste le volume en consequence
    return state


def paused_buttons_displayer(screen, pause_box, text_font, continue_button, quit_button, player):
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
        "Caps_Lock = changer d'attaque (ninja)",
    ]
    for i, text in enumerate(lines):
        globals.screen.blit(buttons.text_font.render(text, True, globals.WHITE), (buttons.pause_info_box.x + 20, buttons.pause_info_box.y + 20 + i * 30))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.lower_speed_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.lower_speed_rect, 2)
    pygame.draw.rect(globals.screen, (120, 20, 20), buttons.lower_speed_minus_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.lower_speed_minus_rect, 2)
    pygame.draw.rect(globals.screen, (20, 120, 20), buttons.lower_speed_plus_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.lower_speed_plus_rect, 2)
    globals.screen.blit(buttons.text_font.render(f"Lower speed: {player.speed}", True, globals.WHITE), (buttons.lower_speed_rect.x + 90, buttons.lower_speed_rect.y + 15))
    globals.screen.blit(buttons.text_font.render("-", True, globals.WHITE), (buttons.lower_speed_minus_rect.x + 22, buttons.lower_speed_minus_rect.y + 15))
    globals.screen.blit(buttons.text_font.render("+", True, globals.WHITE), (buttons.lower_speed_plus_rect.x + 19, buttons.lower_speed_plus_rect.y + 14))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.hitbox_display_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.hitbox_display_rect, 2)
    globals.screen.blit(buttons.text_font.render("Hitbox: ON" if globals.hitbox_display else "Hitbox: OFF", True, globals.WHITE), (buttons.hitbox_display_rect.x + 20, buttons.hitbox_display_rect.y + 15))

    pygame.draw.rect(globals.screen, (0, 0, 180), buttons.music_toggle_rect)
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.music_toggle_rect, 2)
    globals.screen.blit(buttons.text_font.render("Musique: OFF" if globals.music_muted else "Musique: ON", True, globals.WHITE), (buttons.music_toggle_rect.x + 20, buttons.music_toggle_rect.y + 15))

    pygame.draw.rect(globals.screen, globals.GREEN, buttons.continue_button)
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.continue_button, 2)
    globals.screen.blit(buttons.text_font.render("Continuer", True, globals.BLACK), (buttons.continue_button.x + 55, buttons.continue_button.y + 15))

    pygame.draw.rect(globals.screen, globals.RED, buttons.quit_button)
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.quit_button, 2)
    globals.screen.blit(buttons.text_font.render("Quitter", True, globals.BLACK), (buttons.quit_button.x + 80, buttons.quit_button.y + 15))

    pygame.draw.rect(globals.screen, globals.BLUE, buttons.restart_button)
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.restart_button, 2)
    globals.screen.blit(buttons.text_font.render("Recommencer", True, globals.BLACK), (buttons.restart_button.x + 40, buttons.quit_button.y + 15))
    
    pygame.display.flip() # Pour charger la fenetre



# =================================
# MACHINE A RUNES
# =================================

def rune_menu_displayer(screen, inventory_list, machine, rune_hold_start, rune_use_lock, current_time):
    """Affiche le menu de la machine a runes, avec les options pour utiliser les runes disponibles dans l'inventaire du joueur, et affiche une barre de progression lorsque le joueur maintient une touche pour utiliser une rune"""
    box = pygame.Rect(globals.WIDTH//2 - 260, globals.HEIGHT//2 - 170, 520, 340)  # Boite de dialogue centrale
    pygame.draw.rect(screen, globals.WHITE, box)                                  # Dessiner la boite de dialogue...
    pygame.draw.rect(screen, globals.BLACK, box, 3)                               # ...et sa bordure

    title = buttons.text_font.render("Choisis une rune a utiliser", True, globals.BLACK)
    screen.blit(title, (box.x + 40, box.y + 30))

    counts = machine.available_runes(inventory_list) if machine else {
        "rune_vie": 0,
        "rune_vitesse": 0,
        "rune_puissance": 0,
    }  # Obtenir le nombre de chaque type de rune disponible dans l'inventaire du joueur pour les afficher dans le menu, ou 0 si la machine n'est pas disponible pour une raison quelconque (bug, etc.)
    
    lines = [
        (f"1 - Rune de vie ({counts['rune_vie']})", 0),
        (f"2 - Rune de vitesse ({counts['rune_vitesse']})", 1),
        (f"3 - Rune de puissance ({counts['rune_puissance']})", 2),
        ("ECHAP - fermer", None),
    ]  # Les lignes de texte a afficher dans le menu, avec pour les 3 premieres le type de rune et le nombre disponible entre parenthese, et pour la derniere les instructions pour fermer le menu. Chaque ligne est associee a un index de rune (0, 1 ou 2) ou None pour la ligne d'instruction qui n'est pas associee a une rune.

    for i, (text, rune_index) in enumerate(lines):
        """Afficher chaque ligne de texte dans le menu, et si la ligne est associee a une rune, afficher une barre de progression a cote du texte lorsque le joueur maintient la touche correspondante pour utiliser cette rune, en utilisant les listes rune_hold_start et rune_use_lock pour gerer le temps de maintien et eviter les utilisations multiples pendant le maintien."""
        line = buttons.text_font.render(text, True, globals.BLACK)
        screen.blit(line, (box.x + 40, box.y + 90 + i * 45))

        if rune_index is not None and rune_hold_start[rune_index] is not None and not rune_use_lock[rune_index]:
            """Si la ligne est associee a une rune, et que le joueur maintient la touche correspondante, afficher une barre de progression a cote du texte pour indiquer le temps restant avant que la rune soit utilisee."""
            progress = (current_time - rune_hold_start[rune_index]) / globals.ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(box.x + 360, box.y + 110 + i * 45, 120, 6)
            bar_fill = pygame.Rect(box.x + 360, box.y + 110 + i * 45, int(120 * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, globals.GREEN, bar_fill)

    pygame.display.flip()


def rune_menu_manager(state, event, inventory_list, player, machine, time, key, rune_hold_start, rune_use_lock):
    """Gere les interactions du joueur avec le menu de la machine a runes, en utilisant les listes rune_hold_start et rune_use_lock pour gerer le temps de maintien des touches pour utiliser les runes et eviter les utilisations multiples pendant le maintien, et en appliquant les effets des runes utilisees sur le joueur."""
    if event and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        for i in range(3):
            rune_hold_start[i] = None
            rune_use_lock[i] = False
        return "game", ""

    key_map = {
        0: (pygame.K_1, "rune_vie"),
        1: (pygame.K_2, "rune_vitesse"),
        2: (pygame.K_3, "rune_puissance"),
    }  # Dictionnaire pour associer les index de rune aux touches correspondantes et aux noms de rune, pour faciliter la gestion des interactions dans le menu de la machine a runes

    held_index = None  # Index de la rune actuellement maintenue, ou None si aucune touche de rune n'est maintenue
    for i, (key_code, _) in key_map.items():
        if key[key_code]:
            held_index = i  # Si la touche correspondante a une rune est maintenue, enregistrer l'index de cette rune dans held_index pour gerer la barre de progression et l'utilisation de la rune dans le menu de la machine a runes
            break
    
    for i in range(3):
        if i != held_index:
            rune_hold_start[i] = None
            rune_use_lock[i] = False
    
    if held_index is None:
        return state, ""
    
    key_code, rune_name = key_map[held_index]  # Obtenir le code de la touche et le nom de la rune correspondante a l'index de rune actuellement maintenue pour gerer l'utilisation de la rune dans le menu de la machine a runes

    if rune_hold_start[held_index] is None:
        rune_hold_start[held_index] = time  # Si une touche de rune commence a etre maintenue, enregistrer le temps de debut de ce maintien dans la liste rune_hold_start pour gerer la barre de progression et l'utilisation de la rune dans le menu de la machine a runes
        rune_use_lock[held_index] = False   # Et debloquer l'utilisation de cette rune pendant ce maintien en s'assurant que le verrou correspondant dans la liste rune_use_lock est a False

    if not rune_use_lock[held_index] and (time - rune_hold_start[held_index] >= globals.ITEM_USE_HOLD_MS):
        """Si une touche de rune est maintenue depuis suffisamment longtemps, et que cette rune n'a pas encore ete utilisee pendant ce maintien, utiliser cette rune en appliquant son effet sur le joueur, en consommant la rune dans l'inventaire du joueur, et en activant le verrou correspondant dans la liste rune_use_lock pour eviter les utilisations multiples de cette rune pendant ce maintien."""
        if machine and machine.consume_rune(inventory_list, rune_name):
            player.apply_rune_effect(rune_name)
            rune_use_lock[held_index] = True
            print("game", f"{rune_name} utilisee")
            return state, f"{rune_name} utilisee"

        rune_use_lock[held_index] = True
        return state, "Pas de rune a utiliser"

    return state, ""



# =================================
# MENU DE DEPART
# =================================

def beginning_menu_manager(state, event, player, offset_x):
    """Se charge de gerer les clics sur les personnages dans le menu de depart, et de definir les variables correspondantes en fonction du personnage choisi"""
    if imports.archer_menu_rect.collidepoint(event.pos):
        player.hero = "archer"      # Le joueur choisi est l'archer
    
    if imports.swordsman_menu_rect.collidepoint(event.pos):
        player.hero = "swordsman"   # Le joueur choisi est l'epeiste
    
    if imports.ninja_menu_rect.collidepoint(event.pos):
        player.hero = "ninja"       # Le joueur choisi est le ninja

    if imports.beggar_menu_rect.collidepoint(event.pos):
        player.hero = "beggar"      # Le joueur choisi est le mendiant

    if player.hero is not None:
        player.select_the_player()  # Appliquer les caracteristiques du personnage choisi au joueur (image, vitesse, vie, etc.)

    if player.selected_attack is None:
        return state, player        # Si aucun personnage n'est encore choisi, ne pas changer d'etat et retourner le joueur tel quel

    player.selected_attack_right = player.selected_attack                                     # Profil droit de l'image attaquant
    player.selected_attack_left = pygame.transform.flip(player.selected_attack, True, False)  # Profil gauche de l'image attaquant
    spawn_x = offset_x + 2 * 32
    player.perso_rect = player.selected_image.get_rect(topleft=(spawn_x, 300))    # Rect de l'image
    player.hitbox = pygame.Rect(player.perso_rect.x, player.perso_rect.y, 32, 112)            # Hitbox du personnage, positionnee par rapport au rect de l'image du personnage pour que le joueur puisse cliquer sur le personnage lui meme pour le selectionner dans le menu de depart, et pour que les collisions avec les plateformes et les monstres soient plus precises pendant le jeu
    state = "game"                                                                            # Passer au jeu
    player.life = floor(player.max_life)                                                      # S'assurer que la vie du joueur est a son maximum au debut du jeu, au cas ou le joueur aurait clique sur plusieurs personnages dans le menu de depart et que la variable player.life aurait ete modifiee par les caracteristiques d'un personnage avant que le joueur ne choisisse finalement un autre personnage avec des caracteristiques differentes
    player.velocity = 0                                                                       # S'assurer que la vitesse du joueur est a 0 au debut du jeu, pour eviter les bugs de mouvement si le joueur avait clique sur plusieurs personnages dans le menu de depart et que la variable player.velocity aurait ete modifiee par les caracteristiques d'un personnage avant que le joueur ne choisisse finalement un autre personnage avec des caracteristiques differentes
    return state, player


def beginning_menu_displayer(screen, title_surface, title_rect, archer_image, archer_menu_rect, swordsman_image, swordsman_menu_rect, ninja_image, ninja_menu_rect, text_font):
    """Se charge d'afficher le menu de depart, avec les personnages a choisir et les instructions pour jouer"""
    # --- Remplir l'ecran ---
        # Avec la couleur
    screen.fill((30, 30, 45))               # Remplir l'ecran avec une couleur de base
    screen.blit(title_surface, title_rect)  # Afficher le texte

        # Generer les personnages
    screen.blit(imports.archer_image, imports.archer_menu_rect)        # Afficher l'image de l'archer
    screen.blit(imports.swordsman_image, imports.swordsman_menu_rect)  # Afficher l'image de l'epeiste
    screen.blit(imports.ninja_image, imports.ninja_menu_rect)          # Afficher l'image du ninja
    screen.blit(imports.beggar_image, imports.beggar_menu_rect)        # Afficher l'image du mendiant
    
        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                      # Pour definir le texte
    pour_pauser = text_font.render("Appuie sur ESC pour mettre le jeu en pause", True, (200, 200, 200))   # Pour definir le texte
    screen.blit(selection, (globals.WIDTH//2 - selection.get_width()//2, globals.HEIGHT - 160))           # Pour afficher le texte
    screen.blit(pour_pauser, (globals.WIDTH//2 - pour_pauser.get_width()//2, globals.HEIGHT - 60))        # Pour afficher le texte
    pygame.display.flip()                                                                                 # Tout generer sur la fenetre



# =================================
# JEU
# =================================
def game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed, platforms_1, platforms_2, block, traps, shurikens, hazards, monster_platforms):
    """S'occupe de gerer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    
    # --- Mouvements et collisions du joueur ---
    velocity, start_time = player.move(imports.jump_sound, state, time, key, velocity, start_time, arrows, shurikens)
    velocity = player.platform_collisions(platforms_1, platforms_2, block, traps, velocity)
    player.monster_collisions(monsters, time, arrows, platforms_1, platforms_2, block, items, shurikens)
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
    for monster in monsters:
        if monster.alive:
            if abs(monster.rect.centery - player.hitbox.centery) < 2000:
                monster.update(player.hitbox, monsters, monster_platforms)  # Si le monstre est vivantet proche du joueur, il suit le joueur en fonction de la position de sa hitbox

    # --- Pour retourner a la page du depart ---
    if key[pygame.K_m]:
        state = "menu_attribut"    # Passer a l'etat correspondant a celui du menu d'attributs du joueur
    
    
    # --- Utilisation des slots (maintenir 1-5 pendant 1s) ---
    for slot_index, key_code in enumerate(inventory.slot_keys):
        if globals.key[key_code]:
            if slot_hold_start[slot_index] is None:
                """Si une touche de slot d'inventaire commence a etre maintenue, enregistrer le temps de debut de ce maintien dans la liste slot_hold_start pour gerer la barre de progression et l'utilisation de l'item dans le slot d'inventaire, et debloquer l'utilisation de ce slot pendant ce maintien en s'assurant que le verrou correspondant dans la liste slot_use_lock est a False."""
                slot_hold_start[slot_index] = time
                slot_use_lock[slot_index] = False

            if not slot_use_lock[slot_index] and (time - slot_hold_start[slot_index] >= globals.ITEM_USE_HOLD_MS):
                """Si une touche de slot d'inventaire est maintenue depuis suffisamment longtemps, et que ce slot n'a pas encore ete utilise pendant ce maintien, utiliser l'item dans ce slot d'inventaire en appliquant son effet sur le joueur, en consommant l'item dans l'inventaire du joueur, et en activant le verrou correspondant dans la liste slot_use_lock pour eviter les utilisations multiples de ce slot pendant ce maintien."""
                last_inventory_feedback = inventory.use_inventory_slot(inventory_list, slot_index, player, current_time)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True
        else:
            slot_hold_start[slot_index] = None
            slot_use_lock[slot_index] = False

    # --- Jet d'objet (Shift + 1-5) ---
    if globals.key[pygame.K_LSHIFT] or globals.key[pygame.K_RSHIFT]:
        for slot_index, key_code in enumerate(inventory.slot_keys):
            if globals.key[key_code] and not slot_use_lock[slot_index]:
                dropped_x = player.hitbox.centerx + 25
                dropped_y = player.hitbox.bottom - 20
                last_inventory_feedback = inventory.drop_inventory_slot(inventory_list, slot_index, items, dropped_x, dropped_y)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True

    return velocity, state, player, start_time, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed


def background_music():
    """S'occupe de lancer la musique de fond du jeu en boucle, avec un volume ajuste a 0.7 pour ne pas etre trop forte par rapport aux autres sons du jeu"""
    play_music("game")



# =================================
# MORT DU JOUEUR
# =================================

def death_manager(state, event, restart_rect_death, end_rect_death, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, map_design, create_world_from_map):
    """Se charge de gerer les clics sur les boutons pour recommencer ou arreter le jeu lorsqu'on est sur l'ecran de mort, ainsi que réinitialiser toutes les variables et listes du jeu."""

    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner a l'etat du menu de depart
    elif end_rect_death.collidepoint(event.pos):
        state = "end"            # Si le joueur clique sur le bouton pour arreter, passer a l'etat de fin du jeu
    
    # Reinitialise les variableset listes du jeu pour pouvoir recommencer a zero si le joueur choisit de rejouer
    player.xp = 0
    player.level = 0
    player.point_attribut = 0
    player.xp_lvl_up = 5
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
    player.slow_down = False
    player.slow_effect_end_time = 0
    player.attack = False
    player.can_attack = True
    globals.arrows.clear()
    globals.shurikens.clear()
    player.equipped_rings = set()
    player.equipped_ring_images = []

    _, _, _, _, classes.monsters, items, classes.rune_machines, _, classes.hazards, _ = create_world_from_map(map_design)

    return state, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time


def death_displayer(screen, restart_rect_death, death_text_font, end_rect_death, monsters):
    """S'occupe d'afficher l'ecran de mort, avec les boutons pour recommencer ou arreter le jeu, et de reinitialiser les variables du jeu pour pouvoir recommencer a zero si le joueur choisit de rejouer"""
    globals.screen.fill(globals.BLACK)  # Remplir l'ecran de noir pour l'ecran de mort

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

def attributes_menu_displayer(screen, text_font, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
    """S'occupe d'afficher le menu des attributs du joueur, avec les options pour augmenter les differentes caracteristiques du joueur en depensant les points d'attributs gagnés en montant de niveau, et pour retourner au jeu"""

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

        # Leur texte
    txt_continue = buttons.text_font.render("Continuer", True, globals.WHITE)                    # Definir le texte du bouton pour recommencer
    txt_speed = buttons.text_font.render("vitesse : " + str(player.speed), True, globals.WHITE)  # Definir le texte du bouton pour arreter
    txt_vitality = buttons.text_font.render("vie : " + str(player.max_life*10//1/10), True, globals.WHITE)
    txt_puissance = buttons.text_font.render("puissance : " + str(player.puissance*40//100), True, globals.WHITE)
    txt_attack_delay = buttons.text_font.render("vitesse d'attaque : " + str((1000 - player.attack_delay)/50), True, globals.WHITE)
    
        # Les afficher
    globals.screen.blit(txt_continue, txt_continue.get_rect(center = buttons.continue_rect.center))  # Afficher le texte du bouton pour recommencer
    globals.screen.blit(txt_speed, txt_speed.get_rect(center = buttons.speed_rect.center))           # Afficher le texte du bouton pour arreter
    globals.screen.blit(txt_vitality, txt_vitality.get_rect(center = buttons.vitality_rect.center))
    globals.screen.blit(txt_puissance, txt_puissance.get_rect(center = buttons.puissance_rect.center))
    globals.screen.blit(txt_attack_delay, txt_attack_delay.get_rect(center = buttons.attack_delay_rect.center))
    
    pygame.display.flip()  # Tout generer sur la fenetre


def attributes_menu_manager(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
    """Se charge de gerer les clics sur les boutons pour recommencer ou arreter le jeu lorsqu'on est sur l'ecran de mort"""
    
    if continue_rect.collidepoint(event.pos):
        state = "game"
    
    elif speed_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.speed = (player.speed * 20 + 1) / 20
            player.max_speed = (player.max_speed * 20 + 1) / 20
            player.last_player_speed = (player.last_player_speed * 20 + 1) / 20
    
    elif vitality_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.max_life += 0.2
            if player.regeneration_time > 10000:
                player.regeneration_time -= 500
    
    elif puissance_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.puissance += player.degat//40
    
    elif attack_delay_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            if player.attack_delay > 200:
                player.attack_delay -= 10
    
    return state, player



# =================================
# FIN DU JEU
# =================================

def end(running, screen, text_font):
    """Se charge d'afficher l'ecran de fin du jeu, avec un message de remerciement, et de fermer la fenetre apres quelques secondes"""
    screen.fill((0, 0, 100))                                                              # Remplir l'ecran d'une couleur de base pour l'ecran de fin
    txt = text_font.render("Merci d'avoir joue a Tower Of Heights", True, globals.WHITE)  # Definir le texte de l'ecran de fin
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//2)))        # Afficher le texte de l'ecran de fin
    pygame.display.flip()                                                                 # Tout generer sur la fenetre
    pygame.time.wait(2500)                                                                # Attendre 2.5 secondes avant de fermer la fenetre
    running = False                                                                       # Sortir de la boucle principale
    return running
