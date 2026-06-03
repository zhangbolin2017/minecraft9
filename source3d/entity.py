import random
from ursina import Entity, Vec3, color, raycast, scene, time

class Animal(Entity):
    def __init__(self, position, world_ref, animal_type="pig"):
        texture_path = f"image/{animal_type}.png"
        
        # Simple size variations
        scale_map = {
            "pig": (0.8, 0.8, 0.8),
            "cow": (1.2, 1.2, 1.5),
            "sheep": (1.0, 1.0, 1.2),
            "chicken": (0.4, 0.5, 0.4),
        }
        size = scale_map.get(animal_type, (0.8, 0.8, 0.8))
        
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            texture=texture_path,
            scale=size,
            collider="box",
        )
        self.texture.filtering = None
        self.world = world_ref
        self.animal_type = animal_type
        
        self.gravity = 15.0
        self.vertical_velocity = 0.0
        self.speed = 1.5 if animal_type != "chicken" else 2.0
        
        self.health = 5
        self.state = "idle"
        self.state_timer = random.uniform(1.0, 4.0)
        self.move_direction = Vec3(0, 0, 0)

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
                self.state_timer = random.uniform(2.0, 5.0)
                angle = random.uniform(0, 360)
                self.rotation_y = angle
                self.move_direction = self.forward
            else:
                # Stop moving
                self.state = "idle"
                self.state_timer = random.uniform(3.0, 8.0)
                self.move_direction = Vec3(0, 0, 0)

    def _apply_physics(self):
        # 1. Vertical Movement (Gravity & Water)
        current_block = self.world.blocks.get((round(self.x), round(self.y), round(self.z)))
        in_water = current_block == "water"
        
        if in_water:
            # Float up
            self.vertical_velocity = max(-1.0, self.vertical_velocity - self.gravity * time.dt * 0.1)
            if self.y < self.world.get_surface_height(round(self.x), round(self.z)) + 0.5:
                self.vertical_velocity += 4.0 * time.dt
        else:
            self.vertical_velocity -= self.gravity * time.dt
            
        ray = raycast(
            self.position + Vec3(0, self.scale_y / 2, 0),
            Vec3(0, -1, 0),
            distance=self.scale_y / 2 + 0.2,
            ignore=(self,),
            traverse_target=scene,
        )
        
        if ray.hit and self.vertical_velocity <= 0:
            target_y = ray.world_point.y + self.scale_y / 2
            if self.y <= target_y + 0.05:
                self.y = target_y
                self.vertical_velocity = 0.0
                
                # Auto-jump if walking into a wall
                if self.state == "moving" and not in_water:
                    forward_ray = raycast(
                        self.position + Vec3(0, -self.scale_y/2 + 0.1, 0),
                        self.forward,
                        distance=self.scale_z / 2 + 0.3,
                        ignore=(self,),
                        traverse_target=scene,
                    )
                    if forward_ray.hit:
                        self.vertical_velocity = 6.0

        self.y += self.vertical_velocity * time.dt

        # 2. Horizontal Movement
        if self.state == "moving":
            move_step = self.move_direction * self.speed * time.dt
            candidate = self.position + move_step
            
            # Simple collision check
            blocked = raycast(
                self.position,
                self.move_direction,
                distance=self.scale_z / 2 + 0.1,
                ignore=(self,),
                traverse_target=scene,
            ).hit
            
            if not blocked:
                self.position = candidate
            else:
                self.state = "idle"
                self.state_timer = random.uniform(1.0, 2.0)

class ItemDrop(Entity):
    _all_drops = []
    
    def __init__(self, position, source_animal_type):
        meat_type = f"meat_{source_animal_type}"
        super().__init__(
            parent=scene,
            position=position,
            model="quad",
            texture=f"image/{meat_type}.png",
            scale=(0.4, 0.4, 0.4),
            billboard=True, # Always face camera
            collider="box",
        )
        self.texture.filtering = None
        self.item_type = meat_type
        
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
