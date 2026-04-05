import pygame, random
import globals, imports, buttons


# =================================
# FUNCTIONS
# =================================

def add_item_to_inventory(inventory_list, item):
    """Ajoute un item a l'inventaire (max 5 slots). Stack d'abord, sinon premier slot libre."""
    for slot in inventory_list:
        if slot and slot["name"] == item.name:
            """Si l'item existe deja dans l'inventaire, on augmente juste la quantite."""
            slot["quantity"] += item.quantity
            return True

    for index, slot in enumerate(inventory_list):
        if slot is None:
            """Sinon, on ajoute l'item dans le premier slot libre."""
            inventory_list[index] = {
                "name": item.name,
                "image": item.image,
                "quantity": item.quantity,
                "usable": item.usable,
                "heal_amount": item.heal_amount,
            }
            return True
        
    return False


def use_inventory_slot(inventory_list, slot_index, player, current_time):
    """Utilise le slot demande si possible et retourne un message de feedback."""
    slot = inventory_list[slot_index]
    if slot is None:
        """Si le slot est vide, on ne peut rien utiliser."""
        return f"Slot {slot_index + 1} vide"

    if not slot.get("usable", False):
        """Si l'item n'est pas utilisable, on ne peut pas l'utiliser."""
        return f"{slot['name']} non utilisable"

    used = False
    item_name = slot.get("name")

    if item_name == "Potion_vie":
        """Soigne le joueur et applique un bonus de regeneration pendant 20s."""
        player.regeneration_time = player.regeneration_time / 2
        if player.regeneration_effect_end_time <= current_time:
            """Si le bonus de regeneration n'est pas actif, on l'active pour 20s."""
            player.regeneration_effect_end_time = current_time + 20000
        else:
            """Sinon, on prolonge sa duree de 20s supplementaires."""
            player.regeneration_effect_end_time += 20000
        player.regeneration_bonus = True
        used = True

    elif item_name == "Potion_vitesse":
        """Augmente la vitesse du joueur pendant 20s."""
        player.speed_bonus = slot.get("heal_amount", 0)
        player.speed += player.speed_bonus
        if player.speed_effect_end_time <= current_time:
            """Si le bonus de vitesse n'est pas actif, on l'active pour 20s."""
            player.speed_effect_end_time = current_time + 20000
        else:
            """Sinon, on prolonge sa duree de 20s supplementaires."""
            player.speed_effect_end_time += 20000
        used = True

    elif item_name == "Potion_puissance":
        """Augmente la puissance du joueur pendant 20s."""
        player.power_bonus = slot.get("heal_amount", 0)
        player.puissance += player.power_bonus
        if player.power_effect_end_time <= current_time:
            """Si le bonus de puissance n'est pas actif, on l'active pour 20s."""
            player.power_effect_end_time = current_time + 20000
        else:
            """Sinon, on prolonge sa duree de 20s supplementaires."""
            player.power_effect_end_time += 20000
        used = True

    elif item_name == "bague_slug":
        player.equipped_rings.add("slug")
        if slot["image"] not in player.equipped_ring_images:
            player.equipped_ring_images.append(slot["image"])
        used = True
    
    elif item_name == "bague_slime":
        player.equipped_rings.add("slime")
        if slot["image"] not in player.equipped_ring_images:
            player.equipped_ring_images.append(slot["image"])
        used = True
    
    elif item_name == "bague_mushroom":
        player.equipped_rings.add("mushroom")
        if slot["image"] not in player.equipped_ring_images:
            player.equipped_ring_images.append(slot["image"])
        used = True
    
    elif item_name == "bague_bat":
        player.equipped_rings.add("bat")
        if slot["image"] not in player.equipped_ring_images:
            player.equipped_ring_images.append(slot["image"])
        used = True

    if used:
        """Si l'item a ete utilise, on reduit la quantite et on retourne un message de feedback. Si la quantite tombe a 0, on vide le slot."""
        item_name_for_msg = slot["name"]
        slot["quantity"] -= 1
        if slot["quantity"] <= 0:
            inventory_list[slot_index] = None
        return f"{item_name_for_msg} utilise"

    return "Impossible d'utiliser cet objet"


def drop_inventory_slot(inventory_list, slot_index, items, x, y):
    """Jette 1 objet du slot donne au sol proche du joueur."""
    slot = inventory_list[slot_index]
    if slot is None:
        return "Rien a jeter"

    item = Item(slot["name"], x, y, slot["image"], quantity=1, usable=slot.get("usable", False), heal_amount=slot.get("heal_amount", 0))
    items.append(item)

    item_name_for_msg = slot["name"]
    slot["quantity"] -= 1
    if slot["quantity"] <= 0:
        inventory_list[slot_index] = None

    return f"{item_name_for_msg} jete"


def draw_inventory_hud(screen, inventory_list, slot_hold_start, slot_use_lock, current_time):
    """Affiche 5 slots avec icones, quantites et progression de maintien (1s)."""
    slot_size = 60                                                                               # Taille de chaque slot d'inventaire
    spacing = 12                                                                                 # Espace entre les slots
    total_width = globals.INVENTORY_SLOTS * slot_size + (globals.INVENTORY_SLOTS - 1) * spacing  # Largeur totale de l'affichage de l'inventaire
    start_x = globals.WIDTH // 2 - total_width // 2                                              # Position de départ pour centrer l'inventaire
    y = globals.HEIGHT - slot_size - 15                                                          # Position verticale des slots (15 pixels au-dessus du bas de l'écran)

    for i in range(globals.INVENTORY_SLOTS):
        """Dessine chaque slot d'inventaire, son icone, sa quantite et la barre de progression si le slot est en cours d'utilisation."""
        x = start_x + i * (slot_size + spacing)
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        pygame.draw.rect(screen, (35, 35, 50), slot_rect)
        pygame.draw.rect(screen, globals.WHITE, slot_rect, 2)

        label = buttons.text_font.render(str(i + 1), True, globals.WHITE)  # Affiche le numero du slot (1-5) en bas a droite de chaque slot
        screen.blit(label, (x + 4, y + 2))

        slot = inventory_list[i]
        if slot:
            """Si le slot n'est pas vide, on affiche l'icone de l'item et sa quantite. Si le slot est en cours d'utilisation, on affiche une barre de progression en dessous du slot qui se remplit pendant 1 seconde."""
            icon_rect = slot["image"].get_rect(center=slot_rect.center)
            screen.blit(slot["image"], icon_rect)
            qty_txt = buttons.text_font.render(str(slot["quantity"]), True, globals.WHITE)
            screen.blit(qty_txt, (x + slot_size - qty_txt.get_width() - 4, y + slot_size - qty_txt.get_height() - 2))

        if slot_hold_start[i] is not None and slot and not slot_use_lock[i]:
            """Si le slot est en cours d'utilisation, on affiche une barre de progression en dessous du slot qui se remplit pendant 1 seconde."""
            progress = (current_time - slot_hold_start[i]) / globals.ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(x, y + slot_size + 4, slot_size, 6)
            bar_fill = pygame.Rect(x, y + slot_size + 4, int(slot_size * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, globals.GREEN, bar_fill)


def draw_equipped_rings(screen, player):
    """Affiche les bagues equipees en haut a droite."""
    x = globals.WIDTH - 10  # On part du bord droit de l'ecran et on decale vers la gauche pour chaque bague equipee
    y = 10                  # On affiche les bagues en haut de l'ecran, a 10 pixels du bord superieur
    spacing = 6             # Espace entre les icones des bagues
    scale = 1.4             # Facteur de mise a l'echelle pour les icones des bagues (pour les rendre plus visibles)

    for ring_image in player.equipped_ring_images:
        """Affiche chaque bague equipee, en les espaçant et en les mettant a l'echelle."""
        scaled = pygame.transform.smoothscale(ring_image, (int(ring_image.get_width() * scale), int(ring_image.get_height() * scale)))
        x -= scaled.get_width()
        screen.blit(scaled, (x, y))
        x -= spacing



# ================================
# CLASSE
# ================================
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

class life_potion(Item):
    def __init__(self, x, y):
        super().__init__("Potion_vie", x, y, imports.life_potion, quantity=1, usable=True, heal_amount=1)
    
class power_potion(Item):
    def __init__(self, x, y):
        super().__init__("Potion_puissance", x, y, imports.power_potion, quantity=1, usable=True, heal_amount=100)

class speed_potion(Item):
    def __init__(self, x, y):
        super().__init__("Potion_vitesse", x, y, imports.speed_potion, quantity=1, usable=True, heal_amount=1)

class life_rune(Item):  
    def __init__(self, x, y):
        super().__init__("rune_vie", x, y, imports.life_rune, quantity=1, usable=False, heal_amount=0)

class speed_rune(Item):
    def __init__(self, x, y):
        super().__init__("rune_vitesse", x, y, imports.speed_rune, quantity=1, usable=False, heal_amount=0)

class power_rune(Item):
    def __init__(self, x, y):
        super().__init__("rune_puissance", x, y, imports.power_rune, quantity=1, usable=False, heal_amount=0)

class slug_ring(Item):
    def __init__(self, x, y):
        super().__init__("bague_slug", x, y, imports.slug_ring, quantity=1, usable=True, heal_amount=0)

class slime_ring(Item):
    def __init__(self, x, y):
        super().__init__("bague_slime", x, y, imports.slime_ring, quantity=1, usable=True, heal_amount=0)

class bat_ring(Item):
    def __init__(self, x, y):
        super().__init__("bague_bat", x, y, imports.bat_ring, quantity=1, usable=True, heal_amount=0)

class mushroom_ring(Item):
    def __init__(self, x, y):
        super().__init__("bague_mushroom", x, y, imports.mushroom_ring, quantity=1, usable=True, heal_amount=0)


def random_potion(x, y):
    """Genere une potion aleatoire (vie, puissance ou vitesse) a la position x, y."""
    potion_cls = random.choice((life_potion, power_potion, speed_potion))
    return potion_cls(x, y)


def random_rune(x, y):
    """Genere une rune aleatoire (vie, puissance ou vitesse) a la position x, y."""
    rune_cls = random.choice((life_rune, power_rune, speed_rune))
    return rune_cls(x, y)


def generate_default_world_items():
    """Genere une liste d'items a spawn dans le monde aux positions fixes."""
    positions =  []
    return positions



# ================================
# LISTES
# ================================

slot_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]  # Touches pour utiliser les slots d'inventaire (1-5)

# --- Liste des objets presents dans le monde ---
items = generate_default_world_items()

# --- Inventaire du joueur (5 slots) ---
inventory_list = [None] * globals.INVENTORY_SLOTS   # Chaque slot peut etre None (vide) ou un dict avec les infos de l'item (name, image, quantity, usable, heal_amount)
slot_hold_start = [None] * globals.INVENTORY_SLOTS  # Temps de debut de maintien pour chaque slot (None si pas en cours de maintien)
slot_use_lock = [False] * globals.INVENTORY_SLOTS   # Verrou pour empecher l'utilisation multiple d'un slot pendant le maintien (True si le slot a deja ete utilise pendant ce maintien)
