import math

from ursina import Entity, color, destroy, scene, Mesh, Vec3

from constants import (
    BASE_GROUND_HEIGHT,
    BLOCK_COLORS,
    CHUNK_SIZE,
    HEIGHT_VARIATION,
    LOAD_RADIUS,
    TERRAIN_SEED,
    WORLD_HEIGHT,
)


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
        self.loaded_chunks = set()
        self.chunk_blocks = {}

    def get_surface_height(self, x, z):
        wave_a = math.sin((x + TERRAIN_SEED) * 0.11) * 2.7
        wave_b = math.cos((z - TERRAIN_SEED) * 0.08) * 1.9
        wave_c = math.sin((x + z) * 0.045) * 1.6
        height = BASE_GROUND_HEIGHT + wave_a + wave_b + wave_c
        return max(3, min(WORLD_HEIGHT - 4, int(round(height + HEIGHT_VARIATION * 0.35))))

    def get_generated_block_type(self, position):
        override = self.save_manager.get_block_override(position)
        if override != "__missing__":
            return override

        x, y, z = position
        if y < 0 or y >= WORLD_HEIGHT:
            return None

        surface_y = self.get_surface_height(x, z)
        if y > surface_y:
            return None
        if y == 0:
            return "bedrock"
        if y == surface_y:
            return "sand" if surface_y <= BASE_GROUND_HEIGHT + 1 else "grass"
        if y >= surface_y - 3:
            return "dirt"
        return "stone"

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

    def load_chunk(self, chunk_x, chunk_z):
        if (chunk_x, chunk_z) in self.loaded_chunks:
            return

        origin_x, origin_z = self.get_chunk_origin(chunk_x, chunk_z)
        max_x = origin_x + CHUNK_SIZE
        max_z = origin_z + CHUNK_SIZE
        positions = set()
        for local_z in range(CHUNK_SIZE):
            for local_x in range(CHUNK_SIZE):
                world_x = origin_x + local_x
                world_z = origin_z + local_z
                surface_y = self.get_surface_height(world_x, world_z)
                for world_y in range(surface_y + 1):
                    position = (world_x, world_y, world_z)
                    block_type = self.get_generated_block_type(position)
                    if block_type is None:
                        continue
                    self.blocks[position] = block_type
                    positions.add(position)

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

        self.loaded_chunks.discard(chunk_key)

    def get_neighbor_positions(self, position):
        x, y, z = position
        return [
            (x + dx, y + dy, z + dz)
            for dx, dy, dz in NEIGHBOR_OFFSETS
        ]

    def is_exposed(self, position):
        for neighbor in self.get_neighbor_positions(position):
            if neighbor not in self.blocks:
                return True
        return False

    def combine_chunk_mesh(self, chunk_x, chunk_z):
        chunk_key = (chunk_x, chunk_z)
        if chunk_key not in self.chunk_blocks:
            return

        # Destroy existing combined entities for this chunk
        if chunk_key in self.block_entities:
            for entity in self.block_entities[chunk_key]:
                destroy(entity)
            del self.block_entities[chunk_key]

        vertices_by_type = {}
        uvs_by_type = {}
        
        # Standard UV mapping for a quad face (2 triangles)
        face_uvs = [(0,0), (1,0), (1,1), (0,0), (1,1), (0,1)]
        
        positions = self.chunk_blocks[chunk_key]
        for position in positions:
            if not self.is_exposed(position):
                continue
                
            block_type = self.blocks.get(position)
            if not block_type:
                continue
                
            if block_type not in vertices_by_type:
                vertices_by_type[block_type] = []
                uvs_by_type[block_type] = []
            
            verts = vertices_by_type[block_type]
            uvs = uvs_by_type[block_type]
            
            x, y, z = position
            
            # Top face (y+1)
            if (x, y+1, z) not in self.blocks:
                verts.extend([
                    Vec3(x-0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5),
                    Vec3(x-0.5, y+0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5)
                ])
                uvs.extend(face_uvs)
            
            # Bottom face (y-1)
            if (x, y-1, z) not in self.blocks:
                verts.extend([
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z-0.5),
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x+0.5, y-0.5, z-0.5), Vec3(x-0.5, y-0.5, z-0.5)
                ])
                uvs.extend(face_uvs)
                
            # Right face (x+1)
            if (x+1, y, z) not in self.blocks:
                verts.extend([
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x+0.5, y-0.5, z+0.5), Vec3(x+0.5, y+0.5, z+0.5),
                    Vec3(x+0.5, y-0.5, z-0.5), Vec3(x+0.5, y+0.5, z+0.5), Vec3(x+0.5, y+0.5, z-0.5)
                ])
                uvs.extend(face_uvs)
                
            # Left face (x-1)
            if (x-1, y, z) not in self.blocks:
                verts.extend([
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x-0.5, y-0.5, z-0.5), Vec3(x-0.5, y+0.5, z-0.5),
                    Vec3(x-0.5, y-0.5, z+0.5), Vec3(x-0.5, y+0.5, z-0.5), Vec3(x-0.5, y+0.5, z+0.5)
                ])
                uvs.extend(face_uvs)
                
            # Front face (z+1)
            if (x, y, z+1) not in self.blocks:
                verts.extend([
                    Vec3(x+0.5, y-0.5, z+0.5), Vec3(x-0.5, y-0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5),
                    Vec3(x+0.5, y-0.5, z+0.5), Vec3(x-0.5, y+0.5, z+0.5), Vec3(x+0.5, y+0.5, z+0.5)
                ])
                uvs.extend(face_uvs)
                
            # Back face (z-1)
            if (x, y, z-1) not in self.blocks:
                verts.extend([
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x+0.5, y-0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5),
                    Vec3(x-0.5, y-0.5, z-0.5), Vec3(x+0.5, y+0.5, z-0.5), Vec3(x-0.5, y+0.5, z-0.5)
                ])
                uvs.extend(face_uvs)

        entities = []
        for b_type, verts in vertices_by_type.items():
            if verts:
                mesh = Mesh(vertices=verts, uvs=uvs_by_type[b_type], static=True)
                texture_path = f"image/{b_type}.png"
                # Using point filtering to keep the pixel-art look
                ent = Entity(model=mesh, collider='mesh', texture=texture_path)
                ent.texture.filtering = None
                entities.append(ent)
                
        self.block_entities[chunk_key] = entities
            
        # Clean up old methods that are no longer used
        pass

    def has_block(self, position):
        return position in self.blocks

    def remove_block(self, position):
        if position not in self.blocks:
            return False

        self.blocks.pop(position, None)
        self.save_manager.set_block_override(position, None)
        chunk_key = self.get_chunk_coordinates(position)
        if chunk_key in self.loaded_chunks:
            self.combine_chunk_mesh(*chunk_key)
        return True

    def place_block(self, position, block_type):
        if position[1] < 0 or position[1] >= WORLD_HEIGHT:
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
