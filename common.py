#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import os, inspect

# Constants
PATH        = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DEFAULT_MAP = "easy.txt"
DEBUG       = False
MAX_TRAINING_EPISODES = 1500
HIGH_PROB   = 0.7
LOW_PROB    = 0.15

# Frames per second (more means faster)
FPS         = 30
# Image files
PLAYER = "link.bmp"
TILESET = "link_tiles.bmp"
# Map (map values must match the following)
TILE_CLEAR        = 0
TILE_CLOSED       = 1
TILE_CHEST_CLOSED = 2
TILE_CHEST_OPENED = 3
TILE_BLUE_RUPEE   = 4

# Tileset (pixels of image)
ZOOM        = 2
TILE_WIDTH  = 16 * ZOOM
TILE_HEIGHT = 16 * ZOOM
# Player (directions in the image)
MOVE_RIGHT  = 0
MOVE_LEFT   = 1
MOVE_UP     = 2
MOVE_DOWN   = 3
# Pixels per frame, must match tile size (TILE_WIDTH % MOVE_SPEED == 0 and TILE_HEIGHT % MOVE_SPEED == 0)
MOVE_SPEED  = 4 * ZOOM

# ------------------------------------------
# Read map
# ------------------------------------------

def read_map(filename):
    with open(os.path.join(PATH, "maps", filename)) as map_file:
        sx = int(map_file.readline())
        sy = int(map_file.readline())
        map_data = [[int(cell) for cell in row.rstrip()] for row in map_file]
        map_width = len(map_data[0])
        map_height = len(map_data)
        if sx < 0 or sx >= map_width:
            raise Exception("Player outside map width", map_width, sx)
        elif sy < 0 or sy >= map_height:
            raise Exception("Player outside map height", map_height, sy)
        for row in map_data:
            if len(row) != map_width:
                raise Exception("Map width does not match", map_width, len(row))
        for y in range(map_height):
            for x in range(map_width):
                cell = map_data[y][x]
                if not TILE_CLEAR <= cell <= TILE_BLUE_RUPEE:
                    raise Exception("Unknown tile", cell)
        return (sx, sy, map_data, map_width, map_height)

# ------------------------------------------
# Successors
# ------------------------------------------

def successors(x, y, map_data, map_width, map_height):
    n = []
    if x - 1 >= 0 and map_data[y][x-1] != TILE_CLOSED:
        n.append((x-1,y))
    if x + 1 < map_width and map_data[y][x+1] != TILE_CLOSED:
        n.append((x+1,y))
    if y - 1 >= 0 and map_data[y-1][x] != TILE_CLOSED:
        n.append((x,y-1))
    if y + 1 < map_height and map_data[y+1][x] != TILE_CLOSED:
        n.append((x,y+1))
    return n

# ------------------------------------------
# Direction
# ------------------------------------------

def direction(x1, y1, x2, y2):
    if x1 < x2:
        return MOVE_RIGHT
    elif x1 > x2:
        return MOVE_LEFT
    elif y1 < y2:
        return MOVE_DOWN
    elif y1 > y2:
    	return MOVE_UP
    elif x1 == x2:
        return None

    raise Exception("Unknown direction", x1, y1, x2, y2)
