class Solver:

    def __init__(self, root: "Node", strategy: "Strategy") -> None:
        self.root = root
        self.strategy = strategy


    def solve(self):
        root = self.root
        root.createPlaceholders()
        root.propagatePayouts(0)
        root.computePossibilities(self.strategy)
        root.propagateEndgameDistribution(1)



from .node import Node
from .strategy import Strategy
