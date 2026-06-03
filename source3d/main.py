import atexit
import math
import os

from ursina import (
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

from constants import CHUNK_SIZE, HOTBAR_BLOCKS, INTERACTION_DISTANCE, SAVE_FILE, WINDOW_TITLE
from save_system import SaveManager
from world import World


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
        return self.world.blocks.get((bx, by, bz))

    def _is_solid_block(self, block_type):
        return block_type is not None and block_type not in {"water", "leaves"}

    def _collides_lower_body(self, position):
        sample_heights = (0.1, 0.6)
        for dx in (-self.radius, self.radius):
            for dz in (-self.radius, self.radius):
                for dy in sample_heights:
                    block = self._block_at_point(position.x + dx, position.y + dy, position.z + dz)
                    if self._is_solid_block(block):
                        return True
        return False

    def _resolve_embedded_position(self):
        if not self._collides_lower_body(self.position):
            return False

        terrain_surface_y = self.world.get_surface_height(round(self.x), round(self.z)) + 0.55
        if self.y < terrain_surface_y:
            self.position = Vec3(self.x, terrain_surface_y, self.z)
            self.vertical_velocity = 0.0
            self.grounded = True
            self.highest_y_during_fall = self.y
            return True

        for step in range(1, 9):
            candidate = Vec3(self.x, self.y + step * 0.5, self.z)
            if not self._collides_lower_body(candidate):
                self.position = candidate
                self.vertical_velocity = 0.0
                self.grounded = True
                self.highest_y_during_fall = self.y
                return True
        return False

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
                    block = self._block_at_point(position.x + dx, sample_y, position.z + dz)
                    if self._is_solid_block(block):
                        height = round(sample_y) + 0.5
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

    def _move_axis(self, dx, dz):
        if dx == 0 and dz == 0:
            return

        candidate = Vec3(self.x + dx, self.y, self.z + dz)
        if not self._collides_at(candidate):
            self.position = candidate
            return

        if self.grounded and self._try_step_up(candidate):
            return

    def _move_horizontal(self):
        move_direction = (
            self.forward_flat * (held_keys["w"] - held_keys["s"])
            + self.right_flat * (held_keys["d"] - held_keys["a"])
        )
        if move_direction.length() == 0:
            return

        move_direction = move_direction.normalized()
        move_step = move_direction * self.speed * time.dt
        self._move_axis(move_step.x, 0)
        self._move_axis(0, move_step.z)

    def _apply_vertical(self):
        if self._resolve_embedded_position():
            return

        # 兜底：如果玩家掉出世界，直接拉回地表
        if self.y < -10:
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
        
        current_block = self.world.blocks.get((round(self.x), round(self.y), round(self.z)))
        head_block = self.world.blocks.get((round(self.x), round(self.y + 1), round(self.z)))
        in_water = current_block == "water" or head_block == "water"
        
        if in_water:
            # 在水中，按住空格上升，按住Shift下潜，否则缓慢下沉
            if held_keys["space"]:
                self.vertical_velocity = min(self.jump_speed * 0.8, self.vertical_velocity + self.gravity * time.dt * 0.5)
            elif held_keys["left shift"]:
                self.vertical_velocity = max(-self.jump_speed * 0.8, self.vertical_velocity - self.gravity * time.dt * 0.5)
            else:
                self.vertical_velocity = max(-2.0, self.vertical_velocity - self.gravity * time.dt * 0.1)
        else:
            self.vertical_velocity -= self.gravity * time.dt

        candidate = Vec3(self.x, self.y + self.vertical_velocity * time.dt, self.z)
        if self.vertical_velocity <= 0:
            support_height = self._support_height_at(candidate, max_drop=max(1.6, abs(self.vertical_velocity * time.dt) + 0.8))
            if support_height is not None and candidate.y <= support_height + 0.05:
                if not self.grounded:
                    fall_distance = self.highest_y_during_fall - support_height
                    if current_block == "water" or head_block == "water":
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
    def __init__(self, block_types):
        self.block_types = block_types
        self.root = Entity(parent=camera.ui)
        self.slots = []
        self.labels = []
        self.selected_index = 0

        total_width = len(block_types) * 0.105
        start_x = -total_width / 2 + 0.05
        for index, block_type in enumerate(block_types):
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
                texture=f"image/{block_type}.png",
                scale=(0.6, 0.6),
                position=(0, 0.1, -0.1),
            )
            icon.texture.filtering = None
            
            label = Text(
                parent=slot,
                text=f"{index + 1}\n0",
                origin=(0, 0),
                scale=0.6,
                color=color.white,
                y=-0.3,
            )
            self.slots.append(slot)
            self.labels.append(label)

        self.set_selected(0)

    def update_counts(self, inventory):
        for index, block_type in enumerate(self.block_types):
            count = inventory.get(block_type, 0)
            self.labels[index].text = f"{index + 1}\n{count}"

    def set_selected(self, index):
        self.selected_index = index % len(self.block_types)
        for slot_index, slot in enumerate(self.slots):
            if slot_index == self.selected_index:
                slot.color = color.rgba(232/255.0, 196/255.0, 72/255.0, 220/255.0)
            else:
                slot.color = color.rgba(30/255.0, 30/255.0, 30/255.0, 190/255.0)


class Minecraft3DGame:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_manager = SaveManager(os.path.join(self.base_dir, SAVE_FILE))
        self.world = World(self.save_manager)
        self.debug_markers = []

        saved_x, saved_y, saved_z = self.save_manager.get_player_position()
        default_spawn_x = CHUNK_SIZE / 2
        default_spawn_z = CHUNK_SIZE / 2
        
        # 强制修正玩家高度，防止读取到掉出世界的错误存档
        surface_height = self.world.get_surface_height(round(saved_x), round(saved_z))
        if saved_y < 0 or saved_y > 100:
            saved_y = surface_height + 2.0
            saved_x = default_spawn_x
            saved_z = default_spawn_z
            
        self.world.update_loaded_chunks((saved_x, saved_y, saved_z))

        spawn_height = self.world.get_surface_height(round(saved_x), round(saved_z)) + 2.2
        self.player = PlayerController((saved_x, max(saved_y, spawn_height), saved_z), self.world)

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
                "Right click place\n"
                "1-5 or mouse wheel switch block"
            ),
        )
        self.status_text = Text(parent=camera.ui, x=-0.86, y=0.31, scale=0.95, text="")

        self.inventory = self.save_manager.get_inventory()
        self.hotbar = HotbarUI(HOTBAR_BLOCKS)
        self.hotbar.update_counts(self.inventory)
        self.selected_hotbar_index = 0
        self.time_of_day = 8.0
        self.targeted_block = None
        self.targeted_normal = None
        self.targeted_animal = None
        self.position_save_timer = 0.0

        self.health = self.save_manager.get_health()
        self.health_text = Text(parent=camera.ui, x=0, y=-0.36, scale=1.3, origin=(0, 0), color=color.rgba(1, 0.2, 0.2, 1))
        self._update_health_ui()

        self.player.on_take_damage = self.take_damage

        mouse.locked = False
        window.borderless = False
        window.title = WINDOW_TITLE

        self._apply_selected_block()
        self._apply_lighting()
        atexit.register(self.save_and_flush)

    def _update_health_ui(self):
        full_hearts = self.health // 2
        half_heart = self.health % 2
        empty_hearts = 10 - full_hearts - half_heart
        self.health_text.text = "<red>" + "♥" * full_hearts + "♡" * half_heart + "<gray>" + "♡" * empty_hearts

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 20
            # Respawn
            self.player.y = self.world.get_surface_height(round(self.player.x), round(self.player.z)) + 2.0
            self.player.vertical_velocity = 0.0
            self.player.highest_y_during_fall = self.player.y
            
        self.save_manager.set_health(self.health)
        self._update_health_ui()
        self.save_manager.save()

    def _apply_selected_block(self):
        self.hotbar.set_selected(self.selected_hotbar_index)

    def _apply_lighting(self):
        sky_rgb = get_sky_color(self.time_of_day)
        window.color = color.rgba(sky_rgb[0]/255.0, sky_rgb[1]/255.0, sky_rgb[2]/255.0, 1.0)
        sc = lerp_color((170, 170, 190), (255, 244, 214), 0.5)
        self.sun.color = color.rgba(sc[0]/255.0, sc[1]/255.0, sc[2]/255.0, 1.0)
        self.sun.rotation_x = (self.time_of_day / 24.0) * 360.0 - 90.0
        ambient_strength = 18 if sky_rgb[2] < 100 else 54
        scene.ambient_color = color.rgba(ambient_strength/255.0, ambient_strength/255.0, (ambient_strength + 10)/255.0, 1.0)

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
            
            # 对于网格碰撞体，world_point 是更可靠的击中点
            # 沿着法线往回退一点点，就能落到被击中的方块内部
            hit_point = hit_info.world_point - hit_info.world_normal * 0.01
            block_pos = (
                round(hit_point.x),
                round(hit_point.y),
                round(hit_point.z)
            )
            
            if self.world.has_block(block_pos):
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
            # Simple distance check for pickup
            dx = drop.x - px
            dy = drop.y - (py - 0.5) # Check near feet
            dz = drop.z - pz
            if dx*dx + dy*dy + dz*dz < 3.0: # Pickup radius squared
                self.inventory[drop.item_type] = self.inventory.get(drop.item_type, 0) + 1
                self.hotbar.update_counts(self.inventory)
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

        selected_name = HOTBAR_BLOCKS[self.selected_hotbar_index]
        chunk_x, chunk_z = self.world.get_chunk_coordinates(tuple(self.player.position))
        self.status_text.text = (
            f"Time: {self.time_of_day:05.2f}\n"
            f"Chunk: {chunk_x}, {chunk_z}\n"
            f"Selected: {selected_name}"
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
            self.selected_hotbar_index = (self.selected_hotbar_index + 1) % len(HOTBAR_BLOCKS)
            self._apply_selected_block()
            return

        if key == "scroll down":
            self.selected_hotbar_index = (self.selected_hotbar_index - 1) % len(HOTBAR_BLOCKS)
            self._apply_selected_block()
            return

        if key in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            idx = int(key) - 1
            if idx < len(HOTBAR_BLOCKS):
                self.selected_hotbar_index = idx
                self._apply_selected_block()
            return

        if key == "left mouse down":
            if self.targeted_animal is not None:
                # 攻击动物
                self.targeted_animal.take_damage(5)
                return
                
            if self.targeted_block is not None:
                mined_block_type = self.world.blocks.get(self.targeted_block)
                if mined_block_type and mined_block_type not in ("bedrock", "water"):
                    if self.world.remove_block(self.targeted_block):
                        self.inventory[mined_block_type] = self.inventory.get(mined_block_type, 0) + 1
                        self.hotbar.update_counts(self.inventory)
                        self.save_manager.save()
                return

        if key == "right mouse down":
            place_position = self._get_place_position()
            if place_position is None or self._player_would_overlap(place_position):
                return
            selected_block = HOTBAR_BLOCKS[self.selected_hotbar_index]
            if self.inventory.get(selected_block, 0) > 0:
                if self.world.place_block(place_position, selected_block):
                    self.inventory[selected_block] -= 1
                    self.hotbar.update_counts(self.inventory)
                    self.save_manager.save()
            return

        if key == "escape":
            self.player.unlock_mouse()


app = Ursina()
game = Minecraft3DGame()


def update():
    game.update()


def input(key):
    game.input(key)


if __name__ == "__main__":
    app.run()
