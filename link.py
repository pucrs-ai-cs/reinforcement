#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import math, copy, random, logging
import qvalue
from qvalue import *
from common import *
from util import *
from agent import *
from state import *

class Link(Agent):

    def __init__(self):

        Agent.__init__(self)
        self.q_values = dict()
        self.frequency = dict()
        self.prev_qtable = dict()
        self.p_state = self.p_action = self.p_reward = self.state = self.action = self.reward = None
        self.gamma = 0.9
        self.env = None

    
    ################-------------------###################

    def train(self, env):
        """
        Execute MAX_TRAINING_EPISODES rounds or until converge.
        TODO: you can change this method to log executions
        """

        logging.getLogger().debug("It will converge at %f", CONVERGENCE_THRESHOLD)

        self.reset(env)
        self.env = env
        executions = 0
        while executions < MAX_TRAINING_EPISODES:
            action = self.run_train(self.state)
            self.env.execute(action)
            if env.terminal(env.state):
                executions += 1
                
                self.reset(env)

                if self.converged():
                    break
                else:
                    self.prev_qtable = copy.deepcopy(self.q_values)

                logging.getLogger().debug("Episode %d: convergence %f", executions, self.convergence)

        logging.getLogger().info("Episode %d: converged at %f", executions, self.convergence)

    def alpha(self, qv):
        """
        Learning rate
        TODO: set a learning rate function or a fixed number
        """
        raise NotImplementedError
        
    
    def reset(self, game):
        self.p_state = self.p_action = self.p_reward = self.state = self.action = self.reward = None

    def f(self, qv):
        """
        Exploration function
        TODO: implement a exploration function
        """
        raise NotImplementedError 

        
    def max_action(self, state):
        """
        Return value of the best possible action
        TODO: implement a function to return the value of the 
        best possible action in  a given state
        """
        raise NotImplementedError

    def argmax(self, state):
        """
        Return the best possible action
        TODO: implement a function to return the best action 
        to a given state. Remember to use the exploration function.
        """        
        raise NotImplementedError


    def make_state(self, env):
        """
        Using the information in the environment, a state with the relevant information is built
        TODO: create a state represenstation
        """
        raise NotImplementedError


    def converged(self):
        """
        Return True if the change between previous util table and current util table
        are smaller than the convergence_threshold.
        """
        self.convergence = self.convergence_metric()
        return self.convergence < CONVERGENCE_THRESHOLD

    def run(self, env):
        """
        Execute the best action without applying learning.
        """
        self.action = self.argmax(self.make_state(env))
        self.state, self.reward = env.execute(self.action)
        return self.action, self.state


    def run_train(self, env):
        """
        Execute actions and learn. 
        TODO: Implement Q-Learning here
        """
        self.state = self.make_state(env)
        raise NotImplementedError

    def convergence_metric(self):
        """
        Return the convergence metric.
        """
        prev = sum(self.prev_qtable.values())
        curr = sum(self.q_values.values())
        return math.sqrt(abs(curr - prev))
