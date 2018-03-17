from collections import namedtuple
from numbers import Real

import pandas as pd

from .valueactualizer import ValueActualizer, SCALAR_ACTUALIZER


SCALAR_ZERO = 0
SERIES_ZERO = pd.Series()

Limit = namedtuple("Limit", ("name", "predicate"))



class Solver:

    def __init__(self, root: "Node", strategy: "Strategy", cashflowToValue: ValueActualizer = SCALAR_ACTUALIZER,
                 cashflowLimits=None, valueLimits=None, strategicValueLimits=None, cashflowDistributionLimits=None,
                 valueDistributionLimits=None, ) -> None:
        self.root = root  # type: Node
        self.strategy = strategy  # type: Strategy
        self.cashflowToValue = cashflowToValue


        def castLimits(limits):
            if limits is None:
                return []
            return [Limit(*l) for l in limits]


        self.cashflowLimits = castLimits(cashflowLimits)
        self.valueLimits = castLimits(valueLimits)
        self.strategicValueLimits = castLimits(strategicValueLimits)
        self.cashflowDistributionLimits = castLimits(cashflowDistributionLimits)
        self.valueDistributionLimits = castLimits(valueDistributionLimits)

        self.addPayouts = None
        self.hasCFSeries = None


    def solve(self):
        self.reset()

        root = self.root

        self.setCashflowType()
        root.createPlaceholders()

        if self.hasCFSeries:
            zero = SERIES_ZERO
        else:
            zero = SCALAR_ZERO

        root.propagateCashflows(self, zero)
        root.computePossibilities(self)
        root.propagateEndgameDistributions(1)


    def reset(self):
        def resetNode(node: Node):
            node.results = NodeHolder()

            for t in node.transitions:
                t.results = TransitionHolder()
                if isinstance(t.target, EndGame) and t.target.placeholder:
                    t.target = None
                elif t.target is not None:
                    resetNode(t.target)


        resetNode(self.root)

        self.addPayouts = None
        self.hasCFSeries = None


    def payoutDistribution(self, node: "Node" = None):

        if node is None: node = self.root

        df = pd.DataFrame(node.results.valueDistribution, columns=("probability", "value"))
        df = df.groupby("value").sum()

        return df


    def strategicValue(self):
        return self.root.results.strategicValue


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
                    return


    def getFailingLimits(self, node: "Node"):
        rv = []
        for name, limit in self.cashflowLimits:  # type: Limit
            for prob, cf in node.results.cashflowDistribution:
                fail, margin = limit(cf)
                if fail:
                    rv.append((name, margin))

        for limit in self.valueLimits:  # type: Limit
            for prob, v in node.results.valueDistribution:
                fail, margin = limit(v)
                if fail:
                    rv.append((name, margin))

        for limit in self.valueDistributionLimits:  # type: Limit
            fail, margin = limit(node.results.valueDistribution)
            if fail:
                rv.append((name, margin))

        for limit in self.cashflowDistributionLimits:  # type: Limit
            fail, margin = limit(node.results.cashflowDistribution)
            if fail:
                rv.append((name, margin))

        for limit in self.strategicValueLimits:  # type: Limit
            fail, margin = limit(node.results.strategicValue)
            if fail:
                rv.append((name, margin))

        return rv



from .strategy import Strategy
from .cashflow import combineCashflows
from . import Node, EndGame, NodeHolder, TransitionHolder
