#!/usr/bin/env python
# Four spaces as indentation [no tabs]
import math, copy, random, logging
from common import *
from util import *

class Agent:

    def __init__(self):
        self.s = self.a = self.r = None
        self.utility_table = {}
        self.prev_utility_table = {}

    def reset(self, env):
        self.s = env.init

    def train(self, env):
        """
        Execute MAX_TRAINING_EPISODES rounds or until converge.
        """

        logging.getLogger().debug("It will converge at %f", CONVERGENCE_THRESHOLD)

        self.reset(env)

        executions = 0
        while executions < MAX_TRAINING_EPISODES:

            self.prev_s, self.prev_a, self.prev_r = self.s, self.a, self.r

            self.run_train(env)

            if env.terminal(self.s):

                executions += 1
                
                self.prev_s = self.prev_a = self.prev_r = self.s = self.a = self.r = None
                self.reset(env)

                if self.converged():
                    break
                else:
                    self.prev_utility_table = copy.deepcopy(self.utility_table)

                logging.getLogger().debug("Episode %d: convergence %f", executions, self.convergence)

        logging.getLogger().info("Episode %d: converged at %f", executions, self.convergence)

    def converged(self):
        """
        Return True if the change between previous util table and current util table
        are smaller than the convergence_threshold.
        """
        self.convergence = self.convergence_metric()
        return self.convergence < CONVERGENCE_THRESHOLD

    def run(self, env):
        """
        Execute actions.
        """
        self.a, _ = self.choose_action(env, self.s)
        self.s, self.r = env.execute(self.a)
        return self.a, self.s

    def run_train(self, env):
        """
        Execute actions and learn.
        """
        self.run(env)
        if self.prev_s is not None:
            self.update_utility(env)

    def choose_action(self, env, state):
        """
        Return an action and the learned reward by maximizing reward.
        """
        return argmax(ACTIONS, lambda action: self.exploration_function(state, action))

    def convergence_metric(self):
        """
        Return the convergence metric.
        """
        prev = sum(self.prev_utility_table.values())
        curr = sum(self.utility_table.values())
        return math.sqrt(abs(curr - prev))

    def exploration_function(self, state, action):
        return 0

    def update_utility(self):
        pass
