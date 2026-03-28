import pygame
import globals

pygame.init()


# =================================
# IMAGES
# =================================

# --- Images et Rects du menu de debut ---
    # Archer
archer_image = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()          # Charger l'image de l'archer
archer_menu_rect = archer_image.get_rect(center = (globals.WIDTH//2 - 300, globals.HEIGHT//2))  # Rect de l'image de l'archer dans le menu de depart

    # Epeiste
swordsman_image = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()   # Charger l'image de l'epeiste
swordsman_menu_rect = swordsman_image.get_rect(center = (globals.WIDTH//2 - 150, globals.HEIGHT//2))  # Rect de l'image de l'epeiste dans le menu de depart

    # Ninja
ninja_image = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()                 # Charger l'image du ninja
ninja_menu_rect = ninja_image.get_rect(center = (globals.WIDTH//2 + 150, globals.HEIGHT//2))  # Rect de l'image du ninja dans le menu de depart

    # Beggar
beggar_image = pygame.image.load("Images/Beggar/standing_beggar.png").convert_alpha()                 # Charger l'image du mendiant
beggar_menu_rect = beggar_image.get_rect(center = (globals.WIDTH//2 + 300, globals.HEIGHT//2))  # Rect de l'image du mendiant dans le menu de depart

# --- Images de jeu ---
    # Heros
        # Archer
post_attacking_archer = pygame.image.load("Images/Archer/post_attacking_archer.png").convert_alpha()  # Charger l'image de l'archer apres son attaque
attacking_archer = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()            # Charger l'image de l'archer pendant son attaque

        # Epeiste
attacking_swordsman = pygame.image.load("Images/Swordsman/attacking_swordsman.png").convert_alpha()  # Charger l'image de l'epeiste pendant son attaque
standing_swordsman = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il ne fait rien
walking_swordsman1 = pygame.image.load("Images/Swordsman/walking_swordsman1.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il marche
walking_swordsman2 = pygame.image.load("Images/Swordsman/walking_swordsman2.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il marche (2)

        # Ninja
ninja = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()  # Charger l'image du ninja pendant qu'il ne fait rien

        # Beggar
beggar = pygame.image.load("Images/Beggar/standing_beggar.png").convert_alpha()  # Charger l'image du mendiant pendant qu'il ne fait rien
attacking_beggar = pygame.image.load("Images/Beggar/beggar_weaponless_attack.png").convert_alpha()
beggar_walk1 = pygame.image.load("Images/Beggar/walking_beggar1.png").convert_alpha()  # Charger l'image du mendiant pendant qu'il marche
beggar_walk2 = pygame.image.load("Images/Beggar/walking_beggar2.png").convert_alpha()  # Charger l'image du mendiant pendant qu'il marche (2)
beggar_walk3 = pygame.image.load("Images/Beggar/walking_beggar3.png").convert_alpha()  # Charger l'image du mendiant pendant qu'il marche (3)
beggar_walk4 = pygame.image.load("Images/Beggar/walking_beggar4.png").convert_alpha()  # Charger l'image du mendiant pendant qu'il marche (4)

    # Monstres
        # Slug
slug = pygame.transform.scale(pygame.image.load("Images/Monsters/slug.png").convert_alpha(), (150, 112.5))  # Charger l'image du slug et la redimensionner
slug_left = pygame.transform.flip(slug, True, False)                                                        # Creer une version retournee horizontalement de l'image du slug pour le faire aller vers la gauche

        # Chauve-souris
bat1 = pygame.image.load("Images/Monsters/Bat/bat1.png").convert_alpha()  # Charger l'image de la chauve-souris
bat2 = pygame.image.load("Images/Monsters/bat2.png").convert_alpha()  # Charger l'image de la chauve-souris (2)

        # Slime
slime = pygame.image.load("Images/Monsters/Slime/slime.png").convert_alpha()
flat_slime = pygame.image.load("Images/Monsters/Slime/slime_flat.png").convert_alpha()
jumping_slime1 = pygame.image.load("Images/Monsters/Slime/jumping_slime1.png").convert_alpha()
jumping_slime2 = pygame.image.load("Images/Monsters/Slime/jumping_slime2.png").convert_alpha()
jumping_slime3 = pygame.image.load("Images/Monsters/Slime/jumping_slime3.png").convert_alpha()
jumping_slime4 = pygame.image.load("Images/Monsters/Slime/jumping_slime4.png").convert_alpha()

        # Mushroom
mushroom = pygame.image.load("Images/Monsters/Mushroom/mushroom.png").convert_alpha()

        # Bosses
cerberus = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus.png").convert_alpha()


    # Objecs
        # Potions
life_potion = pygame.image.load("Images/Potions/life_potion.png").convert_alpha()    # Charger l'image de la potion de vie
speed_potion = pygame.image.load("Images/Potions/speed_potion.png").convert_alpha()  # Charger l'image de la potion de vitesse
power_potion = pygame.image.load("Images/Potions/power_potion.png").convert_alpha()  # Charger l'image de la potion de force

        # Runes
life_rune = pygame.image.load("Images/Runes/life_rune.png").convert_alpha()    # Charger l'image de la rune de vie
speed_rune = pygame.image.load("Images/Runes/speed_rune.png").convert_alpha()  # Charger l'image de la rune de vitesse
power_rune = pygame.image.load("Images/Runes/power_rune.png").convert_alpha()  # Charger l'image de la rune de force

        # Armes
            # Fleches
arrow = pygame.image.load("Images/Archer/arrow.png").convert_alpha()  # Charger l'image de la fleche de l'archer
arrow_right = arrow                                                   # Le profil droit de la fleche est l'image de base
arrow_left = pygame.transform.flip(arrow, True, False)                # Le profil gauche de la fleche est l'image de base retournee horizontalement
            
            # Shurikens
shuriken = pygame.image.load("Images/Ninja/shuriken.png").convert_alpha()  # Charger l'image du shuriken du ninja
shuriken_right = shuriken                                                  # Le profil droit du shuriken est l'image de base
shuriken_left = pygame.transform.flip(shuriken, True, False)               # Le profil gauche du shuriken est l'image de base retournee horizontalement

    # Images de fond
dark_slab = pygame.image.load("Images/dark_slab.png").convert_alpha()  # Charger l'image de la dalle sombre de l'interface

    # Machine
rune_machine = pygame.image.load("Images/rune_machine.png").convert_alpha()  # Charger l'image de la machine a runes de l'interface



# =================================
# SONS
# =================================

# La musique de saut
jump_sound = pygame.mixer.Sound("Sounds/jump_sound.wav")  # Charger le son de saut
jump_sound.set_volume(1)                                  # Regler le volume du son du saut a 100%
