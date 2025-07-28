import pygame
from map import TileMap
from player import Player
from editor import MapEditor
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

tilemap = TileMap()
tilemap.load_tiles_data("tiles_data.txt")  # önce
tilemap.load("map_data.txt")               # sonra

player = Player(200, 100, tilemap)
editor = MapEditor(tilemap)

edit_mode = False

font = pygame.font.SysFont(None, 24)  # Fontu dışarı alabiliriz

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def get_camera_offset(player_pos):
    cx = player_pos[0] - SCREEN_WIDTH // 2
    cy = player_pos[1] - SCREEN_HEIGHT // 2
    return (cx, cy)

running = True
while running:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tilemap.save("map_data.txt")
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                edit_mode = not edit_mode
            if edit_mode:
                editor.handle_key(event.key)
        elif event.type == pygame.MOUSEWHEEL:
            if edit_mode:
                editor.handle_scroll(event.y)

    if edit_mode:
        tilemap.move_camera(keys)
        camera_offset = tilemap.get_camera_offset()

        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        editor.handle_mouse(mouse_pos, buttons, camera_offset)
    else:
        player.handle_input(keys, tilemap)
        camera_offset = get_camera_offset(player.get_pos())

    tilemap.draw(screen, camera_offset)
    if not edit_mode:
        player.draw(screen, camera_offset)

    font = pygame.font.Font("assets/font.ttf", 16)

    cursor_img = pygame.image.load("assets/cursor.png").convert_alpha()
    pygame.mouse.set_visible(False)
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(cursor_img, mouse_pos)

    if edit_mode:
        selected_img = tilemap.tile_images[editor.selected_tile]
        selected_surf = selected_img.copy()
        selected_surf.set_alpha(180)
        screen.blit(selected_surf, (10, 10))

        text_surf = font.render(f"Selected Tile ID: {editor.selected_tile}", True, (255, 255, 255))
        bg_rect = text_surf.get_rect(topleft=(10, 10 + TILE_SIZE + 5))
        pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect)
        screen.blit(text_surf, (10, 10 + TILE_SIZE + 5))

    pygame.display.set_caption("editor - copy engine" if edit_mode else "copy engine")
    pygame.display.flip()
    clock.tick(60)

