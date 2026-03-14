import pygame
import globals, imports, inventory, classes_and_lists

pygame.init()

# =================================
# FONCTIONS
# =================================

# --- Pause ---
def paused__buttons_manager(state, event, continue_button, quit_button):
    """Gère les clics sur les boutons affichés boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arrêter le jeu
    return state

def paused__buttons_displayer(screen, pause_box, text_font, continue_button, quit_button):
    """Affiche les boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    # Dessiner le rectangle de pause avec la question
    pygame.draw.rect(screen, globals.WHITE, pause_box)                                                                # Pour dessiner un rectangle blanc...
    pygame.draw.rect(screen, globals.BLACK, pause_box, 3)                                                             # ...et sa bordure noire
    screen.blit(text_font.render("Que veux-tu faire ?", True, globals.BLACK), (pause_box.x + 100, pause_box.y + 40))  # Pour afficher le texte

    # Bouton pour continuer
    pygame.draw.rect(screen, globals.GREEN, continue_button)                                                           # Pour dessiner un rectangle vert...
    pygame.draw.rect(screen, globals.BLACK, continue_button, 2)                                                        # ...et sa bordure noire
    screen.blit(text_font.render("Continuer", True, globals.BLACK), (continue_button.x + 20, continue_button.y + 15))  # Pour afficher le texte

    # Bouton pour arrêter
    pygame.draw.rect(screen, globals.RED, quit_button)                                                                 # Pour dessiner un rectangle rouge...
    pygame.draw.rect(screen, globals.BLACK, quit_button, 2)                                                            # ...et sa bordure noire
    screen.blit(text_font.render("Quitter", True, globals.BLACK), (quit_button.x + 40, quit_button.y + 15))            # Pour afficher le texte

    pygame.display.flip() # Pour charger la fenêtre


# --- Beginning menu ---
def beginning_menu__manager(state, event, player):
    """Se charge de gérer les clics sur les personnages dans le menu de départ, et de définir les variables correspondantes en fonction du personnage choisi"""
    if imports.archer_menu_rect.collidepoint(event.pos):
        player.hero = "archer"     # Le joueur choisi est l'archer
    
    if imports.swordsman_menu_rect.collidepoint(event.pos):
        player.hero = "swordsman"  # Le joueur choisi est l'épéiste
    
    if imports.ninja_menu_rect.collidepoint(event.pos):
        player.hero = "ninja"      # Le joueur choisi est le ninja

    if player.hero is not None:
        player.select_the_player()

    if player.selected_attack is None:
        return state, player

    player.selected_attack_right = player.selected_attack                                     # Profil droit de l'image attaquant
    player.selected_attack_left = pygame.transform.flip(player.selected_attack, True, False)  # Profil gauche de l'image attaquant
    player.perso_rect = player.selected_image.get_rect(topleft=(200, 300))                    # Rect de l'image
    player.hitbox = pygame.Rect(player.perso_rect.x, player.perso_rect.y, player.perso_rect.width - 60, player.perso_rect.height - 10)  # Hitbox du personnage
    pygame.mixer.music.play(-1)                                                               # Lancer la musique de fond en boucle
    state = "game"                                                                            # Passer au jeu
    player.life = player.max_life
    return state, player

def beginning_menu__displayer(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font):
    """Se charge d'afficher le menu de départ, avec les personnages à choisir et les instructions pour jouer"""
    # --- Remplir l'écran ---
        # Avec la couleur
    screen.fill((30, 30, 45))                                                                             # Remplir l'écran avec une couleur de base
    screen.blit(title_surface, title_rect)                                                                # Afficher le texte

        # Générer les personnages
    screen.blit(imports.archer_image, imports.archer_menu_rect)                                                           # Afficher l'image de l'archer
    screen.blit(imports.swordsman_image, imports.swordsman_menu_rect)                                                           # Afficher l'image de l'épéiste
    screen.blit(imports.ninja_image, imports.ninja_menu_rect)                                                           # Afficher l'image du ninja

        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                      # Pour définir le texte
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))         # Pour définir le texte
    screen.blit(selection, (globals.WIDTH//2 - selection.get_width()//2, globals.HEIGHT - 160))                           # Pour afficher le texte
    screen.blit(pour_pauser, (globals.WIDTH//2 - pour_pauser.get_width()//2, globals.HEIGHT - 60))                        # Pour afficher le texte
    pygame.display.flip()                                                                                 # Tout générer sur la fenêtre


# --- Game ---
def game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time):
    """S'occupe de gérer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    
    velocity, start_time = player.move(imports.jump_sound, state, time, key, velocity, start_time)
    velocity = player.platform_collisions(classes_and_lists.platforms, velocity)
    player.monster_collisions(monsters, time,arrows)
    player.player_xp()
    items, inventory, last_inventory_feedback, last_inventory_feedback_time = player.player_inventory(items, inventory, key, time, last_inventory_feedback, last_inventory_feedback_time)
    state = player.player_death(time, camera_y,state)

    # --- Gestion du cooldown de l'archer ---
    if player.hero in ("archer", "ninja") and not player.can_attack:
        if time - player.last_attack_time >= player.attack_delay:
            player.can_attack = True  # Cooldown terminé, le joueur peut tirer à nouveau


    # --- Monster movement ---
    for monster in monsters:
        if monster.alive:
            monster.update(player.hitbox, monsters)  # Si le monstre est vivant, il suit le joueur en fonction de la position de sa hitbox

    # --- Pour retourner à la page du départ ---
    if key[pygame.K_m]:
        state = "menu_attribut"    # Passer à l'état correspondant à celui du menu de départ
        pygame.mixer.music.stop()  # Arrêter la musique de fond
    
    xp_lvl_up = 0
    for i in range(player.level + 1):
        xp_lvl_up += i*2
    if player.xp >= xp_lvl_up:
        player.level += 1
        player.point_attribut += 5
    
    # --- Utilisation des slots (maintenir 1..5 pendant 1s) ---
    for slot_index, key_code in enumerate(classes_and_lists.slot_keys):
        if key[key_code]:
            if slot_hold_start[slot_index] is None:
                slot_hold_start[slot_index] = time
                slot_use_lock[slot_index] = False

            if not slot_use_lock[slot_index] and (time - slot_hold_start[slot_index] >= globals.ITEM_USE_HOLD_MS):
                last_inventory_feedback = inventory.use_inventory_slot(inventory, slot_index, player)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True
        else:
            slot_hold_start[slot_index] = None
            slot_use_lock[slot_index] = False

    # --- Jet d'objet (Shift + 1..5) ---
    if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
        for slot_index, key_code in enumerate(classes_and_lists.slot_keys):
            if key[key_code] and not slot_use_lock[slot_index]:
                dropped_x = player.hitbox.centerx + 25
                dropped_y = player.hitbox.bottom - 20
                last_inventory_feedback = inventory.drop_inventory_slot(inventory, slot_index, items, dropped_x, dropped_y)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True

    return velocity, state, camera_y, player, start_time, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time
