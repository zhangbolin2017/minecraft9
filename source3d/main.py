import atexit
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
        super().__init__(position=start_position)
        self.world = world_ref
        self.height = 1.8
        self.speed = 5.5
        self.jump_speed = 6.5
        self.gravity = 20.0
        self.vertical_velocity = 0.0
        self.grounded = False
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

    def _move_horizontal(self):
        move_direction = (
            self.forward_flat * (held_keys["w"] - held_keys["s"])
            + self.right_flat * (held_keys["d"] - held_keys["a"])
        )
        if move_direction.length() == 0:
            return

        move_direction = move_direction.normalized()
        move_step = move_direction * self.speed * time.dt
        candidate = self.position + move_step

        feet_origin = candidate + Vec3(0, 0.5, 0)
        head_origin = candidate + Vec3(0, self.height - 0.1, 0)
        blocked_feet = raycast(feet_origin, move_direction, distance=0.4, ignore=(self,), traverse_target=scene).hit
        blocked_head = raycast(head_origin, move_direction, distance=0.4, ignore=(self,), traverse_target=scene).hit
        if not blocked_feet and not blocked_head:
            self.position = candidate

    def _apply_vertical(self):
        # 兜底：如果玩家掉出世界，直接拉回地表
        if self.y < -10:
            surface_y = self.world.get_surface_height(round(self.x), round(self.z))
            self.y = surface_y + 2.0
            self.vertical_velocity = 0.0
            
        ray = raycast(
            self.position + Vec3(0, self.height + 0.2, 0),
            Vec3(0, -1, 0),
            distance=self.height + 0.5,
            ignore=(self,),
            traverse_target=scene,
        )
        if ray.hit and self.vertical_velocity <= 0:
            target_y = ray.world_point.y
            if self.y <= target_y + 0.05 or ray.distance <= self.height + 0.25:
                self.y = target_y
                self.vertical_velocity = 0.0
                self.grounded = True
                return

        self.grounded = False
        self.vertical_velocity -= self.gravity * time.dt
        self.y += self.vertical_velocity * time.dt

    def jump(self):
        if self.grounded:
            self.vertical_velocity = self.jump_speed
            self.grounded = False

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
                text=f"{index + 1}\n{block_type}",
                origin=(0, 0),
                scale=0.6,
                color=color.white,
                y=-0.3,
            )
            self.slots.append(slot)
            self.labels.append(label)

        self.set_selected(0)

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

        self.hotbar = HotbarUI(HOTBAR_BLOCKS)
        self.selected_hotbar_index = 0
        self.time_of_day = 8.0
        self.targeted_block = None
        self.targeted_normal = None
        self.position_save_timer = 0.0

        mouse.locked = False
        window.borderless = False
        window.title = WINDOW_TITLE

        self._create_debug_markers()
        self._apply_selected_block()
        self._apply_lighting()
        atexit.register(self.save_and_flush)

    def _apply_selected_block(self):
        self.hotbar.set_selected(self.selected_hotbar_index)

    def _create_debug_markers(self):
        marker_specs = [
            ((4, 0, 4), color.red),
            ((12, 0, 4), color.azure),
            ((4, 0, 12), color.orange),
            ((12, 0, 12), color.lime),
        ]
        for base_position, marker_color in marker_specs:
            for height in range(5):
                marker = Entity(
                    parent=scene,
                    model="cube",
                    position=Vec3(base_position[0], 1 + height, base_position[2]),
                    color=marker_color,
                    collider="box",
                )
                self.debug_markers.append(marker)

    def _apply_lighting(self):
        sky_rgb = get_sky_color(self.time_of_day)
        window.color = color.rgba(sky_rgb[0]/255.0, sky_rgb[1]/255.0, sky_rgb[2]/255.0, 1.0)
        sc = lerp_color((170, 170, 190), (255, 244, 214), 0.5)
        self.sun.color = color.rgba(sc[0]/255.0, sc[1]/255.0, sc[2]/255.0, 1.0)
        self.sun.rotation_x = (self.time_of_day / 24.0) * 360.0 - 90.0
        ambient_strength = 18 if sky_rgb[2] < 100 else 54
        scene.ambient_color = color.rgba(ambient_strength/255.0, ambient_strength/255.0, (ambient_strength + 10)/255.0, 1.0)

    def _update_target_block(self):
        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=INTERACTION_DISTANCE,
            ignore=(self.player, self.highlight),
        )

        if hit_info.hit:
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

    def update(self):
        self.world.update_loaded_chunks(tuple(self.player.position))
        self._update_target_block()

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

        if key in {"1", "2", "3", "4", "5"}:
            self.selected_hotbar_index = int(key) - 1
            self._apply_selected_block()
            return

        if key == "left mouse down" and self.targeted_block is not None:
            if self.world.remove_block(self.targeted_block):
                self.save_manager.save()
            return

        if key == "right mouse down":
            place_position = self._get_place_position()
            if place_position is None or self._player_would_overlap(place_position):
                return
            selected_block = HOTBAR_BLOCKS[self.selected_hotbar_index]
            if self.world.place_block(place_position, selected_block):
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
