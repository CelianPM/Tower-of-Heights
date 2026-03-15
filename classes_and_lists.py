import pygame, math
import globals, imports, inventory

pygame.init()


# =================================
# CLASSES
# =================================

# --- Heros ---
class Player:
    def __init__(self, on_ground):
        """Définit les variables requises par le joueur et importe la viariable on_ground pour en avoir une spécialement pour le joueur."""
        self.speed = 0            # Vitesse du joueur
        self.jump_power = -15     # Puissance de saut
        self.attack = False       # Le héro n'attaque pas encore
        self.direction = "right"  # Direction initiale
        self.attack_delay = 0     # Le temps qu'il faut attendre avant de pouvoir rattaquer
        self.max_life = 0         # Nombres de vies de départ
        self.last_attack_time = 0
        self.attack_animation_time = 0
        self.can_attack = True
        self.level = 0
        self.point_attribut = 0
        self.last_damage_time = 0
        self.regeneration_time = 0
        self.invincibility_time = 1000
        self.degat = 0
        self.puissance = 0
        self.speed_bonus = 0
        self.power_bonus = 0
        self.regeneration_bonus = False
        self.speed_effect_end_time = 0
        self.power_effect_end_time = 0
        self.regeneration_effect_end_time = 0


        self.selected_image = None         # Image selectionnée, non-definie pour l'instant
        self.selected_image_left = None    # Profil gauche de l'image selectionnée, non-definie pour l'instant
        self.selected_image_right = None   # Profil droit de l'image sélectionnée, non-definie pour l'instant
        self.selected_attack = None        # Image de base de l'attaque, non-definie pour l'instant
        self.selected_attack_left = None   # Profil gauche de l'image attaquant, non-definie pour l'instant
        self.selected_attack_right = None  # Profil droit de l'image attaquant, non-definie pour l'instant
        self.perso_rect = None             # Rect de l'image selectionnée, non-definie pour l'instant
        self.hero = None                   # Qui sera le héro, non-definie pour l'instant
        self.hitbox = None                 # Hitbox du personnage ( pour les collisions), non-definie pour l'instant
        self.xp = 0
        self.on_ground = on_ground
        self.xp_lvl_up = 0

        self.frame_index = 0
        self.animation_speed = 0.1
        self.prev_hitbox = None
    
    def select_the_player(self):
        """Se charge de gérer les clics sur les personnages dans le menu de départ, et de définir les variables correspondantes en fonction du personnage choisi."""
        
        if self.hero == "archer":
            self.attack_delay = 800                                                             # Définit le temps entre les attaques pour l'archer, pour qui c'est plus long
            self.selected_image = imports.archer_image                                          # L'image sélectionnée est celle de l'archer
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image sélectionnée
            self.selected_attack = imports.attacking_archer                                     # Télécharge l'image de l'attaque de l'archer
            self.speed = 3
            self.max_life = 4
            self.regeneration_time = 25000
            self.degat = 600
            self.walk_frames_right = [
                imports.post_attacking_archer,
            ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]

        elif self.hero == "swordsman":
            self.attack_delay = 300                                                             # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
            self.selected_image = imports.swordsman_image                                       # L'image sélectionnée est celle de l'épéiste
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image sélectionnée
            self.selected_attack = imports.attacking_swordsman                                  # Télécharge l'image de l'attaque de l'épéiste
            self.speed = 4
            self.max_life = 5
            self.regeneration_time = 20000
            self.degat = 500
            self.walk_frames_right = [
                imports.standing_swordsman,
                imports.walking_swordsman1,
                imports.walking_swordsman2,
            ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]

        elif self.hero == "ninja":
            self.attack_delay = 200                                                             # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
            self.selected_image = imports.ninja_image                                           # L'image sélectionnée est celle de l'épéiste
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image sélectionnée
            self.selected_attack = imports.ninja                                                # Télécharge l'image de l'attaque de l'épéiste
            self.speed = 5
            self.max_life = 3
            self.regeneration_time = 20000
            self.degat = 300
            self.walk_frames_right = [
                imports.ninja,
            ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]

        self.attack_animation_time = 300
        self.selected_attack_right = self.selected_attack                                                          # Profil droit de l'image attaquant
        self.selected_attack_left = pygame.transform.flip(self.selected_attack, True, False)                       # Profil gauche de l'image attaquant
        self.perso_rect = self.selected_image.get_rect(topleft=(200, 300))                                         # Rect de l'image
        self.hitbox = pygame.Rect(self.perso_rect.x, self.perso_rect.y, self.perso_rect.width - 60, self.perso_rect.height - 10)  # Hitbox du personnage
        self.life = self.max_life

    def animate(self, frames):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        
        return frames[int(self.frame_index)]
    
    def move(self, jump_sound, state, time, key, velocity, start_time, arrows, shurikens):
        """Se charge de définir les mouvements du joueur et ses attaques."""
        self.prev_hitbox = self.hitbox.copy()

        # --- Mouvements du joueur ---
            # Gauche
        if key[pygame.K_LEFT]:                                   # Si la touche de gauche est appuyée
            self.hitbox.x -= self.speed                          # Déplacer la hitbox vers la gauche en fonction de la vitesse du joueur
            if self.direction == "right":
                self.selected_image = self.selected_image_left   # Si la direction précédente était à droite, changer l'image sélectionnée par celle du profil gauche
            self.direction = "left"                              # Mettre à jour la direction comme étant la gauche gauche

            # Droite
        if key[pygame.K_RIGHT]:                                  # Si la touche de droite est appuyée
            self.hitbox.x += self.speed                          # Déplacer la hitbox vers la droite en fonction de la vitesse du joueur
            if self.direction == "left":
                self.selected_image = self.selected_image_right  # Si la direction précédente était à gauche, changer l'image sélectionnée par celle du profil droit
            self.direction = "right"                             # Mettre à jour la direction comme étant la droite

        is_moving = key[pygame.K_LEFT] or key[pygame.K_RIGHT]
        if is_moving and not self.attack:
            if self.direction == "left":
                self.selected_image = self.animate(self.walk_frames_left)
            else:
                self.selected_image = self.animate(self.walk_frames_right)

            # Le saut
        if key[pygame.K_SPACE] and self.on_ground:               # Si la touche de saut est appuyée et que le joueur est au sol
            velocity += self.jump_power                          # Appliquer la puissance de saut à la variable de vitesse
            self.on_ground = False                               # Le joueur n'est plus au sol après avoir sauté
            imports.jump_sound.play()                                    # Jouer le son du saut
        
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_SPACE] and not self.attack:  # Si aucune touche de déplacement n'est appuyée et que le joueur n'attaque pas
            self.frame_index = 0
            if self.direction == "left":
                self.selected_image = self.selected_image_left       # L'image revient à celle du profil gauche de l'image selectionnée
            else:
                self.selected_image = self.selected_image_right      # L'image revient à celle du profil droit de l'image selectionnée

            # La gravité
        if not self.on_ground:
            velocity += globals.GRAVITY  # Appliquer la gravité à la variable de vitesse pour faire retomber le joueur quand il n'est pas sur le sol

        # --- L'attaque du joueur ---
            # Attaque
        if key[pygame.K_d] and not self.attack and self.can_attack and state == "game":  # Si la touche D est appuyée et que le joueur n''est pas déjà en train d''attaquer
            self.attack = True
            start_time = time        # Enregistrer le temps de début de l''attaque pour gérer le délai entre les attaques
            self.last_attack_time = time

            if self.direction == "left":
                self.selected_image = self.selected_attack_left   # Si la direction est à gauche, changer l''image sélectionnée par celle de l''attaque du profil gauche
            else:
                self.selected_image = self.selected_attack_right  # Si la direction est à droite, changer l''image sélectionnée par celle de l''attaque du profil droit
            
            if self.hero == "archer":
                arrows.append(Arrow(self.hitbox.centerx, self.hitbox.centery, self))
                self.last_attack_time = time 

            if self.hero =="ninja":
                shurikens.append(Shuriken(self.hitbox.centerx, self.hitbox.centery, self))
                self.last_attack_time = time

            self.can_attack = False

        # Délai avant la prochaine attaque
        if self.attack and time - start_time >= self.attack_animation_time:
            if self.direction == "left":
                self.selected_image = self.selected_image_left       # L'image revient à celle du profil gauche de l'image selectionnée
            else:
                self.selected_image = self.selected_image_right   # L'image revient à celle du profil droit de l'image selectionnée
            self.attack = False                                   # Après le délai d'attaque, le joueur n'est plus en train d'attaquer, et son image revient à celle de base
        
        if time - start_time >= self.attack_animation_time + self.attack_delay:  # Après le délai d'attaque plus le temps entre les attaques, le joueur peut à nouveau attaquer
            self.can_attack = True

        if not self.can_attack:
            if self.hero == "archer" and time - self.last_attack_time >= self.attack_delay:
                self.can_attack = True

        self.hitbox.y += velocity  # Appliquer la variable de vitesse à la position verticale de la hitbox pour faire sauter ou faire tomber le joueur
        return velocity, start_time
    
    def update_potion_effects(self, time):
        if self.speed_bonus > 0 and time >= self.speed_effect_end_time:
            self.speed -= self.speed_bonus
            self.speed_bonus = 0
            self.speed_effect_end_time = 0

        if self.power_bonus > 0 and time >= self.power_effect_end_time:
            self.puissance -= self.power_bonus
            self.power_bonus = 0
            self.power_effect_end_time = 0

        if self.regeneration_bonus == True and time >= self.regeneration_effect_end_time:
            self.regeneration_time = self.regeneration_time * 2
            self.regeneration_bonus = False
            self.regeneration_effect_end_time = 0


    def platform_collisions(self, platforms, velocity):
        """S'occupe des collisoins avec les plateformes : si le joueur est en contact avec une plateforme, il n epeut pas la traverser."""
        self.on_ground = False                                                      # Par défaut, le joueur n'est pas au sol, et il le devient seulement s'il est en collision avec une plateforme en dessous de lui
        previous_hitbox = self.prev_hitbox if self.prev_hitbox else self.hitbox.copy()

        for platform in platforms:
            if not self.hitbox.colliderect(platform):
                continue

            horizontal_overlap = self.hitbox.right > platform.left and self.hitbox.left < platform.right
                
            # Collisions du haut de la plateforme
            if velocity >= 0 and horizontal_overlap and previous_hitbox.bottom <= platform.top:
                self.hitbox.bottom = platform.top
                self.on_ground = True
                velocity = 0
                continue                                                   # La vitesse de chute est réinitialiser à 0 quand le joueur touche une plateforme
   
            # Collisions du bas de la plateforme
            if velocity < 0 and horizontal_overlap and previous_hitbox.top >= platform.bottom:
                self.hitbox.top = platform.bottom
                velocity = 0
                continue                                                   # La vitesse de saut est réinitialiser à 0 quand le joueur touche une plateforme par en dessous

            # Collisions des côtés de la plateforme
            if previous_hitbox.right <= platform.left and self.hitbox.right > platform.left:
                self.hitbox.right = platform.left
            elif previous_hitbox.left >= platform.right and self.hitbox.left < platform.right:
                self.hitbox.left = platform.right
            else:
                overlap_left = self.hitbox.right - platform.left
                overlap_right = platform.right - self.hitbox.left
                if overlap_left < overlap_right:
                    self.hitbox.right = platform.left
                else:
                    self.hitbox.left = platform.right
                    
        return velocity

    def monster_collisions(self, monsters, time, arrows, shurikens = None):
        """Se charge des collisions entre le joueur et les monstres."""
        for monster in monsters[:]:
            if monster.alive and self.hitbox.colliderect(monster.rect):                                   # Si le monstre est vivant et que sa hitbox est en collision avec celle du joueur

                if self.attack:
                    if self.selected_image == self.selected_attack_left and self.hero == "swordsman":     # Si le joueur attaque vers la gauche avec l'épée
                        if monster.rect.x < self.hitbox.x:                                                # Si le monstre est à gauche du joueur
                            monster.life -= self.degat + self.puissance                                   # Le monstre perd une vie
                            monster.rect.x -= globals.PUSHBACK
                    elif self.selected_image == self.selected_attack_right and self.hero == "swordsman":  # Si le joueur attaque vers la droite avec l'épée
                        if monster.rect.x > self.hitbox.x:                                                # Si le monstre est à droite du joueur
                            monster.life -= self.degat + self.puissance                                   # Le monstre perd une vie
                            monster.rect.x += globals.PUSHBACK
                    else:
                        if time - self.last_damage_time >= self.invincibility_time:
                            self.life -= 1
                            self.last_damage_time = time

                    if monster.life <= 0:                                   # Quand le monstre n'a plus de vies
                        monster.alive = False                               # Il est retiré du jeu
                        self.xp += monster.xp_reward
                
                else:                                                       # Si le joueur n'attaque pas
                    if time - self.last_damage_time >= self.invincibility_time:
                        self.life -= 1
                        self.last_damage_time = time

                        if self.hitbox.x < monster.rect.x:
                            self.hitbox.x -= globals.PUSHBACK                       # Si le joueur est à gauche du monstre, il recule vers la gauche
                        else:
                            self.hitbox.x += globals.PUSHBACK                       # Si le joueur est à droite du monstre, il recule vers la droite
            
            for arrow in arrows[:]:
                if monster.alive and arrow.rect.colliderect(monster.rect):  # Si la hitbox de la flèche est en collision avec celle du monstre
                    monster.life -= self.degat + self.puissance             # Le monstre perd une vie
                    if arrow.direction == "right":
                        monster.rect.x += globals.PUSHBACK                          # Si la flèche va vers la droite, le monstre recule vers la droite
                    else:
                        monster.rect.x -= globals.PUSHBACK                          # Si la flèche va vers la gauche, le monstre recule vers la gauche
                    arrows.remove(arrow)                                    # Retirer la flèche du jeu
                    if monster.life <= 0:
                        monster.alive = False                               # Quand le monstre n'a plus de vies, il est retiré du jeu
                        self.xp += monster.xp_reward

            if shurikens is None :
                continue
            for shuriken in shurikens[:]:
                if monster.alive and shuriken.rect.colliderect(monster.rect):  # Si la hitbox de la flèche est en collision avec celle du monstre
                    monster.life -= self.degat + self.puissance             # Le monstre perd une vie
                    if shuriken.direction == "right":
                        monster.rect.x += globals.PUSHBACK                          # Si la flèche va vers la droite, le monstre recule vers la droite
                    else:
                        monster.rect.x -= globals.PUSHBACK                          # Si la flèche va vers la gauche, le monstre recule vers la gauche
                    shurikens.remove(shuriken)                                    # Retirer la flèche du jeu
                    if monster.life <= 0:
                        monster.alive = False                               # Quand le monstre n'a plus de vies, il est retiré du jeu
                        self.xp += monster.xp_reward
    
    def player_xp(self):
        """Se charge de gérer l'XP du joueur et de faire monter son niveau quand il atteint le nombre d'XP requis."""
        self.xp_lvl_up = 0
        for i in range(self.level + 1):
            self.xp_lvl_up += i*2
        if self.xp >= self.xp_lvl_up:
            self.level += 1
            self.point_attribut += 5
    
    def player_inventory(self, items, inventory_list, key, time, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed):
        """Gère le ramassage d'objet avec E et un feedback simple à l'écran."""

        if globals.key[pygame.K_e] and not pickup_pressed:
            pickup_pressed = True
            for item in items[:]:
                if self.hitbox.colliderect(item.rect):
                    if inventory.add_item_to_inventory(inventory_list, item):
                        last_inventory_feedback = f"{item.name} ramassé"
                        items.remove(item)
                    else:
                        last_inventory_feedback = "Inventaire plein (5 slots)"
                    last_inventory_feedback_time = time
                    break

        if not globals.key[pygame.K_e]:
            pickup_pressed = False

        return items, inventory_list, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed

    def player_death(self, time, camera_y, state):
        """Se charge de dire quand le joueur est mort : lorsqu'il est hors de la fenêtre ou lorsqu'il n'a plus de vies (à cause des monstres)."""
            # --- Lorsque le héro n'a plus de vies ---
        if self.life <= 0:
            state = "death"  # Passer à l'écran de mort
        
        if time - self.last_damage_time >= self.regeneration_time and self.life < self.max_life:
            self.life += 1
            self.last_damage_time += 1500
            
            # --- Mort si le personnage est en dehors de l'écran ---
        if self.hitbox.top > globals.HEIGHT + camera_y:
            state = "death"  # Si le personnage tombe en dessous de l'écran, passer à l'écran de mort
        
        return state


# --- Monstres ---
    # General
class Monster:
    def __init__(self, x, y, image_right = None, life = 0, speed = 0, xp_reward = 10):
        self.spawn_x = x                                                                                 # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.spawn_y = y                                                                                 # La position de spawn du monstre, qui est utilisée pour réinitialiser sa position quand il meurt
        self.image_right = image_right                                                                   # Le profil droit du monstre est l'image du profil droit
        self.image_left = pygame.transform.flip(image_right, True, False) if image_right else None       # Le profil gauche du monstre est l'image du profil gauche
        self.image = self.image_right                                                                    # L'image de base du monstre est le profil droit
        self.rect = self.image.get_rect(topleft = (x, y)) if image_right else pygame.Rect(x, y, 50, 50)  # Le rectangle de collision du monstre est basé sur l'image du profil droit, et sa position est définie par les coordonnées x et y
        self.life = life                                                                                 # Le monstre commence avec 3 vies
        self.max_life = life                                                                             # Le monstre a un maximum de 3 vies, et cette variable est utilisée pour réinitialiser la vie du monstre quand il meurt
        self.alive = True                                                                                # Le monstre est vivant au début du jeu, et cette variable est utilisée pour déterminer s'il doit être affiché et s'il peut interagir avec le joueur
        self.speed = speed                                                                               # La vitesse à laquelle le monstre suit le joueur, qui est constante et ne change pas selon la direction
        self.xp_reward = xp_reward                                                                       # Quantité d'XP donnée quand ce monstre est vaincu
        self.frame_index = 0
        self.animation_speed = 0.15

    def overlap(self, monsters, horizontal_only = False):
        for other in monsters:
            if other is self or not other.alive or other.__class__ is not self.__class__:
                continue
            if not self.rect.colliderect(other.rect):
                continue

            overlap_x = min(self.rect.right, other.rect.right) - max(self.rect.left, other.rect.left)
            overlap_y = min(self.rect.bottom, other.rect.bottom) - max(self.rect.top, other.rect.top)

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            if horizontal_only or overlap_x < overlap_y:
                push_x = math.ceil(overlap_x / 2)
                if self.rect.centerx < other.rect.centerx:
                    self.rect.x -= push_x
                else:
                    self.rect.x += push_x
            else:
                push_y = math.ceil(overlap_y / 2)
                if self.rect.centery < other.rect.centery:
                    self.rect.y -= push_y
                else:
                    self.rect.y += push_y

    def update(self, player_rect, monsters, plateforms = None):
        if not self.alive:
            return                         # Si le monstre n'est pas vivant, il ne fait rien et ne suit pas le joueur
        if self.rect.x > player_rect.x :
            self.rect.x -= self.speed      # Le monstre se déplace vers la gauche si sa position x est plus grande que celle du joueur
            if self.image_left:
                self.image = self.image_left
        elif self.rect.x < player_rect.x:
            self.rect.x += self.speed      # Le monstre se déplace vers la droite si sa position x est plus petite que celle du joueur
            if self.image_right:
                self.image = self.image_right  # Le monstre affiche son profil droit pour se déplacer vers la droite
        
        self.overlap(monsters, horizontal_only = True)
    
    def reset(self):
        self.alive = True                                 # Quand le monstre est réinitialisé, il redevient vivant
        self.life = self.max_life                         # Quand le monstre est réinitialisé, il retrouve sa vie maximale (qui est de 3)
        self.rect.topleft = (self.spawn_x, self.spawn_y)  # Quand le monstre est réinitialisé, il retourne à sa position de spawn

    def draw(self, screen, camera_y = 0):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))  # Afficher le monstre à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra

    # Slug
class Slug(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, 
            y, 
            image_right = imports.slug,  # Image spécifique
            life=1500,             # Vie spécifique du Slug
            speed=2,               # Vitesse spécifique du Slug
            xp_reward = 8
        )

        self.velocity_y = 0
        self.direction = 1
        self.on_ground = False

    def update(self, player_rect, monsters, platforms = None):
        if not self.alive:
            return

        if platforms is None:
            platforms = []

        # Déplacement horizontal (puis résolution des côtés)
        previous_x = self.rect.x
        self.rect.x += self.speed * self.direction

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue
            if previous_x + self.rect.width <= platform.left:
                self.rect.right = platform.left
                self.direction = -1
            elif previous_x >= platform.right:
                self.rect.left = platform.right
                self.direction = 1

        # Gravité + déplacement vertical (puis résolution haut/bas)
        previous_y = self.rect.y
        self.velocity_y += globals.GRAVITY
        self.rect.y += self.velocity_y

        on_ground = False

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            crossed_top = previous_y + self.rect.height <= platform.top and self.rect.bottom >= platform.top
            if self.velocity_y >= 0 and crossed_top:
                self.rect.bottom = platform.top
                self.velocity_y = 0
                on_ground = True
                continue

            crossed_bottom = previous_y >= platform.bottom and self.rect.top <= platform.bottom
            if self.velocity_y < 0 and crossed_bottom:
                self.rect.top = platform.bottom
                self.velocity_y = 0
                continue

        # --- détection du bord de plateforme ---
        if on_ground:
            front_x = self.rect.centerx + (self.direction * self.rect.width // 2)
            front_y = self.rect.bottom + 5

            ground_ahead = any(platform.collidepoint(front_x, front_y) for platform in platforms)
            if not ground_ahead:
                self.direction *= -1

        # --- image selon direction ---
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

        self.on_ground = on_ground
        self.overlap(monsters, horizontal_only = True)

    # Chauve-souris
class Bat(Monster):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            image_right = imports.bat1,  # Image spécifique
            life=300,             # Moins de vie qu'un slug
            speed=3,              # Plus rapide qu'un slug
            xp_reward = 2
        )
        self.frames_right = [imports.bat1, imports.bat2]
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]

    def update(self, player_rect, monsters, platforms):
        if not self.alive:
            return

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery

        distance = math.sqrt(dx*dx + dy*dy)

        if distance != 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames_right):
            self.frame_index = 0
        current_frame = int(self.frame_index)

        if dx < 0:
            self.image = self.frames_left[current_frame]
        else:
            self.image = self.frames_right[current_frame]
        
        self.overlap(monsters)


# --- Objets ---
    # General
class Projectile:
    def __init__(self, x, y, player):
        self.direction = player.direction     # La direction du projectile est définie par la direction du joueur au moment du tir, et ne change pas après

    def update(self, platforms, arrows, shurikens):
        if self.direction == "right":
            self.rect.x += self.speed  # La flèche se déplace vers la droite si sa direction est à droite
        else:
            self.rect.x -= self.speed  # La flèche se déplace vers la gauche si sa direction est à gauche
        if self.rect.right < 0 or self.rect.left > globals.WIDTH:  # Si la flèche sort de l'écran, elle est retirée du jeu
            if self in arrows:
                arrows.remove(self)
            if self in shurikens:
                shurikens.remove(self)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self in arrows:
                    arrows.remove(self)
                if self in shurikens:
                    shurikens.remove(self)
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Afficher la flèche à sa position actuelle sur l'écran

    # Fleche
class Arrow(Projectile):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.speed = 10                # La vitesse de la flèche, qui est constante et ne change pas selon la direction

        if self.direction == "right":
            self.image = imports.arrow_right   # Le profil droit de la flèche est utilisé si la direction est à droite
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.image = imports.arrow_left    # Le profil gauche de la flèche est utilisé si la direction est à gauche
            self.rect = self.image.get_rect(midright = (x, y))

    # Shuriken
class Shuriken(Projectile):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.base_image = imports.shuriken
        self.image = self.base_image
        self.speed = 12                # La vitesse du shuriken, qui est constante et ne change pas selon la direction
        self.angle = 0                 # L'angle de rotation initial du shuriken
        self.rotation_speed = 15       # La vitesse de rotation du shuriken, qui est constante et ne change pas selon la direction


        if self.direction == "right":
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
             self.rect = self.image.get_rect(midright = (x, y))
        self.image = self.base_image

    def update(self, platforms, arrows, shurikens):
        super().update(platforms, arrows, shurikens)
        if self not in shurikens:
            return  # Si le shuriken a été retiré du jeu (par exemple, s'il a touché une plateforme), ne pas continuer à mettre à jour sa rotation
        
        center = self.rect.center  # Conserver le centre du shuriken avant de faire tourner l'image
        self.angle = (self.angle + self.rotation_speed) % 360  # Mettre à jour l'angle de rotation du shuriken
        self.image = pygame.transform.rotate(self.base_image, self.angle)  # Faire tourner l'image du shuriken en fonction de l'angle
        self.rect = self.image.get_rect(center=self.rect.center)  # Mettre à jour le rect du shuriken pour qu'il reste centré sur sa position actuelle


# =================================
# LISTES
# =================================

# --- Listes des monstres ---
monsters = []


# ---Listes des projectiles---
    # Fleches de l'archer
arrows = []

    # Shurikens du ninja
shurikens = []
