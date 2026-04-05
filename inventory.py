import pygame
import random
import globals, imports, buttons

pygame.init()


# =================================
# FUNCTIONS
# =================================

def add_item_to_inventory(inventory_list, item):
    """Ajoute un item a l'inventaire (max 5 slots). Stack d'abord, sinon premier slot libre."""
    for slot in inventory_list:
        if slot and slot["name"] == item.name:
            slot["quantity"] += item.quantity
            return True

    for index, slot in enumerate(inventory_list):
        if slot is None:
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
        return f"Slot {slot_index + 1} vide"

    if not slot.get("usable", False):
        return f"{slot['name']} non utilisable"

    used = False
    item_name = slot.get("name")

    if item_name == "Potion_vie":
        player.regeneration_time = player.regeneration_time / 2
        if player.regeneration_effect_end_time <= current_time:
            player.regeneration_effect_end_time = current_time + 20000
        else:
            player.regeneration_effect_end_time += 20000
        player.regeneration_bonus = True
        used = True

    elif item_name == "Potion_vitesse":
        player.speed_bonus = slot.get("heal_amount", 0)
        player.speed += player.speed_bonus
        if player.speed_effect_end_time <= current_time:
            player.speed_effect_end_time = current_time + 20000
        else:
            player.speed_effect_end_time += 20000
        used = True

    elif item_name == "Potion_puissance":
        player.power_bonus = slot.get("heal_amount", 0)
        player.puissance += player.power_bonus
        if player.power_effect_end_time <= current_time:
            player.power_effect_end_time = current_time + 20000
        else:
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
        inventory_list[slot_index] = None

    return f"{item_name_for_msg} jete"


def draw_inventory_hud(screen, inventory_list, slot_hold_start, slot_use_lock, current_time):
    """Affiche 5 slots avec icones, quantites et progression de maintien (1s)."""
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

        label = buttons.text_font.render(str(i + 1), True, globals.WHITE)
        screen.blit(label, (x + 4, y + 2))

        slot = inventory_list[i]
        if slot:
            icon_rect = slot["image"].get_rect(center=slot_rect.center)
            screen.blit(slot["image"], icon_rect)
            qty_txt = buttons.text_font.render(str(slot["quantity"]), True, globals.WHITE)
            screen.blit(qty_txt, (x + slot_size - qty_txt.get_width() - 4, y + slot_size - qty_txt.get_height() - 2))

        if slot_hold_start[i] is not None and slot and not slot_use_lock[i]:
            progress = (current_time - slot_hold_start[i]) / globals.ITEM_USE_HOLD_MS
            progress = max(0.0, min(1.0, progress))
            bar_bg = pygame.Rect(x, y + slot_size + 4, slot_size, 6)
            bar_fill = pygame.Rect(x, y + slot_size + 4, int(slot_size * progress), 6)
            pygame.draw.rect(screen, (80, 80, 80), bar_bg)
            pygame.draw.rect(screen, globals.GREEN, bar_fill)


def draw_equipped_rings(screen, player):
    """Affiche les bagues equipees en haut a droite."""
    x = globals.WIDTH - 10
    y = 10
    spacing = 6
    scale = 1.4

    for ring_image in player.equipped_ring_images:
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
    potion_cls = random.choice((life_potion, power_potion, speed_potion))
    return potion_cls(x, y)


def random_rune(x, y):
    rune_cls = random.choice((life_rune, power_rune, speed_rune))
    return rune_cls(x, y)


def generate_default_world_items():
    """Genere une liste d'items a spawn dans le monde aux positions fixes."""
    positions =  []
    return positions



# ================================
# LISTES
# ================================

slot_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

# --- Liste des objets presents dans le monde ---
items = generate_default_world_items()

# --- Inventaire du joueur (5 slots) ---
inventory_list = [None] * globals.INVENTORY_SLOTS
slot_hold_start = [None] * globals.INVENTORY_SLOTS
slot_use_lock = [False] * globals.INVENTORY_SLOTS
