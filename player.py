import pygame
from constants import TILE_SIZE

class Player:
    def __init__(self, x, y, tilemap):
        self.sprites = {
            "up": pygame.transform.scale(pygame.image.load("assets/player_up.png"), (TILE_SIZE, TILE_SIZE)),
            "down": pygame.transform.scale(pygame.image.load("assets/player_down.png"), (TILE_SIZE, TILE_SIZE)),
            "left": pygame.transform.scale(pygame.image.load("assets/player_left.png"), (TILE_SIZE, TILE_SIZE)),
            "right": pygame.transform.scale(pygame.image.load("assets/player_right.png"), (TILE_SIZE, TILE_SIZE)),
        }

        self.direction = "down"
        self.image = self.sprites[self.direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-10, -10)

        if tilemap.is_colliding(self.hitbox):
            new_x, new_y = tilemap.find_nearest_free_tile(self.hitbox.centerx, self.hitbox.centery)
            self.rect.topleft = (new_x, new_y)
            self.hitbox.topleft = (new_x + 5, new_y + 5)

        self.speed = 4

    def handle_input(self, keys, tilemap):
        dx, dy = 0, 0
        new_direction = self.direction

        if keys[pygame.K_a]:
            dx -= self.speed
            new_direction = "left"
        elif keys[pygame.K_d]:
            dx += self.speed
            new_direction = "right"
        if keys[pygame.K_w]:
            dy -= self.speed
            new_direction = "up"
        elif keys[pygame.K_s]:
            dy += self.speed
            new_direction = "down"

        if dx != 0 or dy != 0:
            self.direction = new_direction
            self.image = self.sprites[self.direction]

        new_hitbox = self.hitbox.move(dx, 0)
        if not tilemap.is_colliding(new_hitbox):
            self.hitbox = new_hitbox
            self.rect.x += dx

        new_hitbox = self.hitbox.move(0, dy)
        if not tilemap.is_colliding(new_hitbox):
            self.hitbox = new_hitbox
            self.rect.y += dy

    def draw(self, screen, camera_offset):
        screen.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

    def get_pos(self):
        return self.rect.center
