# -*- coding: UTF-8 -*-

import threading
import random
import time


class CostGenerator:

    def __init__(self, start_cost, tick_cost_rate, tick_period):
        self.cost = start_cost
        self.tick_cost_rate = tick_cost_rate
        self.tick_period = tick_period

    def _generate_cost(self):
        res = -1

        while res < 0:
            res = random.random() * self.tick_cost_rate
            res = (self.cost - res) if random.choice([0, 1]) == 0 else (self.cost + res)
            print(res)

        self.cost = res  # save new cost for the next generator invocations

    def __call__(self):
        self._generate_cost()
        return self.cost
