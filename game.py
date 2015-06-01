#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import sys
import pygame
import time
from pygame.locals import (QUIT, KEYDOWN, K_SPACE, K_ESCAPE)
from common import *
from player import *
from environment import *

# ==========================================
# Game
# ==========================================

class Game:

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, map_name):
        # Setup
        sx, sy, self.map_data, self.map_width, self.map_height = read_map(map_name)
        pygame.init()
        env = Environment(sx, sy, self.map_data, self.map_width, self.map_height)
        start_time = time.time()
        env.train()
        elapsed_time = time.time() - start_time
        print "It took %.2f seconds to train." %elapsed_time
        screen = pygame.display.set_mode((TILE_WIDTH * self.map_width, TILE_HEIGHT * self.map_height))
        pygame.display.set_caption("[T2]   Link's Learning")
        background = pygame.Surface(screen.get_size()).convert()
        self.load_tileset(TILESET, 5, 1)
        self.draw_map(background)
        self.player = Player(sx, sy, self.map_data, self.map_width, self.map_height, self.load_image(PLAYER), 4, 8 / ZOOM)

        # Loop
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:
            screen.blit(background, (0, 0))
            if not self.player.update(screen):
                new_state, restart = env.update()
                self.draw_map(background)

                if restart:
                    # Setup Link to the initial state
                    sx = new_state[0]
                    sy = new_state[1]
                    self.player.setup(sx, sy, self.map_data, self.map_width, self.map_height)
                else:
                    # Get the action based on the Link new coordinates
                    action = direction(sx, sy, new_state[0], new_state[1])
                    if action != None:
                        self.player.action = action
                        sx, sy = new_state[0], new_state[1]

            pygame.display.flip()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE: # Reset this map
                        self.player.setup(sx, sy, self.map_data, self.map_width, self.map_height)
                    elif event.key == K_ESCAPE: # Load map
                        map_name = raw_input('Load map: ')
                        sx, sy, self.map_data, self.map_width, self.map_height = read_map(map_name)
                        if screen.get_size() != (TILE_WIDTH * self.map_width, TILE_HEIGHT * self.map_height):
                            del screen
                            del background
                            screen = pygame.display.set_mode((TILE_WIDTH * self.map_width, TILE_HEIGHT * self.map_height))
                            background = pygame.Surface(screen.get_size()).convert()
                        self.draw_map(background)
                        self.player.setup(sx, sy, self.map_data, self.map_width, self.map_height)


    # ------------------------------------------
    # Draw map
    # ------------------------------------------

    def draw_map(self, surface):
        map_y = 0
        for y in range(self.map_height):
            map_x = 0
            for x in range(self.map_width):
                tile = self.map_data[y][x]
                if TILE_CLEAR <= tile <= TILE_BLUE_RUPEE:
                    surface.blit(self.tileset[tile], (map_x, map_y))
                else:
                    raise Exception("Unknown tile", tile, (map_x, map_y))
                map_x += TILE_WIDTH
            map_y += TILE_HEIGHT

    # ------------------------------------------
    # Load image
    # ------------------------------------------

    def load_image(self, filename):
        img = pygame.image.load(os.path.join(PATH, "sprites", filename)).convert()
        img.set_colorkey((0,128,128))
        if ZOOM > 1:
            return pygame.transform.scale(img, (img.get_width() * ZOOM, img.get_height() * ZOOM))
        return img

    # ------------------------------------------
    # Load tileset
    # ------------------------------------------

    def load_tileset(self, filename, width, height):
        image = self.load_image(filename)
        self.tileset = []
        tile_y = 0
        for y in range(height):
            tile_x = 0
            for x in range(width):
                self.tileset.append(image.subsurface((tile_x, tile_y, TILE_WIDTH, TILE_HEIGHT)))
                tile_x += TILE_WIDTH
            tile_y += TILE_HEIGHT

# ==========================================
# Main
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) == 2:
        map_name = sys.argv[1]
    else:
        map_name = DEFAULT_MAP
    print "Loading map: " + map_name
    Game(map_name)