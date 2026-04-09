import pygame                                                              # Importer la bibliotheque pygame pour creer le jeu
import math                                                                # Impoter la bibliotheque math pour les calculs de distance et de direction des monstres volants
from random import randint
import globals

# Initialier pygame
globals.initialize_runtime()  # Initialiser pygame et les objets runtime partages (ecran, clock, dimensions, clavier)
import imports, buttons, inventory, classes, functions  # Importer les autres fichiers apres l'initialisation runtime

pygame.display.set_caption("Tower of Heights") # Quand la fenetre est ouverte, afficher "Tower of Heights" dans la barre de titre


# --- Pour les bruitages ---
    # Pour la musique de fond
pygame.mixer.music.set_volume(globals.music_volume)                      # Regler le volume de la musique de fond a 70%

# --- Pour la fenetre ---
    # L'ecran
globals.screen.fill((40, 40, 55))  # Remplir la fenetre avec une couleur de base


state = "menu_de_debut"       # Le jeu demarre sur la fenetre de menu
functions.play_music("menu")  # Lancer la musique de menu

# --- Images et classes---
    # Heros
player = classes.Player(globals.on_ground)  # Definit le joueur comme etant membre de la classe Player

# --- Plateformes ---
tile_size = 32
with open("map.txt") as map_layout:
    map_design = map_layout.read().splitlines()

boss_traps_spawned = set()  # Pour suivre les boss dont les plateformes traversables ont déjà été générés
boss_trap_tiles = {  # Dictionnaire pour stocker les coordonnées des tuiles de plateformes traversables associées à chaque boss, afin de pouvoir les générer lorsque le boss correspondant est vaincu
    "cerberus": [],
    "king_slime": [],
    "spider": [],
    "knight": []
}

for row_index, row in enumerate(map_design):
    for col_index, cell in enumerate(row):
        if cell == "1":
            boss_trap_tiles["cerberus"].append((row_index, col_index))  # Ajouter les coordonnées de la tuile traversable du boss Cerbere à la liste correspondante dans le dictionnaire boss_trap_tiles
        elif cell == "2":
            boss_trap_tiles["king_slime"].append((row_index, col_index))
        elif cell == "3":
            boss_trap_tiles["spider"].append((row_index, col_index))
        elif cell == "4":
            boss_trap_tiles["knight"].append((row_index, col_index))


def create_world_from_map(map_design):
    # Importe les listes de globals
    platforms = globals.platforms
    traps = globals.traps
    monsters = globals.monsters
    items = globals.items
    rune_machines = globals.rune_machines
    wall = globals.wall
    hazards = globals.hazards

    # Vide les listes pour pouvoir les remplir avec les elements de la carte, et eviter d'avoir des elements en double si on recommence une partie
    platforms.clear()
    traps.clear()
    monsters.clear()
    items.clear()
    rune_machines.clear()
    wall.clear()
    hazards.clear()
    block = []

    potion_spawns = 0
    rune_spawns = 0
    wall_type = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    map_height_pixels = len(map_design) * tile_size
    offset_y = globals.HEIGHT - map_height_pixels

    map_width_pixels = max(len(row) for row in map_design) * tile_size
    offset_x = (globals.WIDTH - map_width_pixels) // 2


    for row_index, row in enumerate(map_design):
        for col_index, cell in enumerate(row):       
            x = col_index * tile_size + offset_x
            y = row_index * tile_size + offset_y

            if cell == "/":
                rect = pygame.Rect(x, y, tile_size, tile_size)
                block.append(rect)
                wall_type.append(0)
            elif cell == "#":
                rect = pygame.Rect(x, y, tile_size, tile_size)
                platforms.append(rect)
                wall_type.append(1)
            elif cell == "T":
                rect = pygame.Rect(x, y, tile_size, tile_size)
                traps.append(rect)
                wall_type.append(0)

            elif cell == "S":
                monsters.append(classes.Slug(x, y - 78))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "B":
                monsters.append(classes.Bat(x, y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "s":
                monsters.append(classes.Slime(x,y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "m":
                monsters.append(classes.Mushroom(x,y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)

            elif cell == "C":
                monsters.append(classes.Cerberus(x, y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "A":
                monsters.append(classes.Spider(x, y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(3)

            elif cell == "P":
                potion_spawns += 1
                items.append(inventory.random_potion(x, y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "R":
                rune_spawns += 1
                items.append(inventory.random_rune(x, y))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)

            elif cell == "M":
                rune_machines.append(classes.Runemachine(x, y, tile_size))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)

            elif cell == "^":
                hazards.append(classes.Spikes(x, y, tile_size, damage = 1))
                wall.append(classes.Wall(x, y, tile_size))
                wall_type.append(1)
            elif cell == "L":
                wall_type.append(1)
                hazards.append(classes.Lava(x, y, tile_size, damage = 2))
                wall.append(classes.Wall(x, y, tile_size))

            elif cell == "1":
                for monster in monsters:
                    if monster.type == "cerberus" and not monster.alive:
                        rect = pygame.Rect(x, y, tile_size, tile_size)
                        traps.append(rect)
                        wall_type.append(1)
            elif cell == "2":
                for monster in monsters:
                    if monster.type == "king_slime" and not monster.alive:
                        rect = pygame.Rect(x, y, tile_size, tile_size)
                        traps.append(rect)
                        wall_type.append(1)
            elif cell == "3":
                for monster in monsters:
                    if monster.type == "spider" and not monster.alive:
                        rect = pygame.Rect(x, y, tile_size, tile_size)
                        traps.append(rect)
                        wall_type.append(1)
            elif cell == "4":
                for monster in monsters:
                    if monster.type == "knight" and not monster.alive:
                        rect = pygame.Rect(x, y, tile_size, tile_size)
                        traps.append(rect)
                        wall_type.append(1)

            elif cell == ".":
                wall_prob = randint(0,1000)
                if wall_type[-32] == 2:
                    wall.append(classes.Wall(x, y, tile_size, 1))
                    wall_type.append(1)
                elif wall_type[-32] == 3:
                    wall.append(classes.Wall(x, y, tile_size, 4))
                    wall_type.append(4)
                elif wall_type[-1] == 5:
                    wall.append(classes.Wall(x, y, tile_size, 6))
                    wall_type.append(6)
                elif wall_type[-32] == 5:
                    wall.append(classes.Wall(x, y, tile_size, 7))
                    wall_type.append(7)
                elif wall_type[-32] == 6:
                    wall.append(classes.Wall(x, y, tile_size, 8))
                    wall_type.append(8)
                elif wall_type[-32] == 9:
                    wall.append(classes.Wall(x, y, tile_size, 10))
                    wall_type.append(10)
                elif wall_type[-32] == 10 and wall_prob > 500:
                    wall.append(classes.Wall(x, y, tile_size, 11))
                    wall_type.append(11)
                elif wall_type[-32] == 10:
                    wall.append(classes.Wall(x, y, tile_size, 10))
                    wall_type.append(10)
                   
                elif wall_prob == 0:
                    wall.append(classes.Wall(x, y, tile_size, 2))
                    wall_type.append(2)
                elif wall_prob > 850:
                    wall.append(classes.Wall(x, y, tile_size))
                    wall_type.append(1)
                elif wall_type[-32] and wall_prob > 700:
                    wall.append(classes.Wall(x, y, tile_size))
                    wall_type.append(1)
                elif wall_type[-32] and wall_type[-64] and wall_prob > 400:
                    wall.append(classes.Wall(x, y, tile_size))
                    wall_type.append(1)
                elif wall_prob <= 2:
                    wall.append(classes.Wall(x, y, tile_size, 3))
                    wall_type.append(3)
                elif wall_prob <= 4:
                    wall.append(classes.Wall(x, y, tile_size, 5))
                    wall_type.append(5)
                elif wall_prob <= 6:
                    wall.append(classes.Wall(x, y, tile_size, 9))
                    wall_type.append(9)
                else:
                    wall.append(classes.Wall(x, y, tile_size))
                    wall_type.append(1)


    if potion_spawns == 0 and rune_spawns == 0:
        items.extend(inventory.generate_default_world_items())

    return platforms, block, traps, monsters, items, rune_machines, wall, hazards, offset_x

platforms, block, traps, monsters, items, rune_machines, wall, hazards, offset_x = create_world_from_map(map_design)


# --- Variables importees ---
last_inventory_feedback = ""
last_inventory_feedback_time = 0
velocity = globals.velocity
camera_y = globals.camera_y
start_time = globals.start_time
inventory_list = inventory.inventory_list
slot_hold_start = inventory.slot_hold_start
slot_use_lock = inventory.slot_use_lock
rune_hold_start = [None, None, None]
rune_use_lock = [False, False, False]
pickup_pressed = False
current_rune_machine = None


# ===============================
# BOUCLE PRINCIPALE
# ===============================

running = True # Variable du jeu

while running:
    globals.clock.tick(globals.FPS)          # FPS
    time = pygame.time.get_ticks()           # pour relever le temps ecoule depuis le debut du jeu (en millisecondes)
    globals.key = pygame.key.get_pressed()  # Pour relever les touches actuellement appuyees
    functions.update_music_for_state(state, classes.monsters)
    
    for event in pygame.event.get():
        # --- Pour quitter le jeu ---
        if event.type == pygame.QUIT or (state not in ("game", "rune_menu") and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False             # Pour sortir du jeu si on clique sur la croix ou si on appuie sur ECHAPE dans les menus

        # --- Pour mettre le jeu en pause ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and state == "game":
            state = "paused"            # Si l'etat est celui du jeu et que le joueur appuie sur la touche ECHAPE, alors definir l'etat comme etant celui de pause
            pygame.mixer.music.pause()  # Arreter la musique

        # --- Ouvrir la machine a runes ---
        if state == "game" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            for machine in classes.rune_machines:
                if machine.can_interact(player.hitbox):
                    current_rune_machine = machine
                    state = "rune_menu"
                    break
        
        # --- Boutons de pause ---
        if state == "paused" and event.type == pygame.MOUSEBUTTONDOWN:
            state = functions.paused_buttons_manager(state, event, buttons.continue_button, buttons.quit_button, player)  # Si le jeu est mis en pause, faire appel a la fonction paused() pour gerer les interactions avec les boutons de la fenetre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = functions.beginning_menu_manager(state, event, player, offset_x)  # Appeler la fonction menu_de_debut() pour gerer les interactions avec les personnages sur la page du menu de depart, et recuperer les variables mises a jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time = functions.death_manager(state, event, buttons.restart_rect_death, buttons.end_rect_death, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, map_design, create_world_from_map)  # Pour appeler la fonction death() pour gerer les interactions avec les boutons de l'ecran de mort, et recuperer les variables mis a jour par cette fonction
            if state == "menu_de_debut":
                camera_y = 0
                velocity = globals.velocity
                start_time = pygame.time.get_ticks()
                player.pushback = 0

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = functions.attributes_menu_manager(state, event, buttons.continue_rect, buttons.speed_rect, buttons.vitality_rect, buttons.puissance_rect, buttons.attack_delay_rect, player)    

        if state == "rune_menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            state, feedback = functions.rune_menu_manager(state, event, inventory_list, player, current_rune_machine, time, globals.key, rune_hold_start, rune_use_lock)
            if feedback:
                last_inventory_feedback = feedback
                last_inventory_feedback_time = time
            if state == "game":
                current_rune_machine = None
                rune_hold_start[:] = [None, None, None]
                rune_use_lock[:] = [False, False, False]

    
    # --- Pause ---
    if state == "paused":
        functions.paused_buttons_displayer(globals.screen, buttons.pause_box, buttons.text_font, buttons.continue_button, buttons.quit_button, player)  # Appeler la fonction paused2() pour afficher la fenetre de pause
        continue

    if state == "rune_menu":
        state, feedback = functions.rune_menu_manager(state, None, inventory_list, player, current_rune_machine, time, globals.key, rune_hold_start, rune_use_lock)
        if feedback:
            last_inventory_feedback = feedback
            last_inventory_feedback_time = time
        if state == "game":
            current_rune_machine = None
            rune_hold_start[:] = [None, None, None]
            rune_use_lock[:] = [False, False, False]

        functions.rune_menu_displayer(globals.screen, inventory_list, current_rune_machine, rune_hold_start, rune_use_lock, time)
        continue

    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        functions.beginning_menu_displayer(globals.screen, buttons.title_surface, buttons.title_rect, imports.archer_image, imports.archer_menu_rect, imports.swordsman_image, imports.swordsman_menu_rect, imports.ninja_image, imports.ninja_menu_rect, buttons.text_font)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de depart
        continue

    # --- Pour jouer ---
    if state == "game":
        velocity, state, player, start_time, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed = functions.game(velocity, state, classes.monsters, globals.arrows, camera_y, time, globals.key, start_time, player, inventory_list, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed, platforms, block, traps, globals.shurikens, classes.hazards)  # Pour appeler la fonction game() pour gerer les mecaniques du jeu, et recuperer les variables mises a jour par cette fonction

    # --- Pour generer l'ecran de mort ---
    if state == "death":
        functions.death_displayer(globals.screen, buttons.restart_rect_death, buttons.death_text_font, buttons.end_rect_death, classes.monsters)  # Pour appeler la fonction death2() pour afficher l'ecran de mort, et recuperer les variables mises a jour par cette fonction
        continue

    if state == "menu_attribut":
        functions.attributes_menu_displayer(globals.screen, buttons.text_font, buttons.continue_rect, buttons.speed_rect, buttons.vitality_rect, buttons.puissance_rect, buttons.attack_delay_rect, player)
        continue

    if state == "end":
        running = functions.end(running, globals.screen, buttons.text_font)  # Pour appeler la fonction end() pour afficher l'ecran de fin, et recuperer les variables mises a jour par cette fonction
    if player.perso_rect is None:
        continue                                                         # Si le rect du personnage n'est pas encore defini (c'est-a-dire que le joueur n'a pas encore choisi son personnage), ne rien faire et continuer la boucle principale jusqu'a ce que le joueur choisisse son personnage pour que le rect du personnage soit defini et que le jeu puisse commencer

    # --- Synchronisation image avec la hitbox ---
    if player.direction == "right":
        player.perso_rect.x = player.hitbox.x - 20                                                    # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du decalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde a celle de la hitbox)
    else:
        player.perso_rect.x = player.hitbox.x - (player.perso_rect.width - player.hitbox.width - 20)  # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    player.perso_rect.y = player.hitbox.bottom - player.perso_rect.height                                                         # Synchroniser la position y de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)

    # --- Camera montante (lissee) + ne pas descendre sous le sol ---
    if player.hitbox.y >= globals.HEIGHT//2:
        camera_y = 0                                            # Si le personnage est en dessous de la moitie de l'ecran en hauteur, la camera ne descend pas plus bas que le sol (camera_y = 0)
    else:
        target_camera = player.hitbox.y - globals.HEIGHT//2             # La position cible de la camera est calculee pour que le personnage soit toujours a la moitie de l'ecran en hauteur, sauf si le personnage est en dessous de cette moitie, auquel cas la camera ne descend pas plus bas que le sol (camera_y = 0)
        camera_y += (target_camera - camera_y) * globals.CAMERA_SMOOTH  # Pour faire en sorte que la camera suive le joueur de maniere lissee, on calcule la position cible de la camera en fonction de la position du joueur, et on ajuste progressivement la position actuelle de la camera vers cette position cible en utilisant un facteur de lissage (globals.CAMERA_SMOOTH)
    
    if state == "game" :
        for arrow in globals.arrows[:]: 
            arrow.update(platforms, globals.arrows, globals.shurikens)  # Mettre a jour la position de chaque fleche en fonction de sa direction et de sa vitesse, et retirer les fleches qui sortent de l'ecran pour eviter d'avoir trop de fleches inutiles dans la liste des fleches
        for shuriken in globals.shurikens[:]: 
            shuriken.update(platforms, globals.arrows, globals.shurikens)  # Mettre a jour la position de chaque shuriken en fonction de sa direction et de sa vitesse, et retirer les shurikens qui sortent de l'ecran pour eviter d'avoir trop de shurikens inutiles dans la liste des shurikens
    player.update_potion_effects(time)
    
    map_height_pixels = len(map_design) * tile_size
    offset_y = globals.HEIGHT - map_height_pixels
    map_width_pixels = max(len(row) for row in map_design) * tile_size
    offset_x = (globals.WIDTH - map_width_pixels) // 2

    for monster in globals.monsters:
        if not monster.alive and monster.type in boss_trap_tiles:
            if monster.type not in boss_traps_spawned:
                for row_index, col_index in boss_trap_tiles[monster.type]:
                    x = col_index * tile_size + offset_x
                    y = row_index * tile_size + offset_y
                    traps.append(pygame.Rect(x, y, tile_size, tile_size))
                boss_traps_spawned.add(monster.type)


    # --- Generer le jeu ---
    globals.screen.fill((40, 40, 55))                                                                                              # Remplir l'ecran avec une couleur de base pour le jeu
    for platform in platforms:
        globals.screen.blit(imports.platform_1, (platform.x, platform.y - camera_y))  # Afficher les plateformes a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera
    for platform in block:
        globals.screen.blit(imports.platform_wall, (platform.x, platform.y - camera_y))  # Afficher les plateformes a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera

    for trap in traps:
        globals.screen.blit(imports.platform_trap, (trap.x, trap.y - camera_y))
    for wall_tile in wall:
        wall_tile.draw(globals.screen, camera_y)                                                                                      # Afficher les dalles de mur a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera
    for hazard in classes.hazards:
        hazard.draw(globals.screen, camera_y)
    if globals.hitbox_display:
        pygame.draw.rect(globals.screen, (255, 255, 0), (player.hitbox.x, player.hitbox.y - camera_y, player.hitbox.width, player.hitbox.height), 2)
    for machine in classes.rune_machines:
        machine.draw(globals.screen, camera_y)
    globals.screen.blit(player.selected_image, (player.perso_rect.x, player.perso_rect.y - camera_y))                                                   # Afficher l'image du personnage a sa position actuelle sur l'ecran, en tenant compte du decalage de la camera
    for monster in classes.monsters:
        if monster.alive:
            globals.screen.blit(monster.image, (monster.rect.x, monster.rect.y - camera_y))                                        # Afficher les monstres vivants a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera

    for arrow in globals.arrows:
        globals.screen.blit(arrow.image, (arrow.rect.x, arrow.rect.y - camera_y))                                                  # Afficher les fleches a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera

    for shuriken in globals.shurikens:
        globals.screen.blit(shuriken.image, (shuriken.rect.x, shuriken.rect.y - camera_y))                                                  # Afficher les shurikens a leur position actuelle sur l'ecran, en tenant compte du decalage de la camera
    if items:
        for item in items:
            item.draw(globals.screen, camera_y) 
        if any(machine.can_interact(player.hitbox) for machine in classes.rune_machines):
            rune_hint = buttons.text_font.render("Appuie sur R pour utiliser les runes", True, globals.WHITE)
            globals.screen.blit(rune_hint, (20, 80))
    inventory.draw_inventory_hud(globals.screen, inventory_list, slot_hold_start, slot_use_lock, time)
    inventory.draw_equipped_rings(globals.screen, player)

    feedback_y = 50
    active_effects=[]
    if player.regeneration_bonus:
        regen_remaining = (player.regeneration_effect_end_time - time)//1000
        active_effects.append("Regen " + str(regen_remaining) + "s")
    if player.speed_bonus > 0:
        speed_remaining = max(0, (player.speed_effect_end_time - time) // 1000)
        active_effects.append("Vitesse " + str(speed_remaining) + "s")
    if player.power_bonus > 0:
        power_remaining = max(0, (player.power_effect_end_time - time) // 1000)
        active_effects.append("Puissance " + str(power_remaining) + "s")
    if active_effects:
        effect_feedback = "Effet(s)" + " | ".join(active_effects)
        feedback_text = buttons.text_font.render(effect_feedback, True, globals.WHITE)
        globals.screen.blit(feedback_text, (20, feedback_y))
        feedback_y += 30
    if time - last_inventory_feedback_time <= 1400 and last_inventory_feedback:

        feedback_text = buttons.text_font.render(last_inventory_feedback, True, globals.WHITE)
        globals.screen.blit(feedback_text, (20, feedback_y))

    txt = buttons.text_font.render("Vie : " + str(player.life) + "/" + str(math.floor(player.max_life)), True, globals.WHITE)
    globals.screen.blit(txt, (20, 20))
    pygame.display.flip()                                                                                                  # Tout generer sur la fenetre

pygame.quit()  # Arreter Pygame et fermer la fenetre du jeu




# Merci d'avoir lu notre code, nous esperons que vous avez apprecie le jeu et que vous avez trouve notre code interessant a lire


""" Tous droits reserves aux developpeurs de ce jeu :
        - Celian
        - William
        - Samuel
"""
