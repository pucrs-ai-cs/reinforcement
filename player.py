#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import pygame
from common import *

# ==========================================
# Player
# ==========================================

class Player:

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, sx, sy, map_data, map_width, map_height, image, max_pose, max_animation):
        self.direction = MOVE_DOWN
        self.image = image
        self.width = image.get_width() / max_pose
        self.height = image.get_height() / 4
        if self.height > TILE_HEIGHT:
            self.diff_height = self.height - TILE_HEIGHT
        else:
            self.diff_height = 0
        self.animation = 0
        self.max_animation = max_animation
        self.pose = 0
        self.max_pose = max_pose
        self.setup(sx, sy, map_data, map_width, map_height)

    # ------------------------------------------
    # Setup
    # ------------------------------------------

    def setup(self, sx, sy, map_data, map_width, map_height):
        self.x = sx * TILE_WIDTH
        self.y = sy * TILE_HEIGHT - self.diff_height
        self.action = None

    # ------------------------------------------
    # Update
    # ------------------------------------------

    def update(self, screen):
        if self.action == None:
            screen.blit(self.image.subsurface((0, self.direction * self.height, self.width, self.height)), (self.x, self.y))
            return False
        if self.action == MOVE_UP:
            self.direction = MOVE_UP
            self.y -= MOVE_SPEED
        elif self.action == MOVE_DOWN:
            self.direction = MOVE_DOWN
            self.y += MOVE_SPEED
        elif self.action == MOVE_LEFT:
            self.direction = MOVE_LEFT
            self.x -= MOVE_SPEED
        elif self.action == MOVE_RIGHT:
            self.direction = MOVE_RIGHT
            self.x += MOVE_SPEED
        if self.x % TILE_WIDTH == 0 and self.y % TILE_HEIGHT == self.diff_height:
            self.action = None
        self.animation += 1
        if self.animation == self.max_animation:
            self.animation = 0
            self.pose += 1
            if self.pose == self.max_pose:
                self.pose = 0
        screen.blit(self.image.subsurface((self.pose * self.width, self.direction * self.height, self.width, self.height)), (self.x, self.y))
        return True