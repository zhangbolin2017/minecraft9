import sys
import math
import random
import os
import pygame


WIDTH, HEIGHT = 640, 480
FPS = 60
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "image"))

TILE_SIZE = 64
WORLD_W = 240
WORLD_H = 40

PLAYER_SIZE = 32
PLAYER_SPEED = 280  # pixels per second
GRAVITY = 1500
JUMP_VELOCITY = -620
SWIM_SPEED = 185
SWIM_ASCEND_SPEED = 220
SWIM_DESCEND_SPEED = 170
SWIM_SINK_SPEED = 75

# Day/Night Colors
SKY_DAY = (135, 206, 235)
SKY_SUNSET = (253, 94, 83)
SKY_NIGHT = (24, 38, 92)
NIGHT_TINT = (10, 18, 48)

GRASS_COLOR = (95, 159, 53)
DIRT_COLOR = (120, 88, 58)
STONE_COLOR = (100, 100, 100)
BEDROCK_COLOR = (58, 58, 58)
SAND_COLOR = (222, 206, 138)
GRAVEL_COLOR = (136, 132, 128)
PLANK_COLOR = (188, 146, 92)
OBSIDIAN_COLOR = (52, 30, 78)
NETHER_PORTAL_COLOR = (148, 122, 202)
NETHERRACK_COLOR = (122, 56, 58)
NETHER_SKY_COLOR = (82, 28, 24)
NETHER_DARKNESS_TINT = (54, 16, 16)
DIAMOND_BLOCK_COLOR = (76, 224, 220)
COAL_ORE_COLOR = (70, 70, 70)
IRON_ORE_COLOR = (214, 168, 124)
GOLD_ORE_COLOR = (232, 196, 72)
NETHER_GOLD_ORE_COLOR = (238, 194, 84)
REDSTONE_ORE_COLOR = (214, 48, 48)
DIAMOND_ORE_COLOR = (88, 220, 220)
REDSTONE_COLOR = (238, 52, 52)
DIAMOND_ORE_CHANCE = 0.015
WATER_COLOR = (64, 164, 223)
LAVA_COLOR = (238, 102, 28)
WOOD_COLOR = (139, 69, 19)
LEAF_COLOR = (34, 139, 34)
PLAYER_COLOR = (235, 80, 80)
WHITE = (255, 255, 255)
SC_W, SC_A, SC_S, SC_D, SC_E, SC_F, SC_G = 26, 4, 22, 7, 8, 9, 10
MEAT_COLOR = (200, 70, 70)
RAW_FISH_COLOR = (235, 235, 235)
STICK_COLOR = (150, 112, 62)
INITIAL_ANIMAL_COUNT = 10
INITIAL_ZOMBIE_COUNT = 3
INITIAL_SKELETON_COUNT = 2
INITIAL_FISH_COUNT = 7
NIGHT_ZOMBIE_TARGET = 6
NIGHT_ZOMBIE_SPAWN_DELAY = 4.0
NIGHT_SKELETON_TARGET = 4
ZOMBIE_CHASE_SPEED = 95
ZOMBIE_BURN_INTERVAL = 0.6
SKELETON_MOVE_SPEED = 72
SKELETON_BURN_INTERVAL = 0.6
FIRE_DAMAGE_INTERVAL = 0.45
PORTAL_TELEPORT_COOLDOWN = 0.8
SKELETON_MIN_RANGE = 140
SKELETON_MAX_RANGE = 240
SKELETON_SHOOT_RANGE = 320
SKELETON_SHOT_INTERVAL = 1.7
SKELETON_AIM_TIME = 0.45
ARROW_SPEED = 260
ARROW_DAMAGE = 2
RESPAWN_DELAY = 5.0
OCEAN_WIDTH = 72
OCEAN_SHORE_WIDTH = 3
ISLAND_COUNT = 9
ISLAND_WIDTH = 5
MIN_TREES_PER_ISLAND = 5
FISH_MIN_OCEAN_DEPTH = 3
FISH_SWIM_SPEED_MIN = 40
FISH_SWIM_SPEED_MAX = 85
FISH_OUT_OF_WATER_TIME = 3.0
SC_K = 14
WOOD_SLOT_INDEX = 0
STONE_SLOT_INDEX = 1
COAL_ORE_SLOT_INDEX = 2
IRON_ORE_SLOT_INDEX = 3
GOLD_ORE_SLOT_INDEX = 4
DIAMOND_SLOT_INDEX = 5
IRON_INGOT_SLOT_INDEX = 6
GOLD_INGOT_SLOT_INDEX = 7
PLANK_SLOT_INDEX = 8
IRON_SWORD_SLOT_INDEX = 9
DIAMOND_SWORD_SLOT_INDEX = 10
IRON_PICKAXE_SLOT_INDEX = 11
DIAMOND_PICKAXE_SLOT_INDEX = 12
GOLD_PICKAXE_SLOT_INDEX = 13
WOOD_PICKAXE_SLOT_INDEX = 14
STONE_PICKAXE_SLOT_INDEX = 15
DIAMOND_BLOCK_SLOT_INDEX = 16
OBSIDIAN_SLOT_INDEX = 17
HOTBAR_SLOT_COUNT = 22
VISIBLE_HOTBAR_SLOTS = 9
BACKPACK_SLOT_COUNT = 13
HAND_ATTACK_DAMAGE = 1
WOOD_PICKAXE_ATTACK_DAMAGE = 2
STONE_PICKAXE_ATTACK_DAMAGE = 3
IRON_PICKAXE_ATTACK_DAMAGE = 4
GOLD_PICKAXE_ATTACK_DAMAGE = 5
DIAMOND_PICKAXE_ATTACK_DAMAGE = 6
REDSTONE_PICKAXE_ATTACK_DAMAGE = 5
IRON_SWORD_ATTACK_DAMAGE = 7
DIAMOND_SWORD_ATTACK_DAMAGE = 9
HAND_ATTACK_COOLDOWN = 0.30
WOOD_PICKAXE_ATTACK_COOLDOWN = 0.23
STONE_PICKAXE_ATTACK_COOLDOWN = 0.18
IRON_PICKAXE_ATTACK_COOLDOWN = 0.14
GOLD_PICKAXE_ATTACK_COOLDOWN = 0.10
DIAMOND_PICKAXE_ATTACK_COOLDOWN = 0.07
REDSTONE_PICKAXE_ATTACK_COOLDOWN = 0.08
IRON_SWORD_ATTACK_COOLDOWN = 0.22
DIAMOND_SWORD_ATTACK_COOLDOWN = 0.16
WOOD_PICKAXE_MAX_DURABILITY = 59
STONE_PICKAXE_MAX_DURABILITY = 131
IRON_PICKAXE_MAX_DURABILITY = 250
GOLD_PICKAXE_MAX_DURABILITY = 32
DIAMOND_PICKAXE_MAX_DURABILITY = 1561
REDSTONE_PICKAXE_MAX_DURABILITY = 420
FURNACE_FUEL_PER_ITEM = 1
INITIAL_PIGLIN_COUNT = 12
NETHER_PIGLIN_TARGET = 14
NETHER_PIGLIN_SPAWN_DELAY = 3.0
VILLAGER_SIZE = 30
VILLAGER_SPEED = 32
VILLAGER_TRADE_RANGE = 84
PIGLIN_TRADE_RANGE = 88
VILLAGER_HP = 8
IRON_GOLEM_SIZE = 40
IRON_GOLEM_SPEED = 22
IRON_GOLEM_HP = 5
VILLAGER_TRADES = [
    {"item": "iron_sword", "cost": 3, "label": "Iron Sword"},
    {"item": "diamond_sword", "cost": 6, "label": "Diamond Sword"},
    {"item": "diamond_block", "cost": 8, "label": "Diamond Block"},
]
ANIMAL_TYPES = {
    "Sheep": {"color": (235, 235, 235), "size": 26, "hp": 2, "image_file": "sheep.png"},
    "Cow": {"color": (90, 70, 55), "size": 30, "hp": 3, "image_file": "cow.png"},
    "Chicken": {"color": (245, 245, 170), "size": 20, "hp": 1, "image_file": "chicken.png"},
    "Fish": {"color": RAW_FISH_COLOR, "size": 22, "hp": 1, "image_file": "fish.png"},
    "Zombie": {"color": (70, 145, 70), "size": 30, "hp": 4, "image_file": "zombie.png"},
    "Skeleton": {"color": (225, 225, 225), "size": 30, "hp": 4, "image_file": "skeleton.png"},
    "Piglin": {"color": (216, 164, 144), "size": 30, "hp": 4, "image_file": "piglin.png"},
}

def load_animal_images():
    images = {}
    for name, spec in ANIMAL_TYPES.items():
        file_path = os.path.join(IMAGE_DIR, spec["image_file"])
        if os.path.exists(file_path):
            img = pygame.image.load(file_path).convert_alpha()
            # 缩放图片到设定的 size
            img = pygame.transform.scale(img, (spec["size"], spec["size"]))
            images[name] = img
        else:
            images[name] = None # 退回使用颜色绘制
    return images

def load_meat_image():
    file_path = os.path.join(IMAGE_DIR, "meat.png")
    if os.path.exists(file_path):
        img = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.scale(img, (16, 16))
    return None


def create_drop(item_type, x, y, size):
    return {
        "type": item_type,
        "x": x,
        "y": y,
        "size": size,
    }


def is_liquid_block(block_type):
    return block_type in {"water", "lava"}


def is_door_block(block_type):
    return block_type in {
        "door_bottom_closed",
        "door_top_closed",
        "door_bottom_open",
        "door_top_open",
    }


def is_open_door_block(block_type):
    return block_type in {"door_bottom_open", "door_top_open"}


def is_closed_door_block(block_type):
    return block_type in {"door_bottom_closed", "door_top_closed"}


def get_crafting_panel_layout(has_workbench):
    grid_size = 3 if has_workbench else 2
    panel = pygame.Rect(36, 54, WIDTH - 72, 292)
    slot_size = 44
    gap = 8
    grid_x = panel.x + 20
    grid_y = panel.y + 54
    result_x = grid_x + grid_size * (slot_size + gap) + 26
    result_y = grid_y + ((grid_size - 1) * (slot_size + gap)) // 2
    inventory_x = result_x + slot_size + 34
    inventory_y = panel.y + 54
    return {
        "panel": panel,
        "grid_size": grid_size,
        "slot_size": slot_size,
        "gap": gap,
        "grid_x": grid_x,
        "grid_y": grid_y,
        "result_rect": pygame.Rect(result_x, result_y, slot_size, slot_size),
        "inventory_x": inventory_x,
        "inventory_y": inventory_y,
        "inventory_columns": 4,
    }


def evaluate_crafting_recipe(crafting_grid, has_workbench):
    grid_size = 3 if has_workbench else 2
    active_cells = crafting_grid[: grid_size * grid_size]
    non_empty = [(index, cell) for index, cell in enumerate(active_cells) if cell["type"] is not None and cell["count"] > 0]

    if not non_empty:
        return None

    total_wood = sum(cell["count"] for _, cell in non_empty if cell["type"] == "wood")
    other_than_wood = any(cell["type"] != "wood" for _, cell in non_empty)
    if total_wood == 1 and not other_than_wood:
        index = non_empty[0][0]
        return {"item_type": "plank", "count": 2, "consume": {index: 1}}

    total_planks = sum(cell["count"] for _, cell in non_empty if cell["type"] == "plank")
    other_than_planks = any(cell["type"] != "plank" for _, cell in non_empty)
    if not has_workbench and total_planks >= 8 and not other_than_planks:
        consume = {}
        remaining = 8
        for index, cell in non_empty:
            use = min(cell["count"], remaining)
            consume[index] = use
            remaining -= use
            if remaining <= 0:
                break
        return {"item_type": "workbench", "count": 1, "consume": consume}

    if has_workbench:
        top_middle = crafting_grid[1]
        center_middle = crafting_grid[4]
        stick_recipe_ok = (
            top_middle["type"] == "plank"
            and center_middle["type"] == "plank"
            and top_middle["count"] >= 2
            and center_middle["count"] >= 2
        )
        if stick_recipe_ok:
            others = [i for i in range(9) if i not in (1, 4)]
            if all(crafting_grid[i]["type"] is None or crafting_grid[i]["count"] <= 0 for i in others):
                return {"item_type": "stick", "count": 8, "consume": {1: 2, 4: 2}}

        wood_pickaxe_ok = (
            crafting_grid[0]["type"] == "plank"
            and crafting_grid[1]["type"] == "plank"
            and crafting_grid[2]["type"] == "plank"
            and crafting_grid[4]["type"] == "stick"
            and crafting_grid[7]["type"] == "stick"
            and crafting_grid[0]["count"] >= 1
            and crafting_grid[1]["count"] >= 1
            and crafting_grid[2]["count"] >= 1
            and crafting_grid[4]["count"] >= 1
            and crafting_grid[7]["count"] >= 1
        )
        if wood_pickaxe_ok:
            others = [i for i in range(9) if i not in (0, 1, 2, 4, 7)]
            if all(crafting_grid[i]["type"] is None or crafting_grid[i]["count"] <= 0 for i in others):
                return {"item_type": "wood_pickaxe", "count": 1, "consume": {0: 1, 1: 1, 2: 1, 4: 1, 7: 1}}

    return None


def draw_pixel_art(screen, x, y, size, pattern, palette):
    pixel = max(2, int(size // len(pattern)))
    for py, row in enumerate(pattern):
        for px, cell in enumerate(row):
            color = palette.get(cell)
            if color is None:
                continue
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x + px * pixel, y + py * pixel, pixel, pixel),
            )


def draw_ore_block(screen, x, y, size, ore_type):
    pygame.draw.rect(screen, STONE_COLOR, pygame.Rect(x, y, size, size))
    if ore_type == "coal_ore":
        ore_color = COAL_ORE_COLOR
        spots = [(8, 10), (22, 8), (18, 22), (34, 16), (28, 34), (10, 30)]
    elif ore_type == "iron_ore":
        ore_color = IRON_ORE_COLOR
        spots = [(8, 8), (24, 10), (16, 20), (34, 18), (28, 30), (12, 34)]
    elif ore_type == "gold_ore":
        ore_color = GOLD_ORE_COLOR
        spots = [(8, 10), (26, 8), (18, 20), (36, 16), (28, 30), (12, 34)]
    elif ore_type == "redstone_ore":
        ore_color = REDSTONE_ORE_COLOR
        spots = [(8, 8), (24, 8), (16, 20), (34, 18), (10, 32), (28, 32), (22, 42)]
    else:
        ore_color = DIAMOND_ORE_COLOR
        spots = [(10, 8), (26, 10), (16, 22), (34, 20), (24, 34), (8, 30)]

    chip = max(4, size // 6)
    for spot_x, spot_y in spots:
        sx = x + int(spot_x / 64 * size)
        sy = y + int(spot_y / 64 * size)
        pygame.draw.rect(screen, ore_color, pygame.Rect(sx, sy, chip, chip))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, size, size), 1)


def draw_nether_gold_ore_block(screen, x, y, size):
    pygame.draw.rect(screen, NETHERRACK_COLOR, pygame.Rect(x, y, size, size))
    spots = [(8, 8), (26, 10), (16, 22), (36, 18), (28, 30), (12, 36)]
    chip = max(4, size // 6)
    for spot_x, spot_y in spots:
        sx = x + int(spot_x / 64 * size)
        sy = y + int(spot_y / 64 * size)
        pygame.draw.rect(screen, NETHER_GOLD_ORE_COLOR, pygame.Rect(sx, sy, chip, chip))
    crack = max(2, size // 10)
    pygame.draw.rect(screen, (84, 32, 34), pygame.Rect(x + crack, y + size // 2, size - crack * 2, crack))
    pygame.draw.rect(screen, (24, 8, 8), pygame.Rect(x, y, size, size), 1)

def load_player_image():
    file_path = os.path.join(IMAGE_DIR, "player.png")
    if os.path.exists(file_path):
        img = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
    return None


def generate_ore_cluster(blocks, ore_type, attempts, min_y, max_y, cluster_size):
    for _ in range(attempts):
        start_x = random.randint(1, WORLD_W - 2)
        start_y = random.randint(min_y, min(max_y, WORLD_H - 2))
        if blocks.get((start_x, start_y)) != "stone":
            continue
        cluster = [(start_x, start_y)]
        for _ in range(cluster_size - 1):
            base_x, base_y = random.choice(cluster)
            nx = max(0, min(WORLD_W - 1, base_x + random.choice([-1, 0, 1])))
            ny = max(min_y, min(WORLD_H - 1, base_y + random.choice([-1, 0, 1])))
            if blocks.get((nx, ny)) == "stone":
                cluster.append((nx, ny))
        for pos in cluster:
            if blocks.get(pos) == "stone":
                blocks[pos] = ore_type


def generate_ore_cluster_in_block(blocks, ore_type, attempts, min_y, max_y, cluster_size, base_block):
    for _ in range(attempts):
        start_x = random.randint(1, WORLD_W - 2)
        start_y = random.randint(min_y, min(max_y, WORLD_H - 2))
        if blocks.get((start_x, start_y)) != base_block:
            continue
        cluster = [(start_x, start_y)]
        for _ in range(cluster_size - 1):
            base_x, base_y = random.choice(cluster)
            nx = max(0, min(WORLD_W - 1, base_x + random.choice([-1, 0, 1])))
            ny = max(min_y, min(WORLD_H - 1, base_y + random.choice([-1, 0, 1])))
            if blocks.get((nx, ny)) == base_block:
                cluster.append((nx, ny))
        for pos in cluster:
            if blocks.get(pos) == base_block:
                blocks[pos] = ore_type


def generate_diamond_ore(blocks, min_y, max_y, chance):
    for x in range(1, WORLD_W - 1):
        for y in range(min_y, min(max_y, WORLD_H - 1) + 1):
            if blocks.get((x, y)) == "stone" and random.random() < chance:
                blocks[(x, y)] = "diamond_ore"


def resolve_liquid_interactions(blocks):
    to_obsidian = []
    for (x, y), block_type in blocks.items():
        if block_type != "lava":
            continue
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if blocks.get((x + dx, y + dy)) == "water":
                to_obsidian.append((x, y))
                break
    for pos in to_obsidian:
        blocks[pos] = "obsidian"


def get_portal_frame_tiles(left_tile, bottom_tile, outer_w, outer_h):
    tiles = []
    top_tile = bottom_tile - outer_h + 1
    for x in range(left_tile, left_tile + outer_w):
        for y in range(top_tile, bottom_tile + 1):
            if x in (left_tile, left_tile + outer_w - 1) or y in (top_tile, bottom_tile):
                tiles.append((x, y))
    return tiles


def add_ruined_nether_portals(blocks, tree_blocks, heights, shore_start):
    portal_count = random.randint(1, 3)
    placed_left_tiles = []
    spawn_x_tile = WORLD_W // 2
    village_avoid_left = spawn_x_tile - 22
    village_avoid_right = spawn_x_tile + 34

    for _ in range(portal_count):
        outer_w = random.choice((4, 5))
        outer_h = random.choice((5, 6))
        candidates = []

        max_left = shore_start - outer_w - 3
        for left_tile in range(8, max_left):
            if village_avoid_left <= left_tile <= village_avoid_right:
                continue
            if any(abs(left_tile - other_left) < 12 for other_left in placed_left_tiles):
                continue

            surface_values = [heights[x] for x in range(left_tile, left_tile + outer_w)]
            if max(surface_values) - min(surface_values) > 1:
                continue
            if any(blocks.get((x, heights[x])) == "sand" for x in range(left_tile, left_tile + outer_w)):
                continue

            bottom_tile = min(surface_values)
            top_tile = bottom_tile - outer_h + 1
            if top_tile < 3:
                continue
            candidates.append((left_tile, bottom_tile, outer_w, outer_h))

        if not candidates:
            continue

        left_tile, bottom_tile, outer_w, outer_h = random.choice(candidates)
        frame_tiles = get_portal_frame_tiles(left_tile, bottom_tile, outer_w, outer_h)

        keep_tiles = {
            (left_tile, bottom_tile),
            (left_tile + outer_w - 1, bottom_tile),
            (left_tile, bottom_tile - 1),
            (left_tile + outer_w - 1, bottom_tile - 1),
        }
        removable_tiles = [tile for tile in frame_tiles if tile not in keep_tiles]
        remove_count = random.randint(2, min(5, len(removable_tiles)))
        missing_tiles = set(random.sample(removable_tiles, remove_count))

        for x in range(left_tile - 1, left_tile + outer_w + 1):
            ground_y = heights.get(x)
            if ground_y is None:
                continue
            for y in range(bottom_tile + 1, ground_y + 1):
                if 0 <= y < WORLD_H - 1:
                    current = blocks.get((x, y))
                    if current in {"grass", "dirt", "sand"}:
                        blocks[(x, y)] = "dirt"

        for tile in frame_tiles:
            if tile in missing_tiles:
                blocks.pop(tile, None)
            else:
                blocks[tile] = "obsidian"

        remove_tree_blocks_in_tile_rect(
            tree_blocks,
            left_tile - 2,
            bottom_tile - outer_h - 1,
            left_tile + outer_w + 1,
            bottom_tile + 2,
        )
        placed_left_tiles.append(left_tile)

def build_terrain():
    """Create rolling land with a coast, a large ocean, and several tree-filled islands."""
    blocks = {}  # (x, y) -> type: "grass", "dirt", "stone", "water"
    base = WORLD_H // 2
    sea_level = base + 1
    ocean_start = WORLD_W - OCEAN_WIDTH
    shore_start = ocean_start - OCEAN_SHORE_WIDTH
    island_ranges = []
    island_surface = {}

    island_start = ocean_start + 1
    for _ in range(ISLAND_COUNT):
        end_x = island_start + ISLAND_WIDTH - 1
        if end_x >= WORLD_W:
            break
        island_ranges.append((island_start, end_x))
        center_x = (island_start + end_x) / 2.0
        for x in range(island_start, end_x + 1):
            distance = abs(x - center_x)
            if distance < 0.5:
                island_surface[x] = sea_level - 2
            else:
                island_surface[x] = sea_level - 1
        island_start = end_x + 2

    # Generate basic height map
    heights = {}
    for x in range(WORLD_W):
        h = int(base + 2.0 * math.sin(x * 0.35))
        h = max(4, min(h, WORLD_H - 6))
        if x in island_surface:
            h = island_surface[x]
        elif x >= ocean_start:
            h = sea_level + 4 + int(1.5 * math.sin((x - ocean_start) * 0.9))
        elif x >= shore_start:
            slope_t = (x - shore_start + 1) / max(1, OCEAN_SHORE_WIDTH)
            target_h = sea_level + 2
            h = int(h * (1.0 - slope_t) + target_h * slope_t)
        heights[x] = h

    # Fill blocks based on height map
    for x in range(WORLD_W):
        surface_y = heights[x]
        if x >= ocean_start and x not in island_surface:
            seabed_y = max(sea_level + 3, min(surface_y, WORLD_H - 4))
            for y in range(sea_level, seabed_y):
                blocks[(x, y)] = "water"
            for y in range(seabed_y, WORLD_H):
                if y <= seabed_y + 1:
                    blocks[(x, y)] = "sand"
                elif y <= seabed_y + 2:
                    blocks[(x, y)] = "dirt"
                else:
                    blocks[(x, y)] = "stone"
            continue

        for y in range(surface_y, WORLD_H):
            if x >= shore_start and y == surface_y and surface_y >= sea_level:
                blocks[(x, y)] = "sand"
            elif x >= shore_start and y <= surface_y + 2:
                blocks[(x, y)] = "sand"
            elif y == surface_y:
                blocks[(x, y)] = "grass"
            elif y <= surface_y + 2:
                blocks[(x, y)] = "dirt"
            else:
                blocks[(x, y)] = "stone"

    generate_ore_cluster(blocks, "coal_ore", 18, WORLD_H // 2 + 1, WORLD_H - 4, 5)
    # Make iron easier to spot and reach than diamond so progression does not stall.
    generate_ore_cluster(blocks, "iron_ore", 24, WORLD_H // 2 + 2, WORLD_H - 3, 6)
    generate_ore_cluster(blocks, "redstone_ore", 24, WORLD_H // 2 + 2, WORLD_H - 3, 6)
    generate_ore_cluster(blocks, "gold_ore", 14, WORLD_H // 2 + 5, WORLD_H - 3, 4)
    generate_ore_cluster(blocks, "lava", 10, WORLD_H // 2 + 8, WORLD_H - 3, 4)
    generate_diamond_ore(blocks, WORLD_H - 8, WORLD_H - 2, DIAMOND_ORE_CHANCE)
    resolve_liquid_interactions(blocks)

    # Seal the bottom of the world with bedrock so current pickaxes cannot break through.
    for x in range(WORLD_W):
        blocks[(x, WORLD_H - 1)] = "bedrock"
        
    trees = {}
    for x in range(2, WORLD_W - 2):
        if x < shore_start and random.random() < 0.2:
            trunk_height = random.randint(3, 4)
            # 记录在 x, surface_y-1 的位置有树
            # 值包含树干高度
            trees[x] = trunk_height

    for island_start, island_end in island_ranges:
        island_tree_columns = list(range(island_start, island_end + 1))
        for tx in island_tree_columns[:MIN_TREES_PER_ISLAND]:
            trees[tx] = random.randint(3, 4)
            
    # 预计算所有树的小方块
    # tree_blocks 格式: (world_x, world_y) -> block_type
    # 这里用真实的世界坐标(像素)
    TREE_TILE_SIZE = TILE_SIZE // 2
    tree_blocks = {}
    for tx, trunk_height in trees.items():
        surface_y = heights[tx]
        base_x = tx * TILE_SIZE + (TILE_SIZE - TREE_TILE_SIZE) // 2
        base_y = surface_y * TILE_SIZE
        
        # 树干
        for i in range(trunk_height):
            wy = base_y - (i + 1) * TREE_TILE_SIZE
            tree_blocks[(base_x, wy)] = "wood"
            
        # 树叶 (3x3 树冠)
        top_y = base_y - trunk_height * TREE_TILE_SIZE
        for lx in range(-1, 2):
            for ly in range(0, 3):
                # 去掉四个角的一点点让树冠更圆润
                if (lx == -1 and ly == 2) or (lx == 1 and ly == 2):
                    continue
                wx = base_x + lx * TREE_TILE_SIZE
                wy = top_y - ly * TREE_TILE_SIZE
                tree_blocks[(wx, wy)] = "leaf"

    add_ruined_nether_portals(blocks, tree_blocks, heights, shore_start)

    return blocks, tree_blocks


def build_nether_terrain():
    blocks = {}
    tree_blocks = {}
    for x in range(WORLD_W):
        ceiling_depth = 3 + int((math.sin(x * 0.23) + 1.0) * 1.6)
        for y in range(1, min(WORLD_H - 1, ceiling_depth + 1)):
            blocks[(x, y)] = "netherrack"

        floor_top = WORLD_H - 8 + int(math.sin(x * 0.17) * 2 + math.sin(x * 0.47))
        floor_top = max(WORLD_H // 2 + 4, min(WORLD_H - 5, floor_top))
        for y in range(floor_top, WORLD_H - 1):
            blocks[(x, y)] = "netherrack"
        for y in range(max(floor_top + 3, WORLD_H - 3), WORLD_H - 1):
            if blocks.get((x, y)) == "netherrack":
                blocks[(x, y)] = "lava"

    platform_centers = [WORLD_W // 2 - 34, WORLD_W // 2, WORLD_W // 2 + 32]
    for center_x in platform_centers:
        for x in range(max(2, center_x - 7), min(WORLD_W - 2, center_x + 8)):
            curve = 1.0 - abs(x - center_x) / 8.0
            if curve <= 0:
                continue
            top_y = WORLD_H // 2 + int((1.0 - curve) * 4)
            thickness = 2 + int(curve * 2)
            for y in range(top_y, min(WORLD_H - 4, top_y + thickness)):
                blocks[(x, y)] = "netherrack"

    for x in range(WORLD_W // 2 - 2, WORLD_W // 2 + 3):
        for y in range(WORLD_H // 2 + 4, WORLD_H - 4):
            if blocks.get((x, y)) == "lava":
                blocks[(x, y)] = "netherrack"

    generate_ore_cluster_in_block(blocks, "nether_gold_ore", 26, 2, WORLD_H - 5, 5, "netherrack")

    return blocks, tree_blocks


def is_valid_nether_portal_frame(blocks, left, top, right, bottom):
    outer_w = right - left + 1
    outer_h = bottom - top + 1
    if outer_w < 3 or outer_h < 4:
        return False

    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            block_type = blocks.get((x, y))
            is_corner = x in (left, right) and y in (top, bottom)
            is_border = x in (left, right) or y in (top, bottom)
            if is_corner:
                if block_type not in (None, "obsidian"):
                    return False
            elif is_border:
                if block_type != "obsidian":
                    return False
            elif block_type not in (None, "fire", "nether_portal"):
                return False
    return True


def find_nether_portal_frame_from_fire(blocks, fire_pos):
    fx, fy = fire_pos
    best_frame = None
    best_area = None

    for left in range(max(0, fx - 5), fx):
        for right in range(fx + 1, min(WORLD_W, fx + 6)):
            for top in range(max(0, fy - 6), fy):
                for bottom in range(fy + 1, min(WORLD_H, fy + 7)):
                    if not (left < fx < right and top < fy < bottom):
                        continue
                    if not is_valid_nether_portal_frame(blocks, left, top, right, bottom):
                        continue
                    area = (right - left + 1) * (bottom - top + 1)
                    if best_area is None or area < best_area:
                        best_area = area
                        best_frame = (left, top, right, bottom)

    return best_frame


def activate_nether_portal(blocks, fire_pos):
    frame = find_nether_portal_frame_from_fire(blocks, fire_pos)
    if frame is None:
        return False

    left, top, right, bottom = frame
    for x in range(left + 1, right):
        for y in range(top + 1, bottom):
            blocks[(x, y)] = "nether_portal"
    return True


def lerp_color(c1, c2, t):
    """Linear interpolate between two colors."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

def get_time_color_and_darkness(time_of_day):
    """
    time_of_day goes from 0 to 24.
    Returns (sky_color, overlay_color, overlay_alpha)
    """
    if 6 <= time_of_day < 17:
        # Day
        return SKY_DAY, NIGHT_TINT, 0
    elif 17 <= time_of_day < 19:
        # Sunset (17 to 19)
        t = (time_of_day - 17) / 2.0
        return lerp_color(SKY_DAY, SKY_SUNSET, t), NIGHT_TINT, int(lerp_color((0, 0, 0), (45, 0, 0), t)[0])
    elif 19 <= time_of_day < 20:
        # Dusk to Night (19 to 20)
        t = (time_of_day - 19) / 1.0
        return lerp_color(SKY_SUNSET, SKY_NIGHT, t), NIGHT_TINT, int(lerp_color((45, 0, 0), (110, 0, 0), t)[0])
    elif 20 <= time_of_day <= 24 or 0 <= time_of_day < 5:
        # Night
        return SKY_NIGHT, NIGHT_TINT, 110
    elif 5 <= time_of_day < 6:
        # Dawn (5 to 6)
        t = (time_of_day - 5) / 1.0
        return lerp_color(SKY_NIGHT, SKY_DAY, t), NIGHT_TINT, int(lerp_color((110, 0, 0), (0, 0, 0), t)[0])
    return SKY_DAY, NIGHT_TINT, 0


def get_dimension_sky(current_dimension, time_of_day):
    if current_dimension == "nether":
        return NETHER_SKY_COLOR, NETHER_DARKNESS_TINT, 18
    return get_time_color_and_darkness(time_of_day)

def draw_world(screen, camera_x, camera_y, blocks, tree_blocks):
    """Draw blocks and trees."""
    for (x, y), block_type in blocks.items():
        world_x = x * TILE_SIZE
        world_y = y * TILE_SIZE

        screen_x = world_x - camera_x
        screen_y = world_y - camera_y

        # Skip tiles outside the screen for better performance.
        if (
            screen_x + TILE_SIZE < 0
            or screen_x > WIDTH
            or screen_y + TILE_SIZE < 0
            or screen_y > HEIGHT
        ):
            continue

        if block_type == "water":
            color = WATER_COLOR
        elif block_type == "lava":
            color = LAVA_COLOR
        elif block_type == "grass":
            color = GRASS_COLOR
        elif block_type == "dirt":
            color = DIRT_COLOR
        elif block_type == "sand":
            color = SAND_COLOR
        elif block_type == "plank":
            color = PLANK_COLOR
        elif is_door_block(block_type):
            if is_open_door_block(block_type):
                pygame.draw.rect(
                    screen,
                    PLANK_COLOR,
                    pygame.Rect(screen_x + TILE_SIZE - 12, screen_y + 4, 8, TILE_SIZE - 8),
                )
                pygame.draw.rect(
                    screen,
                    (84, 54, 28),
                    pygame.Rect(screen_x + TILE_SIZE - 12, screen_y + 4, 8, TILE_SIZE - 8),
                    1,
                )
                continue
            color = (150, 102, 54)
        elif block_type == "obsidian":
            color = OBSIDIAN_COLOR
        elif block_type == "netherrack":
            color = NETHERRACK_COLOR
        elif block_type == "bedrock":
            color = BEDROCK_COLOR
        elif block_type == "diamond_block":
            color = DIAMOND_BLOCK_COLOR
        elif block_type == "redstone_block":
            color = REDSTONE_COLOR
        elif block_type == "nether_gold_ore":
            draw_nether_gold_ore_block(screen, screen_x, screen_y, TILE_SIZE)
            continue
        elif block_type == "nether_portal":
            pygame.draw.rect(screen, NETHER_PORTAL_COLOR, pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            inner_rect = pygame.Rect(screen_x + 6, screen_y + 6, TILE_SIZE - 12, TILE_SIZE - 12)
            pygame.draw.rect(screen, (196, 170, 236), inner_rect)
            pygame.draw.rect(screen, (110, 82, 154), pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE), 2)
            continue
        elif block_type == "fire":
            pygame.draw.rect(screen, (255, 170, 40), pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            flame_size = max(10, TILE_SIZE // 3)
            flame_x = screen_x + (TILE_SIZE - flame_size) // 2
            flame_y = screen_y + TILE_SIZE // 5
            pygame.draw.polygon(
                screen,
                (255, 220, 110),
                [
                    (flame_x + flame_size // 2, flame_y),
                    (flame_x + flame_size, flame_y + flame_size),
                    (flame_x + flame_size // 2, flame_y + flame_size + flame_size // 3),
                    (flame_x, flame_y + flame_size),
                ],
            )
            pygame.draw.polygon(
                screen,
                (255, 90, 30),
                [
                    (flame_x + flame_size // 2, flame_y + flame_size // 4),
                    (flame_x + flame_size * 3 // 4, flame_y + flame_size),
                    (flame_x + flame_size // 2, flame_y + flame_size),
                    (flame_x + flame_size // 4, flame_y + flame_size),
                ],
            )
            continue
        elif block_type == "coal_ore":
            draw_ore_block(screen, screen_x, screen_y, TILE_SIZE, "coal_ore")
            continue
        elif block_type == "iron_ore":
            draw_ore_block(screen, screen_x, screen_y, TILE_SIZE, "iron_ore")
            continue
        elif block_type == "gold_ore":
            draw_ore_block(screen, screen_x, screen_y, TILE_SIZE, "gold_ore")
            continue
        elif block_type == "redstone_ore":
            draw_ore_block(screen, screen_x, screen_y, TILE_SIZE, "redstone_ore")
            continue
        elif block_type == "diamond_ore":
            draw_ore_block(screen, screen_x, screen_y, TILE_SIZE, "diamond_ore")
            continue
        else:
            color = STONE_COLOR
            
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE),
        )
        if is_closed_door_block(block_type):
            knob_x = screen_x + TILE_SIZE - 12
            knob_y = screen_y + TILE_SIZE // 2
            pygame.draw.rect(screen, (212, 188, 86), pygame.Rect(knob_x, knob_y, 4, 4))

        # Thin grid line to keep the "block" feel clear.
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE),
            1,
        )

    # Draw trees
    TREE_TILE_SIZE = TILE_SIZE // 2
    for (world_x, world_y), block_type in tree_blocks.items():
        screen_x = world_x - camera_x
        screen_y = world_y - camera_y

        if (
            screen_x + TREE_TILE_SIZE < 0
            or screen_x > WIDTH
            or screen_y + TREE_TILE_SIZE < 0
            or screen_y > HEIGHT
        ):
            continue

        color = WOOD_COLOR if block_type == "wood" else LEAF_COLOR
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(screen_x, screen_y, TREE_TILE_SIZE, TREE_TILE_SIZE),
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            pygame.Rect(screen_x, screen_y, TREE_TILE_SIZE, TREE_TILE_SIZE),
            1,
        )


def draw_crosshair(screen, crosshair_x, crosshair_y):
    """Draw a white plus sign at the given screen position."""
    cx, cy = crosshair_x, crosshair_y
    half = 10
    thickness = 2
    pygame.draw.line(screen, WHITE, (cx - half, cy), (cx + half, cy), thickness)
    pygame.draw.line(screen, WHITE, (cx, cy - half), (cx, cy + half), thickness)


def get_workbench_position(player_x, player_facing_right, blocks):
    size = TILE_SIZE // 2
    offset_x = PLAYER_SIZE + 10 if player_facing_right else -size - 10
    world_x = player_x + offset_x
    world_x = max(0, min(world_x, WORLD_W * TILE_SIZE - size))
    ground_top = ground_top_y_for_x(world_x + size / 2, blocks)
    world_y = ground_top - size
    return world_x, world_y, size


def draw_workbench(screen, workbench, camera_x, camera_y):
    if workbench is None:
        return
    sx = workbench["x"] - camera_x
    sy = workbench["y"] - camera_y
    size = workbench["size"]
    if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
        return
    pattern = [
        "12221",
        "23432",
        "24542",
        "23432",
        "13331",
    ]
    palette = {
        "1": (110, 69, 34),
        "2": (145, 93, 48),
        "3": (170, 120, 64),
        "4": (92, 63, 36),
        "5": (194, 166, 103),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    pygame.draw.rect(screen, (30, 20, 10), pygame.Rect(sx, sy, size, size), 1)


def draw_furnace(screen, furnace, camera_x, camera_y):
    if furnace is None:
        return
    sx = furnace["x"] - camera_x
    sy = furnace["y"] - camera_y
    size = furnace["size"]
    if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
        return
    pattern = [
        "11111",
        "12221",
        "13331",
        "14441",
        "11111",
    ]
    palette = {
        "1": (88, 88, 88),
        "2": (128, 128, 128),
        "3": (40, 40, 40),
        "4": (196, 120, 64),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    pygame.draw.rect(screen, (24, 24, 24), pygame.Rect(sx, sy, size, size), 1)


def draw_pickaxe(screen, x, y, size, head_color, handle_color):
    pattern = [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
    ]
    palette = {
        "0": None,
        "1": head_color,
        "2": handle_color,
    }
    pattern = [
        "11111",
        "00200",
        "00200",
        "00200",
        "00200",
    ]
    draw_pixel_art(screen, x, y, size, pattern, palette)


def draw_wood_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (170, 120, 64), (140, 98, 58))


def draw_stone_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (150, 150, 150), (140, 98, 58))


def draw_iron_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (218, 218, 225), (140, 98, 58))


def draw_gold_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (242, 206, 80), (140, 98, 58))


def draw_diamond_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (120, 240, 235), (140, 98, 58))


def draw_redstone_pickaxe(screen, x, y, size):
    draw_pickaxe(screen, x, y, size, (220, 52, 52), (140, 98, 58))


def draw_sword(screen, x, y, size, blade_color, hilt_color):
    pattern = [
        "00100",
        "00100",
        "00100",
        "01110",
        "00100",
    ]
    palette = {
        "0": None,
        "1": blade_color,
    }
    draw_pixel_art(screen, x, y, size, pattern, palette)
    pixel = max(2, int(size // 5))
    pygame.draw.rect(screen, hilt_color, pygame.Rect(x + 2 * pixel, y + 3 * pixel, pixel, 2 * pixel))
    pygame.draw.rect(screen, hilt_color, pygame.Rect(x + pixel, y + 3 * pixel, 3 * pixel, pixel))


def draw_iron_sword(screen, x, y, size):
    draw_sword(screen, x, y, size, (228, 228, 236), (120, 76, 46))


def draw_diamond_sword(screen, x, y, size):
    draw_sword(screen, x, y, size, (110, 236, 232), (120, 76, 46))


def draw_iron_golem(screen, sx, sy, size, facing_right):
    pattern = [
        "01111110",
        "11222211",
        "12333321",
        "12444421",
        "12444421",
        "12422421",
        "12500521",
        "02500520",
    ]
    palette = {
        "0": None,
        "1": (186, 194, 186),
        "2": (150, 156, 150),
        "3": (116, 132, 96),
        "4": (208, 214, 208),
        "5": (124, 88, 56),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    eye_x = sx + (size * 5 // 8 if facing_right else size * 3 // 8)
    pygame.draw.rect(screen, (74, 40, 20), pygame.Rect(eye_x, sy + size // 3, 3, 2))


def draw_villager(screen, sx, sy, size, facing_right):
    pattern = [
        "01111110",
        "11233211",
        "11222211",
        "01344310",
        "01444410",
        "01444410",
        "01555510",
        "01500510",
    ]
    palette = {
        "0": None,
        "1": (110, 70, 44),
        "2": (214, 178, 142),
        "3": (66, 40, 28),
        "4": (130, 84, 44),
        "5": (86, 56, 30),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    eye_x = sx + (size * 5 // 8 if facing_right else size * 3 // 8)
    pygame.draw.rect(screen, (32, 20, 12), pygame.Rect(eye_x, sy + size // 3, 2, 2))


def draw_piglin(screen, sx, sy, size, facing_right):
    pattern = [
        "01111110",
        "11222211",
        "12344321",
        "12455421",
        "12444421",
        "12666621",
        "12600621",
        "02600620",
    ]
    palette = {
        "0": None,
        "1": (148, 92, 92),
        "2": (214, 156, 146),
        "3": (244, 196, 170),
        "4": (198, 136, 128),
        "5": (126, 72, 70),
        "6": (108, 72, 38),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    eye_x = sx + (size * 5 // 8 if facing_right else size * 3 // 8)
    pygame.draw.rect(screen, (30, 18, 18), pygame.Rect(eye_x, sy + size // 3, 2, 2))


def ground_top_y_for_x(world_x, blocks):
    """Get world y of the top surface block for a world x position."""
    tile_x = int(world_x // TILE_SIZE)
    tile_x = max(0, min(tile_x, WORLD_W - 1))
    
    surface_y = WORLD_H
    for y in range(WORLD_H):
        if (tile_x, y) in blocks:
            # Water acts like an open block for entities, they sink into it
            # so we find the first solid block
            if blocks[(tile_x, y)] == "water" or is_door_block(blocks[(tile_x, y)]):
                continue
            surface_y = y
            break
            
    return surface_y * TILE_SIZE


def find_nether_surface_y(tile_x, blocks):
    tile_x = max(0, min(tile_x, WORLD_W - 1))
    for y in range(WORLD_H - 2, 2, -1):
        block_type = blocks.get((tile_x, y))
        if block_type is None or is_liquid_block(block_type) or is_door_block(block_type):
            continue
        above_1 = blocks.get((tile_x, y - 1))
        above_2 = blocks.get((tile_x, y - 2))
        if above_1 is None and above_2 is None:
            return y * TILE_SIZE
    return None


def get_entity_support_y(entity_rect, blocks):
    probe = pygame.Rect(entity_rect.x, entity_rect.bottom, entity_rect.width, max(2, TILE_SIZE // 8))
    support_rects = get_solid_block_rects(probe, blocks)
    if not support_rects:
        return None
    return min(rect.top for rect in support_rects)


def remove_tree_blocks_in_tile_rect(tree_blocks, left_tile, top_tile, right_tile, bottom_tile):
    to_remove = []
    for wx, wy in tree_blocks.keys():
        tile_x = int(wx // TILE_SIZE)
        tile_y = int(wy // TILE_SIZE)
        if left_tile <= tile_x <= right_tile and top_tile <= tile_y <= bottom_tile:
            to_remove.append((wx, wy))
    for pos in to_remove:
        tree_blocks.pop(pos, None)


def can_place_house(blocks, left_tile, width):
    surfaces = []
    for tx in range(left_tile, left_tile + width):
        surface_y = ground_top_y_for_x(tx * TILE_SIZE + TILE_SIZE / 2, blocks) // TILE_SIZE
        if surface_y >= WORLD_H - 2:
            return None
        if blocks.get((tx, surface_y)) == "water":
            return None
        surfaces.append(surface_y)
    if max(surfaces) - min(surfaces) > 1:
        return None
    return max(surfaces)


def place_house(blocks, tree_blocks, left_tile, ground_y):
    width = 5
    top_y = ground_y - 4
    floor_y = ground_y - 1
    door_columns = {left_tile, left_tile + width - 1}

    for tx in range(left_tile, left_tile + width):
        column_surface = ground_top_y_for_x(tx * TILE_SIZE + TILE_SIZE / 2, blocks) // TILE_SIZE
        for ty in range(column_surface, floor_y + 1):
            blocks[(tx, ty)] = "plank"

    for tx in range(left_tile, left_tile + width):
        for ty in range(top_y, floor_y + 1):
            is_border = tx in (left_tile, left_tile + width - 1) or ty in (top_y, floor_y)
            is_door = tx in door_columns and ty in (floor_y, floor_y - 1)
            if is_door:
                if ty == floor_y:
                    blocks[(tx, ty)] = "door_bottom_closed"
                else:
                    blocks[(tx, ty)] = "door_top_closed"
            elif is_border:
                blocks[(tx, ty)] = "plank"
            else:
                blocks.pop((tx, ty), None)

    remove_tree_blocks_in_tile_rect(tree_blocks, left_tile - 1, top_y - 1, left_tile + width, floor_y + 1)
    villager_x = (left_tile + width / 2) * TILE_SIZE - VILLAGER_SIZE / 2
    villager_y = floor_y * TILE_SIZE - VILLAGER_SIZE
    return villager_x, villager_y


def create_village(blocks, tree_blocks):
    villagers = []
    house_width = 5
    spacing = 3
    needed_width = len(VILLAGER_TRADES) * (house_width + spacing)
    spawn_x_tile = WORLD_W // 2
    preferred_start = max(8, min(spawn_x_tile + 2, WORLD_W - OCEAN_WIDTH - needed_width - 4))

    candidate_starts = [preferred_start]
    for offset in range(1, 10):
        left_option = preferred_start - offset
        right_option = preferred_start + offset
        if left_option >= 8:
            candidate_starts.append(left_option)
        if right_option <= WORLD_W - OCEAN_WIDTH - needed_width - 4:
            candidate_starts.append(right_option)

    start_tile = None
    for tx in candidate_starts:
        house_ground = can_place_house(blocks, tx, needed_width)
        if house_ground is not None:
            start_tile = tx
            break

    if start_tile is None:
        start_tile = preferred_start

    for index, trade in enumerate(VILLAGER_TRADES):
        house_left = start_tile + index * (house_width + spacing)
        ground_y = can_place_house(blocks, house_left, house_width)
        if ground_y is None:
            continue
        villager_x, villager_y = place_house(blocks, tree_blocks, house_left, ground_y)
        villagers.append(
            {
                "x": villager_x,
                "y": villager_y,
                "spawn_x": villager_x,
                "spawn_y": villager_y,
                "size": VILLAGER_SIZE,
                "vx": random.choice([-1, 1]) * VILLAGER_SPEED,
                "trade_item": trade["item"],
                "trade_cost": trade["cost"],
                "trade_label": trade["label"],
                "home_left": house_left * TILE_SIZE,
                "home_right": (house_left + house_width - 1) * TILE_SIZE,
                "facing_right": True,
                "hp": VILLAGER_HP,
            }
        )
    return villagers


def create_iron_golems(villagers, blocks):
    if not villagers:
        return []

    min_home = min(villager["home_left"] for villager in villagers)
    max_home = max(villager["home_right"] for villager in villagers)
    center_x = (min_home + max_home) / 2
    ground_y = ground_top_y_for_x(center_x, blocks)
    golem_x = center_x - IRON_GOLEM_SIZE / 2
    golem_y = ground_y - IRON_GOLEM_SIZE
    return [
        {
            "x": golem_x,
            "y": golem_y,
            "spawn_x": golem_x,
            "spawn_y": golem_y,
            "size": IRON_GOLEM_SIZE,
            "vx": random.choice([-1, 1]) * IRON_GOLEM_SPEED,
            "home_left": min_home - TILE_SIZE,
            "home_right": max_home + TILE_SIZE,
            "facing_right": True,
            "hp": IRON_GOLEM_HP,
        }
    ]


def update_villagers(villagers, blocks, dt, items, villager_respawn_queue):
    for villager in villagers[:]:
        if "vy" not in villager:
            villager["vy"] = 0.0
        if random.random() < 0.01:
            villager["vx"] *= -1

        villager["vy"] += GRAVITY * dt
        villager["y"] += villager["vy"] * dt

        next_x = villager["x"] + villager["vx"] * dt
        if next_x < villager["home_left"] or next_x > villager["home_right"]:
            villager["vx"] *= -1
            next_x = max(villager["home_left"], min(next_x, villager["home_right"]))

        move_rect = pygame.Rect(
            math.floor(next_x),
            math.floor(villager["y"]),
            villager["size"],
            villager["size"],
        )
        blocked = False
        for block_rect in get_solid_block_rects(move_rect, blocks):
            blocked = True
            if villager["vx"] > 0:
                move_rect.right = block_rect.left
            else:
                move_rect.left = block_rect.right
        if blocked:
            villager["vx"] *= -1
        villager["x"] = float(move_rect.x)
        villager["facing_right"] = villager["vx"] >= 0

        villager_rect = pygame.Rect(
            math.floor(villager["x"]),
            math.floor(villager["y"]),
            villager["size"],
            villager["size"],
        )
        support_y = get_entity_support_y(villager_rect, blocks)
        if support_y is not None and villager["y"] + villager["size"] >= support_y:
            villager["y"] = support_y - villager["size"]
            villager["vy"] = 0.0

        fire_hits = accumulate_fire_damage(villager, rect_overlaps_block_type(villager_rect, blocks, "fire"), dt)
        if fire_hits > 0:
            villager["hp"] -= fire_hits
            if villager["hp"] <= 0:
                kill_villager(villager, villagers, items, villager_respawn_queue)


def update_village_doors(blocks, player_x, player_y, villagers):
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    handled_bottoms = set()
    for (tx, ty), block_type in list(blocks.items()):
        if block_type not in {"door_bottom_closed", "door_bottom_open"}:
            continue
        if (tx, ty) in handled_bottoms:
            continue
        top_block = blocks.get((tx, ty - 1))
        if top_block not in {"door_top_closed", "door_top_open"}:
            continue
        handled_bottoms.add((tx, ty))

        door_rect = pygame.Rect(tx * TILE_SIZE, (ty - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE * 2)
        proximity_rect = door_rect.inflate(TILE_SIZE // 2, TILE_SIZE // 2)
        should_open = proximity_rect.colliderect(player_rect)

        if not should_open:
            for villager in villagers:
                villager_rect = pygame.Rect(villager["x"], villager["y"], villager["size"], villager["size"])
                if proximity_rect.colliderect(villager_rect):
                    should_open = True
                    break

        bottom_pos = (tx, ty)
        top_pos = (tx, ty - 1)

        if should_open:
            blocks[top_pos] = "door_top_open"
            blocks[bottom_pos] = "door_bottom_open"
        else:
            blocks[top_pos] = "door_top_closed"
            blocks[bottom_pos] = "door_bottom_closed"


def update_iron_golems(iron_golems, blocks, dt, items, iron_golem_respawn_queue):
    for golem in iron_golems[:]:
        if "vy" not in golem:
            golem["vy"] = 0.0
        if random.random() < 0.006:
            golem["vx"] *= -1

        golem["vy"] += GRAVITY * dt
        golem["y"] += golem["vy"] * dt

        next_x = golem["x"] + golem["vx"] * dt
        if next_x < golem["home_left"] or next_x > golem["home_right"]:
            golem["vx"] *= -1
            next_x = max(golem["home_left"], min(next_x, golem["home_right"]))

        move_rect = pygame.Rect(
            math.floor(next_x),
            math.floor(golem["y"]),
            golem["size"],
            golem["size"],
        )
        blocked = False
        for block_rect in get_solid_block_rects(move_rect, blocks):
            blocked = True
            if golem["vx"] > 0:
                move_rect.right = block_rect.left
            else:
                move_rect.left = block_rect.right
        if blocked:
            golem["vx"] *= -1
        golem["x"] = float(move_rect.x)
        golem["facing_right"] = golem["vx"] >= 0

        golem_rect = pygame.Rect(
            math.floor(golem["x"]),
            math.floor(golem["y"]),
            golem["size"],
            golem["size"],
        )
        support_y = get_entity_support_y(golem_rect, blocks)
        if support_y is not None and golem["y"] + golem["size"] >= support_y:
            golem["y"] = support_y - golem["size"]
            golem["vy"] = 0.0

        fire_hits = accumulate_fire_damage(golem, rect_overlaps_block_type(golem_rect, blocks, "fire"), dt)
        if fire_hits > 0:
            golem["hp"] -= fire_hits
            if golem["hp"] <= 0:
                kill_iron_golem(golem, iron_golems, items, iron_golem_respawn_queue)


def draw_villagers(screen, villagers, camera_x, camera_y, font):
    for villager in villagers:
        sx = villager["x"] - camera_x
        sy = villager["y"] - camera_y
        size = villager["size"]
        if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
            continue
        draw_villager(screen, sx, sy, size, villager.get("facing_right", True))
        label = font.render("Villager", True, (20, 20, 20))
        trade = font.render(f"{villager['trade_cost']}D -> {villager['trade_label']}", True, (20, 20, 20))
        hp_text = font.render(f"HP:{villager['hp']}", True, (20, 20, 20))
        screen.blit(label, (sx - 2, sy - 26))
        screen.blit(trade, (sx - 12, sy - 14))
        screen.blit(hp_text, (sx - 2, sy + size + 2))


def draw_iron_golems(screen, iron_golems, camera_x, camera_y, font):
    for golem in iron_golems:
        sx = golem["x"] - camera_x
        sy = golem["y"] - camera_y
        size = golem["size"]
        if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
            continue
        draw_iron_golem(screen, sx, sy, size, golem.get("facing_right", True))
        label = font.render("Iron Golem", True, (20, 20, 20))
        hp_text = font.render(f"HP:{golem['hp']}", True, (20, 20, 20))
        screen.blit(label, (sx - 8, sy - 16))
        screen.blit(hp_text, (sx + 2, sy + size + 2))


def find_nearby_villager(player_x, player_y, villagers):
    player_center_x = player_x + PLAYER_SIZE / 2
    player_center_y = player_y + PLAYER_SIZE / 2
    closest = None
    closest_dist = VILLAGER_TRADE_RANGE
    for villager in villagers:
        villager_center_x = villager["x"] + villager["size"] / 2
        villager_center_y = villager["y"] + villager["size"] / 2
        dist = math.hypot(player_center_x - villager_center_x, player_center_y - villager_center_y)
        if dist <= closest_dist:
            closest = villager
            closest_dist = dist
    return closest


def find_nearby_piglin(player_x, player_y, animals):
    player_center_x = player_x + PLAYER_SIZE / 2
    player_center_y = player_y + PLAYER_SIZE / 2
    closest = None
    closest_dist = PIGLIN_TRADE_RANGE
    for animal in animals:
        if animal["name"] != "Piglin":
            continue
        animal_center_x = animal["x"] + animal["size"] / 2
        animal_center_y = animal["y"] + animal["size"] / 2
        dist = math.hypot(player_center_x - animal_center_x, player_center_y - animal_center_y)
        if dist <= closest_dist:
            closest = animal
            closest_dist = dist
    return closest


def barter_with_piglin(meats, piglin):
    return "fire_resistance_potion", 1, "1 fire resistance potion"


def get_water_column_bounds(tile_x, blocks):
    tile_x = max(0, min(tile_x, WORLD_W - 1))
    top_water = None
    bottom_water = None
    for y in range(WORLD_H):
        if blocks.get((tile_x, y)) == "water":
            if top_water is None:
                top_water = y
            bottom_water = y
    return top_water, bottom_water


def is_ocean_column(tile_x, blocks):
    top_water, bottom_water = get_water_column_bounds(tile_x, blocks)
    return (
        top_water is not None
        and bottom_water is not None
        and bottom_water - top_water + 1 >= FISH_MIN_OCEAN_DEPTH
    )


def is_aquatic(name):
    return name == "Fish"


def get_solid_block_rects(rect, blocks):
    left_tile = max(0, int(rect.left // TILE_SIZE))
    right_tile = min(WORLD_W - 1, int((rect.right - 1) // TILE_SIZE))
    top_tile = max(0, int(rect.top // TILE_SIZE))
    bottom_tile = min(WORLD_H - 1, int((rect.bottom - 1) // TILE_SIZE))

    hit_rects = []
    for tx in range(left_tile, right_tile + 1):
        for ty in range(top_tile, bottom_tile + 1):
            block_type = blocks.get((tx, ty))
            if block_type is None or is_liquid_block(block_type) or is_open_door_block(block_type) or block_type in {"fire", "nether_portal"}:
                continue
            block_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(block_rect):
                hit_rects.append(block_rect)
    return hit_rects


def rect_overlaps_water(rect, blocks):
    left_tile = max(0, int(rect.left // TILE_SIZE))
    right_tile = min(WORLD_W - 1, int((rect.right - 1) // TILE_SIZE))
    top_tile = max(0, int(rect.top // TILE_SIZE))
    bottom_tile = min(WORLD_H - 1, int((rect.bottom - 1) // TILE_SIZE))

    for tx in range(left_tile, right_tile + 1):
        for ty in range(top_tile, bottom_tile + 1):
            if blocks.get((tx, ty)) != "water":
                continue
            water_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(water_rect):
                return True
    return False


def rect_overlaps_block_type(rect, blocks, target_type):
    left_tile = max(0, int(rect.left // TILE_SIZE))
    right_tile = min(WORLD_W - 1, int((rect.right - 1) // TILE_SIZE))
    top_tile = max(0, int(rect.top // TILE_SIZE))
    bottom_tile = min(WORLD_H - 1, int((rect.bottom - 1) // TILE_SIZE))

    for tx in range(left_tile, right_tile + 1):
        for ty in range(top_tile, bottom_tile + 1):
            if blocks.get((tx, ty)) != target_type:
                continue
            block_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(block_rect):
                return True
    return False


def accumulate_fire_damage(state, touching_fire, dt):
    if not touching_fire:
        state["fire_damage_timer"] = 0.0
        return 0

    timer = state.get("fire_damage_timer", 0.0) + dt
    hits = int(timer // FIRE_DAMAGE_INTERVAL)
    state["fire_damage_timer"] = timer % FIRE_DAMAGE_INTERVAL
    return hits


def spawn_animal_by_name(name, blocks, occupied_tiles=None):
    """Spawn one animal by type, preferring a tile different from occupied ones."""
    if occupied_tiles is None:
        occupied_tiles = set()

    spec = ANIMAL_TYPES[name]
    size = spec["size"]

    if is_aquatic(name):
        ocean_columns = [
            x for x in range(1, WORLD_W - 1)
            if x not in occupied_tiles and is_ocean_column(x, blocks)
        ]
        if not ocean_columns:
            ocean_columns = [x for x in range(1, WORLD_W - 1) if is_ocean_column(x, blocks)]
        if not ocean_columns:
            ocean_columns = [WORLD_W - 2]

        tile_x = random.choice(ocean_columns)
        top_water, bottom_water = get_water_column_bounds(tile_x, blocks)
        min_y = top_water * TILE_SIZE + 8
        max_y = (bottom_water + 1) * TILE_SIZE - size - 8
        direction = random.choice([-1, 1])
        min_y += 4
        max_y -= max(4, size // 3)
        return {
            "name": name,
            "color": spec["color"],
            "size": size,
            "x": tile_x * TILE_SIZE + random.uniform(8, TILE_SIZE - size - 8),
            "y": random.uniform(min_y, max(min_y, max_y)),
            "vx": random.uniform(FISH_SWIM_SPEED_MIN, FISH_SWIM_SPEED_MAX) * direction,
            "vy": random.uniform(-25, 25),
            "hp": spec["hp"],
            "facing_right": direction > 0,
            "swim_turn_timer": random.uniform(0.8, 1.8),
            "palette": {"body": RAW_FISH_COLOR, "fin": (250, 250, 250), "eye": (24, 24, 24)},
        }

    tile_x = random.randint(1, WORLD_W - 2)
    for _ in range(40):
        tile_x = random.randint(1, WORLD_W - 2)
        # Avoid water columns for spawn
        is_water = False
        for y in range(WORLD_H):
            if blocks.get((tile_x, y)) == "water":
                is_water = True
                break
        
        if tile_x not in occupied_tiles and not is_water:
            break

    x = tile_x * TILE_SIZE + random.uniform(8, TILE_SIZE - 8)
    ground_top = ground_top_y_for_x(x, blocks)
    y = ground_top - size
    speed = random.uniform(35, 75)
    direction = random.choice([-1, 1])

    return {
        "name": name,
        "color": spec["color"],
        "size": size,
        "x": x,
        "y": y,
        "vx": speed * direction,
        "hp": spec["hp"],
    }


def spawn_nether_piglin(blocks, occupied_tiles=None, preferred_tile_x=None, search_radius=26):
    if occupied_tiles is None:
        occupied_tiles = set()

    candidate_columns = []
    if preferred_tile_x is not None:
        left = max(1, preferred_tile_x - search_radius)
        right = min(WORLD_W - 2, preferred_tile_x + search_radius)
        candidate_columns.extend(range(left, right + 1))
    else:
        candidate_columns.extend(range(1, WORLD_W - 1))

    random.shuffle(candidate_columns)
    fallback_columns = list(range(1, WORLD_W - 1))
    random.shuffle(fallback_columns)

    for columns in (candidate_columns, fallback_columns):
        for tile_x in columns:
            if tile_x in occupied_tiles:
                continue
            if preferred_tile_x is not None and abs(tile_x - preferred_tile_x) < 6:
                continue
            surface_y = find_nether_surface_y(tile_x, blocks)
            if surface_y is None:
                continue
            x = tile_x * TILE_SIZE + random.uniform(8, TILE_SIZE - ANIMAL_TYPES["Piglin"]["size"] - 8)
            y = surface_y - ANIMAL_TYPES["Piglin"]["size"]
            direction = random.choice([-1, 1])
            return {
                "name": "Piglin",
                "color": ANIMAL_TYPES["Piglin"]["color"],
                "size": ANIMAL_TYPES["Piglin"]["size"],
                "x": x,
                "y": y,
                "vx": random.uniform(26, 48) * direction,
                "hp": ANIMAL_TYPES["Piglin"]["hp"],
                "facing_right": direction > 0,
            }
    return None


def get_animal_ground_y(animal, world_x, blocks):
    if animal["name"] == "Piglin":
        surface_y = find_nether_surface_y(int(world_x // TILE_SIZE), blocks)
        if surface_y is not None:
            return surface_y
    return ground_top_y_for_x(world_x, blocks)


def is_daytime(time_of_day):
    return 6 <= time_of_day < 17


def is_nighttime(time_of_day):
    return time_of_day >= 19 or time_of_day < 5


def is_hostile(name):
    return name in {"Zombie", "Skeleton"}


def burns_in_daylight(name):
    return name in {"Zombie", "Skeleton"}


def get_drop_type(name):
    if name == "Zombie":
        return "rotten_meat"
    if name == "Skeleton":
        return "bone"
    if name == "Fish":
        return "raw_fish"
    if name == "Piglin":
        return "gold_ingot"
    return "meat"


def kill_animal(animal, animals, meats, respawn_queue, remove_now=True):
    drop_type = get_drop_type(animal["name"])
    if drop_type is not None:
        drop_size = max(10, animal["size"] // 2)
        drop_count = random.randint(11, 15) if animal["name"] == "Piglin" else 1
        center_x = animal["x"] + (animal["size"] - drop_size) / 2
        center_y = animal["y"] + (animal["size"] - drop_size) / 2
        for _ in range(drop_count):
            meats.append(
                create_drop(
                    drop_type,
                    center_x + random.uniform(-16, 16),
                    center_y + random.uniform(-8, 8),
                    drop_size,
                )
            )
    respawn_queue.append({"name": animal["name"], "time_left": RESPAWN_DELAY})
    animal["dead"] = True
    if remove_now and animal in animals:
        animals.remove(animal)


def kill_villager(villager, villagers, items, villager_respawn_queue):
    drop_size = max(10, TILE_SIZE // 3)
    diamond_drop_count = random.randint(1, 11)
    center_x = villager["x"] + villager["size"] / 2
    center_y = villager["y"] + villager["size"] / 2
    for _ in range(diamond_drop_count):
        items.append(
            {
                "type": "diamond",
                "x": center_x - drop_size / 2 + random.uniform(-10, 10),
                "y": center_y - drop_size / 2 + random.uniform(-8, 8),
                "size": drop_size,
            }
        )
    villager_respawn_queue.append(
        {
            "spawn_x": villager["spawn_x"],
            "spawn_y": villager["spawn_y"],
            "size": villager["size"],
            "vx": random.choice([-1, 1]) * VILLAGER_SPEED,
            "trade_item": villager["trade_item"],
            "trade_cost": villager["trade_cost"],
            "trade_label": villager["trade_label"],
            "home_left": villager["home_left"],
            "home_right": villager["home_right"],
            "time_left": RESPAWN_DELAY,
        }
    )
    if villager in villagers:
        villagers.remove(villager)


def kill_iron_golem(golem, iron_golems, items, iron_golem_respawn_queue):
    drop_size = max(10, TILE_SIZE // 3)
    ingot_drop_count = random.randint(3, 5)
    center_x = golem["x"] + golem["size"] / 2
    center_y = golem["y"] + golem["size"] / 2
    for _ in range(ingot_drop_count):
        items.append(
            {
                "type": "iron_ingot",
                "x": center_x - drop_size / 2 + random.uniform(-10, 10),
                "y": center_y - drop_size / 2 + random.uniform(-8, 8),
                "size": drop_size,
            }
        )
    iron_golem_respawn_queue.append(
        {
            "spawn_x": golem["spawn_x"],
            "spawn_y": golem["spawn_y"],
            "size": golem["size"],
            "vx": random.choice([-1, 1]) * IRON_GOLEM_SPEED,
            "home_left": golem["home_left"],
            "home_right": golem["home_right"],
            "time_left": RESPAWN_DELAY,
        }
    )
    if golem in iron_golems:
        iron_golems.remove(golem)


def spawn_extra_night_zombie(animals, blocks):
    occupied_tiles = {int(a["x"] // TILE_SIZE) for a in animals}
    zombie = spawn_animal_by_name("Zombie", blocks, occupied_tiles)
    animals.append(zombie)


def spawn_extra_night_skeleton(animals, blocks):
    occupied_tiles = {int(a["x"] // TILE_SIZE) for a in animals}
    skeleton = spawn_animal_by_name("Skeleton", blocks, occupied_tiles)
    animals.append(skeleton)


def spawn_skeleton_arrow(animal, arrows, player_x, player_y):
    start_x = animal["x"] + animal["size"] / 2
    start_y = animal["y"] + animal["size"] / 2
    target_x = player_x + PLAYER_SIZE / 2
    target_y = player_y + PLAYER_SIZE / 2
    dx = target_x - start_x
    dy = target_y - start_y
    dist = math.hypot(dx, dy)
    if dist <= 0:
        return
    arrows.append(
        {
            "x": start_x,
            "y": start_y,
            "vx": dx / dist * ARROW_SPEED,
            "vy": dy / dist * ARROW_SPEED,
            "life": 2.4,
        }
    )


def create_animals(blocks, count, time_of_day):
    """Spawn passive mobs anytime, but hostile mobs only at night."""
    animals = []
    used_tiles = set()
    for _ in range(INITIAL_FISH_COUNT):
        animal = spawn_animal_by_name("Fish", blocks, used_tiles)
        used_tiles.add(int(animal["x"] // TILE_SIZE))
        animals.append(animal)

    zombie_count = min(INITIAL_ZOMBIE_COUNT, count) if is_nighttime(time_of_day) else 0
    for _ in range(zombie_count):
        animal = spawn_animal_by_name("Zombie", blocks, used_tiles)
        used_tiles.add(int(animal["x"] // TILE_SIZE))
        animals.append(animal)

    skeleton_count = min(INITIAL_SKELETON_COUNT, max(0, count - zombie_count)) if is_nighttime(time_of_day) else 0
    for _ in range(skeleton_count):
        animal = spawn_animal_by_name("Skeleton", blocks, used_tiles)
        used_tiles.add(int(animal["x"] // TILE_SIZE))
        animals.append(animal)

    passive_names = [
        name
        for name in ANIMAL_TYPES.keys()
        if not is_hostile(name) and not is_aquatic(name) and name != "Piglin"
    ]
    for _ in range(count - zombie_count - skeleton_count):
        name = random.choice(passive_names)
        animal = spawn_animal_by_name(name, blocks, used_tiles)
        used_tiles.add(int(animal["x"] // TILE_SIZE))
        animals.append(animal)
    return animals


def create_nether_animals(blocks, count=INITIAL_PIGLIN_COUNT):
    animals = []
    used_tiles = set()
    for _ in range(count):
        piglin = spawn_nether_piglin(blocks, used_tiles)
        if piglin is None:
            break
        used_tiles.add(int(piglin["x"] // TILE_SIZE))
        animals.append(piglin)
    return animals


def update_animals(animals, blocks, dt, meats, respawn_queue, player_x, player_y, time_of_day, arrows):
    """Move animals left/right, make them jump over 1-block obstacles or bounce back."""
    world_limit = WORLD_W * TILE_SIZE
    for animal in animals:
        if is_aquatic(animal["name"]):
            animal["swim_turn_timer"] = animal.get("swim_turn_timer", 1.0) - dt
            fish_rect = pygame.Rect(
                math.floor(animal["x"]),
                math.floor(animal["y"]),
                animal["size"],
                animal["size"],
            )
            in_water = rect_overlaps_water(fish_rect, blocks)

            if in_water:
                animal["out_of_water_time"] = 0.0
                if animal["swim_turn_timer"] <= 0:
                    animal["vx"] = random.uniform(FISH_SWIM_SPEED_MIN, FISH_SWIM_SPEED_MAX) * random.choice([-1, 1])
                    animal["vy"] = random.uniform(-35, 35)
                    animal["swim_turn_timer"] = random.uniform(0.8, 1.8)

                dx = int(round(animal["vx"] * dt))
                dy = int(round(animal["vy"] * dt))

                if dx != 0:
                    next_rect = fish_rect.move(dx, 0)
                    blocked_x = (
                        next_rect.left < 0
                        or next_rect.right > world_limit
                        or get_solid_block_rects(next_rect, blocks)
                        or not rect_overlaps_water(next_rect, blocks)
                    )
                    if blocked_x:
                        animal["vx"] *= -1
                    else:
                        fish_rect = next_rect

                if dy != 0:
                    next_rect = fish_rect.move(0, dy)
                    blocked_y = (
                        next_rect.top < 0
                        or next_rect.bottom > WORLD_H * TILE_SIZE
                        or get_solid_block_rects(next_rect, blocks)
                        or not rect_overlaps_water(next_rect, blocks)
                    )
                    if blocked_y:
                        animal["vy"] *= -1
                    else:
                        fish_rect = next_rect

                if (
                    fish_rect.left < 0
                    or fish_rect.right > world_limit
                    or not rect_overlaps_water(fish_rect, blocks)
                ):
                    animal["vx"] *= -1
                animal["x"] = float(fish_rect.x)
                animal["y"] = float(fish_rect.y)
                animal["facing_right"] = animal["vx"] >= 0
            else:
                animal["out_of_water_time"] = animal.get("out_of_water_time", 0.0) + dt
                animal["vy"] = animal.get("vy", 0.0) + GRAVITY * dt * 0.45
                animal["y"] += animal["vy"] * dt
                if animal["out_of_water_time"] >= FISH_OUT_OF_WATER_TIME:
                    kill_animal(animal, animals, meats, respawn_queue, remove_now=False)
                    continue
            continue

        # Gravity and jumping
        if "vy" not in animal:
            animal["vy"] = 0.0
            
        animal["vy"] += GRAVITY * dt
        animal["y"] += animal["vy"] * dt
        
        if animal["name"] == "Zombie":
            player_center_x = player_x + PLAYER_SIZE / 2
            animal_center_x = animal["x"] + animal["size"] / 2
            chase_direction = 1 if player_center_x > animal_center_x else -1
            animal["vx"] = ZOMBIE_CHASE_SPEED * chase_direction
        elif animal["name"] == "Skeleton":
            player_center_x = player_x + PLAYER_SIZE / 2
            animal_center_x = animal["x"] + animal["size"] / 2
            dist_x = player_center_x - animal_center_x
            abs_dist_x = abs(dist_x)
            move_dir = 0
            if abs_dist_x < SKELETON_MIN_RANGE:
                move_dir = -1 if dist_x > 0 else 1
            elif abs_dist_x > SKELETON_MAX_RANGE:
                move_dir = 1 if dist_x > 0 else -1
            animal["vx"] = move_dir * SKELETON_MOVE_SPEED
            animal["facing_right"] = dist_x >= 0
            shot_ready_time = SKELETON_SHOT_INTERVAL - SKELETON_AIM_TIME
            if abs_dist_x <= SKELETON_SHOOT_RANGE:
                animal["shoot_timer"] = animal.get("shoot_timer", 0.0) + dt
                animal["aiming"] = animal["shoot_timer"] >= shot_ready_time
                if animal["shoot_timer"] >= SKELETON_SHOT_INTERVAL:
                    spawn_skeleton_arrow(animal, arrows, player_x, player_y)
                    animal["shoot_timer"] = 0.0
                    animal["aiming"] = False
            else:
                animal["shoot_timer"] = max(0.0, animal.get("shoot_timer", 0.0) - dt * 2.0)
                animal["aiming"] = False
        else:
            animal["burning"] = False

        # Horizontal movement
        next_x = animal["x"] + animal["vx"] * dt

        if next_x < TILE_SIZE or next_x > world_limit - TILE_SIZE:
            animal["vx"] *= -1
            next_x = max(TILE_SIZE, min(next_x, world_limit - TILE_SIZE))

        # Randomly change direction to look alive.
        if not is_hostile(animal["name"]) and random.random() < 0.005:
            animal["vx"] *= -1

        # Check ground and obstacles
        current_ground = get_animal_ground_y(animal, animal["x"] + animal["size"] / 2, blocks)
        next_ground = get_animal_ground_y(animal, next_x + animal["size"] / 2, blocks)
        
        # If next ground is higher (obstacle)
        if next_ground < current_ground:
            height_diff = current_ground - next_ground
            # If it's exactly 1 block high (or less), try to jump
            if height_diff <= TILE_SIZE:
                # Only jump if on the ground
                if animal["y"] + animal["size"] >= current_ground:
                    animal["vy"] = JUMP_VELOCITY * 0.8  # slightly smaller jump for animals
            else:
                # Too high, bounce back
                animal["vx"] *= -1
                next_x = animal["x"]
        
        animal["x"] = next_x
        
        # Ground collision
        current_ground = get_animal_ground_y(animal, animal["x"] + animal["size"] / 2, blocks)
        if animal["y"] + animal["size"] >= current_ground:
            animal["y"] = current_ground - animal["size"]
            animal["vy"] = 0.0

        tile_x = int(animal["x"] // TILE_SIZE)
        tile_y = int((animal["y"] + animal["size"] / 2) // TILE_SIZE)

        if burns_in_daylight(animal["name"]) and is_daytime(time_of_day) and blocks.get((tile_x, tile_y)) != "water":
            animal["burn_timer"] = animal.get("burn_timer", 0.0) + dt
            animal["burning"] = True
            burn_interval = ZOMBIE_BURN_INTERVAL if animal["name"] == "Zombie" else SKELETON_BURN_INTERVAL
            if animal["burn_timer"] >= burn_interval:
                animal["burn_timer"] = 0.0
                animal["hp"] -= 1
                if animal["hp"] <= 0:
                    kill_animal(animal, animals, meats, respawn_queue, remove_now=False)
                    continue
        else:
            animal["burn_timer"] = 0.0
            if burns_in_daylight(animal["name"]):
                animal["burning"] = False
        
        # Check water
        if blocks.get((tile_x, tile_y)) == "water":
            if "water_time" not in animal:
                animal["water_time"] = 0.0
            animal["water_time"] += dt
            
            if animal["water_time"] >= 3.0:
                kill_animal(animal, animals, meats, respawn_queue, remove_now=False)
        else:
            animal["water_time"] = 0.0

        animal_rect = pygame.Rect(
            math.floor(animal["x"]),
            math.floor(animal["y"]),
            animal["size"],
            animal["size"],
        )
        fire_hits = accumulate_fire_damage(animal, rect_overlaps_block_type(animal_rect, blocks, "fire"), dt)
        if fire_hits > 0:
            animal["burning"] = True
            animal["hp"] -= fire_hits
            if animal["hp"] <= 0:
                kill_animal(animal, animals, meats, respawn_queue, remove_now=False)
                continue
        elif not burns_in_daylight(animal["name"]):
            animal["burning"] = False
            
    # remove dead animals
    animals[:] = [a for a in animals if not a.get("dead")]


def draw_skeleton_archer(screen, sx, sy, size, facing_right, aiming):
    pattern = [
        "00111100",
        "01111110",
        "01011010",
        "00111100",
        "00111100",
        "01111110",
        "01100110",
        "01000010",
    ]
    palette = {
        "0": None,
        "1": (236, 236, 236),
        "2": (170, 170, 170),
    }
    draw_pixel_art(screen, sx, sy, size, pattern, palette)
    center_x = sx + size // 2
    shoulder_y = sy + size // 2 - 2
    hand_y = sy + size // 2 + 1
    arm_reach = size // 3 + (3 if aiming else 0)
    bow_x = sx + size - 4 if facing_right else sx + 4
    hand_x = center_x + arm_reach if facing_right else center_x - arm_reach
    off_hand_x = center_x - 3 if facing_right else center_x + 3

    # Arms and legs stay thin and blocky like MC mobs.
    pygame.draw.line(screen, (214, 214, 214), (center_x, shoulder_y), (hand_x, hand_y), 2)
    pygame.draw.line(screen, (194, 194, 194), (center_x, shoulder_y), (off_hand_x, hand_y - 1), 2)
    pygame.draw.line(screen, (194, 194, 194), (center_x - 3, sy + size - 10), (center_x - 6, sy + size - 2), 2)
    pygame.draw.line(screen, (194, 194, 194), (center_x + 3, sy + size - 10), (center_x + 6, sy + size - 2), 2)

    bow_top = (bow_x, sy + 5)
    bow_mid = (bow_x + (-2 if facing_right else 2), sy + size // 2)
    bow_bottom = (bow_x, sy + size - 5)
    pygame.draw.line(screen, (120, 80, 45), bow_top, bow_mid, 2)
    pygame.draw.line(screen, (120, 80, 45), bow_mid, bow_bottom, 2)
    string_x = bow_x - 3 if facing_right else bow_x + 3
    pygame.draw.line(screen, (240, 240, 240), (string_x, sy + 6), (string_x, sy + size - 6), 1)

    if aiming:
        arrow_start_x = hand_x - 2 if facing_right else hand_x + 2
        arrow_end_x = bow_x - 2 if facing_right else bow_x + 2
        pygame.draw.line(screen, (160, 118, 70), (arrow_start_x, hand_y), (arrow_end_x, hand_y), 2)
        tip_dir = 1 if facing_right else -1
        pygame.draw.line(
            screen,
            (230, 230, 230),
            (arrow_end_x, hand_y),
            (arrow_end_x + tip_dir * 4, hand_y),
            2,
        )


def draw_fish(screen, sx, sy, size, facing_right, palette):
    pattern = [
        "00011000",
        "00111100",
        "11333321",
        "11333321",
        "00111100",
        "00011000",
    ]
    if not facing_right:
        pattern = [row[::-1] for row in pattern]
    draw_pixel_art(
        screen,
        sx,
        sy,
        size,
        pattern,
        {
            "0": None,
            "1": palette["fin"],
            "2": palette["eye"],
            "3": palette["body"],
        },
    )


def update_arrows(arrows, blocks, dt, player_x, player_y):
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    remain = []
    damage = 0
    for arrow in arrows:
        arrow["x"] += arrow["vx"] * dt
        arrow["y"] += arrow["vy"] * dt
        arrow["life"] -= dt
        if arrow["life"] <= 0:
            continue

        tile_x = int(arrow["x"] // TILE_SIZE)
        tile_y = int(arrow["y"] // TILE_SIZE)
        if 0 <= tile_x < WORLD_W and 0 <= tile_y < WORLD_H:
            block_type = blocks.get((tile_x, tile_y))
            if block_type is not None and not is_liquid_block(block_type):
                continue

        arrow_rect = pygame.Rect(arrow["x"] - 2, arrow["y"] - 2, 4, 4)
        if player_rect.colliderect(arrow_rect):
            damage += ARROW_DAMAGE
            continue
        remain.append(arrow)
    arrows[:] = remain
    return damage


def draw_arrows(screen, arrows, camera_x, camera_y):
    for arrow in arrows:
        sx = arrow["x"] - camera_x
        sy = arrow["y"] - camera_y
        if sx < -8 or sx > WIDTH + 8 or sy < -8 or sy > HEIGHT + 8:
            continue
        speed = math.hypot(arrow["vx"], arrow["vy"])
        if speed <= 0:
            continue
        ux = arrow["vx"] / speed
        uy = arrow["vy"] / speed
        px = -uy
        py = ux
        half_len = 6
        tail_x = sx - ux * half_len
        tail_y = sy - uy * half_len
        head_x = sx + ux * half_len
        head_y = sy + uy * half_len
        feather_x = tail_x + ux * 2
        feather_y = tail_y + uy * 2

        pygame.draw.line(screen, (160, 118, 70), (tail_x, tail_y), (head_x, head_y), 2)
        pygame.draw.line(screen, (230, 230, 230), (head_x, head_y), (head_x - ux * 3 + px * 2, head_y - uy * 3 + py * 2), 1)
        pygame.draw.line(screen, (230, 230, 230), (head_x, head_y), (head_x - ux * 3 - px * 2, head_y - uy * 3 - py * 2), 1)
        pygame.draw.line(screen, (235, 235, 235), (tail_x, tail_y), (feather_x + px * 2, feather_y + py * 2), 1)
        pygame.draw.line(screen, (235, 235, 235), (tail_x, tail_y), (feather_x - px * 2, feather_y - py * 2), 1)


def draw_animals(screen, animals, camera_x, camera_y, font, animal_images):
    for animal in animals:
        sx = animal["x"] - camera_x
        sy = animal["y"] - camera_y
        size = animal["size"]

        if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
            continue

        if animal["name"] == "Skeleton":
            draw_skeleton_archer(
                screen,
                sx,
                sy,
                size,
                animal.get("facing_right", True),
                animal.get("aiming", False),
            )
        elif animal["name"] == "Fish":
            draw_fish(
                screen,
                sx,
                sy,
                size,
                animal.get("facing_right", True),
                animal.get("palette", {"body": RAW_FISH_COLOR, "fin": (250, 250, 250), "eye": (24, 24, 24)}),
            )
        elif animal["name"] == "Piglin":
            draw_piglin(screen, sx, sy, size, animal.get("facing_right", True))
        else:
            img = animal_images.get(animal["name"])
            if img:
                # 图片本身朝左。如果 vx > 0 (向右走), 则水平翻转图片
                if animal["vx"] > 0:
                    flipped_img = pygame.transform.flip(img, True, False)
                    screen.blit(flipped_img, (sx, sy))
                else:
                    screen.blit(img, (sx, sy))
            else:
                pygame.draw.rect(screen, animal["color"], pygame.Rect(sx, sy, size, size))

        if animal.get("burning"):
            flame_color = (255, 140, 40)
            pygame.draw.rect(screen, flame_color, pygame.Rect(sx + 2, sy - 4, 6, 6))
            pygame.draw.rect(screen, flame_color, pygame.Rect(sx + size - 8, sy - 4, 6, 6))
            pygame.draw.rect(screen, (255, 210, 90), pygame.Rect(sx + size // 2 - 3, sy - 6, 6, 6))
            
        label = font.render(animal["name"], True, (20, 20, 20))
        screen.blit(label, (sx, sy - 14))
        hp_text = font.render(f"HP:{animal['hp']}", True, (20, 20, 20))
        screen.blit(hp_text, (sx, sy + size + 2))


def attack_animal_at_crosshair(
    animals, meats, respawn_queue, camera_x, camera_y, crosshair_x, crosshair_y, damage=1
):
    """Hit one animal if crosshair is on it; dead animals drop meat."""
    crosshair_world_x = camera_x + crosshair_x
    crosshair_world_y = camera_y + crosshair_y
    target = None

    for animal in animals:
        rect = pygame.Rect(animal["x"], animal["y"], animal["size"], animal["size"])
        if rect.collidepoint(crosshair_world_x, crosshair_world_y):
            target = animal
            break

    if target is None:
        return False

    target["hp"] -= damage
    if target["hp"] <= 0:
        kill_animal(target, animals, meats, respawn_queue)
    return True


def attack_villager_at_crosshair(
    villagers,
    items,
    villager_respawn_queue,
    camera_x,
    camera_y,
    crosshair_x,
    crosshair_y,
    damage=1,
):
    crosshair_world_x = camera_x + crosshair_x
    crosshair_world_y = camera_y + crosshair_y
    target = None

    for villager in villagers:
        rect = pygame.Rect(villager["x"], villager["y"], villager["size"], villager["size"])
        if rect.collidepoint(crosshair_world_x, crosshair_world_y):
            target = villager
            break

    if target is None:
        return False

    target["hp"] -= damage
    if target["hp"] <= 0:
        kill_villager(target, villagers, items, villager_respawn_queue)
    return True


def attack_iron_golem_at_crosshair(
    iron_golems,
    items,
    iron_golem_respawn_queue,
    camera_x,
    camera_y,
    crosshair_x,
    crosshair_y,
    damage=1,
):
    crosshair_world_x = camera_x + crosshair_x
    crosshair_world_y = camera_y + crosshair_y
    target = None

    for golem in iron_golems:
        rect = pygame.Rect(golem["x"], golem["y"], golem["size"], golem["size"])
        if rect.collidepoint(crosshair_world_x, crosshair_world_y):
            target = golem
            break

    if target is None:
        return False

    target["hp"] -= damage
    if target["hp"] <= 0:
        kill_iron_golem(target, iron_golems, items, iron_golem_respawn_queue)
    return True


def try_place_selected_block(
    blocks,
    tree_blocks,
    player_x,
    player_y,
    camera_x,
    camera_y,
    crosshair_x,
    crosshair_y,
    block_type="diamond_block",
    return_position=False,
):
    world_x = camera_x + crosshair_x
    world_y = camera_y + crosshair_y
    tile_x = int(world_x // TILE_SIZE)
    tile_y = int(world_y // TILE_SIZE)
    if not (0 <= tile_x < WORLD_W and 0 <= tile_y < WORLD_H):
        return None if return_position else False

    place_x = tile_x
    place_y = tile_y
    if (tile_x, tile_y) in blocks:
        local_x = world_x - tile_x * TILE_SIZE
        local_y = world_y - tile_y * TILE_SIZE
        distances = {
            "left": local_x,
            "right": TILE_SIZE - local_x,
            "top": local_y,
            "bottom": TILE_SIZE - local_y,
        }
        side = min(distances, key=distances.get)
        if side == "left":
            place_x -= 1
        elif side == "right":
            place_x += 1
        elif side == "top":
            place_y -= 1
        else:
            place_y += 1

    if not (0 <= place_x < WORLD_W and 0 <= place_y < WORLD_H):
        return None if return_position else False
    if (place_x, place_y) in blocks:
        return None if return_position else False

    tile_rect = pygame.Rect(place_x * TILE_SIZE, place_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    player_rect = pygame.Rect(math.floor(player_x), math.floor(player_y), PLAYER_SIZE, PLAYER_SIZE)
    if tile_rect.colliderect(player_rect):
        return None if return_position else False

    tree_tile_size = TILE_SIZE // 2
    for tree_x, tree_y in tree_blocks.keys():
        tree_rect = pygame.Rect(tree_x, tree_y, tree_tile_size, tree_tile_size)
        if tile_rect.colliderect(tree_rect):
            return None if return_position else False

    blocks[(place_x, place_y)] = block_type
    if return_position:
        return (place_x, place_y)
    return True


def update_respawns(respawn_queue, animals, blocks, dt, time_of_day, current_dimension="overworld", player_x=None):
    """Respawn each dead animal after delay, keeping infinite cycle."""
    if not respawn_queue:
        return

    occupied_tiles = {int(a["x"] // TILE_SIZE) for a in animals}
    remain = []
    for item in respawn_queue:
        item["time_left"] -= dt
        if item["time_left"] <= 0:
            if is_hostile(item["name"]) and not is_nighttime(time_of_day):
                remain.append(item)
                continue
            if item["name"] == "Piglin":
                preferred_tile_x = None if player_x is None else int((player_x + PLAYER_SIZE / 2) // TILE_SIZE)
                animal = spawn_nether_piglin(blocks, occupied_tiles, preferred_tile_x)
            else:
                animal = spawn_animal_by_name(item["name"], blocks, occupied_tiles)
            if animal is None:
                remain.append(item)
                continue
            occupied_tiles.add(int(animal["x"] // TILE_SIZE))
            animals.append(animal)
        else:
            remain.append(item)

    respawn_queue[:] = remain


def update_villager_respawns(villager_respawn_queue, villagers, dt):
    if not villager_respawn_queue:
        return

    remain = []
    for item in villager_respawn_queue:
        item["time_left"] -= dt
        if item["time_left"] <= 0:
            villagers.append(
                {
                    "x": item["spawn_x"],
                    "y": item["spawn_y"],
                    "spawn_x": item["spawn_x"],
                    "spawn_y": item["spawn_y"],
                    "size": item["size"],
                    "vx": item["vx"],
                    "trade_item": item["trade_item"],
                    "trade_cost": item["trade_cost"],
                    "trade_label": item["trade_label"],
                    "home_left": item["home_left"],
                    "home_right": item["home_right"],
                    "facing_right": item["vx"] >= 0,
                    "hp": VILLAGER_HP,
                }
            )
        else:
            remain.append(item)

    villager_respawn_queue[:] = remain


def update_iron_golem_respawns(iron_golem_respawn_queue, iron_golems, dt):
    if not iron_golem_respawn_queue:
        return

    remain = []
    for item in iron_golem_respawn_queue:
        item["time_left"] -= dt
        if item["time_left"] <= 0:
            iron_golems.append(
                {
                    "x": item["spawn_x"],
                    "y": item["spawn_y"],
                    "spawn_x": item["spawn_x"],
                    "spawn_y": item["spawn_y"],
                    "size": item["size"],
                    "vx": item["vx"],
                    "home_left": item["home_left"],
                    "home_right": item["home_right"],
                    "facing_right": item["vx"] >= 0,
                    "hp": IRON_GOLEM_HP,
                }
            )
        else:
            remain.append(item)

    iron_golem_respawn_queue[:] = remain


def mine_block_at_crosshair(blocks, trees, items, camera_x, camera_y, crosshair_x, crosshair_y):
    crosshair_world_x = camera_x + crosshair_x
    crosshair_world_y = camera_y + crosshair_y
    TREE_TILE_SIZE = TILE_SIZE // 2
    
    # 查找被点击的树方块
    clicked_block = None
    for (wx, wy) in trees.keys():
        rect = pygame.Rect(wx, wy, TREE_TILE_SIZE, TREE_TILE_SIZE)
        if rect.collidepoint(crosshair_world_x, crosshair_world_y):
            clicked_block = (wx, wy)
            break
            
    if clicked_block:
        block_type = trees.pop(clicked_block)
        if block_type == "wood":
            drop_size = max(10, TREE_TILE_SIZE // 2)
            items.append({
                "type": "wood",
                "x": clicked_block[0] + (TREE_TILE_SIZE - drop_size) / 2,
                "y": clicked_block[1] + (TREE_TILE_SIZE - drop_size) / 2,
                "size": drop_size,
            })
        return True, None
        
    # Check terrain blocks
    tx = int(crosshair_world_x // TILE_SIZE)
    ty = int(crosshair_world_y // TILE_SIZE)
    
    if (tx, ty) in blocks and not is_liquid_block(blocks[(tx, ty)]):
        # Return the target block for mining
        return False, (tx, ty)
        
    return False, None


def update_water(blocks):
    """Make water flow exactly one step (1 block) per update."""
    new_water = []
    for (x, y), block_type in blocks.items():
        if block_type == "water":
            # 1. Flow down if empty
            if y + 1 < WORLD_H and (x, y + 1) not in blocks:
                new_water.append((x, y + 1))
            elif y + 1 < WORLD_H and blocks.get((x, y + 1)) == "lava":
                blocks[(x, y + 1)] = "obsidian"
            # 2. If blocked below (or standing on something), flow sideways
            elif y + 1 < WORLD_H and (x, y + 1) in blocks and blocks[(x, y + 1)] != "water":
                if x - 1 >= 0 and (x - 1, y) not in blocks:
                    new_water.append((x - 1, y))
                elif x - 1 >= 0 and blocks.get((x - 1, y)) == "lava":
                    blocks[(x - 1, y)] = "obsidian"
                if x + 1 < WORLD_W and (x + 1, y) not in blocks:
                    new_water.append((x + 1, y))
                elif x + 1 < WORLD_W and blocks.get((x + 1, y)) == "lava":
                    blocks[(x + 1, y)] = "obsidian"
                
    for pos in new_water:
        if pos not in blocks:
            blocks[pos] = "water"
    resolve_liquid_interactions(blocks)

def draw_items(screen, items, camera_x, camera_y, meat_image):
    for item in items:
        sx = item["x"] - camera_x
        sy = item["y"] - camera_y
        size = item["size"]
        if sx + size < 0 or sx > WIDTH or sy + size < 0 or sy > HEIGHT:
            continue
            
        if item.get("type") == "wood":
            pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "stone":
            pygame.draw.rect(screen, STONE_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "sand":
            pygame.draw.rect(screen, SAND_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (130, 112, 58), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "gravel":
            pygame.draw.rect(screen, GRAVEL_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (92, 90, 88), pygame.Rect(sx, sy, size, size), 1)
            chip = max(2, size // 5)
            pygame.draw.rect(screen, (170, 168, 166), pygame.Rect(sx + 2, sy + 2, chip, chip))
            pygame.draw.rect(screen, (108, 106, 104), pygame.Rect(sx + size - chip - 3, sy + size // 2, chip, chip))
        elif item.get("type") == "coal":
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                [
                    "00110",
                    "01111",
                    "11111",
                    "01110",
                    "00100",
                ],
                {
                    "0": None,
                    "1": (32, 32, 32),
                },
            )
        elif item.get("type") == "iron_ore":
            draw_ore_block(screen, sx, sy, size, "iron_ore")
        elif item.get("type") == "gold_ore":
            draw_ore_block(screen, sx, sy, size, "gold_ore")
        elif item.get("type") == "nether_gold_ore":
            draw_nether_gold_ore_block(screen, sx, sy, size)
        elif item.get("type") == "redstone_ore":
            draw_ore_block(screen, sx, sy, size, "redstone_ore")
        elif item.get("type") == "redstone":
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                [
                    "00100",
                    "01110",
                    "11111",
                    "01110",
                    "00100",
                ],
                {
                    "0": None,
                    "1": REDSTONE_COLOR,
                },
            )
        elif item.get("type") == "diamond":
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                [
                    "00100",
                    "01110",
                    "11111",
                    "01110",
                    "00100",
                ],
                {
                    "0": None,
                    "1": (88, 240, 235),
                },
            )
        elif item.get("type") == "dirt":
            pygame.draw.rect(screen, DIRT_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "plank":
            pygame.draw.rect(screen, PLANK_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "diamond_block":
            pygame.draw.rect(screen, DIAMOND_BLOCK_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "redstone_block":
            pygame.draw.rect(screen, REDSTONE_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "iron_ingot":
            draw_inventory_icon(screen, "iron_ingot", sx, sy, size, meat_image)
        elif item.get("type") == "gold_nugget":
            draw_inventory_icon(screen, "gold_nugget", sx, sy, size, meat_image)
        elif item.get("type") == "fire_resistance_potion":
            draw_inventory_icon(screen, "fire_resistance_potion", sx, sy, size, meat_image)
        elif item.get("type") == "obsidian":
            pygame.draw.rect(screen, OBSIDIAN_COLOR, pygame.Rect(sx, sy, size, size))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(sx, sy, size, size), 1)
        elif item.get("type") == "rotten_meat":
            # Draw a tiny pixel-art style rotten flesh item.
            rotten_colors = {
                "dark": (72, 92, 52),
                "mid": (112, 140, 76),
                "flesh": (132, 94, 80),
            }
            pattern = [
                "00110",
                "12331",
                "13321",
                "12331",
                "01100",
            ]
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                pattern,
                {
                    "0": None,
                    "1": rotten_colors["dark"],
                    "2": rotten_colors["mid"],
                    "3": rotten_colors["flesh"],
                },
            )
        elif item.get("type") == "bone":
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                [
                    "0110000",
                    "1222000",
                    "0222200",
                    "0022200",
                    "0022220",
                    "0002221",
                    "0000110",
                ],
                {
                    "0": None,
                    "1": (236, 236, 228),
                    "2": (214, 214, 204),
                },
            )
        elif item.get("type") == "raw_fish":
            draw_pixel_art(
                screen,
                sx,
                sy,
                size,
                [
                    "00110",
                    "11331",
                    "23332",
                    "11331",
                    "00110",
                ],
                {
                    "0": None,
                    "1": (248, 248, 248),
                    "2": (24, 24, 24),
                    "3": RAW_FISH_COLOR,
                },
            )
        else:
            if meat_image:
                # 缩放肉图片到实际 drop_size
                scaled_meat = pygame.transform.scale(meat_image, (int(size), int(size)))
                screen.blit(scaled_meat, (sx, sy))
            else:
                pygame.draw.rect(screen, MEAT_COLOR, pygame.Rect(sx, sy, size, size))


def draw_inventory_icon(screen, item_type, x, y, size, meat_image):
    if item_type == "meat":
        if meat_image:
            scaled_meat = pygame.transform.scale(meat_image, (size, size))
            screen.blit(scaled_meat, (x, y))
        else:
            pygame.draw.rect(screen, MEAT_COLOR, pygame.Rect(x, y, size, size))
        return

    if item_type == "rotten_meat":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00110",
                "12331",
                "13321",
                "12331",
                "01100",
            ],
            {
                "0": None,
                "1": (72, 92, 52),
                "2": (112, 140, 76),
                "3": (132, 94, 80),
            },
        )
        return

    if item_type == "bone":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "0110000",
                "1222000",
                "0222200",
                "0022200",
                "0022220",
                "0002221",
                "0000110",
            ],
            {
                "0": None,
                "1": (236, 236, 228),
                "2": (214, 214, 204),
            },
        )
        return

    if item_type == "stick":
        pixel = max(2, size // 8)
        pygame.draw.rect(screen, STICK_COLOR, pygame.Rect(x + size // 2 - pixel // 2, y + 4, pixel, size - 8))
        pygame.draw.rect(screen, (96, 72, 38), pygame.Rect(x + size // 2 - pixel, y + size // 2 - pixel // 2, pixel * 2, pixel))
        return

    if item_type == "raw_fish":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00110",
                "11331",
                "23332",
                "11331",
                "00110",
            ],
            {
                "0": None,
                "1": (248, 248, 248),
                "2": (24, 24, 24),
                "3": RAW_FISH_COLOR,
            },
        )
        return

    if item_type == "wood":
        pygame.draw.rect(screen, WOOD_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (45, 28, 10), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "plank":
        pygame.draw.rect(screen, PLANK_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (70, 48, 22), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "obsidian":
        pygame.draw.rect(screen, OBSIDIAN_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (18, 10, 28), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "stone":
        pygame.draw.rect(screen, STONE_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "sand":
        pygame.draw.rect(screen, SAND_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (130, 112, 58), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "gravel":
        pygame.draw.rect(screen, GRAVEL_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (92, 90, 88), pygame.Rect(x, y, size, size), 1)
        chip = max(2, size // 5)
        pygame.draw.rect(screen, (170, 168, 166), pygame.Rect(x + 2, y + 2, chip, chip))
        pygame.draw.rect(screen, (108, 106, 104), pygame.Rect(x + size - chip - 3, y + size // 2, chip, chip))
        return

    if item_type == "coal":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00110",
                "01111",
                "11111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": (32, 32, 32),
            },
        )
        return

    if item_type == "lighter":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00110",
                "01111",
                "11111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": (32, 32, 32),
            },
        )
        pixel = max(2, size // 8)
        lighter_gray = (188, 188, 188)
        pygame.draw.rect(screen, lighter_gray, pygame.Rect(x + 1, y + 1, pixel * 2, pixel))
        pygame.draw.rect(screen, lighter_gray, pygame.Rect(x + 1, y + 1, pixel, pixel * 3))
        pygame.draw.rect(screen, lighter_gray, pygame.Rect(x + 1, y + pixel * 3, pixel * 2, pixel))
        return

    if item_type == "iron_ore":
        draw_ore_block(screen, x, y, size, "iron_ore")
        return

    if item_type == "gold_ore":
        draw_ore_block(screen, x, y, size, "gold_ore")
        return

    if item_type == "nether_gold_ore":
        draw_nether_gold_ore_block(screen, x, y, size)
        return

    if item_type == "redstone_ore":
        draw_ore_block(screen, x, y, size, "redstone_ore")
        return

    if item_type == "iron_ingot":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00000",
                "01110",
                "12221",
                "01110",
                "00000",
            ],
            {
                "0": None,
                "1": (230, 230, 230),
                "2": (185, 185, 185),
            },
        )
        return

    if item_type == "gold_ingot":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00000",
                "01110",
                "12221",
                "01110",
                "00000",
            ],
            {
                "0": None,
                "1": (244, 214, 92),
                "2": (210, 170, 40),
            },
        )
        return

    if item_type == "gold_nugget":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00000",
                "00110",
                "01111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": (248, 214, 92),
            },
        )
        return

    if item_type == "fire_resistance_potion":
        bottle_rect = pygame.Rect(x + size // 4, y + size // 5, size // 2, size * 3 // 5)
        pygame.draw.rect(screen, (190, 236, 255), bottle_rect, border_radius=max(2, size // 8))
        inner_rect = bottle_rect.inflate(-max(2, size // 8), -max(2, size // 6))
        pygame.draw.rect(screen, (255, 118, 72), inner_rect, border_radius=max(2, size // 10))
        pygame.draw.rect(screen, (90, 60, 24), pygame.Rect(x + size // 3, y + size // 7, size // 3, max(2, size // 8)))
        pygame.draw.rect(screen, (44, 78, 110), bottle_rect, 1, border_radius=max(2, size // 8))
        return

    if item_type == "redstone":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00100",
                "01110",
                "11111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": REDSTONE_COLOR,
            },
        )
        return

    if item_type == "diamond":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "00100",
                "01110",
                "11111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": (88, 240, 235),
            },
        )
        return

    if item_type == "diamond_block":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "11111",
                "12221",
                "12321",
                "12221",
                "11111",
            ],
            {
                "1": (88, 240, 235),
                "2": (56, 192, 188),
                "3": (220, 255, 255),
            },
        )
        return

    if item_type == "redstone_block":
        draw_pixel_art(
            screen,
            x,
            y,
            size,
            [
                "11111",
                "12221",
                "12321",
                "12221",
                "11111",
            ],
            {
                "1": REDSTONE_COLOR,
                "2": (168, 24, 24),
                "3": (255, 180, 180),
            },
        )
        return

    if item_type == "dirt":
        pygame.draw.rect(screen, DIRT_COLOR, pygame.Rect(x, y, size, size))
        pygame.draw.rect(screen, (55, 35, 20), pygame.Rect(x, y, size, size), 1)
        return

    if item_type == "wood_pickaxe":
        draw_wood_pickaxe(screen, x, y, size)
        return

    if item_type == "stone_pickaxe":
        draw_stone_pickaxe(screen, x, y, size)
        return

    if item_type == "iron_pickaxe":
        draw_iron_pickaxe(screen, x, y, size)
        return

    if item_type == "gold_pickaxe":
        draw_gold_pickaxe(screen, x, y, size)
        return

    if item_type == "diamond_pickaxe":
        draw_diamond_pickaxe(screen, x, y, size)
        return

    if item_type == "redstone_pickaxe":
        draw_redstone_pickaxe(screen, x, y, size)
        return

    if item_type == "iron_sword":
        draw_iron_sword(screen, x, y, size)
        return

    if item_type == "diamond_sword":
        draw_diamond_sword(screen, x, y, size)


def draw_status_panel(screen, font, player_hp, time_str):
    panel = pygame.Rect(10, 10, 176, 38)
    pygame.draw.rect(screen, (32, 32, 32), panel)
    pygame.draw.rect(screen, (92, 92, 92), panel, 2)
    max_hearts = 5
    filled_hearts = int(math.ceil(max(0.0, player_hp) / 2.0))
    for i in range(max_hearts):
        hx = panel.x + 8 + i * 18
        hy = panel.y + 8
        color = (210, 40, 40) if i < filled_hearts else (82, 42, 42)
        draw_pixel_art(
            screen,
            hx,
            hy,
            14,
            [
                "01010",
                "11111",
                "11111",
                "01110",
                "00100",
            ],
            {
                "0": None,
                "1": color,
            },
        )
    time_text = font.render(time_str, True, (235, 235, 235))
    screen.blit(time_text, (panel.x + 104, panel.y + 12))


def get_respawn_button_rect():
    return pygame.Rect(WIDTH - 146, 10, 136, 38)


def draw_respawn_button(screen, font):
    button = get_respawn_button_rect()
    pygame.draw.rect(screen, (42, 58, 88), button, border_radius=6)
    pygame.draw.rect(screen, (140, 170, 220), button, 2, border_radius=6)
    label = font.render("Back To Spawn", True, (245, 245, 245))
    label_rect = label.get_rect(center=button.center)
    screen.blit(label, label_rect)


def get_hotbar_key_label(index):
    if index < 9:
        return str(index + 1)
    extra_labels = ["A", "B", "C", "D"]
    extra_index = index - 9
    if 0 <= extra_index < len(extra_labels):
        return extra_labels[extra_index]
    return ""


def get_hotbar_index_for_key(key, slot_count):
    digit_keys = [
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9,
    ]
    if key in digit_keys:
        index = digit_keys.index(key)
        return index if index < slot_count else None

    extra_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]
    if key in extra_keys:
        index = 9 + extra_keys.index(key)
        return index if index < slot_count else None

    return None


def get_selected_tool(selected_item_type):
    if selected_item_type in {
        "diamond_sword",
        "iron_sword",
        "diamond_pickaxe",
        "gold_pickaxe",
        "iron_pickaxe",
        "stone_pickaxe",
        "wood_pickaxe",
        "redstone_pickaxe",
    }:
        return selected_item_type
    return None


def get_selected_item_type(
    selected_hotbar_index,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
):
    slots = build_inventory_slots(
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    if 0 <= selected_hotbar_index < len(slots):
        return slots[selected_hotbar_index]["item_type"]
    return None


def get_attack_stats(selected_item_type):
    selected_tool = get_selected_tool(selected_item_type)
    if selected_tool == "diamond_sword":
        return DIAMOND_SWORD_ATTACK_DAMAGE, DIAMOND_SWORD_ATTACK_COOLDOWN
    if selected_tool == "iron_sword":
        return IRON_SWORD_ATTACK_DAMAGE, IRON_SWORD_ATTACK_COOLDOWN
    if selected_tool == "diamond_pickaxe":
        return DIAMOND_PICKAXE_ATTACK_DAMAGE, DIAMOND_PICKAXE_ATTACK_COOLDOWN
    if selected_tool == "redstone_pickaxe":
        return REDSTONE_PICKAXE_ATTACK_DAMAGE, REDSTONE_PICKAXE_ATTACK_COOLDOWN
    if selected_tool == "gold_pickaxe":
        return GOLD_PICKAXE_ATTACK_DAMAGE, GOLD_PICKAXE_ATTACK_COOLDOWN
    if selected_tool == "iron_pickaxe":
        return IRON_PICKAXE_ATTACK_DAMAGE, IRON_PICKAXE_ATTACK_COOLDOWN
    if selected_tool == "stone_pickaxe":
        return STONE_PICKAXE_ATTACK_DAMAGE, STONE_PICKAXE_ATTACK_COOLDOWN
    if selected_tool == "wood_pickaxe":
        return WOOD_PICKAXE_ATTACK_DAMAGE, WOOD_PICKAXE_ATTACK_COOLDOWN
    return HAND_ATTACK_DAMAGE, HAND_ATTACK_COOLDOWN


def get_selected_pickaxe_tier(selected_item_type):
    selected_tool = get_selected_tool(selected_item_type)
    if selected_tool == "diamond_pickaxe":
        return 5
    if selected_tool == "redstone_pickaxe":
        return 4
    if selected_tool == "gold_pickaxe":
        return 4
    if selected_tool == "iron_pickaxe":
        return 3
    if selected_tool == "stone_pickaxe":
        return 2
    if selected_tool == "wood_pickaxe":
        return 1
    return 0


def is_pickaxe_item(item_type):
    return item_type in {
        "wood_pickaxe",
        "stone_pickaxe",
        "iron_pickaxe",
        "gold_pickaxe",
        "diamond_pickaxe",
        "redstone_pickaxe",
    }


def get_pickaxe_max_durability(item_type):
    if item_type == "wood_pickaxe":
        return WOOD_PICKAXE_MAX_DURABILITY
    if item_type == "stone_pickaxe":
        return STONE_PICKAXE_MAX_DURABILITY
    if item_type == "iron_pickaxe":
        return IRON_PICKAXE_MAX_DURABILITY
    if item_type == "gold_pickaxe":
        return GOLD_PICKAXE_MAX_DURABILITY
    if item_type == "diamond_pickaxe":
        return DIAMOND_PICKAXE_MAX_DURABILITY
    if item_type == "redstone_pickaxe":
        return REDSTONE_PICKAXE_MAX_DURABILITY
    return 0


def add_pickaxe_to_inventory(item_type, wood_pickaxes, stone_pickaxes, iron_pickaxes, gold_pickaxes, diamond_pickaxes, redstone_pickaxes):
    max_durability = get_pickaxe_max_durability(item_type)
    if item_type == "wood_pickaxe":
        wood_pickaxes.append(max_durability)
        wood_pickaxes.sort(reverse=True)
    elif item_type == "stone_pickaxe":
        stone_pickaxes.append(max_durability)
        stone_pickaxes.sort(reverse=True)
    elif item_type == "iron_pickaxe":
        iron_pickaxes.append(max_durability)
        iron_pickaxes.sort(reverse=True)
    elif item_type == "gold_pickaxe":
        gold_pickaxes.append(max_durability)
        gold_pickaxes.sort(reverse=True)
    elif item_type == "diamond_pickaxe":
        diamond_pickaxes.append(max_durability)
        diamond_pickaxes.sort(reverse=True)
    elif item_type == "redstone_pickaxe":
        redstone_pickaxes.append(max_durability)
        redstone_pickaxes.sort(reverse=True)


def get_pickaxe_inventory(item_type, wood_pickaxes, stone_pickaxes, iron_pickaxes, gold_pickaxes, diamond_pickaxes, redstone_pickaxes):
    if item_type == "wood_pickaxe":
        return wood_pickaxes
    if item_type == "stone_pickaxe":
        return stone_pickaxes
    if item_type == "iron_pickaxe":
        return iron_pickaxes
    if item_type == "gold_pickaxe":
        return gold_pickaxes
    if item_type == "diamond_pickaxe":
        return diamond_pickaxes
    if item_type == "redstone_pickaxe":
        return redstone_pickaxes
    return None


def try_refill_furnace_fuel(coal_count, furnace_fuel_uses):
    if furnace_fuel_uses > 0:
        return coal_count, furnace_fuel_uses, False
    if coal_count > 0:
        return coal_count - 1, FURNACE_FUEL_PER_ITEM, True
    return coal_count, furnace_fuel_uses, False


def build_inventory_slots(
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
):
    slots = []
    stackable_items = [
        ("wood", wood_count),
        ("stone", stone_count),
        ("sand", sand_count),
        ("gravel", gravel_count),
        ("dirt", dirt_count),
        ("coal", coal_count),
        ("iron_ore", iron_count),
        ("gold_ore", gold_count),
        ("redstone", redstone_count),
        ("diamond", diamond_count),
        ("iron_ingot", iron_ingot_count),
        ("lighter", lighter_count),
        ("gold_ingot", gold_ingot_count),
        ("gold_nugget", gold_nugget_count),
        ("fire_resistance_potion", fire_resistance_potion_count),
        ("plank", plank_count),
        ("iron_sword", iron_sword_count),
        ("diamond_sword", diamond_sword_count),
        ("diamond_block", diamond_block_count),
        ("redstone_block", redstone_block_count),
        ("obsidian", obsidian_count),
        ("stick", stick_count),
        ("meat", meat_count),
        ("raw_fish", raw_fish_count),
        ("rotten_meat", rotten_meat_count),
        ("bone", bone_count),
    ]
    for item_type, count in stackable_items:
        if count > 0:
            slots.append({"item_type": item_type, "count": count})

    for item_type, pickaxe_values in (
        ("iron_pickaxe", has_iron_pickaxe),
        ("diamond_pickaxe", has_diamond_pickaxe),
        ("redstone_pickaxe", has_redstone_pickaxe),
        ("gold_pickaxe", has_gold_pickaxe),
        ("wood_pickaxe", has_wood_pickaxe),
        ("stone_pickaxe", has_stone_pickaxe),
    ):
        max_durability = get_pickaxe_max_durability(item_type)
        for pickaxe_index, durability in enumerate(pickaxe_values):
            slots.append(
                {
                    "item_type": item_type,
                    "count": 1,
                    "durability": durability,
                    "max_durability": max_durability,
                    "pickaxe_index": pickaxe_index,
                }
            )

    return slots


def find_inventory_slot_index(
    item_type,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
):
    slots = build_inventory_slots(
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    for index, slot in enumerate(slots):
        if slot["item_type"] == item_type:
            return index
    return 0


def get_selected_inventory_entry(
    selected_hotbar_index,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
):
    slots = build_inventory_slots(
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    if 0 <= selected_hotbar_index < len(slots):
        return slots[selected_hotbar_index]
    return None


def damage_selected_pickaxe(
    selected_hotbar_index,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
):
    selected_entry = get_selected_inventory_entry(
        selected_hotbar_index,
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    if not selected_entry or not is_pickaxe_item(selected_entry["item_type"]):
        return None

    pickaxe_values = get_pickaxe_inventory(
        selected_entry["item_type"],
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    pickaxe_index = selected_entry.get("pickaxe_index")
    if pickaxe_values is None or pickaxe_index is None or pickaxe_index >= len(pickaxe_values):
        return None

    pickaxe_values[pickaxe_index] -= 1
    if pickaxe_values[pickaxe_index] <= 0:
        del pickaxe_values[pickaxe_index]
        return selected_entry["item_type"]
    pickaxe_values.sort(reverse=True)
    return None


def draw_hotbar(
    screen,
    font,
    meat_image,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
    selected_index,
):
    slots = build_inventory_slots(
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )[:VISIBLE_HOTBAR_SLOTS]
    slot_size = 42
    gap = 4
    total_width = len(slots) * slot_size + (len(slots) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - 54

    for index, slot_info in enumerate(slots):
        item_type = slot_info["item_type"]
        count = slot_info["count"]
        slot = pygame.Rect(start_x + index * (slot_size + gap), y, slot_size, slot_size)
        border = (240, 240, 240) if index == selected_index else (124, 124, 124)
        pygame.draw.rect(screen, (48, 48, 48), slot)
        pygame.draw.rect(screen, border, slot, 3 if index == selected_index else 2)
        if count > 0:
            draw_inventory_icon(screen, item_type, slot.x + 9, slot.y + 9, 24, meat_image)
            if "durability" in slot_info:
                durability_ratio = slot_info["durability"] / max(1, slot_info["max_durability"])
                bar_width = slot.width - 8
                bar_height = 5
                bar_x = slot.x + 4
                bar_y = slot.bottom - 8
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(bar_x, bar_y, bar_width, bar_height))
                fill_width = max(1, int(bar_width * durability_ratio))
                bar_color = (40, 200, 70) if durability_ratio > 0.5 else (230, 180, 40) if durability_ratio > 0.2 else (210, 60, 60)
                pygame.draw.rect(screen, bar_color, pygame.Rect(bar_x, bar_y, fill_width, bar_height))
            else:
                count_text = font.render(str(count), True, WHITE)
                text_rect = count_text.get_rect(bottomright=(slot.right - 4, slot.bottom - 2))
                screen.blit(count_text, text_rect)
        key_text = font.render(get_hotbar_key_label(index), True, (210, 210, 210))
        screen.blit(key_text, (slot.x + 4, slot.y + 2))

    hint = font.render("Hotbar 1-9  K:Backpack  F:Food  G:Rotten  E:Craft/Trade", True, (230, 230, 230))
    hint_rect = hint.get_rect(center=(WIDTH // 2, y - 12))
    screen.blit(hint, hint_rect)


def draw_backpack_panel(
    screen,
    font,
    meat_image,
    meat_count,
    raw_fish_count,
    rotten_meat_count,
    bone_count,
    wood_count,
    plank_count,
    stone_count,
    sand_count,
    gravel_count,
    dirt_count,
    coal_count,
    iron_count,
    gold_count,
    iron_ingot_count,
    lighter_count,
    gold_ingot_count,
    gold_nugget_count,
    fire_resistance_potion_count,
    redstone_count,
    diamond_count,
    iron_sword_count,
    diamond_sword_count,
    diamond_block_count,
    obsidian_count,
    redstone_block_count,
    stick_count,
    has_wood_pickaxe,
    has_stone_pickaxe,
    has_iron_pickaxe,
    has_gold_pickaxe,
    has_diamond_pickaxe,
    has_redstone_pickaxe,
    selected_index,
):
    slots = build_inventory_slots(
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
        has_redstone_pickaxe,
    )
    if not slots:
        return

    panel = pygame.Rect(52, 72, WIDTH - 104, 236)
    pygame.draw.rect(screen, (34, 34, 34), panel)
    pygame.draw.rect(screen, (132, 132, 132), panel, 2)

    title = font.render("Inventory  K to close", True, (240, 240, 240))
    screen.blit(title, (panel.x + 12, panel.y + 10))
    subtitle = font.render("Shows all items, not only the hidden slots.", True, (190, 190, 190))
    screen.blit(subtitle, (panel.x + 12, panel.y + 28))

    slot_size = 42
    gap = 6
    columns = 5
    start_x = panel.x + 16
    start_y = panel.y + 54

    for offset, slot_info in enumerate(slots):
        item_type = slot_info["item_type"]
        count = slot_info["count"]
        index = offset
        col = offset % columns
        row = offset // columns
        slot = pygame.Rect(
            start_x + col * (slot_size + gap),
            start_y + row * (slot_size + gap),
            slot_size,
            slot_size,
        )
        border = (240, 240, 240) if index == selected_index else (124, 124, 124)
        pygame.draw.rect(screen, (48, 48, 48), slot)
        pygame.draw.rect(screen, border, slot, 3 if index == selected_index else 2)
        if count > 0:
            draw_inventory_icon(screen, item_type, slot.x + 9, slot.y + 9, 24, meat_image)
            if "durability" in slot_info:
                durability_ratio = slot_info["durability"] / max(1, slot_info["max_durability"])
                bar_width = slot.width - 8
                bar_height = 5
                bar_x = slot.x + 4
                bar_y = slot.bottom - 8
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(bar_x, bar_y, bar_width, bar_height))
                fill_width = max(1, int(bar_width * durability_ratio))
                bar_color = (40, 200, 70) if durability_ratio > 0.5 else (230, 180, 40) if durability_ratio > 0.2 else (210, 60, 60)
                pygame.draw.rect(screen, bar_color, pygame.Rect(bar_x, bar_y, fill_width, bar_height))
            else:
                count_text = font.render(str(count), True, WHITE)
                text_rect = count_text.get_rect(bottomright=(slot.right - 4, slot.bottom - 2))
                screen.blit(count_text, text_rect)
        key_text = font.render(get_hotbar_key_label(index), True, (210, 210, 210))
        screen.blit(key_text, (slot.x + 4, slot.y + 2))


def get_backpack_panel_slot_at_pos(mouse_pos, slot_count):
    if slot_count <= 0:
        return None

    panel = pygame.Rect(52, 72, WIDTH - 104, 236)
    if not panel.collidepoint(mouse_pos):
        return None

    slot_size = 42
    gap = 6
    columns = 5
    start_x = panel.x + 16
    start_y = panel.y + 54

    for index in range(slot_count):
        col = index % columns
        row = index // columns
        slot = pygame.Rect(
            start_x + col * (slot_size + gap),
            start_y + row * (slot_size + gap),
            slot_size,
            slot_size,
        )
        if slot.collidepoint(mouse_pos):
            return index
    return -1


def draw_crafting_panel(screen, font, meat_image, crafting_grid, recipe_result, has_workbench, inventory_slots):
    layout = get_crafting_panel_layout(has_workbench)
    panel = layout["panel"]
    pygame.draw.rect(screen, (34, 34, 34), panel)
    pygame.draw.rect(screen, (160, 160, 160), panel, 2)

    title = "Crafting Table  E to close" if has_workbench else "Crafting  E to close"
    subtitle = "Drag wood/planks into the grid to craft." if not has_workbench else "Use planks and sticks in the grid."
    screen.blit(font.render(title, True, (240, 240, 240)), (panel.x + 12, panel.y + 10))
    screen.blit(font.render(subtitle, True, (190, 190, 190)), (panel.x + 12, panel.y + 28))

    grid_size = layout["grid_size"]
    slot_size = layout["slot_size"]
    gap = layout["gap"]
    for index in range(grid_size * grid_size):
        col = index % grid_size
        row = index // grid_size
        slot = pygame.Rect(
            layout["grid_x"] + col * (slot_size + gap),
            layout["grid_y"] + row * (slot_size + gap),
            slot_size,
            slot_size,
        )
        pygame.draw.rect(screen, (58, 58, 58), slot)
        pygame.draw.rect(screen, (126, 126, 126), slot, 2)
        cell = crafting_grid[index]
        if cell["type"] and cell["count"] > 0:
            draw_inventory_icon(screen, cell["type"], slot.x + 10, slot.y + 10, 24, meat_image)
            count_text = font.render(str(cell["count"]), True, WHITE)
            screen.blit(count_text, count_text.get_rect(bottomright=(slot.right - 4, slot.bottom - 2)))

    result_rect = layout["result_rect"]
    arrow = font.render("->", True, (220, 220, 220))
    screen.blit(arrow, (result_rect.x - 26, result_rect.y + 10))
    pygame.draw.rect(screen, (58, 58, 58), result_rect)
    pygame.draw.rect(screen, (200, 200, 140) if recipe_result else (126, 126, 126), result_rect, 2)
    if recipe_result:
        draw_inventory_icon(screen, recipe_result["item_type"], result_rect.x + 10, result_rect.y + 10, 24, meat_image)
        count_text = font.render(str(recipe_result["count"]), True, WHITE)
        screen.blit(count_text, count_text.get_rect(bottomright=(result_rect.right - 4, result_rect.bottom - 2)))

    screen.blit(font.render("Inventory", True, (240, 240, 240)), (layout["inventory_x"], panel.y + 34))
    for index, slot_info in enumerate(inventory_slots):
        item_type = slot_info["item_type"]
        count = slot_info["count"]
        col = index % layout["inventory_columns"]
        row = index // layout["inventory_columns"]
        slot = pygame.Rect(
            layout["inventory_x"] + col * (slot_size + gap),
            layout["inventory_y"] + row * (slot_size + gap),
            slot_size,
            slot_size,
        )
        pygame.draw.rect(screen, (48, 48, 48), slot)
        pygame.draw.rect(screen, (124, 124, 124), slot, 2)
        draw_inventory_icon(screen, item_type, slot.x + 10, slot.y + 10, 24, meat_image)
        if "durability" in slot_info:
            durability_ratio = slot_info["durability"] / max(1, slot_info["max_durability"])
            bar_width = slot.width - 8
            bar_height = 5
            bar_x = slot.x + 4
            bar_y = slot.bottom - 8
            pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(bar_x, bar_y, bar_width, bar_height))
            fill_width = max(1, int(bar_width * durability_ratio))
            bar_color = (40, 200, 70) if durability_ratio > 0.5 else (230, 180, 40) if durability_ratio > 0.2 else (210, 60, 60)
            pygame.draw.rect(screen, bar_color, pygame.Rect(bar_x, bar_y, fill_width, bar_height))
        else:
            count_text = font.render(str(count), True, WHITE)
            screen.blit(count_text, count_text.get_rect(bottomright=(slot.right - 4, slot.bottom - 2)))


def update_items(items, blocks, dt):
    """Apply gravity to items so they fall down to the ground."""
    for item in items:
        if "vy" not in item:
            item["vy"] = 0.0

        item["vy"] += GRAVITY * dt
        item_rect = pygame.Rect(
            math.floor(item["x"]),
            math.floor(item["y"]),
            math.ceil(item["size"]),
            math.ceil(item["size"]),
        )
        item_rect.y += int(round(item["vy"] * dt))

        for block_rect in get_solid_block_rects(item_rect, blocks):
            if item["vy"] > 0:
                item_rect.bottom = block_rect.top
            elif item["vy"] < 0:
                item_rect.top = block_rect.bottom
            item["vy"] = 0.0

        item["x"] = float(item_rect.x)
        item["y"] = float(item_rect.y)

def pickup_items(player_x, player_y, items):
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    remain = []
    collected_meat = 0
    collected_raw_fish = 0
    collected_rotten_meat = 0
    collected_bone = 0
    collected_diamond = 0
    collected_wood = 0
    collected_plank = 0
    collected_stone = 0
    collected_sand = 0
    collected_gravel = 0
    collected_coal = 0
    collected_iron = 0
    collected_iron_ingot = 0
    collected_gold = 0
    collected_gold_ingot = 0
    collected_gold_nugget = 0
    collected_fire_resistance_potion = 0
    collected_redstone = 0
    collected_dirt = 0
    collected_obsidian = 0
    collected_diamond_block = 0
    collected_redstone_block = 0
    for item in items:
        item_rect = pygame.Rect(item["x"], item["y"], item["size"], item["size"])
        if player_rect.colliderect(item_rect):
            if item["type"] == "meat":
                collected_meat += 1
            elif item["type"] == "raw_fish":
                collected_raw_fish += 1
            elif item["type"] == "rotten_meat":
                collected_rotten_meat += 1
            elif item["type"] == "bone":
                collected_bone += 1
            elif item["type"] == "diamond":
                collected_diamond += 1
            elif item["type"] == "wood":
                collected_wood += 1
            elif item["type"] == "plank":
                collected_plank += 1
            elif item["type"] == "stone":
                collected_stone += 1
            elif item["type"] == "sand":
                collected_sand += 1
            elif item["type"] == "gravel":
                collected_gravel += 1
            elif item["type"] == "coal":
                collected_coal += 1
            elif item["type"] == "iron_ore":
                collected_iron += 1
            elif item["type"] == "iron_ingot":
                collected_iron_ingot += 1
            elif item["type"] == "gold_ore":
                collected_gold += 1
            elif item["type"] == "gold_ingot":
                collected_gold_ingot += 1
            elif item["type"] == "gold_nugget":
                collected_gold_nugget += 1
            elif item["type"] == "fire_resistance_potion":
                collected_fire_resistance_potion += 1
            elif item["type"] == "redstone":
                collected_redstone += 1
            elif item["type"] == "dirt":
                collected_dirt += 1
            elif item["type"] == "obsidian":
                collected_obsidian += 1
            elif item["type"] == "diamond_block":
                collected_diamond_block += 1
            elif item["type"] == "redstone_block":
                collected_redstone_block += 1
        else:
            remain.append(item)

    return remain, collected_meat, collected_raw_fish, collected_rotten_meat, collected_bone, collected_diamond, collected_wood, collected_plank, collected_stone, collected_sand, collected_gravel, collected_coal, collected_iron, collected_iron_ingot, collected_gold, collected_gold_ingot, collected_gold_nugget, collected_fire_resistance_potion, collected_redstone, collected_dirt, collected_obsidian, collected_diamond_block, collected_redstone_block


def respawn_player(blocks, current_dimension="overworld"):
    spawn_x_tile = WORLD_W // 2
    if current_dimension == "nether":
        spawn_surface_y = WORLD_H // 2
    else:
        spawn_surface_y = ground_top_y_for_x(spawn_x_tile * TILE_SIZE, blocks) // TILE_SIZE
    player_x = spawn_x_tile * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) / 2
    player_y = (spawn_surface_y - 1) * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) / 2
    return player_x, player_y


def main():
    pygame.init()
    pygame.display.set_caption("Simple Minecraft Prototype")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if hasattr(pygame.key, "stop_text_input"):
        pygame.key.stop_text_input()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("microsoftyaheiui", 14)
    animal_images = load_animal_images()
    meat_image = load_meat_image()
    player_image = load_player_image()

    # Start at daytime, so hostile mobs should not spawn immediately.
    time_of_day = 8.0  # Start at 08:00 AM

    current_dimension = "overworld"
    blocks, tree_blocks = build_terrain()
    nether_blocks, nether_tree_blocks = build_nether_terrain()
    villagers = create_village(blocks, tree_blocks)
    iron_golems = create_iron_golems(villagers, blocks)
    animals = create_animals(blocks, INITIAL_ANIMAL_COUNT, time_of_day)
    respawn_queue = []
    villager_respawn_queue = []
    iron_golem_respawn_queue = []
    arrows = []
    meats = []
    meat_count = 0
    raw_fish_count = 0
    rotten_meat_count = 0
    bone_count = 0
    diamond_count = 0
    wood_count = 0
    plank_count = 0
    stone_count = 0
    sand_count = 0
    gravel_count = 0
    coal_count = 0
    iron_count = 0
    gold_count = 0
    iron_ingot_count = 0
    lighter_count = 0
    gold_ingot_count = 0
    gold_nugget_count = 0
    fire_resistance_potion_count = 0
    redstone_count = 0
    iron_sword_count = 0
    diamond_sword_count = 0
    diamond_block_count = 0
    obsidian_count = 0
    redstone_block_count = 0
    stick_count = 0
    dirt_count = 0
    workbench = None
    furnace = None
    has_furnace = False
    furnace_fuel_uses = 0
    has_wood_pickaxe = []
    has_stone_pickaxe = []
    has_iron_pickaxe = []
    has_gold_pickaxe = []
    has_diamond_pickaxe = []
    has_redstone_pickaxe = []
    selected_hotbar_index = 0
    backpack_open = False
    player_hp = 10.0       # Max HP is 10 (hearts)
    player_fire_damage_timer = 0.0
    starvation_timer = 0.0

    # Spawn near the ground surface so sky/ground layers are visible immediately.
    player_x, player_y = respawn_player(blocks, current_dimension)
    player_vy = 0.0
    on_ground = True
    camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
    camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2
    death_message_timer = 0.0
    craft_message = ""
    craft_message_timer = 0.0
    attack_cooldown_timer = 0.0
    night_spawn_timer = 0.0
    nether_piglin_spawn_timer = 0.0
    portal_teleport_cooldown = 0.0

    overworld_blocks = blocks
    overworld_tree_blocks = tree_blocks
    overworld_villagers = villagers
    overworld_iron_golems = iron_golems
    overworld_animals = animals
    overworld_respawn_queue = respawn_queue
    overworld_villager_respawn_queue = villager_respawn_queue
    overworld_iron_golem_respawn_queue = iron_golem_respawn_queue
    overworld_arrows = arrows
    overworld_meats = meats
    overworld_workbench = workbench
    overworld_furnace = furnace
    overworld_has_furnace = has_furnace
    overworld_furnace_fuel_uses = furnace_fuel_uses

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    player_facing_right = True
    crosshair_x, crosshair_y = WIDTH // 2, HEIGHT // 2
    
    is_mining = False
    mining_timer = 0.0
    mining_target = None
    crafting_open = False
    crafting_grid = [{"type": None, "count": 0} for _ in range(9)]

    # --- Day/Night Cycle ---
    time_speed = 1.0  # 1 in-game hour per 10 real seconds -> 24 hours = 4 minutes real time

    selected_item_type = get_selected_item_type(
        selected_hotbar_index,
        meat_count,
        raw_fish_count,
        rotten_meat_count,
        bone_count,
        wood_count,
        plank_count,
        stone_count,
        sand_count,
        gravel_count,
        dirt_count,
        coal_count,
        iron_count,
        gold_count,
        iron_ingot_count,
        lighter_count,
        gold_ingot_count,
        gold_nugget_count,
        fire_resistance_potion_count,
        redstone_count,
        diamond_count,
        iron_sword_count,
        diamond_sword_count,
        diamond_block_count,
        obsidian_count,
        redstone_block_count,
        stick_count,
        has_wood_pickaxe,
        has_stone_pickaxe,
        has_iron_pickaxe,
        has_gold_pickaxe,
        has_diamond_pickaxe,
    has_redstone_pickaxe,
    )

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                crosshair_x = max(0, min(event.pos[0], WIDTH - 1))
                crosshair_y = max(0, min(event.pos[1], HEIGHT - 1))
                
                # If moving mouse while mining, check if target changed
                if is_mining and mining_target:
                    _, new_target = mine_block_at_crosshair(blocks, tree_blocks, meats, camera_x, camera_y, crosshair_x, crosshair_y)
                    if new_target != mining_target:
                        is_mining = False
                        mining_timer = 0.0
                        mining_target = None
                        
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                is_down = event.type == pygame.KEYDOWN
                key = event.key
                sc = event.scancode

                if is_down:
                    if key == pygame.K_k or sc == SC_K:
                        backpack_open = not backpack_open
                    hotbar_slot_count = len(
                        build_inventory_slots(
                            meat_count,
                            raw_fish_count,
                            rotten_meat_count,
                            bone_count,
                            wood_count,
                            plank_count,
                            stone_count,
                            sand_count,
                            gravel_count,
                            dirt_count,
                            coal_count,
                            iron_count,
                            gold_count,
                            iron_ingot_count,
                            lighter_count,
                            gold_ingot_count,
                            gold_nugget_count,
                            fire_resistance_potion_count,
                            redstone_count,
                            diamond_count,
                            iron_sword_count,
                            diamond_sword_count,
                            diamond_block_count,
                            obsidian_count,
                            redstone_block_count,
                            stick_count,
                            has_wood_pickaxe,
                            has_stone_pickaxe,
                            has_iron_pickaxe,
                            has_gold_pickaxe,
                            has_diamond_pickaxe,
                        has_redstone_pickaxe,
                        )
                    )
                    hotbar_index = get_hotbar_index_for_key(key, hotbar_slot_count)
                    if hotbar_index is not None:
                        selected_hotbar_index = hotbar_index
                        selected_item_type = get_selected_item_type(
                            selected_hotbar_index,
                            meat_count,
                            raw_fish_count,
                            rotten_meat_count,
                            bone_count,
                            wood_count,
                            plank_count,
                            stone_count,
                            sand_count,
                            gravel_count,
                            dirt_count,
                            coal_count,
                            iron_count,
                            gold_count,
                            iron_ingot_count,
                            lighter_count,
                            gold_ingot_count,
                            gold_nugget_count,
                            fire_resistance_potion_count,
                            redstone_count,
                            diamond_count,
                            iron_sword_count,
                            diamond_sword_count,
                            diamond_block_count,
                            obsidian_count,
                            redstone_block_count,
                            stick_count,
                            has_wood_pickaxe,
                            has_stone_pickaxe,
                            has_iron_pickaxe,
                            has_gold_pickaxe,
                            has_diamond_pickaxe,
                            has_redstone_pickaxe,
                        )

                if key == pygame.K_a or key == pygame.K_LEFT or sc == SC_A:
                    moving_left = is_down
                if key == pygame.K_d or key == pygame.K_RIGHT or sc == SC_D:
                    moving_right = is_down
                if key == pygame.K_s or key == pygame.K_DOWN or sc == SC_S:
                    moving_down = is_down
                if (
                    key == pygame.K_SPACE
                    or key == pygame.K_w
                    or key == pygame.K_UP
                    or sc == SC_W
                ):
                    moving_up = is_down
                if is_down and (
                    key == pygame.K_SPACE
                    or key == pygame.K_w
                    or sc == SC_W
                    or key == pygame.K_UP
                ):
                    if on_ground:
                        player_vy = JUMP_VELOCITY
                        on_ground = False
                
                # Eat normal meat with F.
                if is_down and (key == pygame.K_f or sc == SC_F):
                    if meat_count > 0 and player_hp < 10.0:
                        meat_count -= 1
                        player_hp = min(10.0, player_hp + 2.0)
                    elif raw_fish_count > 0 and player_hp < 10.0:
                        raw_fish_count -= 1
                        player_hp = min(10.0, player_hp + 1.0)
                # Eat rotten flesh with G. It kills the player immediately.
                if is_down and (key == pygame.K_g or sc == SC_G):
                    if rotten_meat_count > 0:
                        rotten_meat_count -= 1
                        player_hp = 0
                        death_message_timer = 1.5
                # Use E to place/move a workbench next to the player.
                # If the player has 6 wood and no pickaxe yet, do both at once.
                if is_down and (key == pygame.K_e or sc == SC_E):
                    selected_item_type = get_selected_item_type(
                        selected_hotbar_index,
                        meat_count,
                        raw_fish_count,
                        rotten_meat_count,
                        bone_count,
                        wood_count,
                        plank_count,
                        stone_count,
                        sand_count,
                        gravel_count,
                        dirt_count,
                        coal_count,
                        iron_count,
                        gold_count,
                        iron_ingot_count,
                        lighter_count,
                        gold_ingot_count,
                        gold_nugget_count,
                        fire_resistance_potion_count,
                        redstone_count,
                        diamond_count,
                        iron_sword_count,
                        diamond_sword_count,
                        diamond_block_count,
                        obsidian_count,
                        redstone_block_count,
                        stick_count,
                        has_wood_pickaxe,
                        has_stone_pickaxe,
                        has_iron_pickaxe,
                        has_gold_pickaxe,
                        has_diamond_pickaxe,
                    has_redstone_pickaxe,
                    )
                    if selected_item_type == "diamond_block" and diamond_block_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "diamond_block",
                        ):
                            diamond_block_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "diamond_block",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = "Placed diamond block."
                            craft_message_timer = 1.2
                        else:
                            craft_message = "Aim at a nearby block surface to place it."
                            craft_message_timer = 1.2
                    elif selected_item_type == "obsidian" and obsidian_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "obsidian",
                        ):
                            obsidian_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "obsidian",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = "Placed obsidian."
                            craft_message_timer = 1.2
                        else:
                            craft_message = "Aim at a nearby block surface to place it."
                            craft_message_timer = 1.2
                    elif selected_item_type == "redstone_block" and redstone_block_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "redstone_block",
                        ):
                            redstone_block_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "redstone_block",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count, diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = "Placed redstone block."
                        else:
                            craft_message = "Aim at a nearby block surface to place it."
                        craft_message_timer = 1.2
                    nearby_villager = find_nearby_villager(player_x, player_y, villagers)
                    nearby_piglin = find_nearby_piglin(player_x, player_y, animals)
                    if selected_item_type == "lighter":
                        placed_fire_pos = try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "fire",
                            return_position=True,
                        )
                        if placed_fire_pos is not None:
                            if activate_nether_portal(blocks, placed_fire_pos):
                                craft_message = "Activated the Nether portal."
                            else:
                                craft_message = "Ignited fire."
                            craft_message_timer = 1.0
                        else:
                            craft_message = "Aim at a nearby surface to ignite fire."
                            craft_message_timer = 1.2
                    elif selected_item_type == "gravel":
                        if gravel_count >= 1 and iron_ingot_count >= 1:
                            gravel_count -= 1
                            iron_ingot_count -= 1
                            lighter_count += 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "lighter",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count, diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = "Crafted a lighter."
                            craft_message_timer = 1.2
                        else:
                            craft_message = ""
                            craft_message_timer = 0.0
                    elif selected_item_type == "iron_ingot":
                        if iron_ingot_count >= 3 and wood_count >= 2:
                            iron_ingot_count -= 3
                            wood_count -= 2
                            add_pickaxe_to_inventory(
                                "iron_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "iron_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type == "gold_ingot":
                        if nearby_piglin is not None and gold_ingot_count >= 1:
                            gold_ingot_count -= 1
                            reward_type, reward_count, reward_label = barter_with_piglin(meats, nearby_piglin)
                            if reward_type == "fire_resistance_potion":
                                fire_resistance_potion_count += reward_count
                            craft_message = f"Piglin traded {reward_label}."
                            craft_message_timer = 1.4
                        elif gold_ingot_count >= 3 and wood_count >= 2:
                            gold_ingot_count -= 3
                            wood_count -= 2
                            add_pickaxe_to_inventory(
                                "gold_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "gold_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = ""
                            craft_message_timer = 0.0
                        elif nearby_piglin is not None:
                            craft_message = "Need 1 gold ingot to trade."
                            craft_message_timer = 1.2
                        else:
                            craft_message = ""
                            craft_message_timer = 0.0
                    elif selected_item_type == "gold_nugget":
                        if gold_nugget_count >= 3:
                            gold_nugget_count -= 3
                            gold_ingot_count += 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "gold_ingot",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            craft_message = "Crafted 1 gold ingot from 3 gold nuggets."
                            craft_message_timer = 1.4
                        else:
                            craft_message = "Need 3 gold nuggets."
                            craft_message_timer = 1.2
                    elif selected_item_type == "redstone" and redstone_count >= 9:
                        redstone_count -= 9
                        redstone_block_count += 1
                        selected_hotbar_index = find_inventory_slot_index(
                            "redstone_block",
                            meat_count, raw_fish_count, rotten_meat_count, bone_count,
                            wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                            iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                            fire_resistance_potion_count,
                            redstone_count, diamond_count, iron_sword_count, diamond_sword_count,
                            diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                            has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                        )
                        craft_message = "Crafted a redstone block."
                        craft_message_timer = 1.2
                    elif selected_item_type in ("redstone", "redstone_pickaxe", "redstone_block"):
                        if redstone_count >= 3 and wood_count >= 2:
                            redstone_count -= 3
                            wood_count -= 2
                            add_pickaxe_to_inventory(
                                "redstone_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "redstone_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count, diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("diamond", "gold_pickaxe", "diamond_pickaxe"):
                        if diamond_count >= 3 and wood_count >= 2:
                            diamond_count -= 3
                            wood_count -= 2
                            add_pickaxe_to_inventory(
                                "diamond_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "diamond_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("wood", "plank") and workbench is None and (wood_count >= 4 or plank_count >= 8):
                        wx, wy, wsize = get_workbench_position(player_x, player_facing_right, blocks)
                        workbench = {"x": wx, "y": wy, "size": wsize}
                        if wood_count >= 4:
                            wood_count -= 4
                        else:
                            plank_count -= 8
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("wood", "plank") and not has_wood_pickaxe and (plank_count >= 5 or wood_count >= 2):
                        if plank_count >= 5:
                            plank_count -= 5
                        else:
                            wood_count -= 2
                        add_pickaxe_to_inventory(
                            "wood_pickaxe",
                            has_wood_pickaxe,
                            has_stone_pickaxe,
                            has_iron_pickaxe,
                            has_gold_pickaxe,
                            has_diamond_pickaxe,
                        has_redstone_pickaxe,
                        )
                        selected_hotbar_index = find_inventory_slot_index(
                            "wood_pickaxe",
                            meat_count, raw_fish_count, rotten_meat_count, bone_count,
                            wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                            iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                            fire_resistance_potion_count,
                            redstone_count,
                            diamond_count, iron_sword_count, diamond_sword_count,
                            diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                            has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                        has_redstone_pickaxe,
                        )
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("stone", "wood_pickaxe", "stone_pickaxe") and not has_stone_pickaxe and wood_count >= 2 and stone_count >= 3:
                        wood_count -= 2
                        stone_count -= 3
                        add_pickaxe_to_inventory(
                            "stone_pickaxe",
                            has_wood_pickaxe,
                            has_stone_pickaxe,
                            has_iron_pickaxe,
                            has_gold_pickaxe,
                            has_diamond_pickaxe,
                        has_redstone_pickaxe,
                        )
                        selected_hotbar_index = find_inventory_slot_index(
                            "stone_pickaxe",
                            meat_count, raw_fish_count, rotten_meat_count, bone_count,
                            wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                            iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                            fire_resistance_potion_count,
                            redstone_count,
                            diamond_count, iron_sword_count, diamond_sword_count,
                            diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                            has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                        has_redstone_pickaxe,
                        )
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type == "stone" and wood_count < 2 and not has_furnace:
                        if stone_count >= 8:
                            fx, fy, fsize = get_workbench_position(player_x, player_facing_right, blocks)
                            stone_count -= 8
                            furnace = {"x": fx, "y": fy, "size": fsize}
                            has_furnace = True
                            craft_message = "Crafted a furnace."
                            craft_message_timer = 1.8
                        else:
                            craft_message = ""
                            craft_message_timer = 0.0
                    elif selected_item_type == "iron_ore" and has_furnace:
                        if iron_count <= 0:
                            craft_message = "Need iron ore to smelt."
                            craft_message_timer = 1.8
                        else:
                            coal_count, furnace_fuel_uses, added_fuel = try_refill_furnace_fuel(
                                coal_count,
                                furnace_fuel_uses,
                            )
                            if furnace_fuel_uses <= 0:
                                craft_message = "Need 1 coal as furnace fuel."
                                craft_message_timer = 1.8
                            else:
                                iron_count -= 1
                                iron_ingot_count += 1
                                furnace_fuel_uses -= 1
                                selected_hotbar_index = find_inventory_slot_index(
                                    "iron_ingot",
                                    meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                    wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                    iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                    fire_resistance_potion_count,
                                    redstone_count,
                                    diamond_count, iron_sword_count, diamond_sword_count,
                                    diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                    has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                                )
                                if added_fuel:
                                    craft_message = f"Smelted 1 iron ingot. Fuel uses left: {furnace_fuel_uses}"
                                else:
                                    craft_message = f"Smelted 1 iron ingot. Fuel uses left: {furnace_fuel_uses}"
                                craft_message_timer = 1.8
                    elif selected_item_type == "iron_ore" and not has_furnace:
                        craft_message = "Craft a furnace first."
                        craft_message_timer = 1.8
                    elif selected_item_type == "gold_ore" and has_furnace:
                        if gold_count <= 0:
                            craft_message = "Need gold ore to smelt."
                            craft_message_timer = 1.8
                        else:
                            coal_count, furnace_fuel_uses, added_fuel = try_refill_furnace_fuel(
                                coal_count,
                                furnace_fuel_uses,
                            )
                            if furnace_fuel_uses <= 0:
                                craft_message = "Need 1 coal as furnace fuel."
                                craft_message_timer = 1.8
                            else:
                                gold_count -= 1
                                gold_ingot_count += 1
                                furnace_fuel_uses -= 1
                                selected_hotbar_index = find_inventory_slot_index(
                                    "gold_ingot",
                                    meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                    wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                    iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                    fire_resistance_potion_count,
                                    redstone_count,
                                    diamond_count, iron_sword_count, diamond_sword_count,
                                    diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                    has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                                )
                                if added_fuel:
                                    craft_message = f"Smelted 1 gold ingot. Fuel uses left: {furnace_fuel_uses}"
                                else:
                                    craft_message = f"Smelted 1 gold ingot. Fuel uses left: {furnace_fuel_uses}"
                                craft_message_timer = 1.8
                    elif selected_item_type == "gold_ore" and not has_furnace:
                        craft_message = "Craft a furnace first."
                        craft_message_timer = 1.8
                    elif selected_item_type in ("wood", "plank") and workbench is None:
                        if wood_count >= 4:
                            wx, wy, wsize = get_workbench_position(player_x, player_facing_right, blocks)
                            workbench = {"x": wx, "y": wy, "size": wsize}
                            wood_count -= 4
                        elif plank_count >= 8:
                            wx, wy, wsize = get_workbench_position(player_x, player_facing_right, blocks)
                            workbench = {"x": wx, "y": wy, "size": wsize}
                            plank_count -= 8
                        else:
                            pass
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("wood", "plank"):
                        if plank_count >= 5:
                            plank_count -= 5
                            add_pickaxe_to_inventory(
                                "wood_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "wood_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                        elif wood_count >= 2:
                            wood_count -= 2
                            add_pickaxe_to_inventory(
                                "wood_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "wood_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                        else:
                            pass
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif selected_item_type in ("stone", "wood_pickaxe", "stone_pickaxe"):
                        if wood_count >= 2 and stone_count >= 3:
                            wood_count -= 2
                            stone_count -= 3
                            add_pickaxe_to_inventory(
                                "stone_pickaxe",
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                            selected_hotbar_index = find_inventory_slot_index(
                                "stone_pickaxe",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                            has_redstone_pickaxe,
                            )
                        else:
                            pass
                        craft_message = ""
                        craft_message_timer = 0.0
                    elif nearby_villager is not None:
                        if diamond_count >= nearby_villager["trade_cost"]:
                            diamond_count -= nearby_villager["trade_cost"]
                            if nearby_villager["trade_item"] == "iron_sword":
                                iron_sword_count += 1
                                selected_hotbar_index = find_inventory_slot_index(
                                    "iron_sword",
                                    meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                    wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                    iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                    fire_resistance_potion_count,
                                    redstone_count,
                                    diamond_count, iron_sword_count, diamond_sword_count,
                                    diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                    has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                                )
                            elif nearby_villager["trade_item"] == "diamond_sword":
                                diamond_sword_count += 1
                                selected_hotbar_index = find_inventory_slot_index(
                                    "diamond_sword",
                                    meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                    wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                    iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                    fire_resistance_potion_count,
                                    redstone_count,
                                    diamond_count, iron_sword_count, diamond_sword_count,
                                    diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                    has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                                )
                            elif nearby_villager["trade_item"] == "diamond_block":
                                diamond_block_count += 1
                                selected_hotbar_index = find_inventory_slot_index(
                                    "diamond_block",
                                    meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                    wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                    iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                    fire_resistance_potion_count,
                                    redstone_count,
                                    diamond_count, iron_sword_count, diamond_sword_count,
                                    diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                    has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                                )
                            craft_message = f"Traded {nearby_villager['trade_cost']} diamonds for {nearby_villager['trade_label']}."
                        else:
                            craft_message = f"Need {nearby_villager['trade_cost']} diamonds for {nearby_villager['trade_label']}."
                        craft_message_timer = 1.8
                    else:
                        craft_message = ""
                        craft_message_timer = 0.0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_item_type = get_selected_item_type(
                    selected_hotbar_index,
                    meat_count,
                    raw_fish_count,
                    rotten_meat_count,
                    bone_count,
                    wood_count,
                    plank_count,
                    stone_count,
                    sand_count,
                    gravel_count,
                    dirt_count,
                    coal_count,
                    iron_count,
                    gold_count,
                    iron_ingot_count,
                    lighter_count,
                    gold_ingot_count,
                    gold_nugget_count,
                    fire_resistance_potion_count,
                    redstone_count,
                    diamond_count,
                    iron_sword_count,
                    diamond_sword_count,
                    diamond_block_count,
                    obsidian_count,
                    redstone_block_count,
                    stick_count,
                    has_wood_pickaxe,
                    has_stone_pickaxe,
                    has_iron_pickaxe,
                    has_gold_pickaxe,
                    has_diamond_pickaxe,
                    has_redstone_pickaxe,
                )
                inventory_slot_count = len(
                    build_inventory_slots(
                        meat_count,
                        raw_fish_count,
                        rotten_meat_count,
                        bone_count,
                        wood_count,
                        plank_count,
                        stone_count,
                        sand_count,
                        gravel_count,
                        dirt_count,
                        coal_count,
                        iron_count,
                        gold_count,
                        iron_ingot_count,
                        lighter_count,
                        gold_ingot_count,
                        gold_nugget_count,
                        fire_resistance_potion_count,
                        redstone_count,
                        diamond_count,
                        iron_sword_count,
                        diamond_sword_count,
                        diamond_block_count,
                        obsidian_count,
                        redstone_block_count,
                        stick_count,
                        has_wood_pickaxe,
                        has_stone_pickaxe,
                        has_iron_pickaxe,
                        has_gold_pickaxe,
                        has_diamond_pickaxe,
                        has_redstone_pickaxe,
                    )
                )
                if backpack_open:
                    clicked_slot_index = get_backpack_panel_slot_at_pos(event.pos, inventory_slot_count)
                    if clicked_slot_index is not None:
                        if clicked_slot_index >= 0:
                            selected_hotbar_index = clicked_slot_index
                            selected_item_type = get_selected_item_type(
                                selected_hotbar_index,
                                meat_count,
                                raw_fish_count,
                                rotten_meat_count,
                                bone_count,
                                wood_count,
                                plank_count,
                                stone_count,
                                sand_count,
                                gravel_count,
                                dirt_count,
                                coal_count,
                                iron_count,
                                gold_count,
                                iron_ingot_count,
                                lighter_count,
                                gold_ingot_count,
                                gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count,
                                iron_sword_count,
                                diamond_sword_count,
                                diamond_block_count,
                                obsidian_count,
                                redstone_block_count,
                                stick_count,
                                has_wood_pickaxe,
                                has_stone_pickaxe,
                                has_iron_pickaxe,
                                has_gold_pickaxe,
                                has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                        continue
                if event.button == 1:
                    if get_respawn_button_rect().collidepoint(event.pos):
                        player_x, player_y = respawn_player(blocks, current_dimension)
                        player_vy = 0.0
                        on_ground = True
                        is_mining = False
                        mining_timer = 0.0
                        mining_target = None
                        camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
                        camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2
                        craft_message = "Teleported to spawn."
                        craft_message_timer = 1.5
                    else:
                        mined, target = mine_block_at_crosshair(blocks, tree_blocks, meats, camera_x, camera_y, crosshair_x, crosshair_y)
                        if mined:
                            # Instantly mined a tree block
                            pass
                        elif target:
                            # Start mining a terrain block
                            is_mining = True
                            mining_timer = 0.0
                            mining_target = target
                        else:
                            if attack_cooldown_timer <= 0:
                                attack_damage, attack_cooldown = get_attack_stats(selected_item_type)
                                hit_target = attack_animal_at_crosshair(
                                    animals,
                                    meats,
                                    respawn_queue,
                                    camera_x,
                                    camera_y,
                                    crosshair_x,
                                    crosshair_y,
                                    attack_damage,
                                )
                                if not hit_target:
                                    hit_target = attack_villager_at_crosshair(
                                        villagers,
                                        meats,
                                        villager_respawn_queue,
                                        camera_x,
                                        camera_y,
                                        crosshair_x,
                                        crosshair_y,
                                        attack_damage,
                                    )
                                if not hit_target:
                                    hit_target = attack_iron_golem_at_crosshair(
                                        iron_golems,
                                        meats,
                                        iron_golem_respawn_queue,
                                        camera_x,
                                        camera_y,
                                        crosshair_x,
                                        crosshair_y,
                                        attack_damage,
                                    )
                                if hit_target:
                                    attack_cooldown_timer = attack_cooldown
                elif event.button == 3:
                    if selected_item_type == "diamond_block" and diamond_block_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "diamond_block",
                        ):
                            diamond_block_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "diamond_block",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                    elif selected_item_type == "obsidian" and obsidian_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "obsidian",
                        ):
                            obsidian_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "obsidian",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count,
                                diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
                    elif selected_item_type == "redstone_block" and redstone_block_count > 0:
                        if try_place_selected_block(
                            blocks,
                            tree_blocks,
                            player_x,
                            player_y,
                            camera_x,
                            camera_y,
                            crosshair_x,
                            crosshair_y,
                            "redstone_block",
                        ):
                            redstone_block_count -= 1
                            selected_hotbar_index = find_inventory_slot_index(
                                "redstone_block",
                                meat_count, raw_fish_count, rotten_meat_count, bone_count,
                                wood_count, plank_count, stone_count, sand_count, gravel_count, dirt_count, coal_count,
                                iron_count, gold_count, iron_ingot_count, lighter_count, gold_ingot_count, gold_nugget_count,
                                fire_resistance_potion_count,
                                redstone_count, diamond_count, iron_sword_count, diamond_sword_count,
                                diamond_block_count, obsidian_count, redstone_block_count, stick_count, has_wood_pickaxe,
                                has_stone_pickaxe, has_iron_pickaxe, has_gold_pickaxe, has_diamond_pickaxe,
                                has_redstone_pickaxe,
                            )
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_mining = False
                    mining_timer = 0.0
                    mining_target = None
            elif event.type == pygame.WINDOWFOCUSLOST:
                moving_left = False
                moving_right = False
                moving_up = False
                moving_down = False
            elif event.type == pygame.WINDOWFOCUSGAINED:
                moving_left = False
                moving_right = False
                moving_up = False
                moving_down = False
                if hasattr(pygame.key, "stop_text_input"):
                    pygame.key.stop_text_input()

        update_village_doors(blocks, player_x, player_y, villagers)
        player_rect = pygame.Rect(math.floor(player_x), math.floor(player_y), PLAYER_SIZE, PLAYER_SIZE)
        in_water = rect_overlaps_water(player_rect, blocks)

        if pygame.key.get_focused():
            keys_pressed = pygame.key.get_pressed()
            moving_left = moving_left or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
            moving_right = moving_right or keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]
            moving_up = (
                moving_up
                or keys_pressed[pygame.K_UP]
                or keys_pressed[pygame.K_w]
                or keys_pressed[pygame.K_SPACE]
            )
            moving_down = moving_down or keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]

        move_x = 0
        moving_left_now = moving_left
        moving_right_now = moving_right
        moving_up_now = moving_up
        moving_down_now = moving_down
        selected_pickaxe_tier = get_selected_pickaxe_tier(
            selected_item_type,
        )

        if moving_left_now:
            move_x -= 1
            player_facing_right = False
        if moving_right_now:
            move_x += 1
            player_facing_right = True

        move_speed = SWIM_SPEED if in_water else PLAYER_SPEED
        dx = move_x * move_speed * dt
        if in_water:
            if moving_up_now and not moving_down_now:
                player_vy = -SWIM_ASCEND_SPEED
            elif moving_down_now and not moving_up_now:
                player_vy = SWIM_DESCEND_SPEED
            else:
                player_vy = SWIM_SINK_SPEED
        else:
            player_vy += GRAVITY * dt
        dy = player_vy * dt

        on_ground = False

        if dx != 0:
            player_rect.x += int(round(dx))
            for block_rect in get_solid_block_rects(player_rect, blocks):
                if dx > 0:
                    player_rect.right = block_rect.left
                else:
                    player_rect.left = block_rect.right

        if dy != 0:
            player_rect.y += int(round(dy))
            for block_rect in get_solid_block_rects(player_rect, blocks):
                if dy > 0:
                    player_rect.bottom = block_rect.top
                    on_ground = True
                else:
                    player_rect.top = block_rect.bottom
                player_vy = 0.0

        # Standing detection uses a tiny probe below the feet, so walking on flat
        # ground does not require a "wake-up jump" after collision rounding.
        foot_probe = pygame.Rect(player_rect.x, player_rect.bottom, PLAYER_SIZE, 2)
        if get_solid_block_rects(foot_probe, blocks):
            on_ground = True

        player_x = float(player_rect.x)
        player_y = float(player_rect.y)

        # Keep player inside world.
        max_x = WORLD_W * TILE_SIZE - PLAYER_SIZE
        player_x = max(0, min(player_x, max_x))

        if portal_teleport_cooldown > 0:
            portal_teleport_cooldown = max(0.0, portal_teleport_cooldown - dt)

        player_rect = pygame.Rect(math.floor(player_x), math.floor(player_y), PLAYER_SIZE, PLAYER_SIZE)
        if (
            current_dimension == "overworld"
            and portal_teleport_cooldown <= 0
            and rect_overlaps_block_type(player_rect, blocks, "nether_portal")
        ):
            overworld_blocks = blocks
            overworld_tree_blocks = tree_blocks
            overworld_villagers = villagers
            overworld_iron_golems = iron_golems
            overworld_animals = animals
            overworld_respawn_queue = respawn_queue
            overworld_villager_respawn_queue = villager_respawn_queue
            overworld_iron_golem_respawn_queue = iron_golem_respawn_queue
            overworld_arrows = arrows
            overworld_meats = meats
            overworld_workbench = workbench
            overworld_furnace = furnace
            overworld_has_furnace = has_furnace
            overworld_furnace_fuel_uses = furnace_fuel_uses
            current_dimension = "nether"
            blocks = nether_blocks
            tree_blocks = nether_tree_blocks
            villagers = []
            iron_golems = []
            animals = create_nether_animals(blocks)
            respawn_queue = []
            villager_respawn_queue = []
            iron_golem_respawn_queue = []
            arrows = []
            meats = []
            workbench = None
            furnace = None
            has_furnace = False
            furnace_fuel_uses = 0
            player_x, player_y = respawn_player(blocks, current_dimension)
            player_vy = 0.0
            on_ground = True
            camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
            camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2
            portal_teleport_cooldown = PORTAL_TELEPORT_COOLDOWN
            craft_message = "Entered the Nether."
            craft_message_timer = 1.6
            nether_piglin_spawn_timer = 0.0

        if attack_cooldown_timer > 0:
            attack_cooldown_timer = max(0.0, attack_cooldown_timer - dt)

        if is_mining and mining_target:
            mining_timer += dt
            target_type = blocks.get(mining_target)
            if target_type in {"stone", "netherrack"}:
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.07
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.10
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.14
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.2
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.35
                else:
                    mine_duration = 1.0
            elif target_type == "plank":
                mine_duration = 0.10
            elif is_door_block(target_type):
                mine_duration = 0.10
            elif target_type == "obsidian":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.24
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.35
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.50
                else:
                    mine_duration = 1.2
            elif target_type == "diamond_ore":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.14
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.20
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.28
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.45
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.65
                else:
                    mine_duration = 1.1
            elif target_type == "iron_ore":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.12
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.18
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.24
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.42
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.6
                else:
                    mine_duration = 1.2
            elif target_type in {"gold_ore", "nether_gold_ore"}:
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.10
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.16
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.24
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.4
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.58
                else:
                    mine_duration = 1.1
            elif target_type == "coal_ore":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.08
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.12
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.16
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.28
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.45
                else:
                    mine_duration = 1.0
            elif target_type == "sand":
                mine_duration = 0.08
            elif target_type == "diamond_block":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.12
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.18
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.26
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.40
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.60
                else:
                    mine_duration = 1.1
            elif target_type == "redstone_ore":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.12
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.18
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.24
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.42
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.60
                else:
                    mine_duration = 1.2
            elif target_type == "redstone_block":
                if selected_pickaxe_tier >= 5:
                    mine_duration = 0.12
                elif selected_pickaxe_tier >= 4:
                    mine_duration = 0.18
                elif selected_pickaxe_tier >= 3:
                    mine_duration = 0.26
                elif selected_pickaxe_tier >= 2:
                    mine_duration = 0.40
                elif selected_pickaxe_tier >= 1:
                    mine_duration = 0.60
                else:
                    mine_duration = 1.1
            elif target_type == "bedrock":
                if selected_pickaxe_tier >= 6:
                    mine_duration = 0.8
                else:
                    mine_duration = float("inf")
            else:
                mine_duration = 0.0
                
            if mining_timer >= mine_duration:
                # Block mined
                del blocks[mining_target]
                broken_pickaxe_type = damage_selected_pickaxe(
                    selected_hotbar_index,
                    meat_count,
                    raw_fish_count,
                    rotten_meat_count,
                    bone_count,
                    wood_count,
                    plank_count,
                    stone_count,
                    sand_count,
                    gravel_count,
                    dirt_count,
                    coal_count,
                    iron_count,
                    gold_count,
                    iron_ingot_count,
                    lighter_count,
                    gold_ingot_count,
                    gold_nugget_count,
                    fire_resistance_potion_count,
                    redstone_count,
                    diamond_count,
                    iron_sword_count,
                    diamond_sword_count,
                    diamond_block_count,
                    obsidian_count,
                    redstone_block_count,
                    stick_count,
                    has_wood_pickaxe,
                    has_stone_pickaxe,
                    has_iron_pickaxe,
                    has_gold_pickaxe,
                    has_diamond_pickaxe,
                    has_redstone_pickaxe,
                )
                if broken_pickaxe_type is not None and selected_item_type == broken_pickaxe_type:
                    craft_message = ""
                    craft_message_timer = 0.0
                
                # Make water flow down continuously if empty space created
                update_water(blocks)
                
                # Drop stone or dirt
                if target_type == "stone":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "stone",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "plank":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "plank",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif is_door_block(target_type):
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "plank",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "obsidian":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "obsidian",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "coal_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "coal",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "iron_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "iron_ore",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "gold_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "gold_ore",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "nether_gold_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "gold_nugget",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "redstone_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "redstone",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "diamond_ore":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "diamond",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "redstone_block":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "redstone_block",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "diamond_block":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "diamond_block",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "sand":
                    drop_size = max(10, TILE_SIZE // 3)
                    drop_type = "gravel" if random.random() < 0.05 else "sand"
                    meats.append({
                        "type": drop_type,
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                elif target_type == "dirt" or target_type == "grass":
                    drop_size = max(10, TILE_SIZE // 3)
                    meats.append({
                        "type": "dirt",
                        "x": mining_target[0] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "y": mining_target[1] * TILE_SIZE + (TILE_SIZE - drop_size) / 2,
                        "size": drop_size,
                    })
                
                is_mining = False
                mining_timer = 0.0
                mining_target = None

        # Keep player from flying too high out of world.
        player_y = max(-4 * TILE_SIZE, player_y)

        update_animals(animals, blocks, dt, meats, respawn_queue, player_x, player_y, time_of_day, arrows)
        update_villagers(villagers, blocks, dt, meats, villager_respawn_queue)
        update_iron_golems(iron_golems, blocks, dt, meats, iron_golem_respawn_queue)
        update_respawns(respawn_queue, animals, blocks, dt, time_of_day, current_dimension, player_x)

        if current_dimension == "nether":
            piglin_count = sum(1 for animal in animals if animal["name"] == "Piglin")
            if piglin_count < NETHER_PIGLIN_TARGET:
                nether_piglin_spawn_timer += dt
                if nether_piglin_spawn_timer >= NETHER_PIGLIN_SPAWN_DELAY:
                    occupied_tiles = {int(a["x"] // TILE_SIZE) for a in animals}
                    preferred_tile_x = int((player_x + PLAYER_SIZE / 2) // TILE_SIZE)
                    piglin = spawn_nether_piglin(blocks, occupied_tiles, preferred_tile_x)
                    if piglin is not None:
                        animals.append(piglin)
                    nether_piglin_spawn_timer = 0.0
            else:
                nether_piglin_spawn_timer = 0.0
        else:
            nether_piglin_spawn_timer = 0.0
        update_villager_respawns(villager_respawn_queue, villagers, dt)
        update_iron_golem_respawns(iron_golem_respawn_queue, iron_golems, dt)
        update_items(meats, blocks, dt)
        player_hp = max(0.0, player_hp - update_arrows(arrows, blocks, dt, player_x, player_y))
        player_fire_state = {"fire_damage_timer": player_fire_damage_timer}
        player_touching_fire = rect_overlaps_block_type(player_rect, blocks, "fire")
        player_fire_hits = accumulate_fire_damage(player_fire_state, player_touching_fire, dt)
        player_fire_damage_timer = player_fire_state["fire_damage_timer"]
        if player_fire_hits > 0:
            player_hp = max(0.0, player_hp - player_fire_hits)
        player_touching_lava = rect_overlaps_block_type(player_rect, blocks, "lava")
        if current_dimension == "nether" and player_touching_lava:
            used_fire_resistance = fire_resistance_potion_count > 0
            if used_fire_resistance:
                fire_resistance_potion_count -= 1
                player_hp = 10.0
            else:
                player_hp = 2.0
            current_dimension = "overworld"
            blocks = overworld_blocks
            tree_blocks = overworld_tree_blocks
            villagers = overworld_villagers
            iron_golems = overworld_iron_golems
            animals = overworld_animals
            respawn_queue = overworld_respawn_queue
            villager_respawn_queue = overworld_villager_respawn_queue
            iron_golem_respawn_queue = overworld_iron_golem_respawn_queue
            arrows = overworld_arrows
            meats = overworld_meats
            workbench = overworld_workbench
            furnace = overworld_furnace
            has_furnace = overworld_has_furnace
            furnace_fuel_uses = overworld_furnace_fuel_uses
            player_x, player_y = respawn_player(blocks, current_dimension)
            player_vy = 0.0
            on_ground = True
            player_fire_damage_timer = 0.0
            portal_teleport_cooldown = PORTAL_TELEPORT_COOLDOWN
            camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
            camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2
            if used_fire_resistance:
                craft_message = "Fire resistance brought you home safely."
            else:
                craft_message = "You escaped the Nether with 1 heart left."
            craft_message_timer = 1.8

        meats, got_meat, got_raw_fish, got_rotten_meat, got_bone, got_diamond, got_wood, got_plank, got_stone, got_sand, got_gravel, got_coal, got_iron, got_iron_ingot, got_gold, got_gold_ingot, got_gold_nugget, got_fire_resistance_potion, got_redstone, got_dirt, got_obsidian, got_diamond_block, got_redstone_block = pickup_items(player_x, player_y, meats)
        meat_count += got_meat
        raw_fish_count += got_raw_fish
        rotten_meat_count += got_rotten_meat
        bone_count += got_bone
        diamond_count += got_diamond
        wood_count += got_wood
        plank_count += got_plank
        stone_count += got_stone
        sand_count += got_sand
        gravel_count += got_gravel
        coal_count += got_coal
        iron_count += got_iron
        iron_ingot_count += got_iron_ingot
        gold_count += got_gold
        gold_ingot_count += got_gold_ingot
        gold_nugget_count += got_gold_nugget
        fire_resistance_potion_count += got_fire_resistance_potion
        redstone_count += got_redstone
        dirt_count += got_dirt
        obsidian_count += got_obsidian
        diamond_block_count += got_diamond_block
        redstone_block_count += got_redstone_block

        if player_hp <= 0:
            player_x, player_y = respawn_player(blocks, current_dimension)
            player_vy = 0.0
            on_ground = True
            player_hp = 10.0
            player_fire_damage_timer = 0.0
            death_message_timer = 1.5
            camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
            camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2

        if death_message_timer > 0:
            death_message_timer = max(0.0, death_message_timer - dt)
        if craft_message_timer > 0:
            craft_message_timer = max(0.0, craft_message_timer - dt)

        inventory_slot_count = len(
            build_inventory_slots(
                meat_count,
                raw_fish_count,
                rotten_meat_count,
                bone_count,
                wood_count,
                plank_count,
                stone_count,
                sand_count,
                gravel_count,
                dirt_count,
                coal_count,
                iron_count,
                gold_count,
                iron_ingot_count,
                lighter_count,
                gold_ingot_count,
                gold_nugget_count,
                fire_resistance_potion_count,
                redstone_count,
                diamond_count,
                iron_sword_count,
                diamond_sword_count,
                diamond_block_count,
                obsidian_count,
                redstone_block_count,
                stick_count,
                has_wood_pickaxe,
                has_stone_pickaxe,
                has_iron_pickaxe,
                has_gold_pickaxe,
                has_diamond_pickaxe,
            has_redstone_pickaxe,
            )
        )
        if inventory_slot_count <= 0:
            selected_hotbar_index = 0
        else:
            selected_hotbar_index = max(0, min(selected_hotbar_index, inventory_slot_count - 1))

        selected_item_type = get_selected_item_type(
            selected_hotbar_index,
            meat_count,
            raw_fish_count,
            rotten_meat_count,
            bone_count,
            wood_count,
            plank_count,
            stone_count,
            sand_count,
            gravel_count,
            dirt_count,
            coal_count,
            iron_count,
            gold_count,
            iron_ingot_count,
            lighter_count,
            gold_ingot_count,
            gold_nugget_count,
            fire_resistance_potion_count,
            redstone_count,
            diamond_count,
            iron_sword_count,
            diamond_sword_count,
            diamond_block_count,
            obsidian_count,
            redstone_block_count,
            stick_count,
            has_wood_pickaxe,
            has_stone_pickaxe,
            has_iron_pickaxe,
            has_gold_pickaxe,
            has_diamond_pickaxe,
        has_redstone_pickaxe,
        )

        if current_dimension == "overworld" and is_nighttime(time_of_day):
            zombie_count = sum(1 for animal in animals if animal["name"] == "Zombie")
            skeleton_count = sum(1 for animal in animals if animal["name"] == "Skeleton")
            if zombie_count < NIGHT_ZOMBIE_TARGET or skeleton_count < NIGHT_SKELETON_TARGET:
                night_spawn_timer += dt
                if night_spawn_timer >= NIGHT_ZOMBIE_SPAWN_DELAY:
                    if zombie_count < NIGHT_ZOMBIE_TARGET and (
                        skeleton_count >= NIGHT_SKELETON_TARGET or zombie_count <= skeleton_count
                    ):
                        spawn_extra_night_zombie(animals, blocks)
                    elif skeleton_count < NIGHT_SKELETON_TARGET:
                        spawn_extra_night_skeleton(animals, blocks)
                    night_spawn_timer = 0.0
            else:
                night_spawn_timer = 0.0
        else:
            night_spawn_timer = 0.0

        # Camera follows player smoothly, so movement is visually obvious.
        target_camera_x = player_x - WIDTH / 2 + PLAYER_SIZE / 2
        target_camera_y = player_y - HEIGHT / 2 + PLAYER_SIZE / 2
        camera_x += (target_camera_x - camera_x) * 0.18
        camera_y += (target_camera_y - camera_y) * 0.18

        # Clamp camera to world bounds.
        max_camera_x = WORLD_W * TILE_SIZE - WIDTH
        max_camera_y = WORLD_H * TILE_SIZE - HEIGHT
        camera_x = max(0, min(camera_x, max_camera_x))
        camera_y = max(0, min(camera_y, max_camera_y))

        # Update time of day
        time_of_day += time_speed * dt
        if time_of_day >= 24.0:
            time_of_day -= 24.0
            
        # Get sky color and darkness level
        sky_color, darkness_color, darkness = get_dimension_sky(current_dimension, time_of_day)

        screen.fill(sky_color)
        draw_world(screen, camera_x, camera_y, blocks, tree_blocks)
        draw_workbench(screen, workbench, camera_x, camera_y)
        draw_furnace(screen, furnace, camera_x, camera_y)

        # Draw player in screen space.
        if player_image:
            img_to_draw = player_image
            if not player_facing_right:
                img_to_draw = pygame.transform.flip(player_image, True, False)
            screen.blit(img_to_draw, (player_x - camera_x, player_y - camera_y))
        else:
            pygame.draw.rect(
                screen,
                PLAYER_COLOR,
                pygame.Rect(player_x - camera_x, player_y - camera_y, PLAYER_SIZE, PLAYER_SIZE),
            )
        selected_tool = get_selected_tool(
            selected_item_type,
        )
        if selected_tool == "wood_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_wood_pickaxe(screen, hand_x, hand_y, 14)
        elif selected_tool == "iron_sword":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 4
            draw_iron_sword(screen, hand_x, hand_y, 14)
        elif selected_tool == "diamond_sword":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 4
            draw_diamond_sword(screen, hand_x, hand_y, 14)
        elif selected_tool == "stone_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_stone_pickaxe(screen, hand_x, hand_y, 14)
        elif selected_tool == "iron_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_iron_pickaxe(screen, hand_x, hand_y, 14)
        elif selected_tool == "gold_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_gold_pickaxe(screen, hand_x, hand_y, 14)
        elif selected_tool == "diamond_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_diamond_pickaxe(screen, hand_x, hand_y, 14)
        elif selected_tool == "redstone_pickaxe":
            hand_x = player_x - camera_x + (PLAYER_SIZE - 6 if player_facing_right else -10)
            hand_y = player_y - camera_y + 6
            draw_redstone_pickaxe(screen, hand_x, hand_y, 14)
            
        draw_animals(screen, animals, camera_x, camera_y, font, animal_images)
        draw_villagers(screen, villagers, camera_x, camera_y, font)
        draw_iron_golems(screen, iron_golems, camera_x, camera_y, font)
        draw_arrows(screen, arrows, camera_x, camera_y)
        draw_items(screen, meats, camera_x, camera_y, meat_image)
        nearby_villager = find_nearby_villager(player_x, player_y, villagers)

        # Apply darkness
        if darkness > 0:
            dark_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_surface.fill((*darkness_color, darkness))
            screen.blit(dark_surface, (0, 0))

        # Format time string (e.g. 08:30)
        h = int(time_of_day)
        m = int((time_of_day - h) * 60)
        time_str = f"{h:02d}:{m:02d}"

        draw_status_panel(screen, font, player_hp, time_str)
        draw_respawn_button(screen, font)
        if current_dimension == "nether":
            dimension_text = font.render("Dimension: Nether", True, (228, 214, 255))
            screen.blit(dimension_text, (10, 110))
        draw_hotbar(
            screen=screen,
            font=font,
            meat_image=meat_image,
            meat_count=meat_count,
            raw_fish_count=raw_fish_count,
            rotten_meat_count=rotten_meat_count,
            bone_count=bone_count,
            wood_count=wood_count,
            plank_count=plank_count,
            stone_count=stone_count,
            sand_count=sand_count,
            gravel_count=gravel_count,
            dirt_count=dirt_count,
            coal_count=coal_count,
            iron_count=iron_count,
            gold_count=gold_count,
            iron_ingot_count=iron_ingot_count,
            lighter_count=lighter_count,
            gold_ingot_count=gold_ingot_count,
            gold_nugget_count=gold_nugget_count,
            fire_resistance_potion_count=fire_resistance_potion_count,
            redstone_count=redstone_count,
            diamond_count=diamond_count,
            iron_sword_count=iron_sword_count,
            diamond_sword_count=diamond_sword_count,
            diamond_block_count=diamond_block_count,
            obsidian_count=obsidian_count,
            redstone_block_count=redstone_block_count,
            stick_count=stick_count,
            has_wood_pickaxe=has_wood_pickaxe,
            has_stone_pickaxe=has_stone_pickaxe,
            has_iron_pickaxe=has_iron_pickaxe,
            has_gold_pickaxe=has_gold_pickaxe,
            has_diamond_pickaxe=has_diamond_pickaxe,
            has_redstone_pickaxe=has_redstone_pickaxe,
            selected_index=selected_hotbar_index,
        )
        if backpack_open:
            draw_backpack_panel(
                screen=screen,
                font=font,
                meat_image=meat_image,
                meat_count=meat_count,
                raw_fish_count=raw_fish_count,
                rotten_meat_count=rotten_meat_count,
                bone_count=bone_count,
                wood_count=wood_count,
                plank_count=plank_count,
                stone_count=stone_count,
                sand_count=sand_count,
                gravel_count=gravel_count,
                dirt_count=dirt_count,
                coal_count=coal_count,
                iron_count=iron_count,
                gold_count=gold_count,
                iron_ingot_count=iron_ingot_count,
                lighter_count=lighter_count,
                gold_ingot_count=gold_ingot_count,
                gold_nugget_count=gold_nugget_count,
                fire_resistance_potion_count=fire_resistance_potion_count,
                redstone_count=redstone_count,
                diamond_count=diamond_count,
                iron_sword_count=iron_sword_count,
                diamond_sword_count=diamond_sword_count,
                diamond_block_count=diamond_block_count,
                obsidian_count=obsidian_count,
                redstone_block_count=redstone_block_count,
                stick_count=stick_count,
                has_wood_pickaxe=has_wood_pickaxe,
                has_stone_pickaxe=has_stone_pickaxe,
                has_iron_pickaxe=has_iron_pickaxe,
                has_gold_pickaxe=has_gold_pickaxe,
                has_diamond_pickaxe=has_diamond_pickaxe,
                has_redstone_pickaxe=has_redstone_pickaxe,
                selected_index=selected_hotbar_index,
            )

        if death_message_timer > 0:
            death_text = font.render("You died from rotten flesh!", True, (220, 60, 60))
            screen.blit(death_text, (10, 30))
        if craft_message_timer > 0:
            craft_text = font.render(craft_message, True, (240, 230, 120))
            screen.blit(craft_text, (10, 50))
        if nearby_villager is not None:
            trade_hint = font.render(
                f"Press E to trade: {nearby_villager['trade_cost']} diamonds -> {nearby_villager['trade_label']}",
                True,
                (230, 240, 200),
            )
            screen.blit(trade_hint, (10, 90))
        if has_furnace:
            furnace_text = font.render(
                f"Coal Fuel:{furnace_fuel_uses}",
                True,
                (210, 210, 210),
            )
            screen.blit(furnace_text, (10, 70))

        draw_crosshair(screen, crosshair_x, crosshair_y)
        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
