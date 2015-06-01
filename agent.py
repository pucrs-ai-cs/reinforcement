#!/usr/bin/env python
# Four spaces as indentation [no tabs]
from common import *

class Agent:

    def __init__(self):
    	# TODO Initialize your attributtes here if needed 
    	self.actions = [MOVE_RIGHT, MOVE_LEFT, MOVE_UP, MOVE_DOWN]
    	pass
	
	"""Returns the table containg the computed utilities so far. If you are using TDRL, this is your U table, if you are using Q-learning, this is the table of the Q-values, and so on."""
    def get_utility_table(self):
    	#TODO return a hash table
    	return {}

    """ Updates the learned utility values in the agent and returns the """
    def rl_update(self, state, reward):
        # TODO Return an action to the environment given the state
        # If terminal state, return None

        pass