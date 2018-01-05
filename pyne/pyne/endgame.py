from .node import Node


class EndGame(Node):
    TYPE_NAME = "EndGame"
    DEFAULT_NAME = "Done"

    def __init__(self, name: str = None, placeholder: bool = False):
        super().__init__(name or EndGame.DEFAULT_NAME)

        self.placeholder = placeholder

    def typeName(self):
        return EndGame.TYPE_NAME

    def payout(self):
        return self.results.propagatedPayout

    def propagatePayouts(self, current):
        self.results.propagatedPayout = current

    def computePossibilities(self, strategy):
        self.results.payoutDistribution = ((1, self.results.propagatedPayout),)
        self.results.reducedPayout = strategy.reducePayouts(self.results.payoutDistribution)
