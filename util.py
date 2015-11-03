import os, sys, time, inspect
from common import *

def read_map(filename):
    """
    Read map file, check its consistency, etc.
    """
    with open(os.path.join(PATH, filename)) as map_file:
        map_data = [[int(cell) for cell in row.rstrip()] for row in map_file]
        map_data = [list(x) for x in zip(*map_data)]
        map_width = len(map_data)
        map_height = len(map_data[0])
        for row in map_data:
            if len(row) != map_height:
                raise Exception("Map width does not match", map_height, len(row))
        for x in range(map_width):
            for y in range(map_height):
                cell = map_data[x][y]
                if cell not in ALL:
                    raise Exception("Unknown tile", cell)
                if cell == TILE_INIT:
                    map_data[x][y] = TILE_CLEAR
                    sx, sy = x, y
        return (sx, sy, map_data, map_width, map_height)

def successors(state, map_data, map_width, map_height):
    """
    Fetch valid successors for state.
    """
    n = []
    x, y = state
    if x - 1 >= 0 and map_data[x-1][y] != TILE_CLOSED:
        n.append((x-1,y))
    if x + 1 < map_width and map_data[x+1][y] != TILE_CLOSED:
        n.append((x+1,y))
    if y - 1 >= 0 and map_data[x][y-1] != TILE_CLOSED:
        n.append((x,y-1))
    if y + 1 < map_height and map_data[x][y+1] != TILE_CLOSED:
        n.append((x,y+1))
    return n

def direction(x1, y1, x2, y2):
    """
    Define which direction based on positions.
    """
    if x1 < x2:
        return MOVE_RIGHT
    elif x1 > x2:
        return MOVE_LEFT
    elif y1 < y2:
        return MOVE_DOWN
    elif y1 > y2:
    	return MOVE_UP
    else:
        return None
    raise Exception("Unknown direction", x1, y1, x2, y2)

def newstate(state, action):
    """
    Apply an action to a state.
    """
    if action == MOVE_UP:
        return (state[0], state[1]-1)
    if action == MOVE_DOWN:
        return (state[0], state[1]+1)
    if action == MOVE_LEFT:
        return (state[0]-1, state[1])
    if action == MOVE_RIGHT:
        return (state[0]+1, state[1])
    raise Exception("Unknown direction", x1, y1, x2, y2)

def orthogonal(action1, action2):
    """
    Check if action vectors are perpendicular.
    """
    vertical1 = action1 in [MOVE_UP, MOVE_DOWN]
    vertical2 = action2 in [MOVE_UP, MOVE_DOWN]
    return vertical1 != vertical2

def debug_map(env, stop=False):
    """
    Debug current environment.
    """
    for y in range(env.map_height):
        for x in range(env.map_width):
            if (x, y) == env.state:
                sys.stdout.write('X')
            elif (x, y) == env.init:
                sys.stdout.write('@')
            else:
                if env.map_data[x][y] == TILE_CLOSED:
                    sys.stdout.write(u"\u2588")
                elif env.map_data[x][y] == TILE_CLEAR:
                    sys.stdout.write(' ')
                elif env.map_data[x][y] in TERMINAL:
                    sys.stdout.write('#')
                else:
                    sys.stdout.write(str(env.map_data[x][y]))
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    stop and raw_input()

def argmax(seq, fn):
    best = best_score = None;
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best, best_score