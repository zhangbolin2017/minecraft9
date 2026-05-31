import pygame
import os

# 初始化 pygame 以便使用 Surface
pygame.init()

# 图片保存目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "image")
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def create_animal_image(filename, width, height, colors):
    # colors 格式: list of (x, y, w, h, (r, g, b))
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for x, y, w, h, color in colors:
        pygame.draw.rect(surface, color, (x, y, w, h))
    pygame.image.save(surface, os.path.join(IMAGE_DIR, filename))
    print(f"Created {filename}")

def create_pixel_art_image(filename, width, height, pattern, palette, facing_right=True, extra_draw=None):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rows = len(pattern)
    cols = len(pattern[0])
    draw_pattern = pattern if facing_right else [row[::-1] for row in pattern]

    cell_size = max(1, min(width // cols, height // rows))
    art_width = cols * cell_size
    art_height = rows * cell_size
    offset_x = (width - art_width) // 2
    offset_y = (height - art_height) // 2

    for row_index, row in enumerate(draw_pattern):
        for col_index, code in enumerate(row):
            color = palette.get(code)
            if color is None:
                continue
            x = offset_x + col_index * cell_size
            y = offset_y + row_index * cell_size
            pygame.draw.rect(surface, color, (x, y, cell_size, cell_size))

    if extra_draw is not None:
        extra_draw(surface, width, height, facing_right)

    pygame.image.save(surface, os.path.join(IMAGE_DIR, filename))
    print(f"Created {filename}")

# 1. 羊 (Sheep) - 尺寸 26x26
sheep_colors = [
    # 身体 (白色毛)
    (2, 6, 22, 16, (235, 235, 235)),
    # 脸部 (浅棕色)
    (2, 2, 8, 8, (200, 160, 140)),
    # 眼睛 (黑色)
    (3, 4, 2, 2, (0, 0, 0)),
    (7, 4, 2, 2, (0, 0, 0)),
    # 腿 (棕色)
    (4, 22, 4, 4, (150, 100, 80)),
    (18, 22, 4, 4, (150, 100, 80)),
]
create_animal_image("sheep.png", 26, 26, sheep_colors)

# 2. 牛 (Cow) - 尺寸 30x30
cow_colors = [
    # 身体 (棕色)
    (2, 6, 26, 18, (120, 80, 50)),
    # 白色斑块
    (8, 8, 6, 6, (240, 240, 240)),
    (18, 14, 6, 6, (240, 240, 240)),
    # 脸部 (浅棕色)
    (2, 2, 10, 10, (150, 110, 80)),
    # 眼睛
    (3, 4, 2, 2, (0, 0, 0)),
    (8, 4, 2, 2, (0, 0, 0)),
    # 角
    (1, 0, 2, 3, (200, 200, 200)),
    (11, 0, 2, 3, (200, 200, 200)),
    # 腿
    (4, 24, 4, 6, (80, 50, 30)),
    (22, 24, 4, 6, (80, 50, 30)),
]
create_animal_image("cow.png", 30, 30, cow_colors)

# 3. 鸡 (Chicken) - 尺寸 20x20
chicken_colors = [
    # 身体 (白色)
    (4, 6, 12, 10, (245, 245, 245)),
    # 头 (白色)
    (2, 2, 6, 6, (245, 245, 245)),
    # 眼睛
    (4, 3, 2, 2, (0, 0, 0)),
    # 喙 (黄色)
    (0, 4, 2, 2, (255, 200, 0)),
    # 肉垂 (红色)
    (2, 6, 2, 2, (200, 0, 0)),
    # 腿 (黄色)
    (6, 16, 2, 4, (255, 200, 0)),
    (12, 16, 2, 4, (255, 200, 0)),
]
create_animal_image("chicken.png", 20, 20, chicken_colors)

# 4. 肉 (Meat) - 尺寸 16x16
meat_colors = [
    # 红色肉身
    (4, 4, 8, 8, (220, 60, 60)),
    (2, 6, 2, 4, (220, 60, 60)),
    (12, 6, 2, 4, (220, 60, 60)),
    # 白色脂肪边缘
    (4, 2, 8, 2, (245, 245, 245)),
    (4, 12, 8, 2, (245, 245, 245)),
    # 中间纹理
    (6, 6, 2, 4, (245, 200, 200)),
    (10, 8, 2, 2, (245, 200, 200)),
]
create_animal_image("meat.png", 16, 16, meat_colors)

# 5. 玩家 (Player) - 尺寸 32x32 (类似 Minecraft Steve 风格，朝右)
player_colors = [
    # 皮肤 (头)
    (10, 4, 12, 12, (220, 170, 130)),
    # 头发顶
    (10, 4, 12, 3, (80, 40, 20)),
    # 头发后
    (10, 7, 3, 5, (80, 40, 20)),
    # 眼睛 (朝右)
    (18, 8, 2, 2, (0, 0, 0)),
    # 身体 (青色衬衫)
    (12, 16, 8, 10, (0, 170, 170)),
    # 手臂 (稍微深一点区分袖子)
    (14, 16, 4, 5, (0, 150, 150)),
    # 手
    (14, 21, 4, 5, (220, 170, 130)),
    # 腿 (蓝色裤子)
    (12, 26, 8, 4, (40, 40, 120)),
    # 鞋子
    (12, 30, 8, 2, (100, 100, 100)),
]
create_animal_image("player.png", 32, 32, player_colors)

# 6. 鱼 (Fish) - 尺寸 22x22
fish_pattern = [
    "00011000",
    "00111100",
    "11333321",
    "11333321",
    "00111100",
    "00011000",
]
fish_palette = {
    "0": None,
    "1": (250, 250, 250),
    "2": (24, 24, 24),
    "3": (235, 235, 235),
}
create_pixel_art_image("fish.png", 22, 22, fish_pattern, fish_palette)

# 7. 骷髅 (Skeleton) - 尺寸 30x30
skeleton_pattern = [
    "00111100",
    "01111110",
    "01011010",
    "00111100",
    "00111100",
    "01111110",
    "01100110",
    "01000010",
]
skeleton_palette = {
    "0": None,
    "1": (236, 236, 236),
    "2": (170, 170, 170),
}

def draw_skeleton_details(surface, width, height, facing_right):
    center_x = width // 2
    shoulder_y = height // 2 - 2
    hand_y = height // 2 + 1
    arm_reach = width // 3
    bow_x = width - 4 if facing_right else 4
    hand_x = center_x + arm_reach if facing_right else center_x - arm_reach
    off_hand_x = center_x - 3 if facing_right else center_x + 3

    pygame.draw.line(surface, (214, 214, 214), (center_x, shoulder_y), (hand_x, hand_y), 2)
    pygame.draw.line(surface, (194, 194, 194), (center_x, shoulder_y), (off_hand_x, hand_y - 1), 2)
    pygame.draw.line(surface, (194, 194, 194), (center_x - 3, height - 10), (center_x - 6, height - 2), 2)
    pygame.draw.line(surface, (194, 194, 194), (center_x + 3, height - 10), (center_x + 6, height - 2), 2)

    bow_top = (bow_x, 5)
    bow_mid = (bow_x + (-2 if facing_right else 2), height // 2)
    bow_bottom = (bow_x, height - 5)
    pygame.draw.line(surface, (120, 80, 45), bow_top, bow_mid, 2)
    pygame.draw.line(surface, (120, 80, 45), bow_mid, bow_bottom, 2)
    string_x = bow_x - 3 if facing_right else bow_x + 3
    pygame.draw.line(surface, (240, 240, 240), (string_x, 6), (string_x, height - 6), 1)

create_pixel_art_image(
    "skeleton.png",
    30,
    30,
    skeleton_pattern,
    skeleton_palette,
    extra_draw=draw_skeleton_details,
)

# 8. 猪灵 (Piglin) - 尺寸 30x30
piglin_pattern = [
    "01111110",
    "11222211",
    "12344321",
    "12455421",
    "12444421",
    "12666621",
    "12600621",
    "02600620",
]
piglin_palette = {
    "0": None,
    "1": (148, 92, 92),
    "2": (214, 156, 146),
    "3": (244, 196, 170),
    "4": (198, 136, 128),
    "5": (126, 72, 70),
    "6": (108, 72, 38),
}

def draw_piglin_details(surface, width, height, facing_right):
    eye_x = width * 5 // 8 if facing_right else width * 3 // 8
    pygame.draw.rect(surface, (30, 18, 18), (eye_x, height // 3, 2, 2))

create_pixel_art_image("piglin.png", 30, 30, piglin_pattern, piglin_palette, extra_draw=draw_piglin_details)

# 9. 村民 (Villager) - 尺寸 30x30
villager_pattern = [
    "01111110",
    "11233211",
    "11222211",
    "01344310",
    "01444410",
    "01444410",
    "01555510",
    "01500510",
]
villager_palette = {
    "0": None,
    "1": (110, 70, 44),
    "2": (214, 178, 142),
    "3": (66, 40, 28),
    "4": (130, 84, 44),
    "5": (86, 56, 30),
}

def draw_villager_details(surface, width, height, facing_right):
    eye_x = width * 5 // 8 if facing_right else width * 3 // 8
    pygame.draw.rect(surface, (32, 20, 12), (eye_x, height // 3, 2, 2))

create_pixel_art_image("villager.png", 30, 30, villager_pattern, villager_palette, extra_draw=draw_villager_details)

# 10. 铁傀儡 (Iron Golem) - 尺寸 40x40
iron_golem_pattern = [
    "01111110",
    "11222211",
    "12333321",
    "12444421",
    "12444421",
    "12422421",
    "12500521",
    "02500520",
]
iron_golem_palette = {
    "0": None,
    "1": (186, 194, 186),
    "2": (150, 156, 150),
    "3": (116, 132, 96),
    "4": (208, 214, 208),
    "5": (124, 88, 56),
}

def draw_iron_golem_details(surface, width, height, facing_right):
    eye_x = width * 5 // 8 if facing_right else width * 3 // 8
    pygame.draw.rect(surface, (74, 40, 20), (eye_x, height // 3, 3, 2))

create_pixel_art_image(
    "iron_golem.png",
    40,
    40,
    iron_golem_pattern,
    iron_golem_palette,
    extra_draw=draw_iron_golem_details,
)

# 11. 烈焰人 (Blaze) - 尺寸 30x30
blaze_pattern = [
    "00111100",
    "01222210",
    "12333321",
    "12344321",
    "12333321",
    "01222210",
    "00111100",
    "00011000",
]
blaze_palette = {
    "0": None,
    "1": (244, 188, 54),
    "2": (255, 222, 82),
    "3": (255, 164, 52),
    "4": (110, 44, 10),
}

def draw_blaze_details(surface, width, height, facing_right):
    eye_y = height // 3
    eye_left = width * 3 // 8 if facing_right else width * 2 // 8
    eye_right = width * 5 // 8 if facing_right else width * 4 // 8
    pygame.draw.rect(surface, (82, 24, 8), (eye_left, eye_y, 2, 2))
    pygame.draw.rect(surface, (82, 24, 8), (eye_right, eye_y, 2, 2))
    rod_color = (232, 196, 74)
    rod_shadow = (176, 118, 28)
    for index, rod_y in enumerate((4, 10, 16, 22)):
        offset = -1 if index % 2 == 0 else 1
        left_x = width // 2 - 10 + offset
        right_x = width // 2 + 6 - offset
        pygame.draw.rect(surface, rod_color, (left_x, rod_y, 3, 10))
        pygame.draw.rect(surface, rod_color, (right_x, rod_y + 1, 3, 10))
        pygame.draw.rect(surface, rod_shadow, (left_x, rod_y + 8, 3, 2))
        pygame.draw.rect(surface, rod_shadow, (right_x, rod_y + 9, 3, 2))

create_pixel_art_image("blaze.png", 30, 30, blaze_pattern, blaze_palette, extra_draw=draw_blaze_details)

print("All images generated successfully.")
pygame.quit()
