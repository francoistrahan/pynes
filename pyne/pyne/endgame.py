from .node import Node



class EndGame(Node):
    TYPE_NAME = "EndGame"
    DEFAULT_NAME = "Done"


    def __init__(self, name: str = None, placeholder: bool = False):
        super().__init__(name or EndGame.DEFAULT_NAME)

        self.placeholder = placeholder


    def typeName(self):
        return EndGame.TYPE_NAME


    def cashflow(self):
        return self.results.propagatedCashflow


    def propagateCashflows(self, solver, current):
        self.results.propagatedCashflow = current
        self.results.propagatedValue = solver.cashflowToValue.actualize(current)


    def computePossibilities(self, solver: "Solver"):
        self.results.cashflowDistribution = ((1, self.results.propagatedCashflow),)

        self.results.valueDistribution = ((1, self.results.propagatedValue),)

        self.results.strategicValue = solver.strategy.computeStrategicValue(self.results.valueDistribution)

        failures = solver.getFailingLimits(self)
        if failures:
            self.results.failures = failures
            self.results.deadEnd = True

    def clone(self):
        rv = EndGame(self.name, self.placeholder)

# from .solver import Solver
