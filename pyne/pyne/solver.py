class Solver:

    def __init__(self, root: "Node", strategy: "Strategy") -> None:
        self.root = root  # type: Node
        self.strategy = strategy  # type: Strategy


    def solve(self):
        root = self.root
        root.createPlaceholders()
        root.propagatePayouts(0)
        root.computePossibilities(self.strategy)
        root.propagateEndgameDistribution(1)


    def reset(self):
        def reset(node: Node):
            node.results.clearResults()
            for t in node.transitions:
                t.results.clearResults()
                if isinstance(t.target, EndGame) and t.target.placeholder:
                    t.target = None
                else:
                    reset(t.target)


        reset(self.root)


    def payoutDistribution(self):
        return self.root.results.payoutDistribution



from . import Node, EndGame
from .strategy import Strategy
