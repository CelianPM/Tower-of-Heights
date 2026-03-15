import pygame
import globals, imports, buttons

pygame.init()


# =================================
# FUNCTIONS
# =================================

def add_item_to_inventory(inventory_list, item):
    """Ajoute un item à l'inventaire (max 5 slots). Stack d'abord, sinon premier slot libre."""
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
    """Utilise le slot demandé si possible et retourne un message de feedback."""
    slot = inventory_list[slot_index]
    if slot is None:
        return f"Slot {slot_index + 1} vide"

    if not slot.get("usable", False):
        return f"{slot['name']} non utilisable"

    used = False
    item_name = slot.get("name")

    if item_name == "Potion_vie":
        player.regeneration_time = player.regeneration_time / 2
        player.regeneration_effect_end_time = current_time + 10000
        player.regeneration_bonus = True
        used = True
    elif item_name == "Potion_vitesse":
        player.speed_bonus = slot.get("heal_amount", 0)
        player.speed += player.speed_bonus
        player.speed_effect_end_time = current_time + 20000
        used = True
        player.power_bonus = slot.get("heal_amount", 0)
        player.puissance += player.power_bonus
        player.power_effect_end_time = current_time + 30000
        used = True

    if used:
        item_name_for_msg = slot["name"]
        slot["quantity"] -= 1
        if slot["quantity"] <= 0:
            inventory_list[slot_index] = None
        return f"{item_name_for_msg} utilisé"

    return "Impossible d'utiliser cet objet"

def drop_inventory_slot(inventory_list, slot_index, items, x, y):
    """Jette 1 objet du slot donné au sol proche du joueur."""
    slot = inventory_list[slot_index]
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
        inventory_list[slot_index] = None

    return f"{item_name_for_msg} jeté"

def draw_inventory_hud(screen, inventory_list, slot_hold_start, slot_use_lock, current_time):
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



# ================================
# LISTES
# ================================

slot_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

# --- Liste des objets présents dans le monde ---
items = [
    Item("Potion_vie", 260, 320, imports.life_potion, quantity = 1, usable = True, heal_amount = 1),
    Item("Potion_puissance", 550, 120, imports.power_potion, quantity = 1, usable = True, heal_amount = 100),
    Item("Potion_vitesse", 260, 220, imports.speed_potion, quantity = 1, usable = True, heal_amount = 1),
    Item("rune_vie", 550, 220, imports.life_rune, quantity = 1, usable = False, heal_amount = 0),
    Item("rune_puissance", 260, 120, imports.power_rune, quantity = 1, usable = False, heal_amount = 0),
    Item("rune_vitesse", 550, 20, imports.speed_rune, quantity = 1, usable = False, heal_amount = 0),
]


# --- Inventaire du joueur (5 slots) ---
inventory_list = [None] * globals.INVENTORY_SLOTS
slot_hold_start = [None] * globals.INVENTORY_SLOTS
slot_use_lock = [False] * globals.INVENTORY_SLOTS