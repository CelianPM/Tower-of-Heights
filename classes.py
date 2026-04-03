import pygame, math
import globals, imports, inventory
from random import randint


pygame.init()


# --- Importer les listes
    # Listes des monstres
monsters = globals.monsters

    # Liste des machines a runes
rune_machines = globals.rune_machines

   # Hazards
hazards = globals.hazards


# =================================
# HEROS
# =================================
class Player:
    def __init__(self, on_ground):
        """Definit les variables requises par le joueur et importe la viariable on_ground pour en avoir une specialement pour le joueur."""
        self.speed = 0            # Vitesse du joueur
        self.jump_power = -15     # Puissance de saut
        self.attack = False       # Le hero n'attaque pas encore
        self.direction = "right"  # Direction initiale
        self.attack_delay = 0     # Le temps qu'il faut attendre avant de pouvoir rattaquer
        self.max_life = 0         # Nombres de vies de depart
        self.last_attack_time = 0
        self.attack_animation_time = 0
        self.can_attack = True   # Si le heros peut attaquer, defini comme oui au debut
        self.level = 0           # Le niveau du joueur, qui augmente avec le temps en gagnant de l'XP
        self.point_attribut = 0  # Le nombre de points d'attibuts, utilises pour ameliorer les caracteristiques du joueur
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
        self.pushback = 0
        self.is_speed_lowered = False
        self.last_player_speed = 0
        self.speed_click = 0




        self.selected_image = None         # Image selectionnee, non-definie pour l'instant
        self.selected_image_left = None    # Profil gauche de l'image selectionnee, non-definie pour l'instant
        self.selected_image_right = None   # Profil droit de l'image selectionnee, non-definie pour l'instant
        self.selected_attack = None        # Image de base de l'attaque, non-definie pour l'instant
        self.selected_attack_left = None   # Profil gauche de l'image attaquant, non-definie pour l'instant
        self.selected_attack_right = None  # Profil droit de l'image attaquant, non-definie pour l'instant
        self.perso_rect = None             # Rect de l'image selectionnee, non-definie pour l'instant
        self.hero = None                   # Qui sera le hero, non-definie pour l'instant
        self.hitbox = None                 # Hitbox du personnage ( pour les collisions), non-definie pour l'instant
        self.xp = 0                        # L'experience du joueur, qui augmente en tuant des monstres et permet de monter de niveau
        self.on_ground = on_ground         # Variable pour savoir si le joueur est au sol, utilisee pour gerer les sauts
        self.xp_lvl_up = 0                 # L'experience necessaire pour monter de niveau, qui augmente a chaque niveau


        self.frame_index = 0
        self.animation_speed = 0.27
        self.prev_hitbox = None
        self.weapon = None
        self.attack_transition_time = 0
        self.post_attack_until = 0
  
    def select_the_player(self):
        """Se charge de gerer les clics sur les personnages dans le menu de depart, et de definir les variables correspondantes en fonction du personnage choisi."""
      
        if self.hero == "archer":
            self.attack_delay = 800                                                             # Definit le temps entre les attaques pour l'archer, pour qui c'est plus long
            self.selected_image = imports.archer_image                                          # L'image selectionnee est celle de l'archer
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image selectionnee
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image selectionnee
            self.selected_attack = imports.attacking_archer                                     # Telecharge l'image de l'attaque de l'archer
            self.speed = 3
            self.max_life = 4
            self.regeneration_time = 25000
            self.degat = 600
            self.walk_frames_right = [
               imports.archer_image,
           ]
          
            self.attack_frames_right = [
                imports.attacking_archer,
                imports.post_attacking_archer,
           ]
            self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames_right]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]
          
        elif self.hero == "swordsman":
            self.attack_delay = 300                                                             # Definit le temps entre les attaques pour l'epeiste, pour qui c'est plus court
            self.selected_image = imports.swordsman_image                                       # L'image selectionnee est celle de l'epeiste
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image selectionnee
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image selectionnee
            self.selected_attack = imports.attacking_swordsman                                  # Telecharge l'image de l'attaque de l'epeiste
            self.speed = 4
            self.max_life = 5
            self.regeneration_time = 20000
            self.degat = 500
            self.walk_frames_right = [
                imports.standing_swordsman,
                imports.walking_swordsman1,
                imports.standing_swordsman,
                imports.walking_swordsman2,
           ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]


        elif self.hero == "ninja":
            self.attack_delay = 200                                                             # Definit le temps entre les attaques pour l'epeiste, pour qui c'est plus court
            self.selected_image = imports.ninja_image                                           # L'image selectionnee est celle de l'epeiste
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image selectionnee
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image selectionnee
            self.selected_attack = imports.ninja                                                # Telecharge l'image de l'attaque de l'epeiste
            self.speed = 5
            self.max_life = 3
            self.regeneration_time = 20000
            self.degat = 300
            self.walk_frames_right = [
                imports.ninja,
           ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]


        elif self.hero == "beggar":
            self.attack_delay = 500                                                             # Definit le temps entre les attaques pour le mendiant, pour qui c'est moyen
            self.selected_image = imports.beggar_image                                           # L'image selectionnee est celle du mendiant
            self.selected_image_right = self.selected_image                                     # Profil droit de l'image selectionnee
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)  # Profil gauche de l'image selectionnee
            self.selected_attack = imports.attacking_beggar                                                # Telecharge l'image de l'attaque du mendiant
            self.speed = 2
            self.max_life = 6
            self.regeneration_time = 30000
            self.degat = 400
            self.walk_frames_right = [
                imports.beggar_walk1,
                imports.beggar_walk2,
                imports.beggar_walk3,
                imports.beggar_walk4,
           ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]


        self.attack_animation_time = 300
        self.selected_attack_right = self.selected_attack                                                          # Profil droit de l'image attaquant
        self.selected_attack_left = pygame.transform.flip(self.selected_attack, True, False)                       # Profil gauche de l'image attaquant
        self.perso_rect = self.selected_image.get_rect(topleft=(200, 300))                                         # Rect de l'image
        self.hitbox = pygame.Rect(0, 0, 32, 112)  # Hitbox du personnage
        self.life = math.floor(self.max_life)


    def animate(self, frames):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
      
        return frames[int(self.frame_index)]
  
    def projectile_spawn_position(self):
        """Définit la position de spawn des projectiles du joueur en fonction de sa direction et de son personnage."""
        image_width = self.selected_image.get_width()
        image_height = self.selected_image.get_height()
        image_top = self.hitbox.bottom - image_height
        image_left = self.hitbox.x - (image_width - self.hitbox.width - 20)
        spawn_offsets = {
            "archer" : {
                "left" : (22,0.48),
                "right" : (image_width - 22,0.48),
            },
            "beggar" : {
                "left" : (20,0.44),
                "right" : (image_width - 20,0.44),


            },
            "ninja" : {
                "left" : (18,0.48),
                "right" : (image_width - 18,0.48),
            }
        }
        hero_offsets  = spawn_offsets.get(self.hero, {
            "left" : (16, 0.45),
            "right" : (image_width - 16, 0.45)
        })
        offset_x, offset_y_ratio = hero_offsets[self.direction]


        projectile_x = image_left + offset_x
        projectile_y = image_top + int(image_height * offset_y_ratio)
        return projectile_x, projectile_y
  
    def hitbox_attack(self):
        image_width = self.selected_image.get_width()
        image_height = self.selected_image.get_height()
        image_y = self.hitbox.bottom - image_height
        image_x = self.hitbox.x - 30
      
        return pygame.Rect(image_x, image_y, image_width, image_height)


  
    def move(self, jump_sound, state, time, key, velocity, start_time, arrows, shurikens):
        """Se charge de definir les mouvements du joueur et ses attaques."""
        self.prev_hitbox = self.hitbox.copy()


        # --- Mouvements du joueur ---
            # Gauche
        if key[pygame.K_LEFT]:                                   # Si la touche de gauche est appuyee
            self.hitbox.x -= self.speed                          # Deplacer la hitbox vers la gauche en fonction de la vitesse du joueur
            if self.direction == "right":
                self.selected_image = self.selected_image_left   # Si la direction precedente etait a droite, changer l'image selectionnee par celle du profil gauche
            self.direction = "left"                              # Mettre a jour la direction comme etant la gauche gauche


            # Droite
        if key[pygame.K_RIGHT]:                                  # Si la touche de droite est appuyee
            self.hitbox.x += self.speed                          # Deplacer la hitbox vers la droite en fonction de la vitesse du joueur
            if self.direction == "left":
                self.selected_image = self.selected_image_right  # Si la direction precedente etait a gauche, changer l'image selectionnee par celle du profil droit
            self.direction = "right"                             # Mettre a jour la direction comme etant la droite


        is_moving = key[pygame.K_LEFT] or key[pygame.K_RIGHT]
        if is_moving and not self.attack and self.on_ground:
            if self.direction == "left":
                self.selected_image = self.animate(self.walk_frames_left)
            else:
                self.selected_image = self.animate(self.walk_frames_right)


            # Le saut
        if key[pygame.K_SPACE] and self.on_ground:               # Si la touche de saut est appuyee et que le joueur est au sol
            velocity += self.jump_power                          # Appliquer la puissance de saut a la variable de vitesse
            self.on_ground = False                               # Le joueur n'est plus au sol apres avoir saute
            imports.jump_sound.play()                                    # Jouer le son du saut
      
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_SPACE] and not self.attack and time >= self.post_attack_until:  # Si aucune touche de deplacement n'est appuyee et que le joueur n'attaque pas
            self.frame_index = 0
            if self.direction == "left":
                self.selected_image = self.selected_image_left       # L'image revient a celle du profil gauche de l'image selectionnee
            else:
                self.selected_image = self.selected_image_right      # L'image revient a celle du profil droit de l'image selectionnee


            # La gravite
        if not self.on_ground:
            velocity += globals.GRAVITY  # Appliquer la gravite a la variable de vitesse pour faire retomber le joueur quand il n'est pas sur le sol


        # --- L'attaque du joueur ---
            # Attaque
        if key[pygame.K_d] and not self.attack and self.can_attack and state == "game":  # Si la touche D est appuyee et que le joueur n''est pas deja en train d''attaquer
            self.attack = True
            start_time = time        # Enregistrer le temps de debut de l''attaque pour gerer le delai entre les attaques
            self.last_attack_time = time


            if self.direction == "left":
                self.selected_image = self.selected_attack_left   # Si la direction est a gauche, changer l''image selectionnee par celle de l''attaque du profil gauche
            else:
                self.selected_image = self.selected_attack_right  # Si la direction est a droite, changer l''image selectionnee par celle de l''attaque du profil droit
                self.attack_transition_time = time + self.attack_animation_time // 2  # Le moment ou l'attaque atteint son point de transition (quand le degat est applique) est le temps de debut de l'attaque plus le temps d'animation de l'attaque

            projectile_x, projectile_y = self.projectile_spawn_position()  # Obtenir la position de spawn du projectile en fonction de la direction du joueur
            if self.hero == "archer":
                arrows.append(Arrow(projectile_x, projectile_y, self))
                self.last_attack_time = time


            if self.hero =="ninja":
                shurikens.append(Shuriken(projectile_x, projectile_y, self))
                self.last_attack_time = time


            if self.hero == "beggar":
                if self.weapon == "shuriken":
                    shurikens.append(Shuriken(projectile_x, projectile_y, self))
                    self.last_attack_time = time
                elif self.weapon == "bow":
                    arrows.append(Arrow(projectile_x, projectile_y, self))
                    self.last_attack_time = time


            self.can_attack = False


        # Delai avant la prochaine attaque
        if self.attack and self.hero == "archer" and time >= self.attack_transition_time:  # Pour l'archer, le degat est applique a la moitie de l'animation d'attaque, donc le changement d'image de transition se fait a ce moment la
            if self.direction == "left":
                self.selected_image = self.attack_frames_left[1]       # L'image de transition de l'attaque est celle du milieu de la liste d'images d'attaque, qui correspond a la moitie de l'animation d'attaque
            else:
                self.selected_image = self.attack_frames_right[1]
        if self.attack and time - start_time >= self.attack_animation_time:
            if self.direction == "left":
                self.selected_image = self.selected_image_left       # L'image revient a celle du profil gauche de l'image selectionnee
            else:
                self.selected_image = self.selected_image_right   # L'image revient a celle du profil droit de l'image selectionnee
            self.attack = False                                   # Apres le delai d'attaque, le joueur n'est plus en train d'attaquer, et son image revient a celle de base
      
        if self.hero == "archer":
            self.post_attack_until = time + 120
            if self.direction == "left":
                self.selected_image = self.attack_frames_left[1]
            else:
                self.selected_image = self.attack_frames_right[1]

        if time - start_time >= self.attack_animation_time + self.attack_delay:  # Apres le delai d'attaque plus le temps entre les attaques, le joueur peut a nouveau attaquer
            self.can_attack = True


        if not self.can_attack:
            if self.hero == "archer" and time - self.last_attack_time >= self.attack_delay:
                self.can_attack = True


        self.hitbox.y += velocity  # Appliquer la variable de vitesse a la position verticale de la hitbox pour faire sauter ou faire tomber le joueur
        self.hitbox.x += self.pushback
        if self.pushback > 0:
            self.pushback -= 5
        elif self.pushback < 0:
            self.pushback += 5




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


    def apply_rune_effect(self, rune_name):
        if rune_name == "rune_vie":
            self.max_life += 0.5
            self.life = min(self.life + 1, math.floor(self.max_life))
        elif rune_name == "rune_vitesse":
            self.speed += 0.5
        elif rune_name == "rune_puissance":
            self.puissance += 3




    def platform_collisions(self, platforms, traps, velocity):
        """S'occupe des collisoins avec les plateformes : si le joueur est en contact avec une plateforme, il n epeut pas la traverser."""
        self.on_ground = False                                                      # Par defaut, le joueur n'est pas au sol, et il le devient seulement s'il est en collision avec une plateforme en dessous de lui
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
                continue                                                   # La vitesse de chute est reinitialiser a 0 quand le joueur touche une plateforme
 
            # Collisions du bas de la plateforme
            if velocity < 0 and horizontal_overlap and previous_hitbox.top >= platform.bottom:
                a = self.hitbox
                a.x = previous_hitbox.x
                horizontal_overlap = a.right > platform.left and a.left < platform.right
                if horizontal_overlap:
                    self.hitbox.top = platform.bottom
                    velocity = 0
                    continue                                                   # La vitesse de saut est reinitialiser a 0 quand le joueur touche une plateforme par en dessous


            # Collisions des cotes de la plateforme
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

        for trap in traps:
            if not self.hitbox.colliderect(trap):
                continue
            horizontal_overlap = self.hitbox.right > trap.left and self.hitbox.left < trap.right
            if velocity >= 0 and horizontal_overlap and previous_hitbox.bottom <= trap.top:
                self.hitbox.bottom = trap.top
                self.on_ground = True
                velocity = 0

        return velocity


    def monster_collisions(self, monsters, time, arrows, platforms, shurikens = None):
        """Se charge des collisions entre le joueur et les monstres."""
        for monster in monsters[:]:
            hitbox = self.hitbox
            if self.attack and self.hero in ("swordsman", "beggar"):
                hitbox = self.hitbox_attack()
            collision_rect = monster.collide_rect if hasattr(monster, "collide_rect") else monster.rect
            if monster.alive and hitbox.colliderect(collision_rect):                                  # Si le monstre est vivant et que sa hitbox est en collision avec celle du joueur
                if hasattr(monster, "collide_rect"):
                    if self.prev_hitbox and self.prev_hitbox.right <= collision_rect.left and self.hitbox.right > collision_rect.left:
                        self.hitbox.right = collision_rect.left
                    elif self.prev_hitbox and self.prev_hitbox.left >= collision_rect.right and self.hitbox.left < collision_rect.right:
                        self.hitbox.left = collision_rect.right
 

                if self.attack:
                    if self.selected_image == self.selected_attack_left and self.hero in ("swordsman", "beggar"):     # Si le joueur attaque vers la gauche avec l'épée
                        if monster.rect.x < self.hitbox.x and time > monster.invincible:                                                # Si le monstre est à gauche du joueur
                            monster.take_damage(self.degat + self.puissance, time)                                  # Le monstre perd de la vie
                            if monster.type == "slug" : monster.rect.x -= 5 * globals.PUSHBACK
                            else : monster.rect.x -= globals.PUSHBACK
                            monster.invincible = time + 500
                    elif self.selected_image == self.selected_attack_right and self.hero in ("swordsman", "beggar"):  # Si le joueur attaque vers la droite avec l'épée
                        if monster.rect.x > self.hitbox.x and time > monster.invincible:                                                # Si le monstre est à droite du joueur
                            monster.take_damage(self.degat + self.puissance, time)                                  # Le monstre perd de la vie
                            if monster.type == "slug" :
                                monster.rect.x += 5 * globals.PUSHBACK
                            else :
                                monster.rect.x += globals.PUSHBACK
                            monster.invincible = time + 500
                            monster.resolve_horizontal_collisions(platforms)
                    else:
                        if time - self.last_damage_time >= self.invincibility_time:
                         damage = monster.get_contact_damage() if hasattr(monster, 'get_contact_damage') else 1
                         if damage > 0:
                             self.life -= damage
                             self.last_damage_time = time

                    if monster.life <= 0:                                   # Quand le monstre n'a plus de vies
                        monster.alive = False                               # Il est retire du jeu
                        self.xp += monster.xp_reward
                        if self.hero == "beggar":
                            self.xp += monster.xp_reward
               
                else:                                                       # Si le joueur n'attaque pas
                    if time - self.last_damage_time >= self.invincibility_time:
                        damage = monster.get_contact_damage() if hasattr(monster, 'get_contact_damage') else 1
                        if damage < 0:
                            continue
                        self.life -= damage
                        self.last_damage_time = time


                        if self.hitbox.x < monster.rect.x:
                            self.pushback -= globals.PUSHBACK                       # Si le joueur est a gauche du monstre, il recule vers la gauche
                        else:
                            self.pushback += globals.PUSHBACK                       # Si le joueur est a droite du monstre, il recule vers la droite
          
            for arrow in arrows[:]:
                if monster.alive and arrow.rect.colliderect(monster.rect):  # Si la hitbox de la fleche est en collision avec celle du monstre
                    monster.take_damage(self.degat + self.puissance, time)             # Le monstre perd une vie
                    if arrow.direction == "right":
                        if monster.type == "slug":
                            monster.rect.x += 5 * globals.PUSHBACK
                        else:
                            monster.rect.x += globals.PUSHBACK
                    else:
                        monster.rect.x -= globals.PUSHBACK                  # Si la fleche va vers la gauche, le monstre recule vers la gauche
                    monster.resolve_horizontal_collisions(platforms)
                    arrows.remove(arrow)                                    # Retirer la fleche du jeu
                    if monster.life <= 0:
                        monster.alive = False                               # Quand le monstre n'a plus de vies, il est retire du jeu
                        self.xp += monster.xp_reward


            if shurikens is None :
                continue
            for shuriken in shurikens[:]:
                if monster.alive and shuriken.rect.colliderect(monster.rect):  # Si la hitbox de la fleche est en collision avec celle du monstre
                    monster.take_damage(self.degat + self.puissance, time)                # Le monstre perd une vie
                    if shuriken.direction == "right":
                        if monster.type == "slug":
                            monster.rect.x += 5 * globals.PUSHBACK
                        else:
                            monster.rect.x += globals.PUSHBACK
                    else:
                        monster.rect.x -= globals.PUSHBACK                     # Si la fleche va vers la gauche, le monstre recule vers la gauche
                    monster.resolve_horizontal_collisions(platforms)
                    shurikens.remove(shuriken)                                 # Retirer la fleche du jeu
                    if monster.life <= 0:
                        monster.alive = False                                  # Quand le monstre n'a plus de vies, il est retire du jeu
                        self.xp += monster.xp_reward
  
    def player_xp(self):
        """Se charge de gerer l'XP du joueur et de faire monter son niveau quand il atteint le nombre d'XP requis."""
        self.xp_lvl_up = 0
        for i in range(self.level + 1):
            self.xp_lvl_up += i*2
        if self.xp >= self.xp_lvl_up:
            self.level += 1
            self.point_attribut += 5
  
    def player_inventory(self, items, inventory_list, key, time, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed):
        """Gere le ramassage d'objet avec E et un feedback simple a l'ecran."""


        if globals.key[pygame.K_e] and not pickup_pressed:
            pickup_pressed = True
            for item in items[:]:
                if self.hitbox.colliderect(item.rect):
                    if inventory.add_item_to_inventory(inventory_list, item):
                        last_inventory_feedback = f"{item.name} ramasse"
                        items.remove(item)
                    else:
                        last_inventory_feedback = "Inventaire plein (5 slots)"
                    last_inventory_feedback_time = time
                    break


        if not globals.key[pygame.K_e]:
            pickup_pressed = False


        return items, inventory_list, last_inventory_feedback, last_inventory_feedback_time, pickup_pressed


    def player_death(self, time, camera_y, state):
        """Se charge de dire quand le joueur est mort : lorsqu'il est hors de la fenetre ou lorsqu'il n'a plus de vies (a cause des monstres)."""
            # --- Lorsque le hero n'a plus de vies ---
        if self.life <= 0:
            state = "death"  # Passer a l'ecran de mort
       
        if time - self.last_damage_time >= self.regeneration_time and self.life < math.floor(self.max_life):
            self.life += 1
            self.last_damage_time += 1500
          
            # --- Mort si le personnage est en dehors de l'ecran ---
        if self.hitbox.top > globals.HEIGHT + camera_y:
            state = "death"  # Si le personnage tombe en dessous de l'ecran, passer a l'ecran de mort

        return state

    def hazard_collisions(self, hazards, time):
        """Se charge des collisions entre le joueur et les hazard : si le joueur touche un hazard, il perd une vie."""
        for hazard in hazards:
            if self.hitbox.colliderect(hazard.rect):
                if time - self.last_damage_time >= self.invincibility_time:
                    self.life -= hazard.damage
                    self.last_damage_time = time
                    if self.direction == "left":
                        self.pushback += globals.PUSHBACK                       # Si le joueur est a gauche du hazard, il recule vers la gauche
                    else:
                        self.pushback -= globals.PUSHBACK                       # Si le joueur est a droite du hazard, il recule vers la droite
                break
      







# =================================
# MONSTRES
# =================================


# --- General ---
class Monster:
   def __init__(self, x, y, image_right = None, life = 0, speed = 0, xp_reward = 10):
       self.spawn_x = x                                                                                 # La position de spawn du monstre
       self.spawn_y = y                                                                                 # La position de spawn du monstre
       self.image_right = image_right                                                                   # Le profil droit du monstre
       self.image_left = pygame.transform.flip(image_right, True, False) if image_right else None       # Le profil gauche du monstre
       self.image = self.image_right                                                                    # L'image de base du monstre
       self.rect = self.image.get_rect(topleft = (x, y)) if image_right else pygame.Rect(x, y, 50, 50)  # Le rectangle du monstre
       self.life = life                                                                                 # Vie actuelle du monstre
       self.max_life = life                                                                             # Vie maximale du monstre
       self.alive = True                                                                                # Le monstre est vivant au debut
       self.speed = speed                                                                               # Vitesse du monstre
       self.xp_reward = xp_reward                                                                       # XP donne au joueur
       self.frame_index = 0
       self.animation_speed = 0.15
       self.invincible = 0


       self.direction = 1                                                                               # 1 = droite, -1 = gauche
       self.chasing = False                                                                             # Indique si le monstre poursuit le joueur
       self.chase_distance_x = 180                                                                      # Distance a laquelle le monstre commence la poursuite
       self.chase_distance_y = 230                                                                      # Distance a laquelle le monstre commence la poursuite
       self.type = None                                                                                 # Type de monstre, a definir dans les classes enfants
       self.lose_distance = 260                                                                         # Distance a laquelle le monstre abandonne la poursuite
       self.contact_damage = 1
       self.last_damage_taken_time = 0


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


   def update_chase_state(self, player_rect):
       # Calcule la distance horizontale entre le joueur et le monstre
       distance_x = abs(player_rect.centerx - self.rect.centerx)
       distance_y = abs(player_rect.centery - self.rect.centery)


       # Active la poursuite si le joueur est assez proche
       if not self.chasing and distance_x <= self.chase_distance_x:
           if self.type == "bat" and distance_y <= self.chase_distance_y:
               self.chasing = True
           elif self.type == "slug" or self.type == "slime" or self.type == "mushroom":
               self.chasing = True

       # Arrete la poursuite si le joueur est trop loin
       if self.chasing and distance_x >= self.lose_distance:
           if self.type == "bat" and distance_y >= self.lose_distance:
               self.chasing = False
           elif self.type == "slug" or self.type == "slime" or self.type == "mushroom":
               self.chasing = False


   def face_player(self, player_rect):
       # Oriente le monstre vers le joueur avec une petite zone morte pour eviter le clignotement
       dead_zone = 6


       if player_rect.centerx < self.rect.centerx - dead_zone:
           self.direction = -1
           if self.image_left:
               self.image = self.image_left
       elif player_rect.centerx > self.rect.centerx + dead_zone:
           self.direction = 1
           if self.image_right:
               self.image = self.image_right
  
   def resolve_horizontal_collisions(self, platforms):
       # Empeche le monstre de traverser un mur apres un pushback horizontal
       if platforms is None:
           platforms = []


       for platform in platforms:
           if not self.rect.colliderect(platform):
               continue


           overlap_left = self.rect.right - platform.left
           overlap_right = platform.right - self.rect.left


           if overlap_left < overlap_right:
               self.rect.right = platform.left
           else:
               self.rect.left = platform.right


       # Empeche aussi de sortir de l'ecran
       if self.rect.left < 0:
           self.rect.left = 0
       if self.rect.right > globals.WIDTH:
           self.rect.right = globals.WIDTH


   def patrol_horizontally(self, platforms = None):
       # Fait patrouiller le monstre horizontalement jusqu'a rencontrer un obstacle lateral
       if platforms is None:
           platforms = []


       previous_x = self.rect.x
       self.rect.x += self.speed * self.direction


       blocked = False


       # Collision laterale avec les plateformes
       for platform in platforms:
           if not self.rect.colliderect(platform):
               continue


           if previous_x + self.rect.width <= platform.left:
               self.rect.right = platform.left
               blocked = True
               break
           elif previous_x >= platform.right:
               self.rect.left = platform.right
               blocked = True
               break


       # Collision avec les bords de l'ecran
       if self.rect.left <= 0:
           self.rect.left = 0
           blocked = True
       elif self.rect.right >= globals.WIDTH:
           self.rect.right = globals.WIDTH
           blocked = True


       # Si le monstre est bloque, il change de direction
       if blocked:
           self.direction *= -1


       # Oriente l'image selon la direction
       if self.direction == -1:
           if self.image_left:
               self.image = self.image_left
       else:
           if self.image_right:
               self.image = self.image_right

   def update(self, player_rect, hazards, monsters, platforms = None):
       if not self.alive:
           return


       if platforms is None:
           platforms = []


       # Met a jour l'etat de poursuite
       self.update_chase_state(player_rect)


       if self.chasing:
           # Suit le joueur horizontalement
           self.face_player(player_rect)
           self.rect.x += self.speed * self.direction
       else:
           # Patrouille horizontalement
           self.patrol_horizontally(platforms)


       self.overlap(monsters, horizontal_only = True)

       for danger in hazards:
           if self.rect.colliderect(danger.rect) and self.direction == -1:
                self.rect.x += globals.PUSHBACK
           elif self.rect.colliderect(danger.rect) and self.direction == 1:
             self.rect.x -= globals.PUSHBACK
               
  
   def reset(self):
       self.alive = True
       self.life = self.max_life
       self.rect.topleft = (self.spawn_x, self.spawn_y)
       self.chasing = False
       self.direction = 1


   def draw(self, screen, camera_y = 0):
       screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))

   def get_contect_damage(self):
       return self.contact_damage
   
   def take_damage(self, damage, time = None):
       if not self.alive:
           return
       self.life -= damage
       if time is not None:
           self.last_damage_taken_time = time
       if self.life <= 0:
           self.alive = False




# --- Slug ---
class Slug(Monster):
   def __init__(self, x, y):
       super().__init__(
           x,
           y,
           image_right = imports.slug,
           life = 1500,
           speed = 2,
           xp_reward = 8
       )


       self.velocity_y = 0
       self.on_ground = False
       self.type = "slug"
  
   def ground_ahead(self, platforms, direction = None):
       # Verifie s'il y a du sol juste devant le slug
       if direction is None:
           direction = self.direction


       front_x = self.rect.centerx + (direction * self.rect.width // 2)
       front_y = self.rect.bottom + 5


       return any(platform.collidepoint(front_x, front_y) for platform in platforms)


   def update(self, player_rect, monsters, platforms = None):
       if not self.alive:
           return


       if platforms is None:
           platforms = []


       # Met a jour l'etat de poursuite
       self.update_chase_state(player_rect)


       should_move_horizontally = True


       if self.chasing:
           # Fige le slug sur sa derniere image lorsque le joueur est deja aligne horizontalement
           distance_x = player_rect.centerx - self.rect.centerx
           dead_zone = 6


           if abs(distance_x) <= dead_zone:
               should_move_horizontally = False
           else:
               # Oriente le slug vers le joueur seulement s'il doit vraiment se deplacer
               self.face_player(player_rect)


           # Si le joueur est de l'autre cote d'un vide, le slug s'arrete au bord
           if not self.ground_ahead(platforms, self.direction):
               should_move_horizontally = False


       # Deplacement horizontal
       previous_x = self.rect.x
       if should_move_horizontally:
           self.rect.x += self.speed * self.direction


       # Collision laterale avec les plateformes
       hit_side_wall = False
       for platform in platforms:
           if not self.rect.colliderect(platform):
               continue


           if previous_x + self.rect.width <= platform.left:
               self.rect.right = platform.left
               hit_side_wall = True
           elif previous_x >= platform.right:
               self.rect.left = platform.right
               hit_side_wall = True


       # Collision avec les bords de l'ecran
       if self.rect.left <= 0:
           self.rect.left = 0
           hit_side_wall = True
       elif self.rect.right >= globals.WIDTH:
           self.rect.right = globals.WIDTH
           hit_side_wall = True


       # Si le slug patrouille, il se retourne lorsqu'il est bloque
       # S'il poursuit, il reste contre l'obstacle au lieu de repartir
       if hit_side_wall and not self.chasing:
           self.direction *= -1


       # Gravite
       previous_y = self.rect.y
       self.velocity_y += globals.GRAVITY
       self.rect.y += self.velocity_y


       on_ground = False


       # Collision verticale avec les plateformes
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


       # En patrouille seulement, le slug tourne au bord de la plateforme
       # En poursuite, il reste au bord pour attendre le joueur
       if on_ground and not self.chasing:
           if not self.ground_ahead(platforms):
               self.direction *= -1


       # Oriente l'image selon la direction
       if self.direction == 1:
           self.image = self.image_right
       else:
           self.image = self.image_left


       self.on_ground = on_ground
       self.overlap(monsters, horizontal_only = True)




# --- Chauve-souris ---
class Bat(Monster):
   def __init__(self, x, y):
       super().__init__(
           x,
           y,
           image_right = imports.bat1,
           life = 300,
           speed = 3,
           xp_reward = 2
       )
       self.frames_right = [imports.bat1, imports.bat2]
       self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]
       self.type = "bat"


   def update(self, player_rect, monsters, platforms = None):
       if not self.alive:
           return


       if platforms is None:
           platforms = []


       # Met a jour l'etat de poursuite
       self.update_chase_state(player_rect)
       dx = self.direction


       if self.chasing:
           # Va vers le joueur en 2D
           dx = player_rect.centerx - self.rect.centerx
           dy = player_rect.centery - self.rect.centery
           distance = math.sqrt(dx * dx + dy * dy)


           if distance != 0:
               dx /= distance
               dy /= distance


               self.rect.x += dx * self.speed
               self.rect.y += dy * self.speed
       else:
           # Patrouille horizontalement
           previous_x = self.rect.x
           self.rect.x += self.speed * self.direction


           blocked = False


           # Collision laterale avec les plateformes
           for platform in platforms:
               if not self.rect.colliderect(platform):
                   continue


               if previous_x + self.rect.width <= platform.left:
                   self.rect.right = platform.left
                   blocked = True
                   break
               elif previous_x >= platform.right:
                   self.rect.left = platform.right
                   blocked = True
                   break


           # Collision avec les bords de l'ecran
           if self.rect.left <= 0:
               self.rect.left = 0
               blocked = True
           elif self.rect.right >= globals.WIDTH:
               self.rect.right = globals.WIDTH
               blocked = True


           # Change de direction si bloque
           if blocked:
               self.direction *= -1


           # Revient vers sa hauteur de depart pendant la patrouille
           if self.rect.centery < self.spawn_y:
               self.rect.y += min(self.speed, self.spawn_y - self.rect.centery)
           elif self.rect.centery > self.spawn_y:
               self.rect.y -= min(self.speed, self.rect.centery - self.spawn_y)


           dx = self.direction


       # Animation selon la direction
       self.frame_index += self.animation_speed
       if self.frame_index >= len(self.frames_right):
           self.frame_index = 0
       current_frame = int(self.frame_index)


       if dx < 0:
           self.image = self.frames_left[current_frame]
       else:
           self.image = self.frames_right[current_frame]


       self.overlap(monsters)


class Slime(Monster):
   def __init__(self, x, y):
       super().__init__(
           x,
           y,
           image_right = imports.slime,
           life = 400,
           speed = 2,
           xp_reward = 8
       )


       self.velocity_y = 0
       self.on_ground = False
       self.jump_power = -8
       self.jump_interval = 900
       self.last_jump_time = 0
       self.jump_direction = 1
       self.frames_right = [imports.slime, imports.flat_slime]
       self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]
       self.jumping_frames_right = [imports.jumping_slime1, imports.jumping_slime2, imports.slime, imports.jumping_slime3, imports.jumping_slime4]
       self.jumping_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.jumping_frames_right]
       self.type = "slime"
  
   def ground_ahead(self, platforms, direction = None):
       # Verifie s'il y a du sol juste devant le slime
       if direction is None:
           direction = self.direction


       front_x = self.rect.centerx + (direction * self.rect.width // 2)
       front_y = self.rect.bottom + 5


       return any(platform.collidepoint(front_x, front_y) for platform in platforms)


   def update(self, player_rect, monsters, platforms = None):
       if not self.alive:
           return


       if platforms is None:
           platforms = []


       # Met a jour l'etat de poursuite
       self.update_chase_state(player_rect)
       time = pygame.time.get_ticks()




       if self.chasing:
           distance_x = player_rect.centerx - self.rect.centerx
           if abs(distance_x) > 6:
               self.direction = 1 if distance_x > 0 else -1

           desired_direction = self.direction

       # Evite les sauts dans le vide pendant la poursuite
       desired_direction = self.direction
       if self.chasing and not self.ground_ahead(platforms, desired_direction):
           desired_direction = self.direction

       # Debut de saut: le slime se deplace surtout pendant son arc de saut
       if self.on_ground and time - self.last_jump_time >= self.jump_interval:
           if self.ground_ahead(platforms, desired_direction) or not self.chasing:
               self.direction = desired_direction
               self.jump_direction = self.direction
               self.velocity_y = self.jump_power
               self.on_ground = False
               self.last_jump_time = time



       # Deplacement horizontal uniquement pendant le saut 
       previous_x = self.rect.x
       if not self.on_ground:
           self.rect.x += self.speed * self.jump_direction

       # Collision laterale avec les plateformes
       hit_side_wall = False
       for platform in platforms:
           if not self.rect.colliderect(platform):
               continue


           if previous_x + self.rect.width <= platform.left:
               self.rect.right = platform.left
               hit_side_wall = True
           elif previous_x >= platform.right:
               self.rect.left = platform.right
               hit_side_wall = True


       # Collision avec les bords de l'ecran
       if self.rect.left <= 0:
           self.rect.left = 0
           hit_side_wall = True
       elif self.rect.right >= globals.WIDTH:
           self.rect.right = globals.WIDTH
           hit_side_wall = True


       if hit_side_wall:
           self.jump_direction *= -1
           if self.on_ground and not self.chasing:
               self.direction *= -1


       # Gravite
       previous_y = self.rect.y
       self.velocity_y += globals.GRAVITY
       self.rect.y += self.velocity_y


       on_ground = False


       # Collision verticale avec les plateformes
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


       if on_ground:
           self.direction = self.jump_direction
           if not self.chasing and not self.ground_ahead(platforms, self.direction):
               self.direction *= -1
               self.jump_direction = self.direction


       # Animation
       if on_ground:
           frames = self.frames_right if self.direction == 1 else self.frames_left
       else:
           frames = self.jumping_frames_right if self.jump_direction == 1 else self.jumping_frames_left

       self.frame_index += self.animation_speed
       if self.frame_index >= len(frames):
           self.frame_index = 0
       self.image = frames[int(self.frame_index)]


       self.on_ground = on_ground
       self.overlap(monsters, horizontal_only = True)


class Mushroom(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, 
            y, 
            image_right = imports.mushroom,
            life = 1500,
            speed = 1.5,
            xp_reward = 8
        )
        self.velocity_y = 0
        self.on_ground = False
        self.type = "mushroom"
  
    def ground_ahead(self, platforms, direction = None):
        # Verifie s'il y a du sol juste devant le mushroom
        if direction is None:
            direction = self.direction


        front_x = self.rect.centerx + (direction * self.rect.width // 2)
        front_y = self.rect.bottom + 5


        return any(platform.collidepoint(front_x, front_y) for platform in platforms)


    def update(self, player_rect, monsters, platforms = None):
        if not self.alive:
            return


        if platforms is None:
            platforms = []


        # Met a jour l'etat de poursuite
        self.update_chase_state(player_rect)


        should_move_horizontally = True


        if self.chasing:
            # Fige le mushroom sur sa derniere image lorsque le joueur est deja aligne horizontalement
            distance_x = player_rect.centerx - self.rect.centerx
            dead_zone = 6


            if abs(distance_x) <= dead_zone:
                should_move_horizontally = False
            else:
                # Oriente le mushroom vers le joueur seulement s'il doit vraiment se deplacer
                self.face_player(player_rect)


            # Si le joueur est de l'autre cote d'un vide, le mushroom s'arrete au bord
            if not self.ground_ahead(platforms, self.direction):
                should_move_horizontally = False


        # Deplacement horizontal
        previous_x = self.rect.x
        if should_move_horizontally:
            self.rect.x += self.speed * self.direction


        # Collision laterale avec les plateformes
        hit_side_wall = False
        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue


            if previous_x + self.rect.width <= platform.left:
                self.rect.right = platform.left
                hit_side_wall = True
            elif previous_x >= platform.right:
                self.rect.left = platform.right
                hit_side_wall = True


        # Collision avec les bords de l'ecran
        if self.rect.left <= 0:
            self.rect.left = 0
            hit_side_wall = True
        elif self.rect.right >= globals.WIDTH:
            self.rect.right = globals.WIDTH
            hit_side_wall = True


        # Si le mushroom patrouille, il se retourne lorsqu'il est bloque
        # S'il poursuit, il reste contre l'obstacle au lieu de repartir
        if hit_side_wall and not self.chasing:
            self.direction *= -1


        # Gravite
        previous_y = self.rect.y
        self.velocity_y += globals.GRAVITY
        self.rect.y += self.velocity_y


        on_ground = False


        # Collision verticale avec les plateformes
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


        # En patrouille seulement, le mushroom tourne au bord de la plateforme
        # En poursuite, il reste au bord pour attendre le joueur
        if on_ground and not self.chasing:
            if not self.ground_ahead(platforms):
                self.direction *= -1


        # Oriente l'image selon la direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left


        self.on_ground = on_ground
        self.overlap(monsters, horizontal_only = True)


class Boss(Monster):
    def __init__(self, x, y, image_right, life, speed, xp_reward, attacks, walk_frames_right = None):
        super().__init__(
            x, 
            y, 
            image_right = image_right,
            life = life,
            speed = speed,
            xp_reward = xp_reward
        )
        self.type = "boss"
        self.attacks = attacks
        self.walk_frames_right = walk_frames_right if walk_frames_right else [image_right]
        self.walk_frames_left = self.walk_frames_right
        self.velocity_y = 0
        self.on_ground = False
        self.heal_power = 1200
        self.mana = 0
        self.max_mana = 700
        self.mana_regen_per_second = 10
        self.mana_cost = 100
        self.action_pick_interval = 3000
        self.attack_duration = 1000
        self.last_mana_tick = pygame.time.get_ticks()
        self.last_action_pick = pygame.time.get_ticks()
        self.current_attack = None
        self.action_end_time = 0
        self.backing_up = False
        self.backup_target_distance = 210
        self.collide_rect = self.rect.copy()
        self.contact_damage = 0
        self.chase_distance_x = 500
        self.lose_distance = 700
    
    def refresh_collide_rect(self):
        width = max(30, int(self.rect.width * 0.6))
        self.collide_rect = pygame.Rect(0, 0, width, self.rect.height)
        self.collide_rect.midbottom = self.rect.midbottom

    def regenerate_mana(self, time):
        elapsed = max(0, time - self.last_mana_tick)
        if elapsed == 0:
            return
        self.mana = min(self.max_mana, self.mana + (elapsed / 1000) * self.mana_regen_per_second)
        self.last_mana_tick = time
        
    def apply_gravity(self, platforms):
        previous_y = self.rect.y
        self.velocity_y += globals.GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            crossed_top = previous_y + self.rect.height <= platform.top and self.rect.bottom >= platform.top
            if self.velocity_y >= 0 and crossed_top:
                self.rect.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True
                continue

            crossed_bottom = previous_y >= platform.bottom and self.rect.top <= platform.bottom
            if self.velocity_y < 0 and crossed_bottom:
                self.rect.top = platform.bottom
                self.velocity_y = 0

    def move_horizontal(self, amount, platforms):
        previous_x = self.rect.x
        self.rect.x += amount

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if previous_x + self.rect.width <= platform.left:
                self.rect.right = platform.left
            elif previous_x >= platform.right:
                self.rect.left = platform.right

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > globals.WIDTH:
            self.rect.right = globals.WIDTH

    def advance_toward_player(self, player_rect, platforms):
        direction = 1 if player_rect.centerx > self.rect.centerx else -1
        self.move_horizontal(direction * self.speed, platforms)

    def backup_from_player(self, player_rect, platforms):
        distance_x = abs(player_rect.centerx - self.rect.centerx)
        if distance_x >= self.backup_target_distance:
            self.backing_up = False
            return
        direction = -1 if player_rect.centerx > self.rect.centerx else 1
        self.move_horizontal(direction * self.speed, platforms)

    def choose_action(self):
        action_roll = randint(0, len(self.attacks))
        if action_roll == len(self.attacks):
            return {"name": "heal", "heal": self.heal_power, "range": 0, "damage": 0, "frames_right": [self.image_right]}
        return self.attacks[action_roll]

    def start_attack(self, action, time):
        self.current_attack = action
        self.action_end_time = time + self.attack_duration
        self.contact_damage = action["damage"]
        self.image = action["frames_right"][0]
        self.mana -= self.mana_cost

    def cast_heal(self, action):
        self.life = min(self.max_life, self.life + action["heal"])
        self.mana -= self.mana_cost

    def update(self, player_rect, monsters, platforms = None):
        if not self.alive:
            return

        if platforms is None:
            platforms = []

        time = pygame.time.get_ticks()
        self.direction = 1
        self.regenerate_mana(time)
        self.apply_gravity(platforms)

        if time < self.action_end_time:
            self.image = self.current_attack["frames_right"][0] if self.current_attack else self.image_right
            self.refresh_collide_rect()
            self.overlap(monsters, horizontal_only = True)
            return

        if self.current_attack is not None:
            self.current_attack = None
            self.contact_damage = 0
            self.backing_up = True

        if self.backing_up:
            self.backup_from_player(player_rect, platforms)
            walk_frame = int((time / 150) % len(self.walk_frames_right))
            self.image = self.walk_frames_right[walk_frame]
            self.refresh_collide_rect()
            self.overlap(monsters, horizontal_only = True)
            return

        distance_x = abs(player_rect.centerx - self.rect.centerx)
        if time - self.last_action_pick >= self.action_pick_interval:
            self.last_action_pick = time
            if self.mana >= self.mana_cost:
                action = self.choose_action()
                if action["name"] == "heal":
                    self.cast_heal(action)
                    self.backing_up = True
                elif distance_x <= action["range"]:
                    self.start_attack(action, time)
                else:
                    self.advance_toward_player(player_rect, platforms)
            else:
                self.advance_toward_player(player_rect, platforms)
        else:
            self.image = self.advance_toward_player(player_rect, platforms)

        walk_frame = int((time / 150) % len(self.walk_frames_right))
        self.image = self.walk_frames_right[walk_frame]
        self.refresh_collide_rect()
        self.overlap(monsters, horizontal_only = True)

    def reset(self):
        super().reset()
        self.mana = self.max_mana
        self.current_attack = None
        self.action_end_time = 0
        self.backing_up = False
        self.contact_damage = 0
        self.last_mana_tick = pygame.time.get_ticks()
        self.last_action_pick = self.last_mana_tick
        self.refresh_collide_rect()


class Cerberus(Boss):
    def __init__(self, x, y):
        attacks = [
            {
                "name": "claw",
                "range": 130,
                "damage": 1,
                "frames_right": [imports.cerberus_attack_claw, imports.cerberus_attack_claw]
            },
            {
                "name": "bite",
                "range": 85,
                "damage": 2,
                "frames_right": [imports.cerberus_attack_bite, imports.cerberus_attack_bite]
            }
        ]
        super().__init__(
            x,
            y,
            image_right = imports.cerberus_standing,
            life = 60000,
            speed = 1.8,
            xp_reward = 20,
            attacks = attacks,
            walk_frames_right = [imports.cerberus_walking1, imports.cerberus_walking2]
        )
        self.type = "cerberus"
        self.max_mana = 1000
        self.mana = self.max_mana
        self.mana_regen_per_second = 10
        self.heal_power = 2500
        self.backup_target_distance = 230
        self.attack_duration = 1000
        self.action_pick_interval = 3000
        self.refresh_collide_rect()



# =================================
# OBJETS
# =================================


# --- General ---
class Projectile:
   def __init__(self, x, y, player):
       self.direction = player.direction     # La direction du projectile est definie par la direction du joueur au moment du tir, et ne change pas apres


   def update(self, platforms, arrows, shurikens):
       if self.direction == "right":
           self.rect.x += self.speed  # La fleche se deplace vers la droite si sa direction est a droite
       else:
           self.rect.x -= self.speed  # La fleche se deplace vers la gauche si sa direction est a gauche
       if self.rect.right < 0 or self.rect.left > globals.WIDTH:  # Si la fleche sort de l'ecran, elle est retiree du jeu
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
       screen.blit(self.image, self.rect)  # Afficher la fleche a sa position actuelle sur l'ecran


# --- Fleche ---
class Arrow(Projectile):
   def __init__(self, x, y, player):
       super().__init__(x, y, player)
       self.speed = 10                # La vitesse de la fleche, qui est constante et ne change pas selon la direction


       if self.direction == "right":
           self.image = imports.arrow_right   # Le profil droit de la fleche est utilise si la direction est a droite
           self.rect = self.image.get_rect(midleft = (x, y))
       else:
           self.image = imports.arrow_left    # Le profil gauche de la fleche est utilise si la direction est a gauche
           self.rect = self.image.get_rect(midright = (x, y))


# --- Shuriken ---
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
           return  # Si le shuriken a ete retire du jeu (par exemple, s'il a touche une plateforme), ne pas continuer a mettre a jour sa rotation
      
       center = self.rect.center  # Conserver le centre du shuriken avant de faire tourner l'image
       self.angle = (self.angle + self.rotation_speed) % 360  # Mettre a jour l'angle de rotation du shuriken
       self.image = pygame.transform.rotate(self.base_image, self.angle)  # Faire tourner l'image du shuriken en fonction de l'angle
       self.rect = self.image.get_rect(center=self.rect.center)  # Mettre a jour le rect du shuriken pour qu'il reste centre sur sa position actuelle
# --- Machine pour les runes ---
class Runemachine:
   def __init__(self, x, ground_y, tile_size = 32):
       self.image = imports.rune_machine
       offset_y = self.image.get_height() - tile_size
       self.rect = self.image.get_rect(topleft = (x, ground_y - offset_y))
       self.interact_padding = 40


   def can_interact(self, player_hitbox):
       zone = self.rect.inflate(self.interact_padding * 2, self.interact_padding * 2)
       return zone.colliderect(player_hitbox)


   def draw(self, screen, camera_y = 0):
       screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))


   def available_runes(self, inventory_list):
       counts = {
           "rune_vie": 0,
           "rune_vitesse": 0,
           "rune_puissance": 0,
       }
       for slot in inventory_list:
           if slot and slot.get("name") in counts:
               counts[slot["name"]] += slot.get("quantity", 1)
       return counts


   def consume_rune(self, inventory_list, rune_name):
       for index, slot in enumerate(inventory_list):
           if slot and slot.get("name") == rune_name:
               slot["quantity"] -= 1
               if slot["quantity"] <= 0:
                   inventory_list[index] = None
               return True
       return False



# =================================
# MUR
# =================================


class Wall:
    def __init__(self, x, y, tile_size = 32, type = 0):
        wall_prob = randint(0,1000)
        blood_prob = randint(0,2)
        if type == 1:
            self.image = imports.wall_tile_cuffs
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 2:
            self.image = imports.wall_tile_chains
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 3:
            self.image = imports.wall_tile_arrow_hole2
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 4:
            self.image = imports.wall_tile_arrow_hole
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 5:
            self.image = imports.wall_tile_window_right
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 6:
            self.image = imports.wall_tile_window_left
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 7:
            self.image = imports.wall_tile_window_right2
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 8:
            self.image = imports.wall_tile_window_left2
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 9:
            self.image = imports.wall_tile_rope_attach
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 10:
            self.image = imports.wall_tile_rope
            self.rect = self.image.get_rect(topleft = (x, y))
        elif type == 11:
            self.image = imports.wall_tile_rope_end
            self.rect = self.image.get_rect(topleft = (x, y))


        elif wall_prob <= 10:
            self.image = imports.wall_tile_hole
            self.rect = self.image.get_rect(topleft = (x, y))
        elif wall_prob > 700:
            self.image = imports.wall_tile_grass
            self.rect = self.image.get_rect(topleft = (x, y))
        elif wall_prob <= 15:
            if blood_prob == 0:
                self.image = imports.wall_tile_blood1
            elif blood_prob == 1:
                self.image = imports.wall_tile_blood2
            elif blood_prob == 2:
                self.image = imports.wall_tile_blood3
            self.rect = self.image.get_rect(topleft = (x, y))
        elif wall_prob <= 22:
            self.image = imports.wall_tile_lantern
            self.rect = self.image.get_rect(topleft = (x, y))
        else:
            self.image = imports.wall_tile
            self.rect = self.image.get_rect(topleft = (x, y))




    def draw(self, screen, camera_y = 0):
       screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))


class Hazard:
   def __init__(self, x, y, tile_size = 32, damage = 1):
       self.rect = pygame.Rect(x, y, tile_size, tile_size)
       self.damage = damage
       self.image = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)


   def draw(self, screen, camera_y = 0):
       screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))

class Spikes(Hazard):
   def __init__(self, x, y, tile_size = 32, damage = 1):
       super().__init__(x, y, tile_size, damage)
       self.image = imports.spikes

class Lava(Hazard):
   def __init__(self, x, y, tile_size = 32, damage = 2):
       super().__init__(x, y, tile_size, damage)
       self.image = imports.lava

