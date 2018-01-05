from .node import Node


class Decision(Node):
    TYPE_NAME = "Decision"

    def typeName(self):
        return Decision.TYPE_NAME

    def computePossibilities(self, strategy: "Strategy"):
        for t in self.transitions:
            t.target.computePossibilities(strategy)

        idx, payout = strategy.selectBestReducedPayout(t.target.results.reducedPayout for t in self.transitions)

        choice = self.transitions[idx]
        self.results.choice = choice
        self.results.reducedPayout = choice.target.results.reducedPayout
        self.results.payoutDistribution = choice.target.results.payoutDistribution


from .transition import Transition
from .strategy import Strategy
