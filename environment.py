#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import random
import sys
import math
import copy
import time
from common import *
from agent import *

class Environment:

    def __init__(self, x, y, map_data, map_width, map_height):
        self.init_x     =  self.x = x
        self.init_y     =  self.y = y
        self.map_data   = map_data
        self.map_width  = map_width
        self.map_height = map_height
        self.restart    = False
        self.rewards    = {
            TILE_CLEAR        : -0.1,
            TILE_CLOSED       : -1,
            TILE_CHEST_CLOSED : 50,
            TILE_BLUE_RUPEE   : 5
        }
        self.rupees = []
        self.agent  = Agent()
        self.convergence_threshold = 0.00001
        self.previous_u = {}

    def train(self):
        # Execute MAX_TRAINING_EPISODES rounds or until converge
        executions = 0
        while executions < MAX_TRAINING_EPISODES:
            state, restart = self.update()
            if restart:
                executions += 1
                if self.converged(self.previous_u, self.agent.get_utility_table()):
                    print "Converged! Round: ", executions
                    break
                else:
                    self.previous_u = copy.deepcopy(self.agent.get_utility_table())
        
    def root_mean_square_difference(self, previous_u, current_u):
        # sum = 0
        sub = (sum(previous_u.values()) - sum(current_u.values()))**2
        return math.sqrt(sub)
        
                
    def converged(self, value1, value2):
        # Return True if the change between value1 and value2 are smaller than the convergence_threshold
        if self.root_mean_square_difference(value1,value2) < self.convergence_threshold:
            return True
        else:
            return False

    def update(self):
        # Update the agent current state based on the agent action        
        state = (self.x, self.y)
        reward = self.rewards[self.map_data[self.y][self.x]]
        action = self.agent.rl_update(state, reward)

        if self.map_data[self.y][self.x] == TILE_BLUE_RUPEE:
            # If the agent is in a state with a ruppe, it turns into a TILE_CLEAR
            self.rupees.append((self.y, self.x))
            self.map_data[self.y][self.x] = TILE_CLEAR

        if action != None:
            # If agent is not in a terminal state
            new_state = self.compute_action_result(state, action)
            self.restart = False
            self.x = new_state[0]
            self.y = new_state[1]

            return (new_state, self.restart)
        else:
            # Agent returned None
            return self.reset()

    def reset(self):
        # Reset the agent to the initial state
        self.restart = True
        reset = (self.init_x, self.init_y)
        self.x, self.y = self.init_x, self.init_y
        for rupee in self.rupees:
            self.map_data[rupee[0]][rupee[1]] = TILE_BLUE_RUPEE

        self.rupee = []        
        return (reset, self.restart)
        
    def compute_action_result(self, state, action):
        # Compute the resulting state given the action probabilities
        die = random.random()
        succ = self.successor_states(state,action)
        prob = 0
        for s,p in succ:
            prob += p
            if die <= prob:
                return s

    def successor_states(self, state, action):
        # return a list with states and probs [((state[0]+1,state[1]),0.5)]
        succ_states = []
        available_states = self.available_actions(state)

        prob = 0        

        if action < 2:
            if action == MOVE_LEFT:
                if action in available_states:
                    succ_states.append(((state[0]-1, state[1]), HIGH_PROB))
                else:
                    prob += HIGH_PROB

            else:#if action == MOVE_RIGHT:
                if action in available_states:
                    succ_states.append(((state[0]+1, state[1]), HIGH_PROB))
                else:
                    prob += HIGH_PROB

            if MOVE_UP in available_states:                
                succ_states.append(((state[0], state[1]-1), LOW_PROB))
            else:
                prob += LOW_PROB

            if MOVE_DOWN in available_states:
                succ_states.append(((state[0], state[1]+1), LOW_PROB))
            else:
                prob += LOW_PROB

            if prob > 0:
                succ_states.append(((state[0], state[1]), prob))

        elif action < 4:
            if action == MOVE_UP:
                if action in available_states:
                    succ_states.append(((state[0], state[1]-1), HIGH_PROB))
                else:
                    prob += HIGH_PROB

            else:#if action == MOVE_DOWN:
                if action in available_states:
                    succ_states.append(((state[0], state[1]+1), HIGH_PROB))
                else:
                    prob += HIGH_PROB

            if MOVE_LEFT in available_states:                
                succ_states.append(((state[0]-1, state[1]), LOW_PROB))
            else:
                prob += LOW_PROB

            if MOVE_RIGHT in available_states:
                succ_states.append(((state[0]+1, state[1]), LOW_PROB))
            else:
                prob += LOW_PROB

            if prob > 0:
                succ_states.append(((state[0], state[1]), prob))

        else:
            raise "Unknown action"
            
        return succ_states

    def available_actions(self, state):
        # Return list of available actions at state
        available_actions = []
        succ_list = successors(state[0], state[1], self.map_data, self.map_width, self.map_height)
        for succ_state in succ_list:
            action = direction(state[0], state[1], succ_state[0], succ_state[1])
            available_actions.append(action)

        return available_actions    


if __name__ == "__main__":
    if len(sys.argv) == 2:
        map_name = sys.argv[1]
    else:
        map_name = DEFAULT_MAP
    print "Loading map: " + map_name
    
    sx, sy, map_data, map_width, map_height = read_map(map_name)

    env = Environment(sx, sy, map_data, map_width, map_height)

    start_time = time.time()
    env.train()
    elapsed_time = time.time() - start_time
    print "It took %.2f seconds to train." %elapsed_time