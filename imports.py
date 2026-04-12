import pygame
import globals


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
ninja_image = pygame.image.load("Images/Ninja/ninja.png").convert_alpha()                 # Charger l'image du ninja
ninja_menu_rect = ninja_image.get_rect(center = (globals.WIDTH//2 + 150, globals.HEIGHT//2))  # Rect de l'image du ninja dans le menu de depart

    # Beggar
beggar_image = pygame.image.load("Images/Beggar/standing_beggar.png").convert_alpha()                 # Charger l'image du mendiant
beggar_menu_rect = beggar_image.get_rect(center = (globals.WIDTH//2 + 300, globals.HEIGHT//2))  # Rect de l'image du mendiant dans le menu de depart

# --- Images de jeu ---
    # Heros
        # Archer
post_attacking_archer = pygame.image.load("Images/Archer/post_attacking_archer.png").convert_alpha()  # Charger l'image de l'archer apres son attaque
attacking_archer = pygame.image.load("Images/Archer/attacking_archer.png").convert_alpha()            # Charger l'image de l'archer pendant son attaque
walking_archer1 = pygame.image.load("Images/Archer/walking_archer1.png").convert_alpha()
walking_archer2 = pygame.image.load("Images/Archer/walking_archer2.png").convert_alpha()
walking_archer3 = pygame.image.load("Images/Archer/walking_archer3.png").convert_alpha()
        # Epeiste
attacking_swordsman = pygame.image.load("Images/Swordsman/attacking_swordsman.png").convert_alpha()  # Charger l'image de l'epeiste pendant son attaque
standing_swordsman = pygame.image.load("Images/Swordsman/standing_swordsman.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il ne fait rien
walking_swordsman1 = pygame.image.load("Images/Swordsman/walking_swordsman1.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il marche
walking_swordsman2 = pygame.image.load("Images/Swordsman/walking_swordsman2.png").convert_alpha()    # Charger l'image de l'epeiste pendant qu'il marche (2)
walking_swordsman3 = pygame.image.load("Images/Swordsman/walking_swordsman3.png").convert_alpha()
walking_swordsman4 = pygame.image.load("Images/Swordsman/walking_swordsman4.png").convert_alpha()

        # Ninja
ninja = pygame.image.load("Images/Ninja/ninja.png").convert_alpha()  # Charger l'image du ninja pendant qu'il ne fait rien
ninja_ash = pygame.image.load("Images/Ninja/ninja_ash.png").convert_alpha()
ninja_ada = pygame.image.load("Images/Ninja/ninja_ada.png").convert_alpha()
walking_ninja1 = pygame.image.load("Images/Ninja/walking_ninja1.png").convert_alpha()
walking_ninja2 = pygame.image.load("Images/Ninja/walking_ninja2.png").convert_alpha()
walking_ninja3 = pygame.image.load("Images/Ninja/walking_ninja3.png").convert_alpha()

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
bat2 = pygame.image.load("Images/Monsters/Bat/bat2.png").convert_alpha()  # Charger l'image de la chauve-souris (2)

        # Slime
slime = pygame.image.load("Images/Monsters/Slime/slime.png").convert_alpha()
flat_slime = pygame.image.load("Images/Monsters/Slime/slime_flat.png").convert_alpha()
jumping_slime1 = pygame.image.load("Images/Monsters/Slime/jumping_slime1.png").convert_alpha()
jumping_slime2 = pygame.image.load("Images/Monsters/Slime/jumping_slime2.png").convert_alpha()
jumping_slime3 = pygame.image.load("Images/Monsters/Slime/jumping_slime3.png").convert_alpha()
jumping_slime4 = pygame.image.load("Images/Monsters/Slime/jumping_slime4.png").convert_alpha()

        # Mushroom
mushroom = pygame.image.load("Images/Monsters/mushroom.png").convert_alpha()

        # Bosses
            # Cerbere
cerberus_standing = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus_standing.png").convert_alpha()
cerberus_attack_claw = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus_attack_claw.png").convert_alpha()
cerberus_attack_bite = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus_attack_bite.png").convert_alpha()
cerberus_walking1 = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus_walking1.png").convert_alpha()
cerberus_walking2 = pygame.image.load("Images/Monsters/Bosses/Cerberus/cerberus_walking2.png").convert_alpha()

            # King_Slime
King_Slime = pygame.image.load("Images/Monsters/Bosses/king_slime.png").convert_alpha()

            # Spider
spider_walking1 = pygame.transform.scale(pygame.image.load("Images/Monsters/Bosses/Spider/walking_spider1.png").convert_alpha(), (315, 250))
spider_walking2 = pygame.transform.scale(pygame.image.load("Images/Monsters/Bosses/Spider/walking_spider2.png").convert_alpha(), (315, 250))
spider_jaw_attack = pygame.transform.scale(pygame.image.load("Images/Monsters/Bosses/Spider/spider_attack_jaw.png").convert_alpha(), (315, 250))

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
            # Fleches
arrow = pygame.image.load("Images/Archer/arrow.png").convert_alpha()  # Charger l'image de la fleche de l'archer
arrow_right = arrow                                                   # Le profil droit de la fleche est l'image de base
arrow_left = pygame.transform.flip(arrow, True, False)                # Le profil gauche de la fleche est l'image de base retournee horizontalement
            
            # Shurikens
shuriken = pygame.image.load("Images/Ninja/shuriken.png").convert_alpha()  # Charger l'image du shuriken du ninja
shuriken_right = shuriken                                                  # Le profil droit du shuriken est l'image de base
shuriken_left = pygame.transform.flip(shuriken, True, False)               # Le profil gauche du shuriken est l'image de base retournee horizontalement

        # Bagues
bat_ring = pygame.image.load("Images/Rings/bat_ring.png").convert_alpha()  # Charger l'image de la bague de chauve-souris
slug_ring = pygame.image.load("Images/Rings/slug_ring.png").convert_alpha()  # Charger l'image de la bague de slug
slime_ring = pygame.image.load("Images/Rings/slime_ring.png").convert_alpha()  # Charger l'image de la bague de slime
mushroom_ring = pygame.image.load("Images/Rings/mushroom_ring.png").convert_alpha()  # Charger l'image de la bague de mushroom

    # Images de fond
wall_tile = pygame.image.load("Images/Background/wall_tile.png").convert_alpha()                  # Charger l'image de la dalle sombre de l'interface
wall_tile_grass = pygame.image.load("Images/Background/wall_tile_grass.png").convert_alpha()      # Charger l'image de la dalle herbeuse de l'interface
wall_tile_lantern = pygame.image.load("Images/Background/wall_tile_lantern.png").convert_alpha()  # Charger l'image de la dalle avec une lanterne de l'interface
wall_tile_hole = pygame.image.load("Images/Background/wall_tile_hole.png").convert_alpha()        # Charger l'image de la dalle avec un trou de l'interface

        # Chaine & menotte
wall_tile_cuffs = pygame.image.load("Images/Background/Chains/wall_tile_cuffs.png").convert_alpha()
wall_tile_chains = pygame.image.load("Images/Background/Chains/wall_tile_chains.png").convert_alpha()

        # Sang
wall_tile_blood1 = pygame.image.load("Images/Background/Blood/wall_tile_blood1.png").convert_alpha()
wall_tile_blood2 = pygame.image.load("Images/Background/Blood/wall_tile_blood2.png").convert_alpha()
wall_tile_blood3 = pygame.image.load("Images/Background/Blood/wall_tile_blood3.png").convert_alpha()

        # Meurtirieres
wall_tile_arrow_hole = pygame.image.load("Images/Background/Arrow_hole/wall_tile_arrow_hole.png").convert_alpha()
wall_tile_arrow_hole2 = pygame.image.load("Images/Background/Arrow_hole/wall_tile_arrow_hole2.png").convert_alpha()

        # Fenetres
wall_tile_window_right = pygame.image.load("Images/Background/Window/wall_tile_window.png").convert_alpha()
wall_tile_window_right2 = pygame.image.load("Images/Background/Window/wall_tile_window2.png").convert_alpha()
wall_tile_window_left = pygame.transform.flip(wall_tile_window_right, True, False)
wall_tile_window_left2 = pygame.transform.flip(wall_tile_window_right2, True, False)

        # Cordes
wall_tile_rope = pygame.image.load("Images/Background/Rope/wall_tile_rope.png").convert_alpha()
wall_tile_rope_attach = pygame.image.load("Images/Background/Rope/wall_tile_rope_attach.png").convert_alpha()
wall_tile_rope_end = pygame.image.load("Images/Background/Rope/wall_tile_rope_end.png").convert_alpha()

        # Dangers
lava = pygame.image.load("Images/Background/Hazards/lava_tile.png").convert_alpha()  # Charger l'image de la lave de l'interface
spikes = pygame.image.load("Images/Background/Hazards/spikes.png").convert_alpha()   # Charger l'image de la dalle de piques de l'interface

    

    # Machine
rune_machine = pygame.image.load("Images/rune_machine.png").convert_alpha()  # Charger l'image de la machine a runes de l'interface

    # Autres images pour les plateformes
platform_trap = pygame.image.load("Images/Background/Platforms/platform_trap.png").convert_alpha()  # Charger l'image de la plateforme piegee
platform_wall = pygame.image.load("Images/Background/Platforms/platform_wall.png").convert_alpha()  # Charger l'image de la plateforme murale
platform_1 = pygame.image.load("Images/Background/Platforms/platform_floor1.png").convert_alpha()
platform_2 = pygame.image.load("Images/Background/Platforms/platform_floor2.png").convert_alpha()

# =================================
# SONS
# =================================

# La musique de saut
jump_sound = pygame.mixer.Sound("Sounds/jump_sound.wav")  # Charger le son de saut
jump_sound.set_volume(1)                                  # Regler le volume du son du saut a 100%
