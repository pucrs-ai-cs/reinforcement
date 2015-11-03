#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import sys, time, math, pygame, logging
from pygame.locals import (QUIT, KEYDOWN, K_SPACE, K_ESCAPE)
from common import *
from util import *
from environment import *

class Game:

    def __init__(self, env, agt):

        self.env = env
        self.agt = agt

        pygame.init()

        screen = pygame.display.set_mode((TILE_WIDTH * self.env.map_width + TILE_WIDTH * 2, TILE_HEIGHT * self.env.map_height + TILE_HEIGHT * 2))
        pygame.display.set_caption("[T2] Link's Learning")

        prev_x, prev_y = self.env.init
        sx, sy = self.env.init

        self.setup_tiles()
        self.setup_agent()
        self.setup_agent_pos(prev_x, prev_y)
        self.compute_range()

        around, background, interactive = self.draw_changes()
        contour = self.draw_contour()

        # Loop
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:

            screen.blit(around, (0, 0))
            screen.blit(background, (TILE_WIDTH, TILE_HEIGHT))
            screen.blit(interactive, (TILE_WIDTH, TILE_HEIGHT))
            DEBUG() and screen.blit(contour, (TILE_WIDTH, TILE_HEIGHT))

            if not self.update_agent(screen):

                _, new_state = self.agt.run(self.env)
                sx, sy = new_state

                if self.env.terminal((prev_x, prev_y)):
                    # Setup Link to the initial state
                    prev_x, prev_y = sx, sy = self.env.init
                    self.setup_agent_pos(sx, sy)
                else:
                    # Get the action based on the Link new coordinates
                    action = direction(prev_x, prev_y, sx, sy)
                    if action is not None:
                        self.agent_action = action
                        prev_x, prev_y = sx, sy

                around, background, interactive = self.draw_changes()

            pygame.display.flip()
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if DEBUG():
                            logging.getLogger().setLevel(logging.INFO)
                        else:
                            logging.getLogger().setLevel(logging.DEBUG)
                        around, background, interactive = self.draw_changes()

    def draw_changes(self):
        """
        Draw changes in scenario.
        """
        around = self.draw_around()
        background = self.draw_map()
        interactive = self.draw_interactive()
        return around, background, interactive

    def draw_contour(self):
        """
        Draw map contour.
        """
        contour = pygame.Surface((TILE_WIDTH * self.env.map_width, TILE_HEIGHT * self.env.map_height), pygame.SRCALPHA, 32).convert_alpha()
        for x in xrange(self.env.map_width):
            for y in xrange(self.env.map_height):
                tile = self.env.map_data[x][y]

                x0, y0 = TILE_WIDTH * x, TILE_HEIGHT * y
                x1, y1 = x0 + TILE_WIDTH, y0 + TILE_HEIGHT
                border = 1

                if tile not in VALID:
                    lines = {
                        MOVE_RIGHT: ((x1, y0), (x1, y1)),
                        MOVE_LEFT: ((x0, y0), (x0, y1)),
                        MOVE_DOWN: ((x0, y1), (x1, y1)),
                        MOVE_UP: ((x0, y0), (x1, y0)),
                    }
                    for s in successors((x, y), self.env.map_data, self.env.map_width, self.env.map_height):
                        xn, yn = s
                        d = direction(x, y, xn, yn)
                        line_from, line_to = lines[d]
                        pygame.draw.line(contour, (255, 255, 255), line_from, line_to, border)

        pygame.draw.rect(contour, (255, 255, 255), [0, 0, TILE_WIDTH * self.env.map_width, TILE_HEIGHT * self.env.map_height], 1)
        return contour

    def draw_map(self):
        """
        Draw map and, if on debug, q-states.
        """
        background = pygame.Surface((TILE_WIDTH * self.env.map_width, TILE_HEIGHT * self.env.map_height)).convert()
        for x in xrange(self.env.map_width):
            for y in xrange(self.env.map_height):
                tile = self.env.map_data[x][y]

                if not DEBUG():
                    if tile == TILE_BLUE_RUPEE:
                        background.blit(self.tileset[0][TILE_CLEAR], (TILE_WIDTH * x, TILE_HEIGHT * y))
                    background.blit(self.tileset[0][tile], (TILE_WIDTH * x, TILE_HEIGHT * y))
                    continue

                x0, y0 = TILE_WIDTH * x, TILE_HEIGHT * y
                x1, y1 = x0 + TILE_WIDTH, y0 + TILE_HEIGHT
                xh, yh = x0 + math.floor(TILE_WIDTH / 2), y0 + math.floor(TILE_HEIGHT / 2)
                border = 1

                if tile not in VALID:
                    pygame.draw.rect(background, (0, 0, 0), [TILE_WIDTH * x, TILE_HEIGHT * y, TILE_WIDTH, TILE_HEIGHT], 0)
                else:
                    triangs = [
                        ( MOVE_UP, [[x0, y0], [x1, y0], [xh, yh]] ),
                        ( MOVE_DOWN, [[x0, y1], [x1, y1], [xh, yh]] ),
                        ( MOVE_LEFT, [[x0, y0], [x0, y1], [xh, yh]] ),
                        ( MOVE_RIGHT, [[x1, y0], [x1, y1], [xh, yh]] ),
                    ]

                    for t in triangs:
                        act, poly = t
                        v = self.agt.exploration_function((x,y), act)
                        c = self.scale_range(v, self.min_expl, self.max_expl, 0, 255)
                        pygame.draw.polygon(background, (c,c,c), poly, 0)

        return background

    def draw_interactive(self):
        """
        Draw interactive states.
        """
        interactive = pygame.Surface((
            TILE_WIDTH * self.env.map_width,
            TILE_HEIGHT * self.env.map_height
        ), pygame.SRCALPHA, 32).convert_alpha()

        d = int(DEBUG())
        for x in xrange(self.env.map_width):
            for y in xrange(self.env.map_height):
                tile = self.env.map_data[x][y]
                if tile in INTERACTIVE:
                    interactive.blit(self.tileset[d][tile], (TILE_WIDTH * x, TILE_HEIGHT * y))
        return interactive

    def draw_around(self):
        """
        Draw walls.
        """
        around = pygame.Surface((
            TILE_WIDTH * (self.env.map_width + 2),
            TILE_HEIGHT * (self.env.map_height + 2)
        ), pygame.SRCALPHA, 32).convert_alpha()

        if DEBUG():
            around.fill((0, 0, 0))
            return around
        for x in xrange(self.env.map_width + 2):
            around.blit(self.tileset[0][TILE_CLOSED], (TILE_WIDTH * x, 0))
            around.blit(self.tileset[0][TILE_CLOSED], (TILE_WIDTH * x, TILE_HEIGHT * (self.env.map_height + 1)))
        for y in xrange(1, self.env.map_height + 2):
            around.blit(self.tileset[0][TILE_CLOSED], (TILE_WIDTH * 0, TILE_HEIGHT * y))
            around.blit(self.tileset[0][TILE_CLOSED], (TILE_WIDTH * (self.env.map_width + 1), TILE_HEIGHT * y))
        return around

    def scale_range(self, old_value, old_range_min, old_range_max, new_range_min, new_range_max):
        """
        Scale a value between ranges.
        """
        old_range = (old_range_max - old_range_min)  
        new_range = (new_range_max - new_range_min)  
        new_value = (((old_value - old_range_min) * new_range) / old_range) + new_range_min
        return new_value

    def load_image(self, filename):
        """
        Load image and set transparency.
        """
        img = pygame.image.load(os.path.join(PATH, "sprites", filename)).convert()
        img.set_colorkey((0, 128, 128))
        if ZOOM > 1:
            return pygame.transform.scale(img, (img.get_width() * ZOOM, img.get_height() * ZOOM))
        return img

    def setup_tiles(self):
        """
        Load and split tilesets.
        """        
        width = 5
        self.tileset = [[], []]
        image = self.load_image(TILESET)
        for x in range(width):
            self.tileset[0].append(image.subsurface((x * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)))
        image = self.load_image(TILESET_DEBUG)
        for x in range(width):
            self.tileset[1].append(image.subsurface((x * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)))

    def setup_agent(self):
        """
        Setup agent properties for GUI.
        """
        self.agent_action = None
        self.agent_max_pose = 4
        self.agent_max_animation = 8 / ZOOM
        self.agent_animation = 0
        self.agent_pose = 0
        self.agent_direction = MOVE_DOWN
        self.agent_image = [self.load_image(PLAYER), self.load_image(PLAYER_DEBUG)]
        self.agent_width = self.agent_image[0].get_width() / self.agent_max_pose
        self.agent_height = self.agent_image[0].get_height() / 4
        if self.agent_height > TILE_HEIGHT:
            self.agent_diff_height = self.agent_height - TILE_HEIGHT
        else:
            self.agent_diff_height = 0

    def compute_range(self):
        self.min_expl = float("inf")
        self.max_expl = float("-inf")
        for x in range(self.env.map_width):
            for y in range(self.env.map_height):
                for a in ACTIONS:
                    v = self.agt.exploration_function((x,y), a)
                    self.min_expl = min(self.min_expl, v)
                    self.max_expl = max(self.max_expl, v)

    def setup_agent_pos(self, sx, sy):
        """
        Setup agent position for GUI.
        """
        self.agent_x = sx * TILE_WIDTH
        self.agent_y = sy * TILE_HEIGHT - self.agent_diff_height

    def update_agent(self, surface):
        """
        Update agent animation.
        """
        d = int(DEBUG())
        img = self.agent_image[d]

        if self.agent_action == None:
            subsurface = img.subsurface((0, self.agent_direction * self.agent_height, self.agent_width, self.agent_height))
            surface.blit(subsurface, (self.agent_x + TILE_WIDTH, self.agent_y + TILE_HEIGHT))
            return False

        self.agent_direction = self.agent_action
        if self.agent_action == MOVE_UP:
            self.agent_y -= MOVE_SPEED
        elif self.agent_action == MOVE_DOWN:
            self.agent_y += MOVE_SPEED
        elif self.agent_action == MOVE_LEFT:
            self.agent_x -= MOVE_SPEED
        elif self.agent_action == MOVE_RIGHT:
            self.agent_x += MOVE_SPEED

        if self.agent_x % TILE_WIDTH == 0 and self.agent_y % TILE_HEIGHT == self.agent_diff_height:
            self.agent_action = None

        self.agent_animation += 1
        if self.agent_animation == self.agent_max_animation:
            self.agent_animation = 0
            self.agent_pose += 1
            if self.agent_pose == self.agent_max_pose:
                self.agent_pose = 0

        subsurface = img.subsurface((self.agent_pose * self.agent_width, self.agent_direction * self.agent_height, self.agent_width, self.agent_height))
        surface.blit(subsurface, (self.agent_x + TILE_WIDTH, self.agent_y + TILE_HEIGHT))

        return True

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('map', nargs='?', default=DEFAULT_MAP)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger()

    logger.info("Loading map: %s", args.map)  
    
    sx, sy, map_data, map_width, map_height = read_map(args.map)

    agt = Link()
    env = Environment(sx, sy, map_data, map_width, map_height)

    start_time = time.time()
    agt.train(env)
    elapsed_time = time.time() - start_time

    env.reset()
    agt.reset(env)

    logger.info("It took %.2f seconds to train.", elapsed_time)

    Game(env, agt)