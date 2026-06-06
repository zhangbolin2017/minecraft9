import math
import os
import random
from ursina import Entity, Vec3, color, raycast, scene, time
from constants import get_texture_asset_name


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset_exists(relative_path):
    return os.path.exists(os.path.join(BASE_DIR, relative_path))

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
        if self.texture:
            self.texture.filtering = None
        self.world = world_ref
        self.animal_type = animal_type
        
        self.gravity = 15.0
        self.vertical_velocity = 0.0
        self.speed = 1.8 if animal_type == "fish" else (1.5 if animal_type != "chicken" else 2.0)
        
        self.health = 1 if animal_type == "fish" else 5
        self.state = "idle"
        self.state_timer = random.uniform(1.0, 4.0)
        self.move_direction = Vec3(0, 0, 0)
        self.swim_phase = random.uniform(0.0, math.tau)
        self.body_radius = 0.32 if animal_type != "cow" else 0.42

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
        self._update_ai()
        self._apply_physics()

    def take_damage(self, amount=5):
        self.health -= amount
        if self.health <= 0:
            # Die and drop meat
            ItemDrop(self.position, self.animal_type)
            self.world.animals.remove(self)
            from ursina import destroy
            destroy(self)

    def _update_ai(self):
        self.state_timer -= time.dt
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

    def _apply_physics(self):
        if self.animal_type == "fish":
            self._apply_fish_physics()
            return
        self._apply_land_animal_physics()

    def _is_solid_block(self, block_type):
        return block_type is not None and block_type not in {"water", "leaves"}

    def _block_at_point(self, x, y, z):
        return self.world.blocks.get((round(x), round(y), round(z)))

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

    def _apply_land_animal_physics(self):
        current_block = self._block_at_point(self.x, self.y - self.scale_y / 2 + 0.1, self.z)
        if current_block == "water":
            self.vertical_velocity = max(-1.0, self.vertical_velocity - self.gravity * time.dt * 0.1)
            self.y += self.vertical_velocity * time.dt
            return

        target_y = self._support_y_for(self.x, self.z)
        if self.y < target_y - 2.0:
            self.y = target_y
            self.vertical_velocity = 0.0
        else:
            self.y += (target_y - self.y) * min(1.0, time.dt * 12.0)
            self.vertical_velocity = 0.0

        if self.state != "moving":
            return

        move_step = self.move_direction * self.speed * time.dt
        candidate = self.position + Vec3(move_step.x, 0, move_step.z)
        candidate_target_y = self._support_y_for(candidate.x, candidate.z)
        if abs(candidate_target_y - target_y) > 1.1:
            self.state = "idle"
            self.state_timer = random.uniform(1.0, 2.0)
            return

        candidate = Vec3(candidate.x, candidate_target_y, candidate.z)
        if not self._collides_at(candidate):
            self.position = candidate
        else:
            self.state = "idle"
            self.state_timer = random.uniform(1.0, 2.0)

    def _apply_fish_physics(self):
        current_block = self.world.blocks.get((round(self.x), round(self.y), round(self.z)))
        if current_block != "water":
            self.vertical_velocity -= self.gravity * time.dt
            self.y += self.vertical_velocity * time.dt
            return

        self.vertical_velocity = 0.0
        if self.state == "moving":
            candidate = self.position + self.move_direction * self.speed * time.dt
            candidate_block = self.world.blocks.get((round(candidate.x), round(candidate.y), round(candidate.z)))
            if candidate_block == "water":
                self.position = candidate
            else:
                self.state = "idle"
                self.state_timer = random.uniform(0.4, 1.2)
        else:
            # Keep fish roughly centered in the local water column instead of sinking.
            self.swim_phase += time.dt * 2.0
            self.y += math.sin(self.swim_phase) * 0.003

class ItemDrop(Entity):
    _all_drops = []
    
    def __init__(self, position, item_type):
        if item_type in {"pig", "cow", "sheep", "chicken", "fish"}:
            item_type = f"meat_{item_type}"

        texture_path = f"image/{get_texture_asset_name(item_type)}.png"
        fallback_color = {
            "meat_fish": color.rgba(245/255.0, 170/255.0, 165/255.0, 1.0),
            "meat_pig": color.rgba(1.0, 150/255.0, 150/255.0, 1.0),
            "meat_cow": color.rgba(200/255.0, 100/255.0, 100/255.0, 1.0),
            "meat_sheep": color.rgba(1.0, 100/255.0, 100/255.0, 1.0),
            "meat_chicken": color.rgba(1.0, 200/255.0, 150/255.0, 1.0),
            "grass": color.rgba(95/255.0, 159/255.0, 53/255.0, 1.0),
            "dirt": color.rgba(120/255.0, 88/255.0, 58/255.0, 1.0),
            "stone": color.rgba(110/255.0, 110/255.0, 110/255.0, 1.0),
            "sand": color.rgba(222/255.0, 206/255.0, 138/255.0, 1.0),
            "log": color.rgba(102/255.0, 81/255.0, 51/255.0, 1.0),
            "leaves": color.rgba(61/255.0, 142/255.0, 51/255.0, 1.0),
            "wood": color.rgba(139/255.0, 69/255.0, 19/255.0, 1.0),
        }.get(item_type, color.white)
        super().__init__(
            parent=scene,
            position=position,
            model="quad",
            texture=texture_path if asset_exists(texture_path) else None,
            color=fallback_color,
            scale=(0.4, 0.4, 0.4),
            billboard=True, # Always face camera
            collider="box",
        )
        if self.texture:
            self.texture.filtering = None
        self.item_type = item_type
        
        self.gravity = 15.0
        self.vertical_velocity = 4.0 # Pop up slightly when spawned
        
        ItemDrop._all_drops.append(self)
        
    def update(self):
        # Physics
        self.vertical_velocity -= self.gravity * time.dt
        
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
        else:
            self.y += self.vertical_velocity * time.dt
            
        # Rotate slowly for visual effect
        self.rotation_y += 60 * time.dt
