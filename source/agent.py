class Agent:

  def __init__(self, init_strategy, location, radius, idx, nagents):
    self.strategy = init_strategy
    #self.color = self.colors[self.strategy_transition]
    self.color = ""
    self.location = location
    self.neighbors = self.find_neighbors(radius)
    self.idx = idx
    self.game_log = [0 for _ in range(nagents)]

  def find_neighbors(self, radius):
    neighb_locations = []
    for xdis in range(-radius, radius + 1):
      for ydis in range(-radius, radius + 1):
        new_neighb = [self.location[0] + xdis, self.location[1] + ydis]

        neighb_locations.append(new_neighb)
    self.neighbors = neighb_locations
    #neighb_locations.remove(self.location)
    return neighb_locations

  def play(self):
    "Returns 1 for cooperate and 0 for defect"
    return self.strategy

