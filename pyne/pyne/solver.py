from numbers import Real

import pandas as pd


SCALAR_ZERO = 0
SERIES_ZERO = pd.Series()



class Solver:

    def __init__(self, root: "Node", strategy: "Strategy") -> None:
        self.root = root  # type: Node
        self.strategy = strategy  # type: Strategy
        self.addPayouts = None
        self.hasCFSeries = None


    def solve(self):
        root = self.root
        self.setCashflowType()
        root.createPlaceholders()

        if self.hasCFSeries:
            zero = SERIES_ZERO
        else:
            zero = SCALAR_ZERO

        root.propagatePayouts(self, zero)
        root.computePossibilities(self.strategy)
        root.propagateEndgameDistribution(1)


    def reset(self):
        def resetNode(node: Node):
            node.results.clearResults()
            for t in node.transitions:
                t.results.clearResults()
                if isinstance(t.target, EndGame) and t.target.placeholder:
                    t.target = None
                else:
                    reset(t.target)


        resetNode(self.root)

        self.addPayouts = None
        self.hasCFSeries = None


    def payoutDistribution(self, node: "Node" = None):

        if node is None: node = self.root

        df = pd.DataFrame(node.results.payoutDistribution, columns=("probability", "reducedPayout"))
        df = df.groupby("reducedPayout").sum()

        return df


    def reducedPayout(self):
        return self.root.results.reducedPayout


    def addPayoutsScalar(self, *payouts):
        payouts = [p for p in payouts if p is not None]

        if not payouts: return None

        return sum(payouts)


    def addPayoutsSeries(self, *payouts):
        payouts = [p for p in payouts if p is not None]

        if not payouts: return None

        return combineCashflows(payouts)


    def setCashflowType(self):
        for n in self.root.getNodesFlat():
            for t in n.transitions:
                if t.payout is not None:
                    if isinstance(t.payout, Real):
                        self.addPayouts = self.addPayoutsScalar
                        self.hasCFSeries = False
                    else:
                        self.addPayouts = self.addPayoutsSeries
                        self.hasCFSeries = True



from . import Node, EndGame
from .strategy import Strategy
from .cashflow import combineCashflows
