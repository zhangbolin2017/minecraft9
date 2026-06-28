import math
import os
import random
from ursina import Entity, Text, Vec3, color, destroy, raycast, scene, time
from constants import get_texture_asset_name
from texture_utils import apply_nearest_filter, get_texture_resource


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset_exists(relative_path):
    return os.path.exists(os.path.join(BASE_DIR, relative_path))


def frame_dt(limit=0.05):
    # Clamp very large frame steps so temporary stalls do not turn into teleports.
    return min(time.dt, limit)

class Animal(Entity):
    def __init__(self, position, world_ref, animal_type="pig"):
        texture_path = f"image/{animal_type}.png"
        
        # Simple size variations
        scale_map = {
            "pig": (0.8, 0.8, 0.8),
            "cow": (1.2, 1.2, 1.5),
            "sheep": (1.0, 1.0, 1.2),
            "chicken": (0.4, 0.5, 0.4),
            "fish": (0.6, 0.3, 0.9),
        }
        size = scale_map.get(animal_type, (0.8, 0.8, 0.8))
        model_name = "cube"
        base_color = color.white
        if animal_type == "fish":
            model_name = "cube"
            base_color = color.white
        
        super().__init__(
            parent=scene,
            position=position,
            model=model_name,
            texture=texture_path if asset_exists(texture_path) else None,
            color=base_color,
            scale=size,
            collider="box",
        )
        apply_nearest_filter(self.texture)
        self.world = world_ref
        self.animal_type = animal_type
        self.normal_color = base_color
        
        self.gravity = 15.0
        self.vertical_velocity = 0.0
        self.speed = 0.5 if animal_type == "fish" else (1.5 if animal_type != "chicken" else 2.0)
        self.run_speed = self.speed * (2.2 if animal_type != "fish" else 1.6)

        health_map = {
            "cow": 10,
            "pig": 7,
            "sheep": 7,
            "chicken": 4,
            "fish": 1,
        }
        self.health = health_map.get(animal_type, 6)
        self.state = "idle"
        self.state_timer = random.uniform(1.0, 4.0)
        self.move_direction = Vec3(0, 0, 0)
        self.swim_phase = random.uniform(0.0, math.tau)
        self.body_radius = 0.32 if animal_type != "cow" else 0.42
        self.hurt_flash_timer = 0.0
        self.flee_timer = 0.0
        self.is_dying = False
        self.death_timer = 0.0
        self.death_duration = 0.9
        self.drop_spawned = False

        if animal_type == "fish":
            eye_scale = (0.12, 0.12, 0.12)
            eye_color = color.black
            self.left_eye = Entity(
                parent=self,
                model="cube",
                color=eye_color,
                scale=eye_scale,
                position=(-0.42, 0.12, 0.18),
                collider=None,
            )
            self.right_eye = Entity(
                parent=self,
                model="cube",
                color=eye_color,
                scale=eye_scale,
                position=(0.42, 0.12, 0.18),
                collider=None,
            )

    def update(self):
        dt = frame_dt()
        if self.is_dying:
            self._update_death(dt)
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer = max(0.0, self.hurt_flash_timer - dt)
            if self.hurt_flash_timer <= 0:
                self.color = self.normal_color

        self._update_ai(dt)
        self._apply_physics(dt)
        if self.y < 0.2:
            if self.animal_type == "fish":
                self.y = max(self.world.get_surface_height(round(self.x), round(self.z)) + 1.0, 1.0)
            else:
                self.y = self._support_y_for(self.x, self.z)
            self.vertical_velocity = 0.0

    def take_damage(self, amount=1, scare_direction=None):
        if self.is_dying:
            return

        self.health -= amount
        if self.health <= 0:
            self._start_death()
            return

        self.color = color.rgba(1.0, 0.35, 0.35, 1.0)
        self.hurt_flash_timer = 0.22
        self._flee(scare_direction)

    def _flee(self, scare_direction):
        if scare_direction is None or scare_direction.length() == 0:
            angle = random.uniform(0, 360)
            scare_direction = Vec3(math.sin(math.radians(angle)), 0, math.cos(math.radians(angle)))

        if self.animal_type == "fish":
            direction = Vec3(scare_direction.x, random.uniform(-0.08, 0.08), scare_direction.z)
        else:
            direction = Vec3(scare_direction.x, 0, scare_direction.z)

        if direction.length() == 0:
            direction = Vec3(1, 0, 0)
        self.move_direction = direction.normalized()
        self.state = "fleeing"
        self.flee_timer = 2.3 if self.animal_type != "fish" else 1.4
        self.state_timer = self.flee_timer
        self.rotation_y = math.degrees(math.atan2(self.move_direction.x, self.move_direction.z))

    def _start_death(self):
        self.is_dying = True
        self.death_timer = self.death_duration
        self.color = color.rgba(1.0, 0.2, 0.2, 1.0)
        self.state = "dying"
        self.move_direction = Vec3(0, 0, 0)
        self.collider = None

    def _finalize_death(self):
        if not self.drop_spawned:
            ItemDrop(self.position, self.animal_type)
            self.drop_spawned = True
        if self in self.world.animals:
            self.world.animals.remove(self)
        destroy(self)

    def _update_death(self, dt):
        self.death_timer = max(0.0, self.death_timer - dt)
        progress = 1.0 - (self.death_timer / self.death_duration if self.death_duration > 0 else 1.0)
        self.rotation_z = min(90, progress * 90)
        self.y = max(self.y - dt * 0.35, self.y - 0.01)
        if self.death_timer <= 0:
            self._finalize_death()

    def _update_ai(self, dt):
        if self.state == "fleeing":
            self.flee_timer -= dt
            if self.flee_timer <= 0:
                self.state = "idle"
                self.state_timer = random.uniform(1.0, 2.0)
                self.move_direction = Vec3(0, 0, 0)
            return

        self.state_timer -= dt
        if self.state_timer <= 0:
            if self.state == "idle":
                # Start moving
                self.state = "moving"
                self.state_timer = random.uniform(1.2, 3.5) if self.animal_type == "fish" else random.uniform(2.0, 5.0)
                angle = random.uniform(0, 360)
                self.rotation_y = angle
                if self.animal_type == "fish":
                    self.move_direction = Vec3(
                        math.sin(math.radians(angle)),
                        random.uniform(-0.12, 0.12),
                        math.cos(math.radians(angle)),
                    ).normalized()
                else:
                    self.move_direction = self.forward
            else:
                # Stop moving
                self.state = "idle"
                self.state_timer = random.uniform(1.0, 2.5) if self.animal_type == "fish" else random.uniform(3.0, 8.0)
                self.move_direction = Vec3(0, 0, 0)

    def _apply_physics(self, dt):
        if self.animal_type == "fish":
            self._apply_fish_physics(dt)
            return
        self._apply_land_animal_physics(dt)

    def _is_solid_block(self, block_type):
        return block_type is not None and block_type not in {"water", "leaves"}

    def _block_at_point(self, x, y, z):
        return self.world.get_block_type((
            math.floor(x + 0.5),
            math.floor(y + 0.5),
            math.floor(z + 0.5),
        ))

    def _collides_at(self, position):
        sample_heights = (
            -self.scale_y * 0.35,
            0.0,
            self.scale_y * 0.35,
        )
        for dx in (-self.body_radius, self.body_radius):
            for dz in (-self.body_radius, self.body_radius):
                for dy in sample_heights:
                    block = self._block_at_point(position.x + dx, position.y + dy, position.z + dz)
                    if self._is_solid_block(block):
                        return True
        return False

    def _support_y_for(self, x, z):
        surface_y = self.world.get_surface_height(round(x), round(z))
        return surface_y + 0.5 + self.scale_y / 2

    def _apply_land_animal_physics(self, dt):
        current_block = self._block_at_point(self.x, self.y - self.scale_y / 2 + 0.1, self.z)
        if current_block == "water":
            self.vertical_velocity = max(-1.0, self.vertical_velocity - self.gravity * dt * 0.1)
            self.y += self.vertical_velocity * dt
            return

        target_y = self._support_y_for(self.x, self.z)
        if self.y < target_y - 2.0:
            self.y = target_y
            self.vertical_velocity = 0.0
        else:
            self.y += (target_y - self.y) * min(1.0, dt * 12.0)
            self.vertical_velocity = 0.0

        if self.state not in {"moving", "fleeing"}:
            return

        current_speed = self.run_speed if self.state == "fleeing" else self.speed
        move_step = self.move_direction * current_speed * dt
        candidate = self.position + Vec3(move_step.x, 0, move_step.z)
        candidate_target_y = self._support_y_for(candidate.x, candidate.z)
        if abs(candidate_target_y - target_y) > 1.1:
            if self.state == "fleeing":
                self.rotation_y += random.uniform(-50, 50)
                self.move_direction = self.forward
            else:
                self.state = "idle"
                self.state_timer = random.uniform(1.0, 2.0)
            return

        candidate = Vec3(candidate.x, candidate_target_y, candidate.z)
        if not self._collides_at(candidate):
            self.position = candidate
        else:
            if self.state == "fleeing":
                self.rotation_y += random.uniform(-70, 70)
                self.move_direction = self.forward
            else:
                self.state = "idle"
                self.state_timer = random.uniform(1.0, 2.0)

    def _apply_fish_physics(self, dt):
        current_block = self.world.blocks.get((round(self.x), round(self.y), round(self.z)))
        if current_block != "water":
            self.vertical_velocity -= self.gravity * dt
            self.y += self.vertical_velocity * dt
            return

        self.vertical_velocity = 0.0
        if self.state in {"moving", "fleeing"}:
            current_speed = self.run_speed if self.state == "fleeing" else self.speed
            candidate = self.position + self.move_direction * current_speed * dt
            candidate_block = self.world.blocks.get((round(candidate.x), round(candidate.y), round(candidate.z)))
            if candidate_block == "water":
                self.position = candidate
            else:
                self.state = "idle"
                self.state_timer = random.uniform(0.4, 1.2)
        else:
            # Keep fish roughly centered in the local water column instead of sinking.
            self.swim_phase += dt * 2.0
            self.y += math.sin(self.swim_phase) * 0.003

class ItemDrop(Entity):
    _all_drops = []
    
    def __init__(self, position, item_type, launch_direction=None, lifetime=None, quantity=1, pickup_delay=0.28, launch_speed=1.5, durability_values=None):
        if item_type in {"pig", "cow", "sheep", "chicken", "fish"}:
            item_type = f"meat_{item_type}"

        texture_path = get_texture_resource(get_texture_asset_name(item_type))
        fallback_color = {
            "meat_fish": color.rgba(245/255.0, 170/255.0, 165/255.0, 1.0),
            "meat_pig": color.rgba(1.0, 150/255.0, 150/255.0, 1.0),
            "meat_cow": color.rgba(200/255.0, 100/255.0, 100/255.0, 1.0),
            "meat_sheep": color.rgba(1.0, 100/255.0, 100/255.0, 1.0),
            "meat_chicken": color.rgba(1.0, 200/255.0, 150/255.0, 1.0),
            "grass": color.rgba(95/255.0, 159/255.0, 53/255.0, 1.0),
            "dirt": color.rgba(120/255.0, 88/255.0, 58/255.0, 1.0),
            "stone": color.rgba(110/255.0, 110/255.0, 110/255.0, 1.0),
            "iron_ore": color.rgba(153/255.0, 126/255.0, 108/255.0, 1.0),
            "iron_ingot": color.rgba(226/255.0, 220/255.0, 213/255.0, 1.0),
            "iron_axe": color.rgba(201/255.0, 201/255.0, 201/255.0, 1.0),
            "stone_axe": color.rgba(155/255.0, 155/255.0, 155/255.0, 1.0),
            "wood_axe": color.rgba(161/255.0, 124/255.0, 84/255.0, 1.0),
            "furnace": color.rgba(105/255.0, 105/255.0, 105/255.0, 1.0),
            "sand": color.rgba(222/255.0, 206/255.0, 138/255.0, 1.0),
            "stick": color.rgba(143/255.0, 112/255.0, 72/255.0, 1.0),
            "log": color.rgba(102/255.0, 81/255.0, 51/255.0, 1.0),
            "leaves": color.rgba(61/255.0, 142/255.0, 51/255.0, 1.0),
            "wood": color.rgba(139/255.0, 69/255.0, 19/255.0, 1.0),
        }.get(item_type, color.white)
        super().__init__(
            parent=scene,
            position=position,
            model="quad",
            texture=texture_path,
            color=fallback_color,
            scale=(0.4, 0.4, 0.4),
            billboard=True, # Always face camera
            collider="box",
        )
        apply_nearest_filter(self.texture)
        self.item_type = item_type
        self.quantity = max(1, int(quantity))
        if durability_values is None:
            self.durability_values = []
        else:
            self.durability_values = [int(value) for value in durability_values[:self.quantity]]
        
        self.gravity = 15.0
        self.vertical_velocity = 4.0 # Pop up slightly when spawned
        direction = launch_direction if launch_direction is not None else Vec3(
            random.uniform(-0.35, 0.35),
            0.0,
            random.uniform(-0.35, 0.35),
        )
        if direction.length() == 0:
            direction = Vec3(0.2, 0.0, 0.0)
        direction = direction.normalized()
        self.horizontal_velocity = Vec3(direction.x, 0, direction.z) * launch_speed
        self.pickup_delay = pickup_delay
        self.remaining_lifetime = lifetime
        self.expired = False
        self.on_ground = False
        self.ground_contact_delay = 0.45
        self.time_since_ground_contact = 0.0
        self.count_label = Text(
            parent=self,
            text=str(self.quantity) if self.quantity > 1 else "",
            origin=(-0.5, -0.5),
            scale=3.0,
            color=color.white,
            position=(-0.18, -0.2, -0.1),
        )
        
        ItemDrop._all_drops.append(self)
        
    def update(self):
        dt = frame_dt()
        # Physics
        if self.remaining_lifetime is not None:
            self.remaining_lifetime -= dt
            if self.remaining_lifetime <= 0:
                self.expired = True
                return

        self.pickup_delay = max(0.0, self.pickup_delay - dt)
        if self.on_ground:
            self.time_since_ground_contact += dt
        self.vertical_velocity -= self.gravity * dt
        self.x += self.horizontal_velocity.x * dt
        self.z += self.horizontal_velocity.z * dt
        self.horizontal_velocity *= max(0.0, 1.0 - dt * 5.0)
        
        ray = raycast(
            self.position,
            Vec3(0, -1, 0),
            distance=0.3,
            ignore=(self,),
            traverse_target=scene,
        )
        
        if ray.hit and self.vertical_velocity <= 0:
            self.y = ray.world_point.y + 0.25
            self.vertical_velocity = 0.0
            if not self.on_ground:
                self.on_ground = True
                self.time_since_ground_contact = 0.0
        else:
            self.on_ground = False
            self.y += self.vertical_velocity * dt
            
        # Rotate slowly for visual effect
        self.rotation_y += 60 * dt

    def can_be_picked_up(self):
        if self.pickup_delay > 0:
            return False
        if self.on_ground and self.time_since_ground_contact < self.ground_contact_delay:
            return False
        return True
