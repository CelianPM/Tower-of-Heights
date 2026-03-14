import pygame
import globals

pygame.init()


# =================================
# IMAGES
# =================================

# --- Images et Rects du menu de début ---
    # Archer
archer_image = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()          # Charger l'image de l'archer
archer_menu_rect = archer_image.get_rect(center = (globals.WIDTH//2 - 300, globals.HEIGHT//2))  # Rect de l'image de l'archer dans le menu de départ

    # Epeiste
swordsman_image = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()   # Charger l'image de l'épéiste
swordsman_menu_rect = swordsman_image.get_rect(center = (globals.WIDTH//2 , globals.HEIGHT//2))  # Rect de l'image de l'épéiste dans le menu de départ

    # Ninja
ninja_image = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()                 # Charger l'image du ninja
ninja_menu_rect = ninja_image.get_rect(center = (globals.WIDTH//2 + 300, globals.HEIGHT//2))  # Rect de l'image du ninja dans le menu de départ


# --- Images de jeu ---
    # Heros
        # Archer
post_attacking_archer = pygame.image.load("Images/Archer/post_attacking_archer.png").convert_alpha()  # Charger l'image de l'archer après son attaque
attacking_archer = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()            # Charger l'image de l'archer pendant son attaque

        # Epeiste
attacking_swordsman = pygame.image.load("Images/Swordsman/attacking_swordsman.png").convert_alpha()  # Charger l'image de l'épéiste pendant son attaque
standing_swordsman = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()    # Charger l'image de l'épéiste pendant qu'il ne fait rien
walking_swordsman1 = pygame.image.load("Images/Swordsman/walking_swordsman1.png").convert_alpha()    # Charger l'image de l'épéiste pendant qu'il marche
walking_swordsman2 = pygame.image.load("Images/Swordsman/walking_swordsman2.png").convert_alpha()    # Charger l'image de l'épéiste pendant qu'il marche (2)

        # Ninja
ninja = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()  # Charger l'image du ninja pendant qu'il ne fait rien


    # Monstres
        # Slug
slug = pygame.transform.scale(pygame.image.load("Images/Monsters/slug.png").convert_alpha(), (150, 112.5))  # Charger l'image du slug et la redimensionner
slug_left = pygame.transform.flip(slug, True, False)                                                        # Créer une version retournée horizontalement de l'image du slug pour le faire aller vers la gauche

        # Chauve-souris
bat1 = pygame.image.load("Images/Monsters/bat1.png").convert_alpha()  # Charger l'image de la chauve-souris
bat2 = pygame.image.load("Images/Monsters/bat2.png").convert_alpha()  # Charger l'image de la chauve-souris (2)


    # Objets
        # Potions
life_potion = pygame.image.load("Images/Potions/life_potion.png").convert_alpha()    # Charger l'image de la potion de vie
speed_potion = pygame.image.load("Images/Potions/speed_potion.png").convert_alpha()  # Charger l'image de la potion de vitesse
power_potion = pygame.image.load("Images/Potions/power_potion.png").convert_alpha()  # Charger l'image de la potion de force

        # Runes
life_rune = pygame.image.load("Images/Runes/life_rune.png").convert_alpha()    # Charger l'image de la rune de vie
speed_rune = pygame.image.load("Images/Runes/speed_rune.png").convert_alpha()  # Charger l'image de la rune de vitesse
power_rune = pygame.image.load("Images/Runes/power_rune.png").convert_alpha()  # Charger l'image de la rune de force

        # Armes
            # Fleche
arrow = pygame.image.load("Images/Archer/arrow.png").convert_alpha()  # Charger l'image de la flèche de l'archer
arrow_right = arrow                                                   # Le profil droit de la flèche est l'image de base
arrow_left = pygame.transform.flip(arrow, True, False)                # Le profil gauche de la flèche est l'image de base retournée horizontalement
            
            # Shuriken
shuriken = pygame.image.load("Images/Ninja/shuriken.png").convert_alpha()  # Charger l'image du shuriken du ninja
shuriken_right = shuriken                                                  # Le profil droit du shuriken est l'image de base
shuriken_left = pygame.transform.flip(shuriken, True, False)               # Le profil gauche du shuriken est l'image de base retournée horizontalement


    # Images de fond
dark_slab = pygame.image.load("Images/dark_slab.png").convert_alpha()  # Charger l'image de la dalle sombre de l'interface



# =================================
# SONS
# =================================

# La musique de saut
jump_sound = pygame.mixer.Sound("Sounds/jump_sound.wav")  # Charger le son de saut
jump_sound.set_volume(1)                                  # Régler le volume du son du saut à 100%