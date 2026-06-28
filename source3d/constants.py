WINDOW_TITLE = "Minecraft9 3D Prototype"

CHUNK_SIZE = 16
WORLD_HEIGHT = 16
LOAD_RADIUS = 1
INTERACTION_DISTANCE = 8

TERRAIN_SEED = 9031
BASE_GROUND_HEIGHT = 4
HEIGHT_VARIATION = 2
WATER_LEVEL = 4

SAVE_FILE = "world_save.json"
HOTBAR_SIZE = 9

TEXTURE_FILE_OVERRIDES = {
    "grass": "grass1",
    "wood_axe": "wooden_axe",
}

FOOD_HEAL_AMOUNT = {
    "meat_fish": 2,
    "meat_chicken": 3,
    "meat_pig": 4,
    "meat_sheep": 4,
    "meat_cow": 5,
}

TOOL_DURABILITY = {
    "wood_axe": 57,
    "stone_axe": 100,
    "copper_axe": 186,
    "iron_axe": 206,
}

RIGHT_CLICK_CRAFTING_RECIPES = {
    "log": {
        "consumes": {"log": 1},
        "produces": {"wood": 4},
    },
    "wood": {
        "consumes": {"wood": 2},
        "produces": {"stick": 2},
    },
    "iron_ingot": {
        "consumes": {"iron_ingot": 3, "stick": 2},
        "produces": {"iron_axe": 1},
    },
    "copper_ingot": {
        "consumes": {"copper_ingot": 3, "stick": 2},
        "produces": {"copper_axe": 1},
    },
    "stick": {
        "consumes": {"wood": 3, "stick": 2},
        "produces": {"wood_axe": 1},
    },
    "stone": {
        "consumes": {"stone": 3, "stick": 2},
        "produces": {"stone_axe": 1},
    },
}

CRAFTABLE_BLOCK_RECIPES = {
    "furnace": {
        "stone": 8,
    },
}

SMELTING_RECIPES = {
    "iron_ore": "iron_ingot",
    "copper_ore": "copper_ingot",
}

FURNACE_FUEL_ITEMS = {
    "coal": 1,
}

BLOCK_DROP_ITEMS = {
    "coal_ore": "coal",
}

PLACEABLE_ITEMS = {
    "grass",
    "dirt",
    "stone",
    "sand",
    "log",
    "leaves",
    "wood",
    "coal_ore",
    "copper_ore",
    "iron_ore",
    "furnace",
}

NON_MINEABLE_BLOCKS = {
    "bedrock",
    "water",
}

NON_INVENTORY_BLOCKS = {
    "water",
}

BLOCK_COLORS = {
    "grass": (95, 159, 53),
    "dirt": (120, 88, 58),
    "stone": (110, 110, 110),
    "coal": (52, 52, 52),
    "coal_ore": (96, 96, 96),
    "copper_axe": (198, 126, 88),
    "copper_ingot": (203, 126, 82),
    "copper_ore": (180, 121, 86),
    "iron_ore": (153, 126, 108),
    "iron_ingot": (226, 220, 213),
    "iron_axe": (201, 201, 201),
    "stone_axe": (155, 155, 155),
    "wood_axe": (161, 124, 84),
    "furnace": (105, 105, 105),
    "stick": (143, 112, 72),
    "wood": (139, 69, 19),
    "sand": (222, 206, 138),
    "bedrock": (58, 58, 58),
    "log": (102, 81, 51),
    "leaves": (61, 142, 51),
    "water": (63, 118, 228),
    "meat_fish": (245, 170, 165),
    "meat_pig": (255, 150, 150),
    "meat_cow": (200, 100, 100),
    "meat_sheep": (255, 100, 100),
    "meat_chicken": (255, 200, 150),
}


def get_texture_asset_name(block_type):
    return TEXTURE_FILE_OVERRIDES.get(block_type, block_type)
