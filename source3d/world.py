import math

from ursina import Entity, color, destroy, scene, Mesh, Vec3
import random

from constants import (
    BASE_GROUND_HEIGHT,
    BLOCK_COLORS,
    CHUNK_SIZE,
    get_texture_asset_name,
    NON_MINEABLE_BLOCKS,
    HEIGHT_VARIATION,
    LOAD_RADIUS,
    TERRAIN_SEED,
    WORLD_HEIGHT,
    WATER_LEVEL,
)
from entity import Animal
from texture_utils import apply_nearest_filter


NEIGHBOR_OFFSETS = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


class World:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.blocks = {}
        self.block_entities = {}
        self.animals = []
        self.chunk_animals = {}
        self.loaded_chunks = set()
        self.chunk_blocks = {}
        self.guaranteed_ore_positions = {
            "coal_ore": {},
            "copper_ore": {},
            "iron_ore": {},
        }

    def get_surface_height(self, x, z):
        wave_a = math.sin((x + TERRAIN_SEED) * 0.11) * 2.7
        wave_b = math.cos((z - TERRAIN_SEED) * 0.08) * 1.9
        wave_c = math.sin((x + z) * 0.045) * 1.6
        height = BASE_GROUND_HEIGHT + wave_a + wave_b + wave_c
        return max(3, min(WORLD_HEIGHT - 4, int(round(height + HEIGHT_VARIATION * 0.35))))

    def _get_chunk_guaranteed_ore_positions(
        self,
        chunk_x,
        chunk_z,
        ore_type,
        target_count,
        seed_offset,
        surface_margin,
    ):
        ore_cache = self.guaranteed_ore_positions.setdefault(ore_type, {})
        chunk_key = (chunk_x, chunk_z)
        if chunk_key in ore_cache:
            return ore_cache[chunk_key]

        rng = random.Random((chunk_x * 92821) ^ (chunk_z * 68917) ^ TERRAIN_SEED ^ seed_offset)
        origin_x, origin_z = self.get_chunk_origin(chunk_x, chunk_z)
        ore_positions = set()
        attempts = 0

        while len(ore_positions) < target_count and attempts < 700:
            world_x = origin_x + rng.randrange(CHUNK_SIZE)
            world_z = origin_z + rng.randrange(CHUNK_SIZE)
            surface_y = self.get_surface_height(world_x, world_z)
            max_ore_y = surface_y - surface_margin
            if max_ore_y <= 1:
                attempts += 1
                continue

            world_y = rng.randint(1, max_ore_y)
            ore_positions.add((world_x, world_y, world_z))

            for _ in range(rng.randint(1, 3)):
                nx = max(origin_x, min(origin_x + CHUNK_SIZE - 1, world_x + rng.randint(-1, 1)))
                nz = max(origin_z, min(origin_z + CHUNK_SIZE - 1, world_z + rng.randint(-1, 1)))
                neighbor_surface = self.get_surface_height(nx, nz)
                max_neighbor_y = neighbor_surface - surface_margin
                if max_neighbor_y <= 1:
                    continue
                ny = max(1, min(max_neighbor_y, world_y + rng.randint(-1, 1)))
                ore_positions.add((nx, ny, nz))

            attempts += 1

        ore_cache[chunk_key] = ore_positions
        return ore_positions

    def _get_chunk_coal_ore_positions(self, chunk_x, chunk_z):
        return self._get_chunk_guaranteed_ore_positions(
            chunk_x,
            chunk_z,
            "coal_ore",
            target_count=22,
            seed_offset=0x0C0A1,
            surface_margin=2,
        )

    def _get_chunk_copper_ore_positions(self, chunk_x, chunk_z):
        return self._get_chunk_guaranteed_ore_positions(
            chunk_x,
            chunk_z,
            "copper_ore",
            target_count=18,
            seed_offset=0x0C0B2,
            surface_margin=3,
        )

    def _get_chunk_iron_ore_positions(self, chunk_x, chunk_z):
        return self._get_chunk_guaranteed_ore_positions(
            chunk_x,
            chunk_z,
            "iron_ore",
            target_count=24,
            seed_offset=0x1A2B3C,
            surface_margin=4,
        )

    def _get_ore_block_type(self, x, y, z, surface_y):
        if y <= 0 or y >= surface_y:
            return None

        depth = surface_y - y
        chunk_x, chunk_z = self.get_chunk_coordinates((x, 0, z))
        ore_position = (x, y, z)

        if depth >= 2 and ore_position in self._get_chunk_coal_ore_positions(chunk_x, chunk_z):
            return "coal_ore"
        if depth >= 3 and ore_position in self._get_chunk_copper_ore_positions(chunk_x, chunk_z):
            return "copper_ore"
        if depth >= 4 and ore_position in self._get_chunk_iron_ore_positions(chunk_x, chunk_z):
            return "iron_ore"

        coal_noise = math.sin((x * 0.17) + (y * 0.11) + (z * 0.13) + TERRAIN_SEED * 0.07)
        coal_wave = math.cos((x * 0.31) - (z * 0.29) + y * 0.23)
        if depth >= 2 and coal_noise + coal_wave > 1.48:
            return "coal_ore"

        copper_noise = math.sin((x * 0.23) + (y * 0.41) + (z * 0.19) + TERRAIN_SEED * 0.03)
        copper_wave = math.cos((x * 0.09) + (z * 0.17) - (y * 0.33))
        if depth >= 3 and copper_noise + copper_wave > 1.42:
            return "copper_ore"

        iron_noise = math.sin((x * 12.989 + y * 78.233 + z * 37.719 + TERRAIN_SEED) * 0.17)
        iron_wave = math.cos((x * 0.31) + (z * 0.27) - (y * 0.43) + TERRAIN_SEED * 0.01)
        if depth >= 4 and iron_noise + iron_wave > 1.2:
            return "iron_ore"
        return None

    def get_generated_block_type(self, position):
        override = self.save_manager.get_block_override(position)
        if override != "__missing__":
            return override

        x, y, z = position
        if y < 0 or y >= WORLD_HEIGHT:
            return None

        surface_y = self.get_surface_height(x, z)
        if y > surface_y:
            if surface_y <= WATER_LEVEL and y <= WATER_LEVEL:
                return "water"
            return None
        if y == 0:
            return "bedrock"
        if surface_y <= WATER_LEVEL + 1:
            return "sand"
        if y == surface_y:
            return "sand" if surface_y <= WATER_LEVEL + 1 else "grass"
        if y >= surface_y - 3:
            return "dirt"
        ore_type = self._get_ore_block_type(x, y, z, surface_y)
        if ore_type is not None:
            return ore_type
        return "stone"

    def get_block_type(self, position):
        block_type = self.blocks.get(position)
        if block_type is not None:
            return block_type
        return self.get_generated_block_type(position)

    def get_chunk_coordinates(self, world_position):
        return (
            math.floor(world_position[0] / CHUNK_SIZE),
            math.floor(world_position[2] / CHUNK_SIZE),
        )

    def get_chunk_origin(self, chunk_x, chunk_z):
        return chunk_x * CHUNK_SIZE, chunk_z * CHUNK_SIZE

    def get_loaded_chunk_keys_around(self, world_position):
        center_chunk = self.get_chunk_coordinates(world_position)
        desired = set()
        for dz in range(-LOAD_RADIUS, LOAD_RADIUS + 1):
            for dx in range(-LOAD_RADIUS, LOAD_RADIUS + 1):
                desired.add((center_chunk[0] + dx, center_chunk[1] + dz))
        return desired

    def update_loaded_chunks(self, world_position):
        desired_chunks = self.get_loaded_chunk_keys_around(world_position)
        missing_chunks = desired_chunks - self.loaded_chunks
        extra_chunks = self.loaded_chunks - desired_chunks

        for chunk_key in sorted(missing_chunks):
            self.load_chunk(*chunk_key)

        for chunk_key in sorted(extra_chunks):
            self.unload_chunk(*chunk_key)

    def get_tree_at(self, world_x, world_z):
        random.seed(world_x * 31 + world_z * 17 + TERRAIN_SEED)
        if random.random() < 0.02:
            return random.randint(4, 5)
        return None

    def load_chunk(self, chunk_x, chunk_z):
        if (chunk_x, chunk_z) in self.loaded_chunks:
            return

        origin_x, origin_z = self.get_chunk_origin(chunk_x, chunk_z)
        max_x = origin_x + CHUNK_SIZE
        max_z = origin_z + CHUNK_SIZE
        positions = set()
        spawned_animals = []
        for local_z in range(CHUNK_SIZE):
            for local_x in range(CHUNK_SIZE):
                world_x = origin_x + local_x
                world_z = origin_z + local_z
                surface_y = self.get_surface_height(world_x, world_z)
                top_y = max(surface_y, WATER_LEVEL)
                for world_y in range(top_y + 1):
                    position = (world_x, world_y, world_z)
                    block_type = self.get_generated_block_type(position)
                    if block_type is None:
                        continue
                    self.blocks[position] = block_type
                    positions.add(position)

        # Generate Trees (Logs and Leaves) for this chunk
        for local_z in range(CHUNK_SIZE):
            for local_x in range(CHUNK_SIZE):
                world_x = origin_x + local_x
                world_z = origin_z + local_z
                
                # Animal spawning (only on grass, low probability)
                surface_y = self.get_surface_height(world_x, world_z)
                if surface_y > WATER_LEVEL and surface_y >= BASE_GROUND_HEIGHT:
                    random.seed(world_x * 73 + world_z * 41 + TERRAIN_SEED)
                    if random.random() < 0.005:
                        animal_type = random.choice(["pig", "cow", "sheep", "chicken"])
                        animal = Animal((world_x, surface_y + 1, world_z), self, animal_type)
                        self.animals.append(animal)
                        spawned_animals.append(animal)
                elif surface_y <= WATER_LEVEL:
                    random.seed(world_x * 97 + world_z * 59 + TERRAIN_SEED)
                    water_depth = WATER_LEVEL - surface_y
                    if water_depth >= 1 and random.random() < 0.04:
                        fish_y = min(WATER_LEVEL - 0.2, surface_y + 1.2)
                        if self.blocks.get((world_x, round(fish_y), world_z)) == "water":
                            animal = Animal((world_x, fish_y, world_z), self, "fish")
                            self.animals.append(animal)
                            spawned_animals.append(animal)
                
                # Check neighbors up to 2 blocks away for trees that might overlap into this column
                for tx in range(world_x - 2, world_x + 3):
                    for tz in range(world_z - 2, world_z + 3):
                        tree_h = self.get_tree_at(tx, tz)
                        if not tree_h:
                            continue
                            
                        tree_surface = self.get_surface_height(tx, tz)
                        if tree_surface < BASE_GROUND_HEIGHT: # Only grow on grass
                            continue
                            
                        # If this column is the tree trunk itself
                        if tx == world_x and tz == world_z:
                            for ty in range(1, tree_h + 1):
                                pos = (world_x, tree_surface + ty, world_z)
                                self.blocks[pos] = "log"
                                positions.add(pos)
                                
                        # Leaves logic
                        dx = abs(world_x - tx)
                        dz = abs(world_z - tz)
                        if dx <= 2 and dz <= 2:
                            random.seed(world_x * 13 + world_z * 7 + tx * 3 + tz * 11 + TERRAIN_SEED)
                            for ly in range(tree_surface + tree_h - 1, tree_surface + tree_h + 2):
                                is_top = (ly >= tree_surface + tree_h)
                                radius = 1 if is_top else 2
                                if dx <= radius and dz <= radius:
                                    if dx == radius and dz == radius and random.random() < 0.5:
                                        continue
                                    pos = (world_x, ly, world_z)
                                    # Don't overwrite logs with leaves
                                    if pos not in self.blocks or self.blocks[pos] != "log":
                                        self.blocks[pos] = "leaves"
                                        positions.add(pos)

        for position, block_type in self.save_manager.iter_block_overrides():
            px, py, pz = position
            if not (origin_x <= px < max_x and origin_z <= pz < max_z):
                continue
            if py < 0 or py >= WORLD_HEIGHT:
                continue
            if block_type is None:
                self.blocks.pop(position, None)
                positions.discard(position)
                continue
            self.blocks[position] = block_type
            positions.add(position)

        self.loaded_chunks.add((chunk_x, chunk_z))
        self.chunk_blocks[(chunk_x, chunk_z)] = positions
        self.chunk_animals[(chunk_x, chunk_z)] = spawned_animals
        self.combine_chunk_mesh(chunk_x, chunk_z)

    def unload_chunk(self, chunk_x, chunk_z):
        chunk_key = (chunk_x, chunk_z)
        positions = self.chunk_blocks.pop(chunk_key, set())

        if chunk_key in self.block_entities:
            for entity in self.block_entities[chunk_key]:
                destroy(entity)
            del self.block_entities[chunk_key]

        for position in positions:
            self.blocks.pop(position, None)

        for animal in self.chunk_animals.pop(chunk_key, []):
            if animal in self.animals:
                self.animals.remove(animal)
            destroy(animal)

        self.loaded_chunks.discard(chunk_key)

    def update_animals(self):
        for animal in list(self.animals):
            animal.update()

    def get_neighbor_positions(self, position):
        x, y, z = position
        return [
            (x + dx, y + dy, z + dz)
            for dx, dy, dz in NEIGHBOR_OFFSETS
        ]

    def _water_source_neighbors(self, position):
        x, y, z = position
        return [
            (x, y + 1, z),
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]

    def _has_adjacent_water_source(self, position):
        for neighbor in self._water_source_neighbors(position):
            if self.blocks.get(neighbor) == "water":
                return True
        return False

    def _refresh_chunks_for_positions(self, positions):
        chunk_keys = set()
        for position in positions:
            chunk_keys.add(self.get_chunk_coordinates(position))
            for neighbor in self.get_neighbor_positions(position):
                chunk_keys.add(self.get_chunk_coordinates(neighbor))

        for chunk_key in chunk_keys:
            if chunk_key in self.loaded_chunks:
                self.combine_chunk_mesh(*chunk_key)

    def _spread_water_from(self, start_position):
        changed_positions = set()
        queue = [start_position]
        visited = set()

        while queue:
            position = queue.pop(0)
            if position in visited:
                continue
            visited.add(position)

            x, y, z = position
            if y <= 0 or y >= WORLD_HEIGHT:
                continue
            if position in self.blocks:
                continue
            if not self._has_adjacent_water_source(position):
                continue

            self.blocks[position] = "water"
            chunk_key = self.get_chunk_coordinates(position)
            self.chunk_blocks.setdefault(chunk_key, set()).add(position)
            self.save_manager.set_block_override(position, "water")
            changed_positions.add(position)

            below = (x, y - 1, z)
            if y - 1 > 0 and below not in self.blocks:
                queue.append(below)

        return changed_positions

    def is_exposed(self, position):
        for neighbor in self.get_neighbor_positions(position):
            if self.should_render_face(position, neighbor):
                return True
        return False

    def should_render_face(self, position, neighbor):
        block_type = self.blocks.get(position)
        neighbor_type = self.blocks.get(neighbor)

        if neighbor_type is None:
            return True
        if block_type == "water":
            return neighbor_type != "water"
        return neighbor_type == "water"

    def _get_face_texture_name(self, block_type, face_name):
        if block_type == "grass":
            if face_name == "top":
                return "grass"
            if face_name == "bottom":
                return "dirt"
            return "grass1"
        if block_type == "furnace":
            if face_name in {"top", "bottom"}:
                return "furnace_top"
            return "furnace"
        return get_texture_asset_name(block_type)

    def combine_chunk_mesh(self, chunk_x, chunk_z):
        chunk_key = (chunk_x, chunk_z)
        if chunk_key not in self.chunk_blocks:
            return

        # Destroy existing combined entities for this chunk
        if chunk_key in self.block_entities:
            for entity in self.block_entities[chunk_key]:
                destroy(entity)
            del self.block_entities[chunk_key]

        vertices_by_texture = {}
        uvs_by_texture = {}
        
        # Standard UV mapping for a quad face (2 triangles)
        face_uvs = [(0,0), (1,0), (1,1), (0,0), (1,1), (0,1)]
        
        positions = self.chunk_blocks[chunk_key]
        for position in positions:
            if not self.is_exposed(position):
                continue
                
            block_type = self.blocks.get(position)
            if not block_type:
                continue
            
            x, y, z = position
            
            # Top face (y+1) - Normal +Y. Looking down from +Y, CW.
            if self.should_render_face(position, (x, y+1, z)):
                texture_name = self._get_face_texture_name(block_type, "top")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x-0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), # Triangle 1
                    Vec3(x-0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)
            
            # Bottom face (y-1) - Normal -Y. Looking up from -Y, CW.
            if self.should_render_face(position, (x, y-1, z)):
                texture_name = self._get_face_texture_name(block_type, "bottom")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x-0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z+0.5), # Triangle 1
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x+0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z-0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)
                
            # Right face (x+1) - Normal +X. Looking from +X, CW.
            if self.should_render_face(position, (x+1, y, z)):
                texture_name = self._get_face_texture_name(block_type, "side")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), # Triangle 1
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), Vec3(x+0.5, y-0.5, z+0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)
                
            # Left face (x-1) - Normal -X. Looking from -X, CW.
            if self.should_render_face(position, (x-1, y, z)):
                texture_name = self._get_face_texture_name(block_type, "side")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x-0.5, y-0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5), # Triangle 1
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x-0.5, y+0.5, z+0.5), Vec3(x-0.5, y+0.5, z-0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)
                
            # Front face (z+1) - Normal +Z. Looking from +Z, CW.
            if self.should_render_face(position, (x, y, z+1)):
                texture_name = self._get_face_texture_name(block_type, "side")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z+0.5), Vec3(x+0.5, y+0.5, z+0.5), # Triangle 1
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x+0.5, y+0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)
                
            # Back face (z-1) - Normal -Z. Looking from -Z, CW.
            if self.should_render_face(position, (x, y, z-1)):
                texture_name = self._get_face_texture_name(block_type, "side")
                vertices_by_texture.setdefault(texture_name, [])
                uvs_by_texture.setdefault(texture_name, [])
                verts = vertices_by_texture[texture_name]
                uvs = uvs_by_texture[texture_name]
                verts.extend([
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x-0.5, y-0.5, z-0.5), Vec3(x-0.5, y+0.5, z-0.5), # Triangle 1
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x-0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5)  # Triangle 2
                ])
                uvs.extend(face_uvs)

        entities = []
        for texture_name, verts in vertices_by_texture.items():
            if verts:
                mesh = Mesh(vertices=verts, uvs=uvs_by_texture[texture_name], static=True)
                texture_path = f"image/{texture_name}.png"
                
                # Using point filtering to keep the pixel-art look
                has_collider = None if texture_name == "water" else 'mesh'
                ent = Entity(model=mesh, collider=has_collider, texture=texture_path)
                apply_nearest_filter(ent.texture)
                # Merged chunk meshes sometimes expose winding mistakes on side faces.
                # Rendering both sides avoids vertical faces disappearing for the player.
                ent.double_sided = True
                
                if texture_name == "water":
                    ent.color = color.rgba(0.68, 0.85, 1.0, 0.9)
                    
                entities.append(ent)
                
        self.block_entities[chunk_key] = entities
            
        # Clean up old methods that are no longer used
        pass

    def has_block(self, position):
        return self.get_block_type(position) is not None

    def remove_block(self, position):
        block_type = self.get_block_type(position)
        if block_type is None or block_type in NON_MINEABLE_BLOCKS:
            return False

        if position not in self.blocks:
            chunk_key = self.get_chunk_coordinates(position)
            if chunk_key not in self.loaded_chunks:
                self.load_chunk(*chunk_key)
            self.blocks[position] = block_type
            self.chunk_blocks.setdefault(chunk_key, set()).add(position)

        self.blocks.pop(position, None)
        self.save_manager.set_block_override(position, None)
        chunk_key = self.get_chunk_coordinates(position)
        changed_positions = {position}
        changed_positions.update(self._spread_water_from(position))
        self._refresh_chunks_for_positions(changed_positions)
        return True

    def place_block(self, position, block_type):
        if position[1] < 0 or position[1] >= WORLD_HEIGHT:
            return False
        if block_type == "water":
            return False
        if position in self.blocks:
            return False

        chunk_key = self.get_chunk_coordinates(position)
        if chunk_key not in self.loaded_chunks:
            self.load_chunk(*chunk_key)

        self.blocks[position] = block_type
        self.chunk_blocks.setdefault(chunk_key, set()).add(position)
        self.save_manager.set_block_override(position, block_type)
        if chunk_key in self.loaded_chunks:
            self.combine_chunk_mesh(*chunk_key)
        return True
