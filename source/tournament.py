from simulate import colors
from agent import Agent
import numpy as np
import random
import copy
from scipy.spatial.distance import jensenshannon


class Tournament:

    def __init__(self, args):
        "Initialize tournament object."
        self.benefit = args.benefit
        self.grid_length = args.grid_length
        self.game = args.game
        self.radius = args.radius

        self.create_agents(args.init_coop, args.grid_length)
        self.payoffs = self.create_payoffs()
        self.well_mixed = args.well_mixed
        self.counter = 0

        self.rounds = args.rounds
        self.inter_per_round = args.inter_per_round

    def create_agents(self, init_coop, grid_length):
        # randomly sample location of initial cooperators
        self.agents = []
        self.nagents = self.grid_length*self.grid_length
        num_coop = int(np.floor(self.nagents * init_coop))

        # put agents in random positions in the grid
        agent_positions = random.sample(list(range(self.grid_length * self.grid_length)), self.nagents)
        coop_indexes = random.sample(agent_positions, num_coop)

        if init_coop == 0.999:
            coop_indexes = list(range(self.nagents))
            x = y = np.ceil(int(self.grid_length / 2))

            coop_indexes.remove(x + y * self.grid_length)
        for index, i in enumerate(agent_positions):
            location = [i % grid_length, i // grid_length]
            init_strategy = (i in coop_indexes)

            agent = Agent(nagents=self.nagents, idx=index, location=location, init_strategy=init_strategy,
                          radius=self.radius)
            self.agents.append(agent)

    def create_payoffs(self):
        if self.game == "PD":
            #payoffs = {'R': self.benefit - self.cost, 'P': 0, 'T': self.benefit, 'S': -self.cost}
            payoffs = {'R': 1, 'P': 0, 'T': self.benefit, 'S': 0}
        elif self.game == "Snow":
            #payoffs = {'R': self.benefit - self.cost / 2, 'P': 0, 'T': self.benefit, 'S': self.benefit - self.cost}
            payoffs = {'R': 1, 'P': 0, 'T': self.benefit, 'S': 2 - self.benefit}
        return payoffs

    def actions_to_outcome(self, action_a, action_b):
        """Converts the binary strategies to the outcome of the game. Possible outcomes are R (reward), S (sucker),
    T (traitor?), P (punishment)"""
        if action_a and action_b:
            return 'R'
        elif not action_a and not action_b:
            return 'P'
        elif action_a and not action_b:
            return 'S'
        else:
            return 'T'

    def move_day(self, prob_move, replace=False):
        " Move agents during the day."
        for idx, a_move in enumerate(self.agents):
            epsilon = random.random()
            if epsilon < prob_move:

                # if replace:
                #   new_idx = random.sample(list(range(self.grid_length*self.grid_length)), 1)[0]
                #   new_loc = [new_idx % self.grid_length, new_idx // self.grid_length]
                #   #print("moving from ", a_move.location, "to ", new_loc )
                # else:
                #   x_move = random.sample(list(range(-self.radius, self.radius + 1)), 1)[0]
                #   y_move = random.sample(list(range(-self.radius, self.radius + 1)), 1)[0]
                #   new_loc = [(a_move.location[0] + x_move) % self.grid_length,
                #              (a_move.location[1] + y_move) % self.grid_length]

                x_move = random.sample(list(range(-self.radius, self.radius + 1)), 1)[0]
                y_move = random.sample(list(range(-self.radius, self.radius + 1)), 1)[0]
                new_loc = [(a_move.location[0] + x_move) % self.grid_length,
                           (a_move.location[1] + y_move) % self.grid_length]

                filled = False
                for idx2, agent in enumerate(self.agents):
                    if agent.location == new_loc:
                        filled = True
                        if replace:
                            agent.location = a_move.location
                            agent.find_neighbors(self.radius)
                            self.agents[idx2] = agent
                            a_move.location = new_loc
                            # a_move.find_neighbors(self.radius)
                            self.agents[idx] = a_move
                if not filled:
                    a_move.location = new_loc
                    # a_move.find_neighbors(self.radius)
                    self.agents[idx] = a_move

        for idx in range(len(self.agents)):
            self.agents[idx].find_neighbors(self.radius)
    def compete(self):
        for central_agent in self.agents:
            central_agent.value = 0

            if self.well_mixed:
                neighbors = random.sample(self.agents, self.inter_per_round)
            else:
                neighbor_locs = central_agent.neighbors
                neighbors = []
                for neighbor_loc in neighbor_locs:
                    # out = [el % self.grid_length for el in neighbor_loc]
                    out = [1 if el >= 0 and el < self.grid_length else 0 for el in neighbor_loc]
                    if 0 not in out:
                        for agent in self.agents:
                            if agent.location == neighbor_loc:
                                neighbors.append(agent)

            for neighbor in neighbors:
                # print("new battle")

                # print(central_agent.idx, neighbor.idx)
                action_a = central_agent.play()

                # find neighbor based on his location
                action_b = neighbor.play()
                # neighbor.game_log[central_agent.idx] += 1
                central_agent.game_log[neighbor.idx] += 1
                outcome = self.actions_to_outcome(action_a, action_b)
                payoff = self.payoffs[outcome]
                central_agent.value += payoff



        prev_agents = copy.deepcopy(self.agents)
        for idx, central_agent in enumerate(prev_agents):

            max_value = central_agent.value
            winner_strat = central_agent.strategy
            # if not central_agent.strategy:
            #   print(central_agent.value)
            if self.well_mixed:
                neighbors = random.sample(self.agents, 8)
            else:
                neighbor_locs = central_agent.neighbors
                neighbors = []
                for neighbor_loc in neighbor_locs:
                    # folding
                    out = [el % self.grid_length for el in neighbor_loc]
                    # out = [1 if el > 0 and el < self.grid_length else 0 for el in neighbor_loc]
                    for agent in prev_agents:
                        if agent.location == neighbor_loc:
                            neighbors.append(agent)
            for neighbor in neighbors:

                if neighbor.value > max_value:
                    max_value = neighbor.value
                    winner_strat = neighbor.strategy
                    # print("changing agent ",central_agent.idx, central_agent.location, neighbor.location )

            self.agents[idx].transition = self.encode_transition(central_agent.strategy,
                                                                 winner_strat)
            self.agents[idx].strategy = winner_strat

    def play_round(self):
        # move agents according to day/night

        self.compete()
        # for agent in self.agents:
        #   agent.transition = self.encode_transition( agent.strategy, agent.strategy)
        #

        # self.agents = copy.deepcopy(prev_agents)
        log = self.collect_log()
        return log

    def encode_transition(self, prev_strat, current_strat):
        if prev_strat and current_strat:
            return 0
        elif not prev_strat and not current_strat:
            return 1
        elif not prev_strat and current_strat:
            return 2
        else:
            return 3

    def collect_log(self):
        log = {}
        width = self.grid_length
        strat_transitions = np.ones(shape=(width, width)) * 4
        for agent in self.agents:
            loc = agent.location
            strat_trans = agent.transition
            strat_transitions[loc[0], loc[1]] = strat_trans
        log["strat_transitions"] = strat_transitions

        return log

    def pop_log(self):
        log = {}
        coop_perc = np.sum([1 for agent in self.agents if agent.strategy]) / len(self.agents)
        log["coop_perc"] = coop_perc
        uniform = [self.rounds * self.inter_per_round / (len(self.agents)) for agent in self.agents]
        distances = []

        for agent in self.agents:
            distr = [el for el in agent.game_log]
            distances.append(jensenshannon(distr, uniform))
        log["uniform_day"] = np.mean(distances)
        log["uniform_day"] = np.mean([jensenshannon(agent.game_log, uniform) for agent in self.agents])
        return log
