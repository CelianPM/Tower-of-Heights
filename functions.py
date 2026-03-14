import pygame
import globals

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
                "heal_amount": item.heal_amount
            }
            return True

    return False

def use_inventory_slot(inventory, slot_index, life, max_life):
    """Utilise le slot demandé si utilisable et retourne (life, message)."""
    slot = inventory[slot_index]
    if slot is None:
        return life, f"Slot {slot_index + 1} vide"

    if not slot.get("usable", False):
        return life, f"{slot['name']} non utilisable"

    used = False
    if slot.get("usable", False):
        if life < max_life:
            life = min(max_life, life + slot.get("heal_amount", 0))
            used = True
        else:
            return life, "Vie déjà au maximum"

    if used:
        slot["quantity"] -= 1
        if slot["quantity"] <= 0:
            inventory[slot_index] = None
        return life, f"{slot['name']} utilisé"

    return life, "Aucun effet"


def draw_inventory_hud(screen, inventory, slot_hold_start, slot_use_lock, current_time):
    """Affiche 5 slots avec icônes, quantités et progression de maintien (1s)."""
    slot_size = 60
    spacing = 12
    start_x = 20
    y = 70

    for i in range(INVENTORY_SLOTS):
        x = start_x + i * (slot_size + spacing)
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        pygame.draw.rect(screen, (35, 35, 50), slot_rect)
        pygame.draw.rect(screen, WHITE, slot_rect, 2)

        num_txt = text_font.render(str(i + 1), True, WHITE)
        screen.blit(num_txt, (x + 4, y + 2))

        slot = inventory[i]
        if slot:
            icon_rect = slot["image"].get_rect(center=slot_rect.center)
            screen.blit(slot["image"], icon_rect)
            qty_txt = text_font.render(str(slot["quantity"]), True, WHITE)
            screen.blit(qty_txt, (x + slot_size - qty_txt.get_width() - 4, y + slot_size - qty_txt.get_height() - 2))

        # Barre de progression pour maintenir la touche 1 seconde
        if slot_hold_start[i] is not None and slot and not slot_use_lock[i]:
            progress = (current_time - slot_hold_start[i]) / ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(x, y + slot_size + 4, slot_size, 6)
            bar_fill = pygame.Rect(x, y + slot_size + 4, int(slot_size * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, GREEN, bar_fill)

def paused(state, event, continue_button, quit_button):
    """Ggère les clics sur les boutons affichés boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arrêter le jeu
    return state

def paused2(screen, pause_box, text_font, continue_button, quit_button, WHITE, BLACK, GREEN, RED):
    """Affiche les boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    # Dessiner le rectangle de pause avec la question
    pygame.draw.rect(screen, WHITE, pause_box)                                                                # Pour dessiner un rectangle blanc...
    pygame.draw.rect(screen, BLACK, pause_box, 3)                                                             # ...et sa bordure noire
    screen.blit(text_font.render("Que veux-tu faire ?", True, BLACK), (pause_box.x + 100, pause_box.y + 40))  # Pour afficher le texte

    # Bouton pour continuer
    pygame.draw.rect(screen, GREEN, continue_button)                                                           # Pour dessiner un rectangle vert...
    pygame.draw.rect(screen, BLACK, continue_button, 2)                                                        # ...et sa bordure noire
    screen.blit(text_font.render("Continuer", True, BLACK), (continue_button.x + 20, continue_button.y + 15))  # Pour afficher le texte

    # Bouton pour arrêter
    pygame.draw.rect(screen, RED, quit_button)                                                                 # Pour dessiner un rectangle rouge...
    pygame.draw.rect(screen, BLACK, quit_button, 2)                                                            # ...et sa bordure noire
    screen.blit(text_font.render("Quitter", True, BLACK), (quit_button.x + 40, quit_button.y + 15))            # Pour afficher le texte

    pygame.display.flip() # Pour charger la fenêtre

def menu_de_debut(selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, perso1_rect_menu, perso2_rect_menu, perso1_image, perso2_image, event, attack_delay, attack_animation_time, player_speed, max_life, regenaration_time, degat):
    """Se charge de gérer les clics sur les personnages dans le menu de départ, et de définir les variables correspondantes en fonction du personnage choisi"""
    if perso1_rect_menu.collidepoint(event.pos):
        attack_delay = 800                                                                          # Définit le temps entre les attaques pour l'archer, pour qui c'est plus long
        attack_animation_time = 300
        player = "archer"                                                                            # Le joueur choisi est l'archer
        selected_image = perso1_image                                                                # L'image sélectionnée est celle de l'archer
        selected_image_right = selected_image                                                        # Profil droit de l'image sélectionnée
        selected_image_left = pygame.transform.flip(selected_image, True, False)                     # Profil gauche de l'image sélectionnée
        selected_attack = pygame.image.load("archer_post_attaque.png").convert_alpha()               # Télécharge l'image de l'attaque de l'archer
        player_speed = 3
        max_life = 4
        regenaration_time = 25000
        degat = 600
    
    if perso2_rect_menu.collidepoint(event.pos):
        attack_delay = 300                                                                          # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
        attack_animation_time = 300
        player = "swordsman"                                                                         # Le joueur choisi est l'épéiste
        selected_image = perso2_image                                                                # L'image sélectionnée est celle de l'épéiste
        selected_image_right = selected_image                                                        # Profil droit de l'image sélectionnée
        selected_image_left = pygame.transform.flip(selected_image, True, False)                     # Profil gauche de l'image sélectionnée
        selected_attack = pygame.image.load("epeiste_attaque.png").convert_alpha()                   # Télécharge l'image de l'attaque de l'épéiste
        player_speed = 4
        max_life = 5
        regenaration_time = 20000
        degat = 500

    
    if selected_attack is None:
        return (selected_image, hitbox, selected_image_left,
            selected_image_right, selected_attack_left,
            selected_attack_right, selected_attack,
            perso_rect, state, player,
            attack_delay, attack_animation_time,
            player_speed, max_life, life,
            regenaration_time)


    selected_attack_right = selected_attack                                                          # Profil droit de l'image attaquant
    selected_attack_left = pygame.transform.flip(selected_attack, True, False)                       # Profil gauche de l'image attaquant
    perso_rect = selected_image.get_rect(topleft=(200, 300))                                         # Rect de l'image
    hitbox = pygame.Rect(perso_rect.x, perso_rect.y, perso_rect.width - 60, perso_rect.height - 10)  # Hitbox du personnage
    pygame.mixer.music.play(-1)                                                                      # Lancer la musique de fond en boucle
    state = "game"                                                                                   # Passer au jeu
    life = max_life
    return selected_image, hitbox, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, selected_attack, perso_rect, state, player, attack_delay, attack_animation_time, player_speed, max_life, life, regenaration_time, degat

def menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font, WIDTH, HEIGHT):
    """Se charge d'afficher le menu de départ, avec les personnages à choisir et les instructions pour jouer"""
    # --- Remplir l'écran ---
        # Avec la couleur
    screen.fill((30, 30, 45))                                                                             # Remplir l'écran avec une couleur de base
    screen.blit(title_surface, title_rect)                                                                # Afficher le texte

        # Générer les personnages
    screen.blit(perso1_image, perso1_rect_menu)                                                           # Afficher l'image de l'archer
    screen.blit(perso2_image, perso2_rect_menu)                                                           # Afficher l'image de l'épéiste

        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                      # Pour définir le texte
    revenir_au_menu = text_font.render("Appuie sur M pour revenir sur cette page", True, (200, 200, 200)) # Pour définir le texte
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))         # Pour définir le texte
    screen.blit(selection, (WIDTH//2 - selection.get_width()//2, HEIGHT - 160))                           # Pour afficher le texte
    screen.blit(revenir_au_menu, (WIDTH//2 - revenir_au_menu.get_width()//2, HEIGHT - 110))               # Pour afficher le texte
    screen.blit(pour_pauser, (WIDTH//2 - pour_pauser.get_width()//2, HEIGHT - 60))                        # Pour afficher le texte
    pygame.display.flip()                                                                                 # Tout générer sur la fenêtre

def game(start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, player, monsters, arrows, GRAVITY, jump_power, player_speed, PUSHBACK, camera_y, HEIGHT, time, key, last_attack_time, last_damage_time, attack_delay, attack_animation_time, can_attack, xp, level, point_attribut, life, regenaration_time, degat, puissance, items, inventory, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time):
    """S'occupe de gérer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    # --- Mouvements du joueur ---
        # Gauche
    if key[pygame.K_LEFT]:                         # Si la touche de gauche est appuyée
        hitbox.x -= player_speed                   # Déplacer la hitbox vers la gauche en fonction de la vitesse du joueur
        if direction == "right":
            selected_image = selected_image_left   # Si la direction précédente était à droite, changer l'image sélectionnée par celle du profil gauche
        direction = "left"                         # Mettre à jour la direction comme étant la gauche gauche

        # Droite
    if key[pygame.K_RIGHT]:                        # Si la touche de droite est appuyée
        hitbox.x += player_speed                   # Déplacer la hitbox vers la droite en fonction de la vitesse du joueur
        if direction == "left":
            selected_image = selected_image_right  # Si la direction précédente était à gauche, changer l'image sélectionnée par celle du profil droit
        direction = "right"                        # Mettre à jour la direction comme étant la droite
    
        # Le saut
    if key[pygame.K_SPACE] and on_ground:          # Si la touche de saut est appuyée et que le joueur est au sol
        velocity += jump_power                     # Appliquer la puissance de saut à la variable de vitesse
        on_ground = False                          # Le joueur n'est plus au sol après avoir sauté
        jump_sound.play()                          # Jouer le son du saut

        # La gravité
    if not on_ground:
        velocity += GRAVITY                        # Appliquer la gravité à la variable de vitesse pour faire retomber le joueur quand il n'est pas sur le sol
    
    # --- Le joueur attaquant ---
        # Attaque
    if key[pygame.K_d] and not attack and can_attack and state == "game":         # Si la touche D est appuyée et que le joueur n'est pas déjà en train d'attaquer
        attack = True
        start_time = time        # Enregistrer le temps de début de l'attaque pour gérer le délai entre les attaques
        if direction == "left":
            selected_image = selected_attack_left   # Si la direction est à gauche, changer l'image sélectionnée par celle de l'attaque du profil gauche
        else:
            selected_image = selected_attack_right  # Si la direction est à droite, changer l'image sélectionnée par celle de l'attaque du profil droit
        
        # Tirer une flèche uniquement si le cooldown est terminé
        if player == "archer" and can_attack:
            arrows.append(Arrow(hitbox.centerx, hitbox.centery, direction))
            last_attack_time = time        
                
        can_attack = False
        # Délai avant la prochaine attaque
    if attack and time - start_time >= attack_animation_time:
        if direction == "left":
            selected_image = selected_image_left    # L'image revient à celle du profil gauche de l'image selectionnée
        else:
            selected_image = selected_image_right   # L'image revient à celle du profil droit de l'image selectionnée
        attack = False                              # Après le délai d'attaque, le joueur n'est plus en train d'attaquer, et son image revient à celle de base
    if time - start_time >= attack_animation_time + attack_delay:
        can_attack = True

        # --- Gestion du cooldown de l'archer ---
    if player == "archer" and not can_attack:
        if time - last_attack_time >= attack_delay:
            can_attack = True  # Cooldown terminé, le joueur peut tirer à nouveau

    # --- Collision avec les plateformes ---
    on_ground = False
    for plateform in plateforms:
        if hitbox.colliderect(plateform):                                   # Si la hitbox du personnage (et donc le personnage) est en collision avec une plateforme

        # Collisions de chaque côté de la plateforme
            if velocity > 0 and hitbox.bottom - velocity <= plateform.top:  # Si le joueur est en train de tomber et que sa hitbox est juste au-dessus de la plateforme
                hitbox.bottom = plateform.top                               # Aligner le bas de la hitbox avec le dessus de la plateforme pour que le joueur puisse marcher dessus
                on_ground = True                                            # Lorsqu'une plateforme est en dessous du joueur, il est au sol
                velocity = 0                                                # La vitesse de chute est réinitialiser à 0 quand le joueur touche une plateforme
            if velocity < 0 and hitbox.top - velocity >= plateform.bottom:  # Si le joueur est en train de sauter et que sa hitbox est juste en dessous de la plateforme
                hitbox.top = plateform.bottom                               # Aligner le haut de la hitbox avec le bas de la plateforme, de sorte à ce que cette plateforme crée un plafond que le joueur ne peut pas traverser en sautant
                velocity = 0                                                # La vitesse de saut est réinitialiser à 0 quand le joueur touche une plateforme par en dessous
            if hitbox.right - player_speed <= plateform.left:               # Si le joueur se déplace vers la droite et que sa hitbox est juste à gauche de la plateforme
                hitbox.right = plateform.left                               # Aligner le côté droit de la hitbox avec le côté gauche de la plateforme, de sorte à ce que cette plateforme crée un mur que le joueur ne peut pas traverser en se déplaçant vers la droite
            if hitbox.left + player_speed >= plateform.right:               # Si le joueur se déplace vers la gauche et que sa hitbox est juste à droite de la plateforme
                hitbox.left = plateform.right                               # Aligner le côté gauche de la hitbox avec le côté droit de la plateforme, de sorte à ce que cette plateforme crée un mur que le joueur ne peut pas traverser en se déplaçant vers la gauche
            
    # Ramassage des items avec E (respecte la limite de 5 slots)
    if key[pygame.K_e]:
        for item in items[:]:
            if hitbox.colliderect(item.rect):
                if add_item_to_inventory(inventory, item):
                    items.remove(item)
                    last_inventory_feedback = f"{item.name} ramassé"
                else:
                    last_inventory_feedback = "Inventaire plein (5 slots)"
                last_inventory_feedback_time = time

    # Utilisation d'objets: maintenir 1..5 pendant 1 seconde
    for slot_index, key_code in enumerate(slot_keys):
        slot = inventory[slot_index]
        if key[key_code] and slot is not None and slot.get("usable", False):
            if slot_hold_start[slot_index] is None:
                slot_hold_start[slot_index] = time
                slot_use_lock[slot_index] = False

            if not slot_use_lock[slot_index] and (time - slot_hold_start[slot_index] >= ITEM_USE_HOLD_MS):
                life, feedback = use_inventory_slot(inventory, slot_index, life, max_life)
                last_inventory_feedback = feedback
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True
        else:
            slot_hold_start[slot_index] = None
            slot_use_lock[slot_index] = False

    # --- Monster movement ---
    for monster in monsters:
        if monster.alive:
            monster.update(hitbox, monsters)  # Si le monstre est vivant, il suit le joueur en fonction de la position de sa hitbox

    # --- Monster collision ---
    for monster in monsters[:]:
        if monster.alive and hitbox.colliderect(monster.rect):                           # Si le monstre est vivant et que sa hitbox est en collision avec celle du joueur

            if attack:
                if selected_image == selected_attack_left and player == "swordsman":     # Si le joueur attaque vers la gauche avec l'épée
                    if monster.rect.x < hitbox.x:                                        # Si le monstre est à gauche du joueur
                        monster.life -= degat + puissance                                                # Le monstre perd une vie
                        monster.rect.x -= PUSHBACK
                elif selected_image == selected_attack_right and player == "swordsman":  # Si le joueur attaque vers la droite avec l'épée
                    if monster.rect.x > hitbox.x:                                        # Si le monstre est à droite du joueur
                        monster.life -= degat + puissance                                                # Le monstre perd une vie
                        monster.rect.x += PUSHBACK
                else:
                    if time - last_damage_time >= invincibility_time:
                        life -= 1
                        last_damage_time = time

                if monster.life <= 0:                                                    # Quand le monstre n'a plus de vies
                    monster.alive = False                                                # Il est retiré du jeu
                    xp += monster.xp_reward
            
            else:                                                                        # Si le joueur n'attaque pas
                if time - last_damage_time >= invincibility_time:
                    life -= 1
                    last_damage_time = time

                    if hitbox.x < monster.rect.x:
                        hitbox.x -= PUSHBACK                                                 # Si le joueur est à gauche du monstre, il recule vers la gauche
                    else:
                        hitbox.x += PUSHBACK                                                 # Si le joueur est à droite du monstre, il recule vers la droite
        
        for arrow in arrows[:]:
            if monster.alive and arrow.rect.colliderect(monster.rect):                   # Si la hitbox de la flèche est en collision avec celle du monstre
                monster.life -= degat + puissance                                                        # Le monstre perd une vie
                if arrow.direction == "right":
                    monster.rect.x += PUSHBACK                                           # Si la flèche va vers la droite, le monstre recule vers la droite
                else:
                    monster.rect.x -= PUSHBACK                                           # Si la flèche va vers la gauche, le monstre recule vers la gauche
                arrows.remove(arrow)                                                     # Retirer la flèche du jeu
                if monster.life <= 0:
                    monster.alive = False                                                # Quand le monstre n'a plus de vies, il est retiré du jeu
                    xp += monster.xp_reward

    
    # --- Lorsque le héro n'a plus de vies ---
    if life <= 0:
        state = "death"  # Passer à l'écran de mort

    if time - last_damage_time >= regenaration_time and life < max_life:
        life += 1
        last_damage_time += 1500

    # --- Pour retourner à la page du départ ---
    if key[pygame.K_m]:
        state = "menu_attribut"    # Passer à l'état correspondant à celui du menu de départ
        pygame.mixer.music.stop()  # Arrêter la musique de fond

    hitbox.y += velocity  # Appliquer la variable de vitesse à la position verticale de la hitbox pour faire sauter ou faire tomber le joueur

    # --- Mort si le personnage est en dehors de l'écran ---
    if hitbox.top > HEIGHT + camera_y:
        state = "death"  # Si le personnage tombe en dessous de l'écran, passer à l'écran de mort
    xp_lvl_up = 0
    for i in range(level + 1):
        xp_lvl_up += i*2
    if xp >= xp_lvl_up:
        level += 1
        point_attribut += 5


    
    return start_time, direction, attack, on_ground, velocity, max_life, state, selected_image, selected_image_left, selected_image_right, selected_attack_left, selected_attack_right, hitbox, camera_y, last_attack_time, last_damage_time, can_attack, xp, level, point_attribut, life, regenaration_time, degat, items, inventory, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time

def death(state, event, restart_rect_death, end_rect_death, xp, point_attribut, level, inventory, items):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    if restart_rect_death.collidepoint(event.pos):
        state = "menu_de_debut"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
    elif end_rect_death.collidepoint(event.pos):
        state = "end"            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
    xp = 0
    level = 0
    point_attribut = 0
    inventory = {}
    items = [
    Item("Potion_vie", 260, 320, fiole_vie_img),
    Item("Potion_puissance", 550, 120, fiole_puissance_img),
    Item("Potion_vitesse", 260, 320, fiole_vitesse_img),
    Item("rune_vie", 550, 120, rune_vie_img),
    Item("rune_puissance", 260, 320, rune_puissance_img),
    Item("rune_vitesse", 550, 120, rune_vitesse_img),
    ]
    return state, xp, point_attribut, level, inventory, items

def death2(screen, WIDTH, HEIGHT, restart_rect_death, death_txt_font, WHITE, end_rect_death, monsters):
    """S'occupe d'afficher l'écran de mort, avec les boutons pour recommencer ou arrêter le jeu, et de réinitialiser les variables du jeu pour pouvoir recommencer à zéro si le joueur choisit de rejouer"""
    screen.fill(BLACK)         # Remplir l'écran de noir pour l'écran de mort
    pygame.mixer.music.stop()  # Arrêter la musique de fond quand le joueur meurt

    txt = death_txt_font.render("Bienvenue au Royaume des Defunts", True, (150, 20, 40))  # Définir le texte de l'écran de mort
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))                    # Afficher le texte de l'écran de mort

    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), restart_rect_death)                         # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), end_rect_death)                             # Dessiner un rectangle bleu pour le bouton d'arrêter

        # Leur texte
    txt_restart = text_font.render("Rejouer", True, WHITE)                            # Définir le texte du bouton pour recommencer
    txt_end = text_font.render("Quitter", True, WHITE)                                # Définir le texte du bouton pour arrêter
    
        # Les afficher
    screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect_death.center))  # Afficher le texte du bouton pour recommencer
    screen.blit(txt_end, txt_end.get_rect(center=end_rect_death.center))              # Afficher le texte du bouton pour arrêter
    
    
    for monster in monsters:
        monster.reset()    # Faire recommencer à 0 les monstres avec les 3 vies de chaque monstre
    pygame.display.flip()  # Tout générer sur la fenêtre

def end(running, screen, text_font, WIDTH, HEIGHT, WHITE):
    """Se charge d'afficher l'écran de fin du jeu, avec un message de remerciement, et de fermer la fenêtre après quelques secondes"""
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base pour l'écran de fin
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, WHITE)  # Définir le texte de l'écran de fin
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//2)))                # Afficher le texte de l'écran de fin
    pygame.display.flip()                                                         # Tout générer sur la fenêtre
    pygame.time.wait(2500)                                                        # Attendre 2.5 secondes avant de fermer la fenêtre
    running = False                                                               # Sortir de la boucle principale
    return running

def menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, level, player_speed, point_attribut, max_life, regenaration_time, attack_delay, puissance):
    """Se charge de gérer les clics sur les boutons pour recommencer ou arrêter le jeu lorsqu'on est sur l'écran de mort"""
    if continue_rect.collidepoint(event.pos):
        state = "game"  # Si le joueur clique sur le bouton pour recommencer, retourner à l'état du menu de départ
        pygame.mixer.music.play()
    elif speed_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1            # Si le joueur clique sur le bouton pour arrêter, passer à l'état de fin du jeu
            player_speed = (player_speed * 10 + 1) / 10
    elif vitality_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1
            max_life += 1
            regenaration_time -= 500
    elif puissance_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1
            puissance += degat//40
    elif attack_delay_rect.collidepoint(event.pos):
        if point_attribut>0:
            point_attribut -= 1
            attack_delay -= 10
    return level, state, player_speed, point_attribut, max_life, regenaration_time, attack_delay, puissance

def menu_attribut(screen, text_font, WIDTH, HEIGHT, RED, level, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player_speed, point_attribut, max_life, regenaration_time, attack_delay):
   
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base
    txt = text_font.render("ATTRIBUT", True, RED)                                 # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//5)))                # Afficher le texte de l'écran
    txt = text_font.render("level " + str(level), True, WHITE)                                    # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3, HEIGHT//4)))                # Afficher le texte de l'écran
    txt = text_font.render("point(s) d'attribut(s) " + str(point_attribut), True, WHITE)                                    # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3*2, HEIGHT//4)))                # Afficher le texte de l'écran