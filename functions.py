import pygame
import globals, imports, buttons, inventory, classes_and_lists

pygame.init()



# =================================
# PAUSE
# =================================

# --- Gere les boutons ---
def paused__buttons_manager(state, event, continue_button, quit_button):
    """Gere les clics sur les boutons affiches boutons pour continuer ou arreter le jeu lorsqu'il est mis en pause"""
    if buttons.continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if buttons.quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arreter le jeu
    return state

# --- Affiche les boutons ---
def paused__buttons_displayer(screen, pause_box, text_font, continue_button, quit_button):
    """Affiche les boutons pour continuer ou arreter le jeu lorsqu'il est mis en pause"""
    # Dessiner le rectangle de pause avec la question
    pygame.draw.rect(globals.screen, globals.WHITE, buttons.pause_box)                                                                # Pour dessiner un rectangle blanc...
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.pause_box, 3)                                                             # ...et sa bordure noire
    globals.screen.blit(buttons.text_font.render("Que veux-tu faire ?", True, globals.BLACK), (buttons.pause_box.x + 100, buttons.pause_box.y + 40))  # Pour afficher le texte

    # Bouton pour continuer
    pygame.draw.rect(globals.screen, globals.GREEN, buttons.continue_button)                                                           # Pour dessiner un rectangle vert...
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.continue_button, 2)                                                        # ...et sa bordure noire
    globals.screen.blit(buttons.text_font.render("Continuer", True, globals.BLACK), (buttons.continue_button.x + 20, buttons.continue_button.y + 15))  # Pour afficher le texte

    # Bouton pour arreter
    pygame.draw.rect(globals.screen, globals.RED, buttons.quit_button)                                                                 # Pour dessiner un rectangle rouge...
    pygame.draw.rect(globals.screen, globals.BLACK, buttons.quit_button, 2)                                                            # ...et sa bordure noire
    globals.screen.blit(buttons.text_font.render("Quitter", True, globals.BLACK), (buttons.quit_button.x + 40, buttons.quit_button.y + 15))            # Pour afficher le texte

    pygame.display.flip() # Pour charger la fenetre



# =================================
# MENU DE DEPART
# =================================

# --- Gere les boutons ---
def beginning_menu__manager(state, archer_menu_rect, swordsman_menu_rect, ninja_menu_rect, beggar_menu_rect, event, player):
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
    player.perso_rect = player.selected_image.get_rect(topleft=(200, 300))                                                              # Rect de l'image
    player.hitbox = pygame.Rect(player.perso_rect.x, player.perso_rect.y, player.perso_rect.width - 60, player.perso_rect.height - 10)  # Hitbox du personnage
    pygame.mixer.music.play(-1)                                                                                                         # Lancer la musique de fond en boucle
    state = "game"                                                                                                                      # Passer au jeu
    player.life = player.max_life
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
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))   # Pour definir le texte
    screen.blit(selection, (globals.WIDTH//2 - selection.get_width()//2, globals.HEIGHT - 160))     # Pour afficher le texte
    screen.blit(pour_pauser, (globals.WIDTH//2 - pour_pauser.get_width()//2, globals.HEIGHT - 60))  # Pour afficher le texte
    pygame.display.flip()                                                                           # Tout generer sur la fenetre



# =================================
# JEU
# =================================
def game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed, platforms, shurikens):
    """S'occupe de gerer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    
    velocity, start_time = player.move(imports.jump_sound, state, time, key, velocity, start_time, arrows, shurikens)
    velocity = player.platform_collisions(platforms, velocity)
    player.monster_collisions(monsters, time, arrows, platforms, shurikens)
    player.player_xp()
    items, inventory_list, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed = player.player_inventory(items, inventory_list, key, time, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed)
    state = player.player_death(time, camera_y,state)

    # --- Gestion du cooldown de l'archer ---
    if player.hero in ("archer", "ninja") and not player.can_attack:
        if time - player.last_attack_time >= player.attack_delay:
            player.can_attack = True  # Cooldown termine, le joueur peut tirer a nouveau


    # --- Monster movement ---
    for monster in monsters:
        if monster.alive:
            monster.update(player.hitbox, monsters, platforms)  # Si le monstre est vivant, il suit le joueur en fonction de la position de sa hitbox

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
                last_inventory_feedback = inventory.use_inventory_slot(inventory_list, slot_index, player, time)
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
def death__manager(state, event, restart_rect_death, end_rect_death, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time):
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

    items = [
        inventory.Item("Potion_vie", 260, 320, imports.life_potion, quantity = 1, usable = True, heal_amount = 1),
        inventory.Item("Potion_puissance", 550, 120, imports.power_potion, quantity = 1, usable = True, heal_amount = 100),
        inventory.Item("Potion_vitesse", 260, 220, imports.speed_potion, quantity = 1, usable = True, heal_amount = 1),
        inventory.Item("rune_vie", 550, 220, imports.life_rune, quantity = 1, usable = False, heal_amount = 0),
        inventory.Item("rune_puissance", 260, 120, imports.power_rune, quantity = 1, usable = False, heal_amount = 0),
        inventory.Item("rune_vitesse", 550, 20, imports.speed_rune, quantity = 1, usable = False, heal_amount = 0),
    ]

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
    
    for monster in classes_and_lists.monsters:
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

        # Leur texte
    txt_continue = buttons.text_font.render("Continuer", True, globals.WHITE)                    # Definir le texte du bouton pour recommencer
    txt_speed = buttons.text_font.render("vitesse : " + str(player.speed), True, globals.WHITE)  # Definir le texte du bouton pour arreter
    txt_vitality = buttons.text_font.render("vie : " + str(player.max_life), True, globals.WHITE)
    txt_puissance = buttons.text_font.render("puissance : " + str(player.puissance*40//100), True, globals.WHITE)
    txt_attack_delay = buttons.text_font.render("vitesse d'attaque : " + str((1000 - player.attack_delay)/50), True, globals.WHITE)

        # Les afficher
    globals.screen.blit(txt_continue, txt_continue.get_rect(center = buttons.continue_rect.center))  # Afficher le texte du bouton pour recommencer
    globals.screen.blit(txt_speed, txt_speed.get_rect(center = buttons.speed_rect.center))           # Afficher le texte du bouton pour arreter
    globals.screen.blit(txt_vitality, txt_vitality.get_rect(center = buttons.vitality_rect.center))
    globals.screen.blit(txt_puissance, txt_puissance.get_rect(center = buttons.puissance_rect.center))
    globals.screen.blit(txt_attack_delay, txt_attack_delay.get_rect(center = buttons.attack_delay_rect.center))
    
    pygame.display.flip()  # Tout generer sur la fenetre

def attributes_menu__manager(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
    """Se charge de gerer les clics sur les boutons pour recommencer ou arreter le jeu lorsqu'on est sur l'ecran de mort"""
    if continue_rect.collidepoint(event.pos):
        state = "game"  # Si le joueur clique sur le bouton pour recommencer, retourner a l'etat du menu de depart
        pygame.mixer.music.play()
    elif speed_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1            # Si le joueur clique sur le bouton pour arreter, passer a l'etat de fin du jeu
            player.speed = (player.speed * 10 + 1) / 10
    elif vitality_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.max_life += 1
            player.regeneration_time -= 500
    elif puissance_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.puissance += player.degat//40
    elif attack_delay_rect.collidepoint(event.pos):
        if player.point_attribut > 0:
            player.point_attribut -= 1
            player.attack_delay -= 10
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
