import pygame # Importer la bibliothèque pygame pour créer le jeu
import math   # Impoter la bibliothèque math pour les calculs de distance et de direction des monstres volants

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
jump_sound = pygame.mixer.Sound("Sounds/jump_sound.wav")   # Son très moche qui va changer, mais qui est pour l'instant le son du saut
jump_sound.set_volume(1)                      # Régler le volume du son du saut à 100%

# --- Pour la fenêtre ---
    # L'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Definit la taille de la fenêtre (plein ecran)
screen.fill((40, 40, 55))                                    # Remplir la fenêtre avec une couleur de base

    # Le FPS
clock = pygame.time.Clock() # Variable de FPS

# --- Les couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# --- Constantes pour la fenêtre ---
WIDTH = screen.get_width()    # Largeur de l'ecran
HEIGHT = screen.get_height()  # Hauteur de l'ecran
camera_y = 0                  # Position verticale de la caméra, qui va suivre le joueur quand il monte
CAMERA_SMOOTH = 0.1           # Facteur de lissage pour le mouvement de la caméra, plus il est élevé, plus la caméra suit rapidement le joueur
state = "menu_de_debut"       # Le jeu demarre sur la fenêtre de menu

# --- Variables communes ---
GRAVITY = 0.4      # vitesse de chute --non
velocity = 0       # variable = vitesse de saut - vitesse de chute --non
on_ground = False  # contact avec le sol --non
start_time = 0     # Lorsque le jeu commence, le temps de départ est à 0 --non
PUSHBACK = 100     # La distance de recul quand le joueur ou le monstre est touché --non

# --- Images et classes---
    # Heros
perso1_image = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()   # Charger l'image de l'archer
perso2_image = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()  # Charger l'image de l'épéiste
perso3_image = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()       # Charger l'image du ninja

perso1_rect_menu = perso1_image.get_rect(center = (WIDTH//2 - 300, HEIGHT//2))  # Rect de l'image de l'archer dans le menu de départ
perso2_rect_menu = perso2_image.get_rect(center = (WIDTH//2 , HEIGHT//2))  # Rect de l'image de l'épéiste dans le menu de départ
perso3_rect_menu = perso3_image.get_rect(center = (WIDTH//2 + 300, HEIGHT//2))  # Rect de l'image du mage dans le menu de départ

class Player:
    def __init__(self, on_ground):
        """Définit les variables requises par le joueur et importe la viariable on_ground pour en avoir une spécialement pour le joueur."""
        self.speed = 0            # vitesse du joueur
        self.jump_power = -15     # puissance de saut
        self.attack = False       # le héro n'attaque pas encore
        self.direction = "right"  # direction initiale
        self.attack_delay = 0     # le temps qu'il faut attendre avant de pouvoir rattaquer
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
            self.attack_delay = 800                                                                           # Définit le temps entre les attaques pour l'archer, pour qui c'est plus long
            self.selected_image = perso1_image                                                                # L'image sélectionnée est celle de l'archer
            self.selected_image_right = self.selected_image                                                        # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)                     # Profil gauche de l'image sélectionnée
            self.selected_attack = pygame.image.load("Images/Archer/post_attacking_archer.png").convert_alpha()               # Télécharge l'image de l'attaque de l'archer
            self.speed = 3
            self.max_life = 4
            self.regeneration_time = 25000
            self.degat = 600
            self.walk_frames_right = [
                pygame.image.load("Images/Archer/post_attacking_archer.png").convert_alpha(),
            ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]

        elif self.hero == "swordsman":
            self.attack_delay = 300                                                                           # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
            self.selected_image = perso2_image                                                                # L'image sélectionnée est celle de l'épéiste
            self.selected_image_right = self.selected_image                                                        # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)                     # Profil gauche de l'image sélectionnée
            self.selected_attack = pygame.image.load("Images/Swordsman/attacking_swordsman.png").convert_alpha()                   # Télécharge l'image de l'attaque de l'épéiste
            self.speed = 4
            self.max_life = 5
            self.regeneration_time = 20000
            self.degat = 500
            self.walk_frames_right = [
                pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha(),
                pygame.image.load("Images/Swordsman/walking_swordsman1.png").convert_alpha(),
                pygame.image.load("Images/Swordsman/walking_swordsman2.png").convert_alpha(),
            ]
            self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_right]

        elif self.hero == "ninja":
            self.attack_delay = 200                                                                           # Définit le temps entre les attaques pour l'épéiste, pour qui c'est plus court
            self.selected_image = perso3_image                                                                # L'image sélectionnée est celle de l'épéiste
            self.selected_image_right = self.selected_image                                                        # Profil droit de l'image sélectionnée
            self.selected_image_left = pygame.transform.flip(self.selected_image, True, False)                     # Profil gauche de l'image sélectionnée
            self.selected_attack = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()                   # Télécharge l'image de l'attaque de l'épéiste
            self.speed = 5
            self.max_life = 3
            self.regeneration_time = 20000
            self.degat = 300
            self.walk_frames_right = [
                pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha(),
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
    
    def move(self, jump_sound, state, time, key, velocity, start_time):
        """Se charge de définir les mouvements du joueur et ses attaques."""
            
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
            jump_sound.play()                                    # Jouer le son du saut
        
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_SPACE] and not self.attack:  # Si aucune touche de déplacement n'est appuyée et que le joueur n'attaque pas
            self.frame_index = 0
            if self.direction == "left":
                self.selected_image = self.selected_image_left       # L'image revient à celle du profil gauche de l'image selectionnée
            else:
                self.selected_image = self.selected_image_right      # L'image revient à celle du profil droit de l'image selectionnée

            # La gravité
        if not self.on_ground:
            velocity += GRAVITY  # Appliquer la gravité à la variable de vitesse pour faire retomber le joueur quand il n'est pas sur le sol

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
                shuris.append(Shuri(self.hitbox.centerx, self.hitbox.centery, self))
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

        self.prev_hitbox = self.hitbox.copy()
        self.hitbox.y += velocity  # Appliquer la variable de vitesse à la position verticale de la hitbox pour faire sauter ou faire tomber le joueur
        return velocity, start_time

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
            if previous_hitbox.right <= platform.left:
                self.hitbox.right = platform.left
            elif previous_hitbox.left >= platform.right:
                self.hitbox.left = platform.right

        return velocity

    def monster_collisions(self, monsters, time, arrows):
        """Se charge des collisions entre le joueur et les monstres."""
        for monster in monsters[:]:
            if monster.alive and self.hitbox.colliderect(monster.rect):                                   # Si le monstre est vivant et que sa hitbox est en collision avec celle du joueur

                if self.attack:
                    if self.selected_image == self.selected_attack_left and self.hero == "swordsman":     # Si le joueur attaque vers la gauche avec l'épée
                        if monster.rect.x < self.hitbox.x:                                                # Si le monstre est à gauche du joueur
                            monster.life -= self.degat + self.puissance                                   # Le monstre perd une vie
                            monster.rect.x -= PUSHBACK
                    elif self.selected_image == self.selected_attack_right and self.hero == "swordsman":  # Si le joueur attaque vers la droite avec l'épée
                        if monster.rect.x > self.hitbox.x:                                                # Si le monstre est à droite du joueur
                            monster.life -= self.degat + self.puissance                                   # Le monstre perd une vie
                            monster.rect.x += PUSHBACK
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
                            self.hitbox.x -= PUSHBACK                       # Si le joueur est à gauche du monstre, il recule vers la gauche
                        else:
                            self.hitbox.x += PUSHBACK                       # Si le joueur est à droite du monstre, il recule vers la droite
            
            for arrow in arrows[:]:
                if monster.alive and arrow.rect.colliderect(monster.rect):  # Si la hitbox de la flèche est en collision avec celle du monstre
                    monster.life -= self.degat + self.puissance             # Le monstre perd une vie
                    if arrow.direction == "right":
                        monster.rect.x += PUSHBACK                          # Si la flèche va vers la droite, le monstre recule vers la droite
                    else:
                        monster.rect.x -= PUSHBACK                          # Si la flèche va vers la gauche, le monstre recule vers la gauche
                    arrows.remove(arrow)                                    # Retirer la flèche du jeu
                    if monster.life <= 0:
                        monster.alive = False                               # Quand le monstre n'a plus de vies, il est retiré du jeu
                        self.xp += monster.xp_reward
    
    def player_xp(self):
        """Se charge de gérer l'XP du joueur et de faire monter son niveau quand il atteint le nombre d'XP requis."""
        for i in range(self.level + 1):
            self.xp_lvl_up += i*2
        if self.xp >= self.xp_lvl_up:
            self.level += 1
            self.point_attribut += 5
    
    def player_inventory(self, items, inventory, key, time, last_inventory_feedback, last_inventory_feedback_time):
        """Gère le ramassage d'objet avec E et un feedback simple à l'écran."""
        global pickup_pressed

        if key[pygame.K_e] and not pickup_pressed:
            pickup_pressed = True
            for item in items[:]:
                if self.hitbox.colliderect(item.rect):
                    if add_item_to_inventory(inventory, item):
                        last_inventory_feedback = f"{item.name} ramassé"
                        items.remove(item)
                    else:
                        last_inventory_feedback = "Inventaire plein (5 slots)"
                    last_inventory_feedback_time = time
                    break

        if not key[pygame.K_e]:
            pickup_pressed = False

        return items, inventory, last_inventory_feedback, last_inventory_feedback_time                

    def player_death(self, time, camera_y, state):
        """Se charge de dire quand le joueur est mort : lorsqu'il est hors de la fenêtre ou lorsqu'il n'a plus de vies (à cause des monstres)."""
            # --- Lorsque le héro n'a plus de vies ---
        if self.life <= 0:
            state = "death"  # Passer à l'écran de mort
        
        if time - self.last_damage_time >= self.regeneration_time and self.life < self.max_life:
            self.life += 1
            self.last_damage_time += 1500
            
            # --- Mort si le personnage est en dehors de l'écran ---
        if self.hitbox.top > HEIGHT + camera_y:
            state = "death"  # Si le personnage tombe en dessous de l'écran, passer à l'écran de mort
        
        return state

player = Player(on_ground)  # Définit le joueur comme étant membre de la classe Player


    # Fleche
arrow_img = pygame.image.load("Images/Archer/arrow.png").convert_alpha()  # Charger l'image de la flèche
arrow_right = arrow_img                                      # Le profil droit de la flèche est l'image de base
arrow_left = pygame.transform.flip(arrow_img, True, False)   # Le profil gauche de la flèche est l'image de base retournée horizontalement

shuri_img = pygame.image.load("Images/Monsters/slug.png").convert_alpha()  # Charger l'image du shuriken
shuri_right = shuri_img                                      # Le profil droit du shuriken est l'image de base
shuri_left = pygame.transform.flip(shuri_img, True, False)   # Le profil gauche du shuriken est l'image de base retournée horizontalement
  
class Projectile:
    def __init__(self, x, y, player):
        self.direction = player.direction     # La direction du projectile est définie par la direction du joueur au moment du tir, et ne change pas après

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed  # La flèche se déplace vers la droite si sa direction est à droite
        else:
            self.rect.x -= self.speed  # La flèche se déplace vers la gauche si sa direction est à gauche
        if self.rect.right < 0 or self.rect.left > WIDTH:  # Si la flèche sort de l'écran, elle est retirée du jeu
            if self in arrows:
                arrows.remove(self)
            if self in shuris:
                shuris.remove(self)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self in arrows:
                    arrows.remove(self)
                if self in shuris:
                    shuris.remove(self)
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Afficher la flèche à sa position actuelle sur l'écran

class Arrow(Projectile):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.speed = 10                # La vitesse de la flèche, qui est constante et ne change pas selon la direction

        if self.direction == "right":
            self.image = arrow_right   # Le profil droit de la flèche est utilisé si la direction est à droite
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.image = arrow_left    # Le profil gauche de la flèche est utilisé si la direction est à gauche
            self.rect = self.image.get_rect(midright = (x, y))

class Shuri(Projectile):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.speed = 12                # La vitesse du shuriken, qui est constante et ne change pas selon la direction

        if self.direction == "right":
            self.image = shuri_right   # Le profil droit du shuriken est utilisé si la direction est à droite
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.image = shuri_left    # Le profil gauche du shuriken est utilisé si la direction est à gauche
            self.rect = self.image.get_rect(midright = (x, y))

    # Monstre
monster_img = pygame.transform.scale(pygame.image.load("Images/Monsters/slug.png").convert_alpha(), (150, 112.5))  # Charger l'image du monstre et la redimensionner à une taille plus appropriée
monster_right = monster_img                                                                        # Le profil droit du monstre est l'image de base
monster_left = pygame.transform.flip(monster_img, True, False)                                     # Le profil gauche du monstre est l'image de base retournée horizontalement

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

    def update(self, player_rect, monsters):
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


slug_img = pygame.transform.scale(pygame.image.load("Images/Monsters/slug.png").convert_alpha(), (150, 112))
bat_img_1 = pygame.transform.scale(pygame.image.load("Images/Monsters/bat1.png").convert_alpha(), (60, 28))
bat_img_2 = pygame.transform.scale(pygame.image.load("Images/Monsters/bat2.png").convert_alpha(), (60, 28))

class Slug(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, 
            y, 
            image_right=slug_img,  # Image spécifique
            life=1500,             # Vie spécifique du Slug
            speed=2,               # Vitesse spécifique du Slug
            xp_reward = 8
        )

class Bat(Monster):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            image_right=bat_img_1,  # Image spécifique
            life=300,             # Moins de vie qu'un slug
            speed=3,              # Plus rapide qu'un slug
            xp_reward = 2
        )
        self.frames_right = [bat_img_1, bat_img_2]
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]

    def update(self, player_rect, monsters):
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
            self.image = self.frames_left[current_frame]
        
        self.overlap(monsters)

tile_size = 32
map_design = [
"................................",
"................................",
"......................###.......",
"................................",
"................................",
"................................",
"................................",
"..............###...............",
"..............###...............",
"................................",
"................................",
"................................",
"................................",
"................................",
"........###.....................",
"........###.....................",
"...........###..................",
"...........###..................",
"......###.......................",
"......###.......................",
"################################"
]
def create_platforms_from_map(map_design):
    platforms = []

    map_height_pixels = len(map_design) * tile_size
    offset_y = HEIGHT - map_height_pixels


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
INVENTORY_SLOTS = 5
ITEM_USE_HOLD_MS = 1000
slot_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

fiole_vie_img = pygame.transform.scale(pygame.image.load("Images/Potions/life_potion.png").convert_alpha(), (32, 32))
fiole_puissance_img = pygame.transform.scale(pygame.image.load("Images/Potions/power_potion.png").convert_alpha(), (32, 32))
fiole_vitesse_img = pygame.transform.scale(pygame.image.load("Images/Potions/speed_potion.png").convert_alpha(), (32, 32))
rune_vie_img = pygame.transform.scale(pygame.image.load("Images/Runes/life_rune.png").convert_alpha(), (32, 32))
rune_puissance_img = pygame.transform.scale(pygame.image.load("Images/Runes/power_rune.png").convert_alpha(), (32, 32))
rune_vitesse_img = pygame.transform.scale(pygame.image.load("Images/Runes/speed_rune.png").convert_alpha(), (32, 32))


class Item:
    def __init__(self, name, x, y, image, quantity=1, usable=False, heal_amount=0):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.quantity = quantity
        self.usable = usable
        self.heal_amount = heal_amount

    def draw(self, screen, camera_y=0):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))

# Liste des objets présents dans le monde
items = [
    Item("Potion_vie", 260, 320, fiole_vie_img, quantity=1, usable=True, heal_amount=1),
    Item("Potion_puissance", 550, 120, fiole_puissance_img, quantity=1, usable=True, heal_amount=100),
    Item("Potion_vitesse", 260, 220, fiole_vitesse_img, quantity=1, usable=True, heal_amount=1),
    Item("rune_vie", 550, 220, rune_vie_img, quantity=1, usable=False, heal_amount=0),
    Item("rune_puissance", 260, 120, rune_puissance_img, quantity=1, usable=False, heal_amount=0),
    Item("rune_vitesse", 550, 20, rune_vitesse_img, quantity=1, usable=False, heal_amount=0),
]


# Inventaire du joueur (5 slots)
inventory = [None] * INVENTORY_SLOTS
slot_hold_start = [None] * INVENTORY_SLOTS
slot_use_lock = [False] * INVENTORY_SLOTS
last_inventory_feedback = ""
last_inventory_feedback_time = 0
pickup_pressed = False   # évite de ramasser 60 fois si E reste appuyé

# --- Dictionnaires ---
    # Monstres
monsters = [
    Slug(1000, HEIGHT - 130),
    Slug(800, HEIGHT - 130),
    Bat(1000, HEIGHT - 250),
    Bat(1000, HEIGHT - 300)
]

    # Fleches
arrows = []
shuris = []


# --- Polices de texte ---
title_font = pygame.font.SysFont(None, 100)                                         # Police du titre
text_font = pygame.font.SysFont(None, 40)                                           # Police du texte
death_txt_font = pygame.font.SysFont("Fonts/youmurdererbb_reg.ttf", 64)  # Police du texte de mort

# --- Boutons ---
    # Celui dans l'écran de mort pour recommencer
restart_rect_death = pygame.Rect(0, 255, 200, 60)
restart_rect_death.center = (WIDTH//2 - 150, HEIGHT//2 + 120)

continue_rect = pygame.Rect(0, 255, 200, 60)
continue_rect.center = (WIDTH//2 - 150, HEIGHT//2)

speed_rect = pygame.Rect(0, 255, 300, 30)
speed_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 8)

vitality_rect = pygame.Rect(0, 255, 300, 30)
vitality_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 9)

puissance_rect = pygame.Rect(0, 255, 300, 30)
puissance_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 10)

attack_delay_rect = pygame.Rect(0,255, 300, 30)
attack_delay_rect.center = (WIDTH//2 + 150, HEIGHT//16 * 11)

    # Celui dans l'écran de mort pour arrêter
end_rect_death = pygame.Rect(255, 0, 200, 60)
end_rect_death.center = (WIDTH//2 + 150, HEIGHT//2 + 120)

    # Ceux pour quand on pause le jeu
pause_box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)      # Rectangle dans lquel se situeront les boutons
continue_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 40, 180, 60)  # Celui pour continuer
quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 40, 180, 60)       # Celui pour arrêter

title_surface = title_font.render("Tower of Heights", True, (240, 240, 240))
title_rect = title_surface.get_rect(center=(WIDTH//2, 120))


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

    item = Item(
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
    total_width = INVENTORY_SLOTS * slot_size + (INVENTORY_SLOTS - 1) * spacing
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT - slot_size - 15

    for i in range(INVENTORY_SLOTS):
        x = start_x + i * (slot_size + spacing)
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        pygame.draw.rect(screen, (35, 35, 50), slot_rect)
        pygame.draw.rect(screen, WHITE, slot_rect, 2)

        label = text_font.render(str(i + 1), True, WHITE)
        screen.blit(label, (x + 4, y + 2))

        slot = inventory[i]
        if slot:
            icon_rect = slot["image"].get_rect(center=slot_rect.center)
            screen.blit(slot["image"], icon_rect)
            qty_txt = text_font.render(str(slot["quantity"]), True, WHITE)
            screen.blit(qty_txt, (x + slot_size - qty_txt.get_width() - 4, y + slot_size - qty_txt.get_height() - 2))

        if slot_hold_start[i] is not None and slot and not slot_use_lock[i]:
            progress = (current_time - slot_hold_start[i]) / ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(x, y + slot_size + 4, slot_size, 6)
            bar_fill = pygame.Rect(x, y + slot_size + 4, int(slot_size * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, GREEN, bar_fill)



# ===============================
# FONCTIONS
# ===============================

def paused(state, event, continue_button, quit_button):
    """Gère les clics sur les boutons affichés boutons pour continuer ou arrêter le jeu lorsqu'il est mis en pause"""
    if continue_button.collidepoint(event.pos): # Si on appuie sur le bouton pour continuer
        state = "game"                          # Continuer le jeu
        pygame.mixer.music.unpause()            # Continuer la musique
    
    if quit_button.collidepoint(event.pos):     # Si on appuie sur le bouton pour quitter
        state = "end"                           # Arrêter le jeu
    return state

def paused2(screen, pause_box, text_font, continue_button, quit_button):
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

def menu_de_debut(state, perso1_rect_menu, perso2_rect_menu, event, player):
    """Se charge de gérer les clics sur les personnages dans le menu de départ, et de définir les variables correspondantes en fonction du personnage choisi"""
    if perso1_rect_menu.collidepoint(event.pos):
        player.hero = "archer"     # Le joueur choisi est l'archer
    
    if perso2_rect_menu.collidepoint(event.pos):
        player.hero = "swordsman"  # Le joueur choisi est l'épéiste
    
    if perso3_rect_menu.collidepoint(event.pos):
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

def menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font):
    """Se charge d'afficher le menu de départ, avec les personnages à choisir et les instructions pour jouer"""
    # --- Remplir l'écran ---
        # Avec la couleur
    screen.fill((30, 30, 45))                                                                             # Remplir l'écran avec une couleur de base
    screen.blit(title_surface, title_rect)                                                                # Afficher le texte

        # Générer les personnages
    screen.blit(perso1_image, perso1_rect_menu)                                                           # Afficher l'image de l'archer
    screen.blit(perso2_image, perso2_rect_menu)                                                           # Afficher l'image de l'épéiste
    screen.blit(perso3_image, perso3_rect_menu)                                                           # Afficher l'image du ninja

        # Afficher le texte, 
    selection = text_font.render("Clique sur ton personnage", True, (200, 200, 200))                      # Pour définir le texte
    pour_pauser = text_font.render("Appuie sur ECHAPE pour pauser le jeu", True, (200, 200, 200))         # Pour définir le texte
    screen.blit(selection, (WIDTH//2 - selection.get_width()//2, HEIGHT - 160))                           # Pour afficher le texte
    screen.blit(pour_pauser, (WIDTH//2 - pour_pauser.get_width()//2, HEIGHT - 60))                        # Pour afficher le texte
    pygame.display.flip()                                                                                 # Tout générer sur la fenêtre

def game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time):
    """S'occupe de gérer les mouvements du joueur, les attaques, les collisions avec les plateformes et les monstres, et la mort du joueur"""
    
    velocity, start_time = player.move(jump_sound, state, time, key, velocity, start_time)
    velocity = player.platform_collisions(platforms, velocity)
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
    for slot_index, key_code in enumerate(slot_keys):
        if key[key_code]:
            if slot_hold_start[slot_index] is None:
                slot_hold_start[slot_index] = time
                slot_use_lock[slot_index] = False

            if not slot_use_lock[slot_index] and (time - slot_hold_start[slot_index] >= ITEM_USE_HOLD_MS):
                last_inventory_feedback = use_inventory_slot(inventory, slot_index, player)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True
        else:
            slot_hold_start[slot_index] = None
            slot_use_lock[slot_index] = False

    # --- Jet d'objet (Shift + 1..5) ---
    if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
        for slot_index, key_code in enumerate(slot_keys):
            if key[key_code] and not slot_use_lock[slot_index]:
                dropped_x = player.hitbox.centerx + 25
                dropped_y = player.hitbox.bottom - 20
                last_inventory_feedback = drop_inventory_slot(inventory, slot_index, items, dropped_x, dropped_y)
                last_inventory_feedback_time = time
                slot_use_lock[slot_index] = True

    return velocity, state, camera_y, player, start_time, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time

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
    inventory = [None] * INVENTORY_SLOTS
    slot_hold_start = [None] * INVENTORY_SLOTS
    slot_use_lock = [False] * INVENTORY_SLOTS
    last_inventory_feedback = ""
    last_inventory_feedback_time = 0

    items = [
        Item("Potion_vie", 260, 320, fiole_vie_img, quantity=1, usable=True, heal_amount=1),
        Item("Potion_puissance", 550, 120, fiole_puissance_img, quantity=1, usable=True, heal_amount=100),
        Item("Potion_vitesse", 260, 220, fiole_vitesse_img, quantity=1, usable=True, heal_amount=1),
        Item("rune_vie", 550, 220, rune_vie_img, quantity=1, usable=False, heal_amount=0),
        Item("rune_puissance", 260, 120, rune_puissance_img, quantity=1, usable=False, heal_amount=0),
        Item("rune_vitesse", 550, 20, rune_vitesse_img, quantity=1, usable=False, heal_amount=0),
    ]

    return state, player, inventory, items

def death2(screen, restart_rect_death, death_txt_font, end_rect_death, monsters):
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

def end(running, screen, text_font):
    """Se charge d'afficher l'écran de fin du jeu, avec un message de remerciement, et de fermer la fenêtre après quelques secondes"""
    screen.fill((0, 0, 100))                                                      # Remplir l'écran d'une couleur de base pour l'écran de fin
    txt = text_font.render("Merci d'avoir joue à Tower Of Heights", True, WHITE)  # Définir le texte de l'écran de fin
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//2)))                # Afficher le texte de l'écran de fin
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
    txt = text_font.render("ATTRIBUT", True, RED)                                                # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//2, HEIGHT//5)))                               # Afficher le texte de l'écran
    txt = text_font.render("level " + str(player.level), True, WHITE)                            # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3, HEIGHT//4)))                               # Afficher le texte de l'écran
    txt = text_font.render("point(s) d'attribut(s) " + str(player.point_attribut), True, WHITE)  # Définir le texte de l'écran
    screen.blit(txt, txt.get_rect(center = (WIDTH//3*2, HEIGHT//4)))                             # Afficher le texte de l'écran


    # --- Pour les boutons ---
        # Leur rect
    pygame.draw.rect(screen, (200, 0, 0), continue_rect)  # Dessiner un rectangle rouge pour le bouton de recommencer
    pygame.draw.rect(screen, (0, 0, 200), speed_rect)     # Dessiner un rectangle bleu pour le bouton d'arrêter
    pygame.draw.rect(screen, (0, 0, 200), vitality_rect)
    pygame.draw.rect(screen, (0, 0, 200), puissance_rect)
    pygame.draw.rect(screen, (0, 0, 200), attack_delay_rect)

        # Leur texte
    txt_continue = text_font.render("Continuer", True, WHITE)                    # Définir le texte du bouton pour recommencer
    txt_speed = text_font.render("vitesse : " + str(player.speed), True, WHITE)  # Définir le texte du bouton pour arrêter
    txt_vitality = text_font.render("vie : " + str(player.max_life), True, WHITE)
    txt_puissance = text_font.render("puissance : " + str(player.puissance*40//100), True, WHITE)
    txt_attack_delay = text_font.render("vitesse d'attaque : " + str((1000 - player.attack_delay)/50), True, WHITE)

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
    clock.tick(60) # FPS
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
            state = paused(state, event, continue_button, quit_button)  # Si le jeu est mis en pause, faire appel à la fonction paused() pour gérer les interactions avec les boutons de la fenêtre de pause

        # --- Pour donner le choix de personnages sur la page menu de depart ---
        if state == "menu_de_debut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = menu_de_debut(state, perso1_rect_menu, perso2_rect_menu, event, player)  # Appeler la fonction menu_de_debut() pour gérer les interactions avec les personnages sur la page du menu de départ, et récupérer les variables mises à jour par cette fonction

        # --- Pour la page de mort ---
        if state == "death" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player, inventory, items = death(state, event, restart_rect_death, end_rect_death, player, inventory, items)  # Pour appeler la fonction death() pour gérer les interactions avec les boutons de l'écran de mort, et récupérer les variables mis à jour par cette fonction

        if state == "menu_attribut" and event.type == pygame.MOUSEBUTTONDOWN:
            state, player = menu_attribut2(state, event, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player)    
    
    # --- Pause ---
    if state == "paused":
        paused2(screen, pause_box, text_font, continue_button, quit_button)  # Appeler la fonction paused2() pour afficher la fenêtre de pause
        continue
        
    # --- Pour creer la page du menu de depart ---
    if state == "menu_de_debut":
        menu_de_debut2(screen, title_surface, title_rect, perso1_image, perso1_rect_menu, perso2_image, perso2_rect_menu, text_font)  # Pour appeler la fonction menu_de_debut2() pour afficher la page du menu de départ
        continue

    # --- Pour jouer ---
    if state == "game":
        velocity, state, camera_y, player, start_time, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time = game(velocity, state, monsters, arrows, camera_y, time, key, start_time, player, inventory, items, slot_hold_start, slot_use_lock, last_inventory_feedback, last_inventory_feedback_time)  # Pour appeler la fonction game() pour gérer les mécaniques du jeu, et récupérer les variables mises à jour par cette fonction


    # --- Pour generer l'ecran de mort ---
    if state == "death":
        death2(screen, restart_rect_death, death_txt_font, end_rect_death, monsters)  # Pour appeler la fonction death2() pour afficher l'écran de mort, et récupérer les variables mises à jour par cette fonction
        continue

    if state == "menu_attribut":
        menu_attribut(screen, text_font, continue_rect, speed_rect, vitality_rect, puissance_rect, attack_delay_rect, player)
        continue

    if state == "end":
        running = end(running, screen, text_font)  # Pour appeler la fonction end() pour afficher l'écran de fin, et récupérer les variables mises à jour par cette fonction
    if player.perso_rect is None:
        continue                                                         # Si le rect du personnage n'est pas encore défini (c'est-à-dire que le joueur n'a pas encore choisi son personnage), ne rien faire et continuer la boucle principale jusqu'à ce que le joueur choisisse son personnage pour que le rect du personnage soit défini et que le jeu puisse commencer

    # --- Synchronisation image avec la hitbox ---
    if player.direction == "right":
        player.perso_rect.x = player.hitbox.x - 20                                                    # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    else:
        player.perso_rect.x = player.hitbox.x - (player.perso_rect.width - player.hitbox.width - 20)  # Synchroniser la position x de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)
    player.perso_rect.y = player.hitbox.y - 10                                                        # Synchroniser la position y de l'image du personnage avec celle de sa hitbox, en tenant compte du décalage entre les deux (la hitbox est plus petite que l'image, donc il faut ajuster la position de l'image pour qu'elle corresponde à celle de la hitbox)

    # --- Caméra montante (lissée) + ne pas descendre sous le sol ---
    if player.hitbox.y >= HEIGHT//2:
        camera_y = 0                                            # Si le personnage est en dessous de la moitié de l'écran en hauteur, la caméra ne descend pas plus bas que le sol (camera_y = 0)
    else:
        target_camera = player.hitbox.y - HEIGHT//2             # La position cible de la caméra est calculée pour que le personnage soit toujours à la moitié de l'écran en hauteur, sauf si le personnage est en dessous de cette moitié, auquel cas la caméra ne descend pas plus bas que le sol (camera_y = 0)
        camera_y += (target_camera - camera_y) * CAMERA_SMOOTH  # Pour faire en sorte que la caméra suive le joueur de manière lissée, on calcule la position cible de la caméra en fonction de la position du joueur, et on ajuste progressivement la position actuelle de la caméra vers cette position cible en utilisant un facteur de lissage (CAMERA_SMOOTH)
    
    if state == "game" :
        for arrow in arrows[:]: 
            arrow.update()  # Mettre à jour la position de chaque flèche en fonction de sa direction et de sa vitesse, et retirer les flèches qui sortent de l'écran pour éviter d'avoir trop de flèches inutiles dans la liste des flèches
        for shuri in shuris[:]: 
            shuri.update()  # Mettre à jour la position de chaque shuriken en fonction de sa direction et de sa vitesse, et retirer les shurikens qui sortent de l'écran pour éviter d'avoir trop de shurikens inutiles dans la liste des shurikens

    # --- Générer le jeu ---
    screen.fill((40, 40, 55))                                                                                              # Remplir l'écran avec une couleur de base pour le jeu
    for platform in platforms:
        pygame.draw.rect(screen, (120, 60, 60), (platform.x, platform.y - camera_y, platform.width, platform.height))  # Afficher les plateformes à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    screen.blit(player.selected_image, (player.perso_rect.x, player.perso_rect.y - camera_y))                                                   # Afficher l'image du personnage à sa position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for monster in monsters:
        if monster.alive:
            screen.blit(monster.image, (monster.rect.x, monster.rect.y - camera_y))                                        # Afficher les monstres vivants à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for arrow in arrows:
        screen.blit(arrow.image, (arrow.rect.x, arrow.rect.y - camera_y))                                                  # Afficher les flèches à leur position actuelle sur l'écran, en tenant compte du décalage de la caméra
    for item in items:
        item.draw(screen, camera_y) 
    draw_inventory_hud(screen, inventory, slot_hold_start, slot_use_lock, time)
    if time - last_inventory_feedback_time <= 1400 and last_inventory_feedback:
        feedback_text = text_font.render(last_inventory_feedback, True, WHITE)
        screen.blit(feedback_text, (20, 50))

    txt = text_font.render("Vie : " + str(player.life) + "/" + str(player.max_life), True, WHITE)
    screen.blit(txt, (20, 20))
    pygame.display.flip()                                                                                                  # Tout générer sur la fenêtre

pygame.quit()  # Arrêter Pygame et fermer la fenêtre du jeu




# Merci d'avoir lu notre code, nous espérons que vous avez apprécié le jeu et que vous avez trouvé notre code intéressant à lire


""" Tous droits réservés aux développeurs de ce jeu :
        - Célian
        - William
        - Samuel
"""