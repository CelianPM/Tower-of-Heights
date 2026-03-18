import pygame                                                              # Importer la bibliothèque pygame pour créer le jeu
import math                                                                # Impoter la bibliothèque math pour les calculs de distance et de direction des monstres volants
import globals, imports, buttons, inventory, classes_and_lists, functions  # Importer les autres fichiers du projet pour pouvoir utiliser les variables et les fonctions qu'ils contiennent

# Initialier pygame
pygame.init()        # Initialiser tous les modules de pygame
pygame.mixer.init()  # Initialiser le module de son de pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights" dans la barre de titre


# --- Pour les bruitages ---
    # Pour la musique de fond
pygame.mixer.music.set_volume(0.7)                      # Régler le volume de la musique de fond à 70%

# --- Pour la fenêtre ---
    # L'écran
globals.screen.fill((40, 40, 55))  # Remplir la fenêtre avec une couleur de base


state = "menu_de_debut"       # Le jeu demarre sur la fenêtre de menu
functions.background_music()  # Lancer la musique de fond

# --- Images et classes---
    # Heros
player = classes_and_lists.Player(globals.on_ground)  # Définit le joueur comme étant membre de la classe Player

# --- Plateformes ---
tile_size = 32
with open("map.txt") as map_layout:
    map_design = map_layout.read().splitlines()

def create_world_from_map(map_design):
    platforms = []
    monsters = []

    map_height_pixels = len(map_design) * tile_size
    offset_y = globals.HEIGHT - map_height_pixels


    for row_index, row in enumerate(map_design):
        for col_index, cell in enumerate(row):       
            x = col_index * tile_size
            y = row_index * tile_size + offset_y
            if cell == "#":
                rect = pygame.Rect(x, y, tile_size, tile_size)
                platforms.append(rect)
            elif cell == "S":
                monsters.append(classes_and_lists.Slug(x, y - 78))
            elif cell == "B":
                monsters.append(classes_and_lists.Bat(x, y))


    return platforms, monsters

platforms, classes_and_lists.monsters = create_world_from_map(map_design)


# --- Variables importees ---
last_inventory_feedback = ""
last_inventory_feedback_time = 0
velocity = globals.velocity
camera_y = globals.camera_y
start_time = globals.start_time
inventory_list = inventory.inventory_list
items = inventory.items
slot_hold_start = inventory.slot_hold_start
slot_use_lock = inventory.slot_use_lock
pickup_pressed = False


# ===============================
# BOUCLE PRINCIPALE
# ===============================

running = True # Variable du jeu

while running:
    globals.clock.tick(globals.FPS)          # FPS
    time = pygame.time.get_ticks()           # pour relever le temps écoulé depuis le début du jeu (en millisecondes)
    globals.key = pygame.key.get_pressed()  # Pour relever les touches actuellement appuyées

    for event in pygame.event.get():
        # --- Pour quitter le jeu ---
        if event.type == pygame.QUIT or (state != "game" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False             # Pour sortir du jeu si on clique sur la croix ou si on appuie sur ECHAPE dans les menus

        # --- Pour mettre le jeu en pause ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and state == "game":
            state = "paused"            # Si l'état est celui du jeu et que le joueur appuie sur la touche ECHAPE, alors définir l'état comme étant celui de pause
            pygame.mixer.music.pause()  # Arrêter la musique
        
        # --- Boutons de pause ---
        if state == "paused" and event.type == pygame.MOUSEBUTTONDOWN:
            state = functions.paused__buttons_manager(state, event, buttons.continue_button, buttons.quit_button)  # Si le jeu est mis en pause, faire appel à la fonction paused() pour gérer les interactions avec les boutons de la fenêtre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = functions.beginning_menu__manager(state, imports.archer_menu_rect, imports.swordsman_menu_rect, imports.ninja_menu_rect, imports.beggar_menu_rect, event, player)  # Appeler la fonction menu_de_debut() pour gérer les interactions avec les personnages sur la page du menu de départ, et récupérer les variables mises à jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time = functions.death__manager(state, event, buttons.restart_rect_death, buttons.end_rect_death, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time)  # Pour appeler la fonction death() pour gérer les interactions avec les boutons de l'écran de mort, et récupérer les variables mis à jour par cette fonction

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = functions.attributes_menu__manager(state, event, buttons.continue_rect, buttons.speed_rect, buttons.vitality_rect, buttons.puissance_rect, buttons.attack_delay_rect, player)    
    
    # --- Pause ---
    if state == "paused":
        functions.paused__buttons_displayer(globals.screen, buttons.pause_box, buttons.text_font, buttons.continue_button, buttons.quit_button)  # Appeler la fonction paused2() pour afficher la fenêtre de pause
        continue
        
    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        functions.beginning_menu__displayer(globals.screen, buttons.title_surface, buttons.title_rect, imports.archer_image, imports.archer_menu_rect, imports.swordsman_image, imports.swordsman_menu_rect, imports.ninja_image, imports.ninja_menu_rect, buttons.text_font)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de départ
        continue

    # --- Pour jouer ---
    if state == "game":
        velocity, state, player, start_time, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed = functions.game(velocity, state, classes_and_lists.monsters, classes_and_lists.arrows, camera_y, time, globals.key, start_time, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed, platforms, classes_and_lists.shurikens)  # Pour appeler la fonction game() pour gérer les mécaniques du jeu, et récupérer les variables mises à jour par cette fonction

    # --- Pour generer l'ecran de mort ---
    if state == "death":
        functions.death__displayer(globals.screen, buttons.restart_rect_death, buttons.death_text_font, buttons.end_rect_death, classes_and_lists.monsters)  # Pour appeler la fonction death2() pour afficher l'écran de mort, et récupérer les variables mises à jour par cette fonction
        continue

    if state == "menu_attribut":
        functions.attributes_menu__displayer(globals.screen, buttons.text_font, buttons.continue_rect, buttons.speed_rect, buttons.vitality_rect, buttons.puissance_rect, buttons.attack_delay_rect, player)
        continue

    if state == "end":
        running = functions.end(running, globals.screen, buttons.text_font)  # Pour appeler la fonction end() pour afficher l'écran de fin, et récupérer les variables mises à jour par cette fonction
    if player.perso_rect is None:
        continue                                                         # Si le rect du personnage n'est pas encore défini (c'est-à-dire que le joueur n'a pas encore choisi son personnage), ne rien faire et continuer la boucle principale jusqu'à ce que le joueur choisisse son personnage pour que le rect du personnage soit défini et que le jeu puisse commencer

    # --- Synchronisation image avec la hitbox ---
    if player.direction == "right":
        player.perso_rect.x = player.hitbox.x - 20                                                    # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    else:
        player.perso_rect.x = player.hitbox.x - (player.perso_rect.width - player.hitbox.width - 20)  # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    player.perso_rect.y = player.hitbox.bottom - player.perso_rect.height                                                         # Synchroniser la position y de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)

    # --- Caméra montante (lissée) + ne pas descendre sous le sol ---
    if player.hitbox.y >= globals.HEIGHT//2:
        camera_y = 0                                            # Si le personnage est en dessous de la moitié de l'écran en hauteur, la caméra ne descend pas plus bas que le sol (camera_y = 0)
    else:
        target_camera = player.hitbox.y - globals.HEIGHT//2             # La position cible de la caméra est calculée pour que le personnage soit toujours à la moitié de l'écran en hauteur, sauf si le personnage est en dessous de cette moitié, auquel cas la caméra ne descend pas plus bas que le sol (camera_y = 0)
        camera_y += (target_camera - camera_y) * globals.CAMERA_SMOOTH  # Pour faire en sorte que la caméra suive le joueur de manière lissée, on calcule la position cible de la caméra en fonction de la position du joueur, et on ajuste progressivement la position actuelle de la caméra vers cette position cible en utilisant un facteur de lissage (globals.CAMERA_SMOOTH)
    
    if state == "game" :
        for arrow in classes_and_lists.arrows[:]: 
            arrow.update(platforms, classes_and_lists.arrows, classes_and_lists.shurikens)  # Mettre à jour la position de chaque flèche en fonction de sa direction et de sa vitesse, et retirer les flèches qui sortent de l'écran pour éviter d'avoir trop de flèches inutiles dans la liste des flèches
        for shuriken in classes_and_lists.shurikens[:]: 
            shuriken.update(platforms, classes_and_lists.arrows, classes_and_lists.shurikens)  # Mettre à jour la position de chaque shuriken en fonction de sa direction et de sa vitesse, et retirer les shurikens qui sortent de l'écran pour éviter d'avoir trop de shurikens inutiles dans la liste des shurikens

    # --- Générer le jeu ---
    globals.screen.fill((40, 40, 55))                                                                                              # Remplir l'écran avec une couleur de base pour le jeu
    for platform in platforms:
        pygame.draw.rect(globals.screen, (120, 60, 60), (platform.x, platform.y - camera_y, platform.width, platform.height))  # Afficher les plateformes à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    globals.screen.blit(player.selected_image, (player.perso_rect.x, player.perso_rect.y - camera_y))                                                   # Afficher l'image du personnage à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for monster in classes_and_lists.monsters:
        if monster.alive:
            globals.screen.blit(monster.image, (monster.rect.x, monster.rect.y - camera_y))                                        # Afficher les monstres vivants à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for arrow in classes_and_lists.arrows:
        globals.screen.blit(arrow.image, (arrow.rect.x, arrow.rect.y - camera_y))                                                  # Afficher les flèches à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for shuriken in classes_and_lists.shurikens:
        globals.screen.blit(shuriken.image, (shuriken.rect.x, shuriken.rect.y - camera_y))                                                  # Afficher les shurikens à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for item in items:
        item.draw(globals.screen, camera_y) 
    inventory.draw_inventory_hud(globals.screen, inventory_list, slot_hold_start, slot_use_lock, time)
    if time - last_inventory_feedback_time <= 1400 and last_inventory_feedback:
        feedback_text = buttons.text_font.render(last_inventory_feedback, True, globals.WHITE)
        globals.screen.blit(feedback_text, (20, 50))

    txt = buttons.text_font.render("Vie : " + str(player.life) + "/" + str(player.max_life), True, globals.WHITE)
    globals.screen.blit(txt, (20, 20))
    pygame.display.flip()                                                                                                  # Tout générer sur la fenêtre

pygame.quit()  # Arrêter Pygame et fermer la fenêtre du jeu




# Merci d'avoir lu notre code, nous espérons que vous avez apprécié le jeu et que vous avez trouvé notre code intéressant à lire


""" Tous droits réservés aux développeurs de ce jeu :
        - Célian
        - William
        - Samuel
"""
