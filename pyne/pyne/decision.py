from .node import Node



class Decision(Node):
    TYPE_NAME = "Decision"


    def typeName(self):
        return Decision.TYPE_NAME


    def computePossibilities(self, solver):
        for t in self.transitions:
            t.target.computePossibilities(solver)

        for t in self.transitions:
            if t.target.results.deadEnd:
                t.results.rejected = True

        ts = [t for t in self.transitions if not t.results.rejected]

        if not any(ts):
            self.results.deadEnd = True
            return

        idx, payout = solver.strategy.selectBestStrategicValue(t.target.results.strategicValue for t in ts)

        choice = ts[idx]
        self.results.choice = choice

        self.results.cashflowDistribution = choice.target.results.cashflowDistribution
        self.results.valueDistribution = choice.target.results.valueDistribution
        self.results.strategicValue = choice.target.results.strategicValue


    def propagateEndgameDistributions(self, currentProbability):
        super().propagateEndgameDistributions(currentProbability)
        for t in self.transitions:
            if t is self.results.choice:
                t.target.propagateEndgameDistributions(currentProbability)


    def clone(self):
        return Decision(self.name, [t.clone() for t in self.transitions])

# from .solver import Solver
