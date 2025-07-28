import pygame
from constants import TILE_SIZE

class TileMap:
    def __init__(self):
        self.tile_images = {}
        self.tile_solid = {}
        self.tiles = []
        self.width = 0
        self.height = 0

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 10

    def load_tiles_data(self, filename):
        self.tile_images.clear()
        self.tile_solid.clear()
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 3:
                    continue
                tile_id = int(parts[0])
                image_file = parts[1]
                solid = parts[2].lower() == "true"
                try:
                    image = pygame.image.load(f"assets/{image_file}").convert_alpha()
                    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    self.tile_images[tile_id] = image
                    self.tile_solid[tile_id] = solid
                except Exception:
                    pass

    def load(self, filename):
        self.tiles.clear()
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = [int(tile_id) for tile_id in line.split()]
                self.tiles.append(row)
        self.height = len(self.tiles)
        self.width = max(len(row) for row in self.tiles) if self.tiles else 0

    def is_solid(self, tile_id):
        return self.tile_solid.get(tile_id, False)

    def is_colliding(self, rect):
        left = rect.left // TILE_SIZE
        right = rect.right // TILE_SIZE
        top = rect.top // TILE_SIZE
        bottom = rect.bottom // TILE_SIZE

        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if 0 <= ty < self.height and 0 <= tx < self.width:
                    try:
                        tile_id = self.tiles[ty][tx]
                    except IndexError:
                        continue
                    if self.is_solid(tile_id):
                        tile_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if rect.colliderect(tile_rect):
                            return True
        return False

    def find_nearest_free_tile(self, x, y):
        tx = x // TILE_SIZE
        ty = y // TILE_SIZE
        max_radius = max(self.width, self.height)

        for radius in range(1, max_radius):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx = tx + dx
                    ny = ty + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        tile_id = self.tiles[ny][nx]
                        if not self.is_solid(tile_id):
                            return nx * TILE_SIZE, ny * TILE_SIZE
        return x, y

    def move_camera(self, keys):
        if keys[pygame.K_w]:
            self.camera_y -= self.camera_speed
        if keys[pygame.K_s]:
            self.camera_y += self.camera_speed
        if keys[pygame.K_a]:
            self.camera_x -= self.camera_speed
        if keys[pygame.K_d]:
            self.camera_x += self.camera_speed

        max_x = max(0, self.width * TILE_SIZE - pygame.display.get_surface().get_width())
        max_y = max(0, self.height * TILE_SIZE - pygame.display.get_surface().get_height())

        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))

    def get_camera_offset(self):
        return (self.camera_x, self.camera_y)

    def draw(self, screen, camera_offset=None):
        if camera_offset is None:
            camera_offset = (self.camera_x, self.camera_y)
        ox, oy = camera_offset
        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                if tile_id == 0:
                    continue
                img = self.tile_images.get(tile_id)
                if img:
                    screen.blit(img, (x * TILE_SIZE - ox, y * TILE_SIZE - oy))

    def get_tile_at(self, x, y):
        tx = x // TILE_SIZE
        ty = y // TILE_SIZE
        if 0 <= ty < self.height and 0 <= tx < self.width:
            try:
                return self.tiles[ty][tx]
            except IndexError:
                return 0
        return 0

    def save(self, filename):
        with open(filename, "w") as f:
            for row in self.tiles:
                line = " ".join(str(tile_id) for tile_id in row)
                f.write(line + "\n")
