import atexit
import math
import os
import traceback
from pathlib import Path

from ursina import (
    Audio,
    DirectionalLight,
    Entity,
    Text,
    Ursina,
    Vec3,
    camera,
    color,
    held_keys,
    mouse,
    raycast,
    scene,
    time,
    window,
)

from constants import (
    BLOCK_DROP_ITEMS,
    CHUNK_SIZE,
    CRAFTABLE_BLOCK_RECIPES,
    FOOD_HEAL_AMOUNT,
    FURNACE_FUEL_ITEMS,
    HOTBAR_SIZE,
    INTERACTION_DISTANCE,
    NON_INVENTORY_BLOCKS,
    NON_MINEABLE_BLOCKS,
    PLACEABLE_ITEMS,
    RIGHT_CLICK_CRAFTING_RECIPES,
    SAVE_FILE,
    SMELTING_RECIPES,
    TOOL_DURABILITY,
    WINDOW_TITLE,
    get_texture_asset_name,
)
from save_system import SaveManager
from texture_utils import apply_nearest_filter, get_texture_resource
from world import World


CRASH_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crash.log")
app = None
game = None


def write_crash_log(exc):
    with open(CRASH_LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write("\n=== Minecraft3D Crash ===\n")
        log_file.write(traceback.format_exc())


def lerp_color(color_a, color_b, factor):
    return tuple(
        int(color_a[index] + (color_b[index] - color_a[index]) * factor)
        for index in range(3)
    )


def get_sky_color(time_of_day):
    day = (135, 206, 235)
    sunset = (253, 134, 83)
    night = (18, 28, 64)
    dawn = (220, 166, 120)

    if 6 <= time_of_day < 17:
        return day
    if 17 <= time_of_day < 19:
        return lerp_color(day, sunset, (time_of_day - 17) / 2.0)
    if 19 <= time_of_day < 21:
        return lerp_color(sunset, night, (time_of_day - 19) / 2.0)
    if 21 <= time_of_day or time_of_day < 5:
        return night
    return lerp_color(dawn, day, (time_of_day - 5) / 1.0)


def get_item_ui_color(block_type):
    color_map = {
        "meat_fish": color.rgba(245/255.0, 170/255.0, 165/255.0, 1.0),
    }
    return color_map.get(block_type, color.white)


def get_durability_bar_color(remaining_ratio):
    if remaining_ratio > 0.6:
        return color.rgba(0.15, 0.82, 0.16, 1.0)
    if remaining_ratio > 0.3:
        return color.rgba(0.85, 0.82, 0.2, 1.0)
    return color.rgba(0.9, 0.24, 0.2, 1.0)


class PlayerController(Entity):
    def __init__(self, start_position, world_ref):
        super().__init__(
            position=start_position,
            model=None, # 确保第一人称下自身完全不可见，也没有奇怪的网格
            collider=None, # 我们自己做了射线检测，不需要内置碰撞体
        )
        self.world = world_ref
        self.height = 1.8
        self.speed = 5.5
        self.jump_speed = 6.5
        self.gravity = 20.0
        self.vertical_velocity = 0.0
        self.grounded = False
        self.radius = 0.32
        self.step_height = 1.05
        self.look_sensitivity_x = 120
        self.look_sensitivity_y = 90
        self.pitch = -10
        self.rotation_y = 140

        self.camera_pivot = Entity(parent=self, y=self.height)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (self.pitch, 0, 0)
        camera.fov = 90
        mouse.locked = False
        self.highest_y_during_fall = start_position[1]
        self.on_take_damage = None

    def _frame_dt(self):
        # Clamp oversized frame steps so a temporary hitch does not become a huge physics jump.
        return min(time.dt, 0.05)

    @property
    def forward_flat(self):
        direction = Vec3(self.forward.x, 0, self.forward.z)
        return direction.normalized() if direction.length() > 0 else Vec3(0, 0, 1)

    @property
    def right_flat(self):
        direction = Vec3(self.right.x, 0, self.right.z)
        return direction.normalized() if direction.length() > 0 else Vec3(1, 0, 0)

    def lock_mouse(self):
        mouse.locked = True

    def unlock_mouse(self):
        mouse.locked = False

    def _apply_look(self):
        if not mouse.locked:
            return
        self.rotation_y += mouse.velocity[0] * self.look_sensitivity_x
        self.pitch -= mouse.velocity[1] * self.look_sensitivity_y
        self.pitch = max(-85, min(85, self.pitch))
        self.camera_pivot.rotation_x = self.pitch

    def _block_at_point(self, x, y, z):
        bx = math.floor(x + 0.5)
        by = math.floor(y + 0.5)
        bz = math.floor(z + 0.5)
        position = (bx, by, bz)
        return self.world.get_block_type(position)

    def _is_solid_block(self, block_type):
        return block_type is not None and block_type not in {"water", "leaves"}

    def _is_in_water(self, position=None):
        position = position or self.position
        current_block = self._block_at_point(position.x, position.y + 0.1, position.z)
        head_block = self._block_at_point(position.x, position.y + self.height - 0.1, position.z)
        return current_block == "water" or head_block == "water"

    def _collides_lower_body(self, position):
        sample_heights = (0.1, 0.6)
        for dx in (-self.radius, self.radius):
            for dz in (-self.radius, self.radius):
                for dy in sample_heights:
                    block = self._block_at_point(position.x + dx, position.y + dy, position.z + dz)
                    if self._is_solid_block(block):
                        return True
        return False

    def _feet_inside_solid(self, position):
        sample_points = (
            (0.0, 0.0),
            (-self.radius * 0.55, 0.0),
            (self.radius * 0.55, 0.0),
            (0.0, -self.radius * 0.55),
            (0.0, self.radius * 0.55),
        )
        for dx, dz in sample_points:
            block = self._block_at_point(position.x + dx, position.y + 0.05, position.z + dz)
            if self._is_solid_block(block):
                return True
        return False

    def _resolve_embedded_position(self):
        if self._is_in_water(self.position):
            return False
        if not self._feet_inside_solid(self.position):
            return False

        terrain_surface_y = self.world.get_surface_height(round(self.x), round(self.z)) + 0.55
        self.position = Vec3(self.x, terrain_surface_y, self.z)
        self.vertical_velocity = 0.0
        self.grounded = True
        self.highest_y_during_fall = self.y
        return True

    def _collides_at(self, position):
        sample_heights = (0.1, self.height * 0.5, self.height - 0.1)
        for dx in (-self.radius, self.radius):
            for dz in (-self.radius, self.radius):
                for dy in sample_heights:
                    block = self._block_at_point(position.x + dx, position.y + dy, position.z + dz)
                    if self._is_solid_block(block):
                        return True
        return False

    def _support_height_at(self, position, max_drop=1.6):
        support_height = None
        steps = max(2, int(max_drop / 0.25) + 2)
        for dx in (-self.radius, self.radius):
            for dz in (-self.radius, self.radius):
                for step in range(steps):
                    sample_y = position.y - 0.05 - step * 0.25
                    bx = math.floor(position.x + dx + 0.5)
                    by = math.floor(sample_y + 0.5)
                    bz = math.floor(position.z + dz + 0.5)
                    block = self._block_at_point(position.x + dx, sample_y, position.z + dz)
                    if self._is_solid_block(block):
                        height = by + 0.5
                        if support_height is None or height > support_height:
                            support_height = height
                        break
        return support_height

    def _try_step_up(self, candidate):
        lifted = Vec3(candidate.x, self.y + self.step_height, candidate.z)
        if self._collides_at(lifted):
            return False

        support_height = self._support_height_at(lifted, max_drop=self.step_height + 0.4)
        if support_height is None:
            return False

        if 0.0 < support_height - self.y <= self.step_height + 0.05:
            self.position = Vec3(candidate.x, support_height, candidate.z)
            self.grounded = True
            self.vertical_velocity = 0.0
            self.highest_y_during_fall = self.y
            return True
        return False

    def _can_step_up(self):
        return self.grounded or self._is_in_water(self.position)

    def _move_axis(self, dx, dz):
        if dx == 0 and dz == 0:
            return

        candidate = Vec3(self.x + dx, self.y, self.z + dz)
        if not self._collides_at(candidate):
            self.position = candidate
            return

        if self._can_step_up() and self._try_step_up(candidate):
            return

    def _move_horizontal(self):
        dt = self._frame_dt()
        move_direction = (
            self.forward_flat * (held_keys["w"] - held_keys["s"])
            + self.right_flat * (held_keys["d"] - held_keys["a"])
        )
        if move_direction.length() == 0:
            return

        move_direction = move_direction.normalized()
        move_step = move_direction * self.speed * dt

        diagonal_candidate = Vec3(self.x + move_step.x, self.y, self.z + move_step.z)
        if not self._collides_at(diagonal_candidate):
            self.position = diagonal_candidate
            return

        if self._can_step_up() and self._try_step_up(diagonal_candidate):
            return

        self._move_axis(move_step.x, 0)
        self._move_axis(0, move_step.z)

    def _apply_vertical(self):
        dt = self._frame_dt()
        if self._resolve_embedded_position():
            return

        # 兜底：一旦掉到过低位置，立刻拉回当前列地表，避免穿过基岩层后继续下坠。
        if self.y < 0.2:
            surface_y = self.world.get_surface_height(round(self.x), round(self.z))
            self.y = surface_y + 0.55
            self.vertical_velocity = 0.0
            self.grounded = True
            self.highest_y_during_fall = self.y
            return
            
        if not self.grounded:
            if self.y > self.highest_y_during_fall:
                self.highest_y_during_fall = self.y

        self.grounded = False
        
        in_water = self._is_in_water(self.position)
        
        if in_water:
            # 在水中，按住空格上升，按住Shift下潜，否则缓慢下沉
            if held_keys["space"]:
                self.vertical_velocity = min(self.jump_speed * 0.8, self.vertical_velocity + self.gravity * dt * 0.5)
            elif held_keys["left shift"]:
                self.vertical_velocity = max(-self.jump_speed * 0.8, self.vertical_velocity - self.gravity * dt * 0.5)
            else:
                self.vertical_velocity = max(-2.0, self.vertical_velocity - self.gravity * dt * 0.1)
        else:
            self.vertical_velocity -= self.gravity * dt

        candidate = Vec3(self.x, self.y + self.vertical_velocity * dt, self.z)
        if self.vertical_velocity <= 0:
            support_height = self._support_height_at(candidate, max_drop=max(1.6, abs(self.vertical_velocity * dt) + 0.8))
            if support_height is not None and candidate.y <= support_height + 0.05:
                if not self.grounded:
                    fall_distance = self.highest_y_during_fall - support_height
                    if in_water:
                        fall_distance = 0
                    if fall_distance > 3.5 and self.on_take_damage:
                        damage = int(fall_distance - 3.0)
                        self.on_take_damage(damage)

                self.y = support_height
                self.vertical_velocity = 0.0
                self.grounded = True
                self.highest_y_during_fall = self.y
                return

        if self.vertical_velocity > 0 and self._collides_at(candidate):
            self.vertical_velocity = 0.0
            return

        self.y = candidate.y

    def jump(self):
        current_block = self.world.blocks.get((round(self.x), round(self.y), round(self.z)))
        head_block = self.world.blocks.get((round(self.x), round(self.y + 1), round(self.z)))
        in_water = current_block == "water" or head_block == "water"
        if self.grounded or in_water:
            self.vertical_velocity = self.jump_speed * (0.6 if in_water else 1.0)
            self.grounded = False
            self.highest_y_during_fall = self.y

    def update(self):
        self._apply_look()
        self._move_horizontal()
        self._apply_vertical()


class HotbarUI:
    def __init__(self, slot_count):
        self.slot_count = slot_count
        self.root = Entity(parent=camera.ui)
        self.slots = []
        self.icons = []
        self.key_labels = []
        self.count_labels = []
        self.durability_backdrops = []
        self.durability_bars = []
        self.selected_index = 0

        total_width = slot_count * 0.105
        start_x = -total_width / 2 + 0.05
        for index in range(slot_count):
            slot = Entity(
                parent=self.root,
                model="quad",
                color=color.rgba(30/255.0, 30/255.0, 30/255.0, 190/255.0),
                scale=(0.095, 0.095),
                position=(start_x + index * 0.105, -0.43, 0),
            )
            
            icon = Entity(
                parent=slot,
                model="quad",
                texture=None,
                color=color.white,
                scale=(0.6, 0.6),
                position=(0, 0.06, -0.1),
                enabled=False,
            )

            key_label = Text(
                parent=slot,
                text=f"{index + 1}",
                origin=(-0.5, 0.5),
                scale=0.45,
                color=color.rgba(0.85, 0.85, 0.85, 1.0),
                position=(-0.04, 0.035, -0.2),
            )

            count_label = Text(
                parent=slot,
                text="",
                origin=(-0.5, -0.5),
                scale=0.55,
                color=color.white,
                position=(-0.04, -0.038, -0.2),
            )
            durability_backdrop = Entity(
                parent=slot,
                model="quad",
                color=color.rgba(0.08, 0.08, 0.08, 0.95),
                scale=(0.82, 0.085),
                position=(0, -0.39, -0.16),
                enabled=False,
            )
            durability_bar = Entity(
                parent=durability_backdrop,
                model="quad",
                color=color.rgba(0.15, 0.82, 0.16, 1.0),
                scale=(1.0, 1.0),
                origin=(-0.5, 0),
                position=(-0.5, 0, -0.01),
                enabled=False,
            )
            self.slots.append(slot)
            self.icons.append(icon)
            self.key_labels.append(key_label)
            self.count_labels.append(count_label)
            self.durability_backdrops.append(durability_backdrop)
            self.durability_bars.append(durability_bar)

        self.set_selected(0)

    def update_slots(self, slot_items, inventory, tool_durability):
        for index in range(self.slot_count):
            item_type = slot_items[index] if index < len(slot_items) else None
            count = inventory.get(item_type, 0) if item_type else 0
            icon = self.icons[index]
            durability_backdrop = self.durability_backdrops[index]
            durability_bar = self.durability_bars[index]
            if item_type and count > 0:
                texture_name = get_texture_asset_name(item_type)
                icon.enabled = True
                icon.texture = get_texture_resource(texture_name)
                icon.color = get_item_ui_color(item_type)
                apply_nearest_filter(icon.texture)
                self.count_labels[index].text = str(count) if count > 1 else ""
                durability_values = tool_durability.get(item_type, []) if item_type in TOOL_DURABILITY else []
                if durability_values:
                    remaining_ratio = max(0.0, min(1.0, durability_values[0] / float(TOOL_DURABILITY[item_type])))
                    durability_backdrop.enabled = True
                    durability_bar.enabled = True
                    durability_bar.scale_x = max(0.04, remaining_ratio)
                    durability_bar.color = get_durability_bar_color(remaining_ratio)
                else:
                    durability_backdrop.enabled = False
                    durability_bar.enabled = False
            else:
                icon.enabled = False
                icon.texture = None
                self.count_labels[index].text = ""
                durability_backdrop.enabled = False
                durability_bar.enabled = False

    def set_selected(self, index):
        self.selected_index = index % self.slot_count
        for slot_index, slot in enumerate(self.slots):
            if slot_index == self.selected_index:
                slot.color = color.rgba(232/255.0, 196/255.0, 72/255.0, 220/255.0)
            else:
                slot.color = color.rgba(30/255.0, 30/255.0, 30/255.0, 190/255.0)


class InventoryUI:
    def __init__(self):
        self.root = Entity(parent=camera.ui, enabled=False)
        self.panel = Entity(
            parent=self.root,
            model="quad",
            color=color.rgba(18/255.0, 18/255.0, 18/255.0, 220/255.0),
            scale=(0.62, 0.42),
            position=(0, 0.04, 0),
        )
        self.title = Text(
            parent=self.panel,
            text="Backpack",
            origin=(0, 0),
            scale=1.0,
            color=color.white,
            position=(0, 0.16, -0.1),
        )
        self.empty_label = Text(
            parent=self.panel,
            text="empty",
            origin=(0, 0),
            scale=0.9,
            color=color.rgba(0.8, 0.8, 0.8, 1.0),
            position=(0, -0.01, -0.1),
        )
        self.slots = []
        self.icons = []
        self.count_labels = []
        self.durability_backdrops = []
        self.durability_bars = []

        columns = 9
        rows = 3
        slot_spacing_x = 0.06
        slot_spacing_y = 0.1
        start_x = -((columns - 1) * slot_spacing_x) / 2.0
        start_y = 0.08
        for row in range(rows):
            for column in range(columns):
                x = start_x + column * slot_spacing_x
                y = start_y - row * slot_spacing_y
                slot = Entity(
                    parent=self.panel,
                    model="quad",
                    color=color.rgba(42/255.0, 42/255.0, 42/255.0, 230/255.0),
                    scale=(0.052, 0.052),
                    position=(x, y, 0),
                )
                icon = Entity(
                    parent=slot,
                    model="quad",
                    texture=None,
                    color=color.white,
                    scale=(0.72, 0.72),
                    position=(0, 0, -0.1),
                    enabled=False,
                )
                count_label = Text(
                    parent=slot,
                    text="",
                    origin=(-0.5, -0.5),
                    scale=0.6,
                    color=color.white,
                    position=(-0.02, -0.024, -0.2),
                )
                durability_backdrop = Entity(
                    parent=slot,
                    model="quad",
                    color=color.rgba(0.08, 0.08, 0.08, 0.95),
                    scale=(0.82, 0.1),
                    position=(0, -0.39, -0.16),
                    enabled=False,
                )
                durability_bar = Entity(
                    parent=durability_backdrop,
                    model="quad",
                    color=color.rgba(0.15, 0.82, 0.16, 1.0),
                    scale=(1.0, 1.0),
                    origin=(-0.5, 0),
                    position=(-0.5, 0, -0.01),
                    enabled=False,
                )
                self.slots.append(slot)
                self.icons.append(icon)
                self.count_labels.append(count_label)
                self.durability_backdrops.append(durability_backdrop)
                self.durability_bars.append(durability_bar)

    def toggle(self):
        self.root.enabled = not self.root.enabled

    def update_inventory(self, inventory, tool_durability):
        items = [
            (item_type, count)
            for item_type, count in sorted(inventory.items())
            if count > 0
        ]

        for index, icon in enumerate(self.icons):
            durability_backdrop = self.durability_backdrops[index]
            durability_bar = self.durability_bars[index]
            if index < len(items):
                item_type, count = items[index]
                texture_name = get_texture_asset_name(item_type)
                icon.enabled = True
                icon.texture = get_texture_resource(texture_name)
                icon.color = get_item_ui_color(item_type)
                apply_nearest_filter(icon.texture)
                self.count_labels[index].text = str(count) if count > 1 else ""
                durability_values = tool_durability.get(item_type, []) if item_type in TOOL_DURABILITY else []
                if durability_values:
                    remaining_ratio = max(0.0, min(1.0, durability_values[0] / float(TOOL_DURABILITY[item_type])))
                    durability_backdrop.enabled = True
                    durability_bar.enabled = True
                    durability_bar.scale_x = max(0.04, remaining_ratio)
                    durability_bar.color = get_durability_bar_color(remaining_ratio)
                else:
                    durability_backdrop.enabled = False
                    durability_bar.enabled = False
            else:
                icon.enabled = False
                icon.texture = None
                self.count_labels[index].text = ""
                durability_backdrop.enabled = False
                durability_bar.enabled = False

        self.empty_label.enabled = len(items) == 0


class Minecraft3DGame:
    def _clear_spawn_space(self, spawn_position):
        x, y, z = spawn_position
        occupied_blocks = set()
        for dy in (0.1, 0.9, 1.7, 2.3):
            occupied_blocks.add((
                math.floor(x + 0.5),
                math.floor(y + dy + 0.5),
                math.floor(z + 0.5),
            ))

        for block_pos in occupied_blocks:
            block_type = self.world.get_generated_block_type(block_pos)
            if block_type is None or block_type == "bedrock":
                continue
            self.world.remove_block(block_pos)

    def _find_spawn_position(self):
        center_x = int(CHUNK_SIZE / 2)
        center_z = int(CHUNK_SIZE / 2)
        best_ground_spawn = None
        best_ground_score = None

        for dz in range(-24, 25):
            for dx in range(-24, 25):
                world_x = center_x + dx
                world_z = center_z + dz
                surface_y = self.world.get_surface_height(world_x, world_z)
                if surface_y <= 4:
                    continue

                if self.world.get_generated_block_type((world_x, surface_y + 1, world_z)) is not None:
                    continue
                if self.world.get_generated_block_type((world_x, surface_y + 2, world_z)) is not None:
                    continue
                if self.world.get_tree_at(world_x, world_z):
                    continue

                neighbor_heights = [
                    self.world.get_surface_height(world_x + 1, world_z),
                    self.world.get_surface_height(world_x - 1, world_z),
                    self.world.get_surface_height(world_x, world_z + 1),
                    self.world.get_surface_height(world_x, world_z - 1),
                ]
                slope = max(abs(surface_y - height) for height in neighbor_heights)
                if slope > 1:
                    continue

                distance_penalty = abs(dx) + abs(dz)
                ground_score = slope * 100 + distance_penalty
                if best_ground_score is None or ground_score < best_ground_score:
                    best_ground_score = ground_score
                    best_ground_spawn = (world_x, surface_y + 0.55, world_z)

        return best_ground_spawn or (center_x, 18.0, center_z)

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_dir = os.path.join(self.base_dir, "audio")
        self.background_music = None
        self.music_track_name = "missing"
        self.music_enabled = True
        self.save_manager = SaveManager(os.path.join(self.base_dir, SAVE_FILE))
        self.world = World(self.save_manager)
        self.debug_markers = []
        self.spawn_position = self._find_spawn_position()
        self.world.update_loaded_chunks(self.spawn_position)
        self._clear_spawn_space(self.spawn_position)
        self.player = PlayerController(self.spawn_position, self.world)
        self.player.grounded = True
        self.player.highest_y_during_fall = self.player.y

        self.sun = DirectionalLight()
        self.sun.rotation = (45, -30, 0)

        self.crosshair = Text(text="+", parent=camera.ui, origin=(0, 0), scale=2.0, color=color.white)
        self.highlight = Entity(
            parent=scene,
            model="cube",
            color=color.rgba(1.0, 1.0, 1.0, 42/255.0),
            scale=1.01,
            enabled=False,
            collider=None, # 防止自身阻挡射线
        )

        self.help_text = Text(
            parent=camera.ui,
            x=-0.86,
            y=0.47,
            scale=0.9,
            text=(
                "Left click: lock mouse\n"
                "Esc: unlock mouse\n"
                "WASD move\n"
                "Space jump\n"
                "Left click mine\n"
                "Right click place/eat/craft\n"
                "Q drop item\n"
                "F craft furnace\n"
                "M toggle music\n"
                "E backpack\n"
                "1-9 or mouse wheel switch slot"
            ),
        )
        self.status_text = Text(parent=camera.ui, x=-0.86, y=0.31, scale=0.95, text="")

        self.inventory = self.save_manager.get_inventory()
        self.tool_durability = self.save_manager.get_tool_durability()
        self.hotbar_slots = self.save_manager.get_hotbar_slots()
        self._sanitize_inventory_state()
        self._normalize_tool_durability_state()
        self.hotbar = HotbarUI(HOTBAR_SIZE)
        self.inventory_ui = InventoryUI()
        self.selected_hotbar_index = 0
        self.time_of_day = 8.0
        self.targeted_block = None
        self.targeted_normal = None
        self.targeted_animal = None
        self.position_save_timer = 0.0
        self._sync_hotbar_slots()

        self.health = self.save_manager.get_health()
        self.health_text = Text(parent=camera.ui, x=0, y=-0.36, scale=1.3, origin=(0, 0), color=color.rgba(1, 0.2, 0.2, 1))
        self._update_health_ui()

        self.player.on_take_damage = self.take_damage

        mouse.locked = False
        window.borderless = False
        window.title = WINDOW_TITLE

        self._setup_background_music()
        self._apply_selected_block()
        self._apply_lighting()
        atexit.register(self.save_and_flush)

    def _sanitize_inventory_state(self):
        inventory_changed = False
        for item_type in NON_INVENTORY_BLOCKS:
            if self.inventory.pop(item_type, None) is not None:
                inventory_changed = True

        normalized_slots = []
        for item_type in self.hotbar_slots[:HOTBAR_SIZE]:
            if item_type in NON_INVENTORY_BLOCKS:
                normalized_slots.append(None)
                inventory_changed = True
            else:
                normalized_slots.append(item_type)

        while len(normalized_slots) < HOTBAR_SIZE:
            normalized_slots.append(None)

        self.hotbar_slots = normalized_slots
        if inventory_changed:
            self.save_manager.set_hotbar_slots(self.hotbar_slots)
            self.save_manager.save()

    def _normalize_tool_durability_state(self):
        state_changed = False
        for tool_type, max_durability in TOOL_DURABILITY.items():
            item_count = max(0, int(self.inventory.get(tool_type, 0)))
            raw_values = self.tool_durability.get(tool_type, [])
            if not isinstance(raw_values, list):
                raw_values = []
                state_changed = True

            normalized_values = []
            for value in raw_values[:item_count]:
                try:
                    current_value = int(value)
                except (TypeError, ValueError):
                    current_value = max_durability
                    state_changed = True
                current_value = max(1, min(max_durability, current_value))
                normalized_values.append(current_value)

            if len(normalized_values) < item_count:
                normalized_values.extend([max_durability] * (item_count - len(normalized_values)))
                state_changed = True
            elif len(raw_values) > item_count:
                state_changed = True

            if item_count > 0:
                if self.tool_durability.get(tool_type) != normalized_values:
                    self.tool_durability[tool_type] = normalized_values
                    state_changed = True
            elif tool_type in self.tool_durability:
                self.tool_durability.pop(tool_type, None)
                state_changed = True

        for tool_type in list(self.tool_durability.keys()):
            if tool_type not in TOOL_DURABILITY:
                self.tool_durability.pop(tool_type, None)
                state_changed = True

        self.save_manager.set_tool_durability(self.tool_durability)
        return state_changed

    def _update_health_ui(self):
        full_hearts = self.health // 2
        half_heart = self.health % 2
        empty_hearts = 10 - full_hearts - half_heart
        self.health_text.text = "<red>" + "♥" * full_hearts + "♡" * half_heart + "<gray>" + "♡" * empty_hearts

    def _find_background_music_file(self):
        if not os.path.isdir(self.audio_dir):
            return None

        preferred_files = (
            "MC.wav",
            "mc.wav",
            "Sweden.ogg",
            "sweden.ogg",
            "bgm.ogg",
            "bgm.mp3",
            "bgm.wav",
            "backup_bgm.wav",
        )
        for file_name in preferred_files:
            file_path = os.path.join(self.audio_dir, file_name)
            if os.path.isfile(file_path):
                return file_path

        for file_name in sorted(os.listdir(self.audio_dir)):
            if file_name.lower().endswith((".ogg", ".mp3", ".wav")):
                return os.path.join(self.audio_dir, file_name)
        return None

    def _setup_background_music(self):
        music_path = self._find_background_music_file()
        if music_path is None:
            self.background_music = None
            self.music_track_name = "missing"
            return

        try:
            self.background_music = Audio(
                sound_file_name=Path(music_path),
                autoplay=False,
                loop=True,
                volume=0.9,
                group="music",
            )
            self.music_track_name = os.path.basename(music_path)
            if self.music_enabled and self.background_music.clip is not None:
                self.background_music.play()
            elif self.background_music.clip is None:
                self.music_track_name = "load failed"
        except Exception:
            self.background_music = None
            self.music_track_name = "error"
            write_crash_log(RuntimeError(f"Failed to load music: {music_path}"))

    def _get_music_status_text(self):
        if self.background_music is None:
            if self.music_track_name == "error":
                return "load failed"
            return "missing"
        if self.background_music.clip is None:
            return "load failed"
        return f"{'on' if self.music_enabled else 'off'} ({self.music_track_name})"

    def _toggle_music(self):
        if self.background_music is None or self.background_music.clip is None:
            return False

        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.background_music.play()
        else:
            self.background_music.stop()
        return True

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 20
            # Respawn
            self.spawn_position = self._find_spawn_position()
            self.world.update_loaded_chunks(self.spawn_position)
            self._clear_spawn_space(self.spawn_position)
            self.player.position = Vec3(*self.spawn_position)
            self.player.vertical_velocity = 0.0
            self.player.grounded = True
            self.player.highest_y_during_fall = self.player.y
            
        self.save_manager.set_health(self.health)
        self._update_health_ui()
        self.save_manager.save()

    def _apply_selected_block(self):
        self.hotbar.set_selected(self.selected_hotbar_index)

    def _sync_hotbar_slots(self):
        self._normalize_tool_durability_state()
        normalized_slots = []
        used_items = set()
        for item_type in list(self.hotbar_slots[:HOTBAR_SIZE]):
            count = self.inventory.get(item_type, 0) if item_type else 0
            if not item_type or count <= 0 or item_type in used_items:
                normalized_slots.append(None)
                continue
            normalized_slots.append(item_type)
            used_items.add(item_type)

        while len(normalized_slots) < HOTBAR_SIZE:
            normalized_slots.append(None)

        self.hotbar_slots = normalized_slots

        for item_type, count in list(self.inventory.items()):
            if count <= 0:
                self.inventory.pop(item_type, None)
                continue
            if item_type in used_items:
                continue
            for slot_index in range(HOTBAR_SIZE):
                if self.hotbar_slots[slot_index] is None:
                    self.hotbar_slots[slot_index] = item_type
                    used_items.add(item_type)
                    break

        self.save_manager.set_hotbar_slots(self.hotbar_slots)
        self.save_manager.set_tool_durability(self.tool_durability)
        self.hotbar.update_slots(self.hotbar_slots, self.inventory, self.tool_durability)
        self.inventory_ui.update_inventory(self.inventory, self.tool_durability)

    def _get_selected_item(self):
        if not (0 <= self.selected_hotbar_index < len(self.hotbar_slots)):
            return None
        item_type = self.hotbar_slots[self.selected_hotbar_index]
        if item_type and self.inventory.get(item_type, 0) > 0:
            return item_type
        return None

    def _consume_inventory_item(self, item_type, amount=1):
        current_count = self.inventory.get(item_type, 0)
        if current_count < amount:
            return False
        if item_type in TOOL_DURABILITY:
            durability_values = self.tool_durability.get(item_type, [])
            self.tool_durability[item_type] = durability_values[amount:]
            if not self.tool_durability[item_type]:
                self.tool_durability.pop(item_type, None)
        remaining = current_count - amount
        if remaining > 0:
            self.inventory[item_type] = remaining
        else:
            self.inventory.pop(item_type, None)
        self._sync_hotbar_slots()
        return True

    def _add_inventory_item(self, item_type, amount=1, durability_values=None):
        if amount <= 0:
            return False
        if item_type in TOOL_DURABILITY:
            if durability_values is None:
                values_to_add = [TOOL_DURABILITY[item_type]] * amount
            else:
                values_to_add = [
                    max(1, min(TOOL_DURABILITY[item_type], int(value)))
                    for value in durability_values[:amount]
                ]
                if len(values_to_add) < amount:
                    values_to_add.extend([TOOL_DURABILITY[item_type]] * (amount - len(values_to_add)))
            self.tool_durability.setdefault(item_type, []).extend(values_to_add)
        self.inventory[item_type] = self.inventory.get(item_type, 0) + amount
        self._sync_hotbar_slots()
        return True

    def _damage_selected_tool(self, amount=1):
        selected_item = self._get_selected_item()
        if selected_item not in TOOL_DURABILITY:
            return False

        durability_values = self.tool_durability.get(selected_item, [])
        if not durability_values:
            return False

        durability_values[0] -= amount
        if durability_values[0] > 0:
            self.tool_durability[selected_item] = durability_values
        else:
            durability_values.pop(0)
            remaining_count = self.inventory.get(selected_item, 0) - 1
            if remaining_count > 0:
                self.inventory[selected_item] = remaining_count
                self.tool_durability[selected_item] = durability_values
            else:
                self.inventory.pop(selected_item, None)
                self.tool_durability.pop(selected_item, None)
        self._sync_hotbar_slots()
        return True

    def _has_recipe_items(self, recipe_items):
        for item_type, amount in recipe_items.items():
            if self.inventory.get(item_type, 0) < amount:
                return False
        return True

    def _craft_selected_item_by_right_click(self):
        selected_item = self._get_selected_item()
        recipe = RIGHT_CLICK_CRAFTING_RECIPES.get(selected_item)
        if recipe is None:
            return False

        # `iron_ingot` is not placeable, so always prioritize crafting it into an axe.
        # `log` / `wood` keep block placement when the player is pointing at a block,
        # and craft when right-clicking into the air.
        if selected_item in PLACEABLE_ITEMS and self.targeted_block is not None:
            return False

        consumes = recipe.get("consumes", {})
        produces = recipe.get("produces", {})
        if not self._has_recipe_items(consumes):
            return False

        for item_type, amount in consumes.items():
            if not self._consume_inventory_item(item_type, amount):
                return False
        for item_type, amount in produces.items():
            self._add_inventory_item(item_type, amount)

        self.save_manager.save()
        return True

    def _craft_furnace_in_front(self):
        recipe = CRAFTABLE_BLOCK_RECIPES.get("furnace", {})
        stone_cost = recipe.get("stone", 0)
        if stone_cost <= 0 or self.inventory.get("stone", 0) < stone_cost:
            return False

        place_position = self._get_place_position()
        if place_position is None or self._player_would_overlap(place_position):
            return False
        if not self.world.place_block(place_position, "furnace"):
            return False

        self._consume_inventory_item("stone", stone_cost)
        self.save_manager.save()
        return True

    def _smelt_selected_item(self):
        if self.targeted_block is None:
            return False
        if self.world.get_block_type(self.targeted_block) != "furnace":
            return False

        selected_item = self._get_selected_item()
        product = SMELTING_RECIPES.get(selected_item)
        if product is None:
            return False
        fuel_item, fuel_cost = next(iter(FURNACE_FUEL_ITEMS.items()))
        if self.inventory.get(fuel_item, 0) < fuel_cost:
            return False
        if not self._consume_inventory_item(selected_item, 1):
            return False
        if not self._consume_inventory_item(fuel_item, fuel_cost):
            self._add_inventory_item(selected_item, 1)
            return False

        self._add_inventory_item(product, 1)
        self.save_manager.save()
        return True

    def _drop_selected_item(self):
        item_type = self._get_selected_item()
        if item_type is None:
            return False
        drop_count = self.inventory.get(item_type, 0)
        if drop_count <= 0:
            return False
        durability_values = None
        if item_type in TOOL_DURABILITY:
            durability_values = list(self.tool_durability.get(item_type, [])[:drop_count])
        if not self._consume_inventory_item(item_type, drop_count):
            return False

        from entity import ItemDrop

        drop_origin = camera.world_position + camera.forward * 1.6 + Vec3(0, -0.15, 0)
        launch_direction = camera.forward + Vec3(0, 0.12, 0)
        ItemDrop(
            drop_origin,
            item_type,
            launch_direction=launch_direction,
            lifetime=5.0,
            quantity=drop_count,
            pickup_delay=1.0,
            launch_speed=4.8,
            durability_values=durability_values,
        )
        self.save_manager.save()
        return True

    def _get_attack_damage(self):
        selected_item = self._get_selected_item()
        damage_by_item = {
            "wood_axe": 2,
            "stone_axe": 3,
            "copper_axe": 3,
            "iron_axe": 4,
        }
        return damage_by_item.get(selected_item, 1)

    def _eat_selected_item(self):
        item_type = self._get_selected_item()
        if item_type not in FOOD_HEAL_AMOUNT:
            return False
        if self.health >= 20:
            return False
        if not self._consume_inventory_item(item_type, 1):
            return False
        self.health = min(20, self.health + FOOD_HEAL_AMOUNT[item_type])
        self.save_manager.set_health(self.health)
        self._update_health_ui()
        self.save_manager.save()
        return True

    def _apply_lighting(self):
        sky_rgb = get_sky_color(self.time_of_day)
        window.color = color.rgba(sky_rgb[0]/255.0, sky_rgb[1]/255.0, sky_rgb[2]/255.0, 1.0)
        sc = lerp_color((170, 170, 190), (255, 244, 214), 0.5)
        self.sun.color = color.rgba(sc[0]/255.0, sc[1]/255.0, sc[2]/255.0, 1.0)
        self.sun.rotation_x = (self.time_of_day / 24.0) * 360.0 - 90.0
        ambient_strength = 18 if sky_rgb[2] < 100 else 54
        scene.ambient_color = color.rgba(ambient_strength/255.0, ambient_strength/255.0, (ambient_strength + 10)/255.0, 1.0)

    def _world_to_block_position(self, world_point):
        return (
            math.floor(world_point.x + 0.5),
            math.floor(world_point.y + 0.5),
            math.floor(world_point.z + 0.5),
        )

    def _resolve_target_block(self, hit_info):
        # 从相机射线继续往命中后的方块内部采样，比只沿面法线偏移更稳，
        # 尤其在侧面边角位置时不会总是串到顶部那一层。
        for depth in (0.02, 0.08, 0.16, 0.28, 0.4):
            hit_point = hit_info.world_point + camera.forward * depth
            block_pos = self._world_to_block_position(hit_point)
            if self.world.get_block_type(block_pos) is not None:
                return block_pos

        # 兜底：如果极少数情况下射线方向采样没命中，再退回到沿法线向内采样。
        for depth in (0.02, 0.08, 0.16):
            hit_point = hit_info.world_point - hit_info.world_normal * depth
            block_pos = self._world_to_block_position(hit_point)
            if self.world.get_block_type(block_pos) is not None:
                return block_pos
        return None

    def _update_target_block(self):
        # 忽略玩家自己、高亮框，但不再忽略动物，因为我们要能打动物
        ignore_list = [self.player, self.highlight]
        from entity import ItemDrop
        ignore_list.extend(ItemDrop._all_drops)
        
        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=INTERACTION_DISTANCE,
            ignore=ignore_list,
        )

        if hit_info.hit:
            # 检查是否击中了动物
            from entity import Animal
            if isinstance(hit_info.entity, Animal):
                self.targeted_animal = hit_info.entity
                self.targeted_block = None
                self.targeted_normal = None
                self.highlight.enabled = False
                return

            self.targeted_animal = None
            
            block_pos = self._resolve_target_block(hit_info)
            if block_pos is not None:
                self.targeted_block = block_pos
                self.targeted_normal = hit_info.world_normal
                self.highlight.enabled = True
                self.highlight.position = block_pos
                return

        self.targeted_block = None
        self.targeted_normal = None
        self.targeted_animal = None
        self.highlight.enabled = False

    def _save_player_position_if_needed(self, force=False):
        self.position_save_timer += time.dt
        if not force and self.position_save_timer < 0.8:
            return
        self.position_save_timer = 0.0
        self.save_manager.set_player_position(tuple(self.player.position))
        self.save_manager.save()

    def save_and_flush(self):
        self.save_manager.set_player_position(tuple(self.player.position))
        self.save_manager.save()

    def _get_place_position(self):
        if self.targeted_block is None or self.targeted_normal is None:
            return None

        tx, ty, tz = self.targeted_block
        normal = self.targeted_normal
        return (
            int(round(tx + normal.x)),
            int(round(ty + normal.y)),
            int(round(tz + normal.z)),
        )

    def _get_jump_place_position(self):
        return (
            math.floor(self.player.x + 0.5),
            math.floor(self.player.y - 0.5),
            math.floor(self.player.z + 0.5),
        )

    def _player_would_overlap(self, position):
        px, py, pz = self.player.position
        return (
            abs(px - position[0]) < 0.8
            and abs((py - 0.9) - position[1]) < 1.6
            and abs(pz - position[2]) < 0.8
        )

    def _check_item_pickup(self):
        from entity import ItemDrop
        from ursina import destroy
        
        px, py, pz = self.player.position
        to_remove = []
        for drop in ItemDrop._all_drops:
            drop.update()
            if drop.expired:
                to_remove.append(drop)
                continue
            if not drop.can_be_picked_up():
                continue
            # Simple distance check for pickup
            dx = drop.x - px
            dy = drop.y - (py - 0.5) # Check near feet
            dz = drop.z - pz
            if dx*dx + dy*dy + dz*dz < 3.0: # Pickup radius squared
                self._add_inventory_item(drop.item_type, drop.quantity, durability_values=drop.durability_values)
                self.save_manager.save()
                to_remove.append(drop)
                
        for drop in to_remove:
            ItemDrop._all_drops.remove(drop)
            destroy(drop)

    def update(self):
        self.world.update_loaded_chunks(tuple(self.player.position))
        self.world.update_animals()
        self._update_target_block()
        self._check_item_pickup()

        self.time_of_day = (self.time_of_day + time.dt * 0.35) % 24.0
        self._apply_lighting()
        self._save_player_position_if_needed()

        selected_name = self._get_selected_item() or "empty"
        chunk_x, chunk_z = self.world.get_chunk_coordinates(tuple(self.player.position))
        self.status_text.text = (
            f"Time: {self.time_of_day:05.2f}\n"
            f"Chunk: {chunk_x}, {chunk_z}\n"
            f"Selected: {selected_name}\n"
            f"Music: {self._get_music_status_text()}"
        )

    def input(self, key):
        if key == "left mouse down":
            if not mouse.locked:
                self.player.lock_mouse()
                return

        if key == "space":
            self.player.jump()
            return

        if key == "scroll up":
            self.selected_hotbar_index = (self.selected_hotbar_index + 1) % HOTBAR_SIZE
            self._apply_selected_block()
            return

        if key == "scroll down":
            self.selected_hotbar_index = (self.selected_hotbar_index - 1) % HOTBAR_SIZE
            self._apply_selected_block()
            return

        if key in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            idx = int(key) - 1
            if idx < HOTBAR_SIZE:
                self.selected_hotbar_index = idx
                self._apply_selected_block()
            return

        if key == "e":
            self.inventory_ui.toggle()
            return

        if key == "f":
            self._craft_furnace_in_front()
            return

        if key == "m":
            self._toggle_music()
            return

        if key == "q":
            self._drop_selected_item()
            return

        if key == "left mouse down":
            if self.targeted_animal is not None:
                # 攻击动物
                self.targeted_animal.take_damage(
                    self._get_attack_damage(),
                    scare_direction=self.player.forward_flat,
                )
                return
                
            if self.targeted_block is not None:
                from entity import ItemDrop
                mined_block_type = self.world.get_block_type(self.targeted_block)
                if mined_block_type and mined_block_type not in NON_MINEABLE_BLOCKS:
                    if self.world.remove_block(self.targeted_block):
                        self._damage_selected_tool(1)
                        drop_item_type = BLOCK_DROP_ITEMS.get(mined_block_type, mined_block_type)
                        launch_direction = Vec3(0, 0.6, 0)
                        if self.targeted_normal is not None:
                            launch_direction += Vec3(
                                self.targeted_normal.x,
                                max(0.0, self.targeted_normal.y),
                                self.targeted_normal.z,
                            )
                        ItemDrop(Vec3(*self.targeted_block), drop_item_type, launch_direction=launch_direction)
                return

        if key == "right mouse down":
            selected_item = self._get_selected_item()
            if selected_item is None:
                return
            if selected_item in FOOD_HEAL_AMOUNT:
                self._eat_selected_item()
                return
            if self._craft_selected_item_by_right_click():
                return
            if self._smelt_selected_item():
                return
            if selected_item not in PLACEABLE_ITEMS:
                return
            if held_keys["space"]:
                place_position = self._get_jump_place_position()
            else:
                place_position = self._get_place_position()
                if place_position is None or self._player_would_overlap(place_position):
                    return
            if self.inventory.get(selected_item, 0) > 0:
                if self.world.place_block(place_position, selected_item):
                    self._consume_inventory_item(selected_item, 1)
                    self.save_manager.save()
            return

        if key == "escape":
            self.player.unlock_mouse()


def update():
    if game is not None:
        game.update()


def input(key):
    if game is not None:
        game.input(key)


def main():
    global app, game
    app = Ursina()
    game = Minecraft3DGame()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_crash_log(exc)
        raise
