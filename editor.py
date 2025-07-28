from constants import TILE_SIZE
import pygame

class MapEditor:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.tile_ids = sorted(self.tilemap.tile_images.keys())  # Örn: [0,1]
        self.selected_index = 0
        self.selected_tile = self.tile_ids[self.selected_index]

    def handle_mouse(self, mouse_pos, buttons, camera_offset):
        mx, my = mouse_pos
        world_x = mx + camera_offset[0]
        world_y = my + camera_offset[1]
        tile_x = world_x // TILE_SIZE
        tile_y = world_y // TILE_SIZE

        if 0 <= tile_x < self.tilemap.width and 0 <= tile_y < self.tilemap.height:
            if buttons[0]:
                self.tilemap.tiles[tile_y][tile_x] = self.selected_tile
            elif buttons[2]:
                self.tilemap.tiles[tile_y][tile_x] = 0

    def handle_key(self, key):
        # İstersen sayı tuşları ile de seçim ekle
        if key == pygame.K_0 and 0 in self.tile_ids:
            self.selected_index = self.tile_ids.index(0)
            self.selected_tile = 0
        elif key == pygame.K_1 and 1 in self.tile_ids:
            self.selected_index = self.tile_ids.index(1)
            self.selected_tile = 1

    def handle_scroll(self, y_offset):
        # y_offset >0 scroll up, <0 scroll down
        self.selected_index = (self.selected_index - y_offset) % len(self.tile_ids)
        self.selected_tile = self.tile_ids[self.selected_index]
