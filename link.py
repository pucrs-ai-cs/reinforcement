#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import math, copy, random, logging
from common import *
from util import *
from agent import *

class Link(Agent):

    def __init__(self):
        Agent.__init__(self)

    def update_utility(self, env):
        """
        Updates the learned utility values in the agent.

        Use self.utility_table to store values

        TODO implement your solution!

        """
        raise NotImplementedError

    def q_value(self, state, action):
        """
        Return the utility for an action and/or action.

        Use self.utility_table to retrieve values

        TODO implement your solution!

        """
        raise NotImplementedError