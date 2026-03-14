import pygame                               # Importer la bibliothèque pygame pour créer le jeu
import math                                 # Impoter la bibliothèque math pour les calculs de distance et de direction des monstres volants
import globals, imports, classes_and_lists, functions  # Importer les autres fichiers du projet pour pouvoir utiliser les variables et les fonctions qu'ils contiennent

# Initialier pygame
pygame.init()        # Initialiser tous les modules de pygame
pygame.mixer.init()  # Initialiser le module de son de pygame

pygame.display.set_caption("Tower of Heights") # Quand la fenêtre est ouverte, afficher "Tower of Heights" dans la barre de titre

# ================================
# VARIABLES GLOBALES
# ================================

# --- Pour les bruitages ---
    # Pour la musique de fond
pygame.mixer.music.load("Sounds/background_music.mp3")  # Télécharger la musique de fond
pygame.mixer.music.set_volume(0.7)            # Régler le volume de la musique de fond à 70%

    # Pour le son du saut


# --- Pour la fenêtre ---
    # L'écran
globals.screen.fill((40, 40, 55))                                    # Remplir la fenêtre avec une couleur de base


state = "menu_de_debut"       # Le jeu demarre sur la fenêtre de menu


# --- Images et classes---
    # Heros
player = classes_and_lists.Player(globals.on_ground)  # Définit le joueur comme étant membre de la classe Player


tile_size = 32
with open("map.txt") as map_layout:
    map_design = map_layout.read().splitlines()

def create_platforms_from_map(map_design):
    platforms = []

    map_height_pixels = len(map_design) * tile_size
    offset_y = globals.HEIGHT - map_height_pixels


    for row_index, row in enumerate(map_design):
        for col_index, cell in enumerate(row):

            if cell == "#":
                x = col_index * tile_size
                y = row_index * tile_size + offset_y

                rect = pygame.Rect(x, y, tile_size, tile_size)
                platforms.append(rect)

    return platforms

platforms = create_platforms_from_map(map_design)

# --- Items / Inventaire ---
    # Inventaire du joueur (5 slots)
last_inventory_feedback = ""
last_inventory_feedback_time = 0


# --- Polices de texte ---
title_font = pygame.font.SysFont(None, 100)  # Police du titre
text_font = pygame.font.SysFont(None, 40)    # Police du texte

# --- Boutons ---
    # Celui dans l'écran de mort pour recommencer
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (globals.WIDTH//2 - 150, globals.HEIGHT//2 + 120)

continue_rect = pygame.Rect(0, 255, 200, 60)
continue_rect.center = (globals.WIDTH//2 - 150, globals.HEIGHT//2)

speed_rect = pygame.Rect(0, 255, 300, 30)
speed_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 8)

vitality_rect = pygame.Rect(0, 255, 300, 30)
vitality_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 9)

puissance_rect = pygame.Rect(0, 255, 300, 30)
puissance_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 10)

attack_delay_rect = pygame.Rect(0,255, 300, 30)
attack_delay_rect.center = (globals.WIDTH//2 + 150, globals.HEIGHT//16 * 11)

    # Celui dans l'écran de mort pour arrêter
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (globals.WIDTH//2 + 150, globals.HEIGHT//2 + 120)

    # Ceux pour quand on pause le jeu
pause_box = pygame.Rect(globals.WIDTH//2 - 250, globals.HEIGHT//2 - 150, 500, 300)      # Rectangle dans lquel se situeront les boutons
continue_button = pygame.Rect(globals.WIDTH//2 - 200, globals.HEIGHT//2 + 40, 180, 60)  # Celui pour continuer
quit_button = pygame.Rect(globals.WIDTH//2 + 20, globals.HEIGHT//2 + 40, 180, 60)       # Celui pour arrêter

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(globals.WIDTH//2, 120))


def add_item_to_inventory(inventory, item):
    """Ajoute un item à l'inventaire (max 5 slots). Stack d'abord, sinon premier slot libre."""
    for slot in inventory:
        if slot and slot["name"] == item.name:
            slot["quantity"] += item.quantity
            return True

    for index, slot in enumerate(inventory):
        if slot is None:
            inventory[index] = {
                "name": item.name,
                "image": item.image,
                "quantity": item.quantity,
                "usable": item.usable,
                "heal_amount": item.heal_amount,
            }
            return True
        
    return False

def use_inventory_slot(inventory, slot_index, player):
    """Utilise le slot demandé si possible et retourne un message de feedback."""
    slot = inventory[slot_index]
    if slot is None:
        return f"Slot {slot_index + 1} vide"

    if not slot.get("usable", False):
        return f"{slot['name']} non utilisable"

    used = False
    item_name = slot.get("name")

    if item_name == "Potion_vie":
        if player.life < player.max_life:
            player.life = min(player.max_life, player.life + slot.get("heal_amount", 0))
            used = True
        else:
            return "Vie déjà au maximum"
    elif item_name == "Potion_vitesse":
        player.speed += slot.get("heal_amount", 0)
        used = True
    elif item_name == "Potion_puissance":
        player.puissance += slot.get("heal_amount", 0)
        used = True

    if used:
        item_name_for_msg = slot["name"]
        slot["quantity"] -= 1
        if slot["quantity"] <= 0:
            inventory[slot_index] = None
        return f"{item_name_for_msg} utilisé"

    return "Impossible d'utiliser cet objet"

def drop_inventory_slot(inventory, slot_index, items, x, y):
    """Jette 1 objet du slot donné au sol proche du joueur."""
    slot = inventory[slot_index]
    if slot is None:
        return "Rien à jeter"

    item = classes_and_lists.Item(
        slot["name"],
        x,
        y,
        slot["image"],
        quantity=1,
        usable=slot.get("usable", False),
        heal_amount=slot.get("heal_amount", 0),
    )
    items.append(item)

    item_name_for_msg = slot["name"]
    slot["quantity"] -= 1
    if slot["quantity"] <= 0:
        inventory[slot_index] = None

    return f"{item_name_for_msg} jeté"

def draw_inventory_hud(screen, inventory, slot_hold_start, slot_use_lock, current_time):
    """Affiche 5 slots avec icônes, quantités et progression de maintien (1s)."""
    slot_size = 60
    spacing = 12
    total_width = globals.INVENTORY_SLOTS * slot_size + (globals.INVENTORY_SLOTS - 1) * spacing
    start_x = globals.WIDTH // 2 - total_width // 2
    y = globals.HEIGHT - slot_size - 15

    for i in range(globals.INVENTORY_SLOTS):
        x = start_x + i * (slot_size + spacing)
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        pygame.draw.rect(screen, (35, 35, 50), slot_rect)
        pygame.draw.rect(screen, globals.WHITE, slot_rect, 2)

        label = text_font.render(str(i + 1), True, globals.WHITE)
        screen.blit(label, (x + 4, y + 2))

        slot = inventory[i]
        if slot:
            icon_rect = slot["image"].get_rect(center=slot_rect.center)
            screen.blit(slot["image"], icon_rect)
            qty_txt = text_font.render(str(slot["quantity"]), True, globals.WHITE)
            screen.blit(qty_txt, (x + slot_size - qty_txt.get_width() - 4, y + slot_size - qty_txt.get_height() - 2))

        if slot_hold_start[i] is not None and slot and not slot_use_lock[i]:
            progress = (current_time - slot_hold_start[i]) / globals.ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(x, y + slot_size + 4, slot_size, 6)
            bar_fill = pygame.Rect(x, y + slot_size + 4, int(slot_size * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, globals.GREEN, bar_fill)



# ===============================
# FONCTIONS
# ===============================
def death(state, event, restart_rect_death, end_rect_death, player, inventory, items):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    global slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time

    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
    elif end_rect_death.collidepoint(event.pos):
        state = "end"            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
    player.xp = 0
    player.level = 0
    player.point_attribut = 0
    inventory = [None] * globals.INVENTORY_SLOTS
    slot_hold_start = [None] * globals.INVENTORY_SLOTS
    slot_use_lock = [False] * globals.INVENTORY_SLOTS
    last_inventory_feedback = ""
    last_inventory_feedback_time = 0

    items = [
        classes_and_lists.Item("Potion_vie", 260, 320, globals.fiole_vie_img, quantity=1, usable=True, heal_amount=1),
        classes_and_lists.Item("Potion_puissance", 550, 120, globals.fiole_puissance_img, quantity=1, usable=True, heal_amount=100),
        classes_and_lists.Item("Potion_vitesse", 260, 220, globals.fiole_vitesse_img, quantity=1, usable=True, heal_amount=1),
        classes_and_lists.Item("rune_vie", 550, 220, globals.rune_vie_img, quantity=1, usable=False, heal_amount=0),
        classes_and_lists.Item("rune_puissance", 260, 120, globals.rune_puissance_img, quantity=1, usable=False, heal_amount=0),
        classes_and_lists.Item("rune_vitesse", 550, 20, globals.rune_vitesse_img, quantity=1, usable=False, heal_amount=0),
    ]

    return state, player, inventory, items

def death2(screen, restart_rect_death, death_txt_font, end_rect_death, monsters):
    """S'occupe d'afficher l'écran de mort, avec les boutons pour recommencer ou arrêter le jeu, et de réinitialiser les variables du jeu pour pouvoir recommencer à zéro si le joueur choisit de rejouer"""
    screen.fill(globals.BLACK)         # Remplir l'écran de noir pour l'écran de mort
    pygame.mixer.music.stop()  # Arrêter la musique de fond quand le joueur meurt

    txt = death_txt_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))  # Définir le texte de l'écran de mort
    screen.blit(txt, txt.get_rect(center=(globals.WIDTH//2, globals.HEIGHT//2 - 100)))                    # Afficher le texte de l'écran de mort

    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)                         # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), end_rect_death)                             # Dessiner un rectangle bleu pour le bouton d'arrêter

        # Leur texte
    txt_restart = text_font.render("Rejouer", True, globals.WHITE)                            # Définir le texte du bouton pour recommencer
    txt_end = text_font.render("Quitter", True, globals.WHITE)                                # Définir le texte du bouton pour arrêter
    
        # Les afficher
    screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))  # Afficher le texte du bouton pour recommencer
    screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))              # Afficher le texte du bouton pour arrêter
    
    for monster in monsters:
        monster.reset()    # Faire recommencer à 0 les monstres avec les 3 vies de chaque monstre
    pygame.display.flip()  # Tout générer sur la fenêtre

def end(running, screen, text_font):
    """Se charge d'afficher l'écran de fin du jeu, avec un message de remerciement, et de fermer la fenêtre après quelques secondes"""
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base pour l'écran de fin
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, globals.WHITE)  # Définir le texte de l'écran de fin
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//2)))                # Afficher le texte de l'écran de fin
    pygame.display.flip()                                                         # Tout générer sur la fenêtre
    pygame.time.wait(2500)                                                        # Attendre 2.5 secondes avant de fermer la fenêtre
    running = False                                                               # Sortir de la boucle principale
    return running

def menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    if continue_rect.collidepoint(event.pos):
        state = "game"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
        pygame.mixer.music.play()
    elif speed_rect.collidepoint(event.pos):
        if player.point_attribut>0:
            player.point_attribut -= 1            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
            player.speed = (player.speed * 10 + 1) / 10
    elif vitality_rect.collidepoint(event.pos):
        if player.point_attribut>0:
            player.point_attribut -= 1
            player.max_life += 1
            player.regeneration_time -= 500
    elif puissance_rect.collidepoint(event.pos):
        if player.point_attribut>0:
            player.point_attribut -= 1
            player.puissance += player.degat//40
    elif attack_delay_rect.collidepoint(event.pos):
        if player.point_attribut>0:
            player.point_attribut -= 1
            player.attack_delay -= 10
    return state, player

def menu_attribut(screen, text_font, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player):
   
    screen.fill((0, 0, 100))                                                                     # Remplir l'écran d'une couleur de base
    txt = text_font.render("ATTRIBUT", True, globals.RED)                                                # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//2, globals.HEIGHT//5)))                               # Afficher le texte de l'écran
    txt = text_font.render("level " + str(player.level), True, globals.WHITE)                            # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//3, globals.HEIGHT//4)))                               # Afficher le texte de l'écran
    txt = text_font.render("point(s) d'attribut(s) " + str(player.point_attribut), True, globals.WHITE)  # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (globals.WIDTH//3*2, globals.HEIGHT//4)))                             # Afficher le texte de l'écran


    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), continue_rect)  # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), speed_rect)     # Dessiner un rectangle bleu pour le bouton d'arrêter
    pygame.draw.rect(screen, (0, 0, 200), vitality_rect)
    pygame.draw.rect(screen, (0, 0, 200), puissance_rect)
    pygame.draw.rect(screen, (0, 0, 200), attack_delay_rect)

        # Leur texte
    txt_continue = text_font.render("Continuer", True, globals.WHITE)                    # Définir le texte du bouton pour recommencer
    txt_speed = text_font.render("vitesse : " + str(player.speed), True, globals.WHITE)  # Définir le texte du bouton pour arrêter
    txt_vitality = text_font.render("vie : " + str(player.max_life), True, globals.WHITE)
    txt_puissance = text_font.render("puissance : " + str(player.puissance*40//100), True, globals.WHITE)
    txt_attack_delay = text_font.render("vitesse d'attaque : " + str((1000 - player.attack_delay)/50), True, globals.WHITE)

        # Les afficher
    screen.blit(txt_continue, txt_continue.get_rect(center=continue_rect.center))  # Afficher le texte du bouton pour recommencer
    screen.blit(txt_speed, txt_speed.get_rect(center=speed_rect.center))           # Afficher le texte du bouton pour arrêter
    screen.blit(txt_vitality, txt_vitality.get_rect(center=vitality_rect.center))
    screen.blit(txt_puissance, txt_puissance.get_rect(center=puissance_rect.center))
    screen.blit(txt_attack_delay, txt_attack_delay.get_rect(center=attack_delay_rect.center))
    
    pygame.display.flip()  # Tout générer sur la fenêtre

# ===============================
# BOUCLE PRINCIPALE
# ===============================

running = True # Variable du jeu

while running:
    globals.clock.tick(60) # FPS
    time = pygame.time.get_ticks()  # pour relever le temps écoulé depuis le début du jeu (en millisecondes)

    key = pygame.key.get_pressed()  # Pour quand on appuie sur une touche

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
            state = functions.paused__buttons_manager(state, event, continue_button, quit_button)  # Si le jeu est mis en pause, faire appel à la fonction paused() pour gérer les interactions avec les boutons de la fenêtre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = functions.beginning_menu__manager(state, imports.archer_menu_rect, imports.swordsman_menu_rect, event, player)  # Appeler la fonction menu_de_debut() pour gérer les interactions avec les personnages sur la page du menu de départ, et récupérer les variables mises à jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player, inventory, items = death(state, event, restart_rect_death, end_rect_death, player, inventory, items)  # Pour appeler la fonction death() pour gérer les interactions avec les boutons de l'écran de mort, et récupérer les variables mis à jour par cette fonction

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player)    
    
    # --- Pause ---
    if state == "paused":
        functions.paused__character_displayer(globals.screen, pause_box, text_font, continue_button, quit_button)  # Appeler la fonction paused2() pour afficher la fenêtre de pause
        continue
        
    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        functions.beginning_menu__displayer(globals.screen, title_surface, title_rect, imports.archer_image, imports.archer_menu_rect, imports.swordsman_image, imports.swordsman_menu_rect, text_font)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de départ
        continue

    # --- Pour jouer ---
    if state == "game":
        velocity, state, camera_y, player, start_time, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time = functions.game(velocity, state, classes_and_lists.monsters, classes_and_lists.arrows, camera_y, time, key, start_time, player, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time)  # Pour appeler la fonction game() pour gérer les mécaniques du jeu, et récupérer les variables mises à jour par cette fonction


    # --- Pour generer l'ecran de mort ---
    if state == "death":
        death2(globals.screen, restart_rect_death, imports.death_text_font, end_rect_death, classes_and_lists.monsters)  # Pour appeler la fonction death2() pour afficher l'écran de mort, et récupérer les variables mises à jour par cette fonction
        continue

    if state == "menu_attribut":
        menu_attribut(globals.screen, text_font, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player)
        continue

    if state == "end":
        running = end(running, globals.screen, text_font)  # Pour appeler la fonction end() pour afficher l'écran de fin, et récupérer les variables mises à jour par cette fonction
    if player.perso_rect is None:
        continue                                                         # Si le rect du personnage n'est pas encore défini (c'est-à-dire que le joueur n'a pas encore choisi son personnage), ne rien faire et continuer la boucle principale jusqu'à ce que le joueur choisisse son personnage pour que le rect du personnage soit défini et que le jeu puisse commencer

    # --- Synchronisation image avec la hitbox ---
    if player.direction == "right":
        player.perso_rect.x = player.hitbox.x - 20                                                    # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    else:
        player.perso_rect.x = player.hitbox.x - (player.perso_rect.width - player.hitbox.width - 20)  # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    player.perso_rect.y = player.hitbox.y - 10                                                        # Synchroniser la position y de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)

    # --- Caméra montante (lissée) + ne pas descendre sous le sol ---
    if player.hitbox.y >= globals.HEIGHT//2:
        camera_y = 0                                            # Si le personnage est en dessous de la moitié de l'écran en hauteur, la caméra ne descend pas plus bas que le sol (camera_y = 0)
    else:
        target_camera = player.hitbox.y - globals.HEIGHT//2             # La position cible de la caméra est calculée pour que le personnage soit toujours à la moitié de l'écran en hauteur, sauf si le personnage est en dessous de cette moitié, auquel cas la caméra ne descend pas plus bas que le sol (camera_y = 0)
        camera_y += (target_camera - camera_y) * globals.CAMERA_SMOOTH  # Pour faire en sorte que la caméra suive le joueur de manière lissée, on calcule la position cible de la caméra en fonction de la position du joueur, et on ajuste progressivement la position actuelle de la caméra vers cette position cible en utilisant un facteur de lissage (globals.CAMERA_SMOOTH)
    
    if state == "game" :
        for arrow in classes_and_lists.arrows[:]: 
            arrow.update()  # Mettre à jour la position de chaque flèche en fonction de sa direction et de sa vitesse, et retirer les flèches qui sortent de l'écran pour éviter d'avoir trop de flèches inutiles dans la liste des flèches
        for shuri in classes_and_lists.shurikens[:]: 
            shuri.update()  # Mettre à jour la position de chaque shuriken en fonction de sa direction et de sa vitesse, et retirer les shurikens qui sortent de l'écran pour éviter d'avoir trop de shurikens inutiles dans la liste des shurikens

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
    for item in classes_and_lists.items:
        item.draw(globals.screen, camera_y) 
    draw_inventory_hud(globals.screen, inventory, slot_hold_start, slot_use_lock, time)
    if time - last_inventory_feedback_time <= 1400 and last_inventory_feedback:
        feedback_text = text_font.render(last_inventory_feedback, True, globals.WHITE)
        globals.screen.blit(feedback_text, (20, 50))

    txt = text_font.render("Vie : " + str(player.life) + "/" + str(player.max_life), True, globals.WHITE)
    globals.screen.blit(txt, (20, 20))
    pygame.display.flip()                                                                                                  # Tout générer sur la fenêtre

pygame.quit()  # Arrêter Pygame et fermer la fenêtre du jeu




# Merci d'avoir lu notre code, nous espérons que vous avez apprécié le jeu et que vous avez trouvé notre code intéressant à lire


""" Tous droits réservés aux développeurs de ce jeu :
        - Célian
        - William
        - Samuel
"""