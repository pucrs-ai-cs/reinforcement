#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import os, sys, time, inspect, logging

# Constants
PATH        = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DEFAULT_MAP = "maps/easy.txt"
HIGH_PROB   = 0.7
LOW_PROB    = 0.15
DEBUG       = lambda: logging.getLogger().level == logging.DEBUG
IS_DEBUG    = DEBUG()

MAX_TRAINING_EPISODES = 10000
CONVERGENCE_THRESHOLD = 0.1

# Frames per second (more means faster)
FPS         = 60

# Image files
PLAYER        = "link.bmp"
PLAYER_DEBUG  = "link_debug.bmp"
TILESET       = "link_tiles.bmp"
TILESET_DEBUG = "link_tiles_debug.bmp"

# Map (map values must match the following)
TILE_INIT         = 9
TILE_CLEAR        = 0
TILE_CLOSED       = 1
TILE_CHEST_CLOSED = 2
TILE_CHEST_OPENED = 3
TILE_BLUE_RUPEE   = 4
TERMINAL          = [TILE_CHEST_CLOSED, TILE_CHEST_OPENED]
INTERACTIVE       = [TILE_BLUE_RUPEE, TILE_CHEST_CLOSED, TILE_CHEST_OPENED]
VALID             = [TILE_CLEAR, TILE_BLUE_RUPEE, TILE_CHEST_CLOSED, TILE_CHEST_OPENED]
ALL               = [TILE_INIT, TILE_CLEAR, TILE_CLOSED, TILE_CHEST_CLOSED, TILE_CHEST_OPENED, TILE_BLUE_RUPEE]

# Tileset (pixels of image)
ZOOM        = 2
TILE_WIDTH  = 16 * ZOOM
TILE_HEIGHT = 16 * ZOOM

# Player (directions in the image)
MOVE_RIGHT  = 0
MOVE_LEFT   = 1
MOVE_UP     = 2
MOVE_DOWN   = 3
NO_OP   = 4

# Pixels per frame, must match tile size (TILE_WIDTH % MOVE_SPEED == 0 and TILE_HEIGHT % MOVE_SPEED == 0)
MOVE_SPEED  = 4 * ZOOM

# Available actions
ACTIONS = [MOVE_RIGHT, MOVE_LEFT, MOVE_UP, MOVE_DOWN]
ACTIONS_NAMES = ['RIGHT', 'LEFT', 'UP', 'DOWN', 'NO_OP']