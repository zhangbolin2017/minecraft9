import pygame
import os

# 初始化 pygame 以便使用 Surface
pygame.init()

# 图片保存目录
IMAGE_DIR = r"d:\python\minecraft\image"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def create_animal_image(filename, width, height, colors):
    # colors 格式: list of (x, y, w, h, (r, g, b))
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for x, y, w, h, color in colors:
        pygame.draw.rect(surface, color, (x, y, w, h))
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

print("All images generated successfully.")
pygame.quit()
