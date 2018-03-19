from collections import namedtuple

import pandas as pd


LOW = "Low"
HIGH = "High"
EXTREMUM_NAMES = [LOW, HIGH]

Variable = namedtuple("Variable", ["name", "setter", "base", "domain"])
Output = namedtuple("Output", "name getter".split())



class SensitivityAnalysis:

    def __init__(self, solver: "Solver", variables: "list(Variable)", outputs: "list(Output)"):
        self.outputs = outputs
        self.variables = variables
        self.solver = solver

        self.variableNames = [v.name for v in self.variables]
        self.outputNames = [out.name for out in self.outputs]
        self.outputGetters = [out.getter for out in self.outputs]

        self.extremums = pd.DataFrame(
            index=[v.name for v in self.variables],
            columns=(pd.MultiIndex.from_product((self.outputNames, EXTREMUM_NAMES)))
        )

        for var in self.variables:
            var.setter(var.base)

        self.solver.solve()

        self.baseValues = pd.DataFrame(index=self.outputNames, columns=["base"])
        for out in self.outputs:
            self.baseValues.loc[out.name, "base"] = out.getter()


        self.individualResponses = dict()
        for var in self.variables:  # type: Variable
            X = pd.DataFrame(var.domain)

            evaluator = Evaluator(self.solver, [var.setter], self.outputGetters)
            Y = evaluator.evaluateMany(X)

            Y.columns = [var.name] + self.outputNames

            self.individualResponses[var.name] = Y

            mins = Y.min()
            maxs = Y.max()

            for on in self.outputNames:
                self.extremums.loc[var.name, (on, LOW)] = mins[on]
                self.extremums.loc[var.name, (on, HIGH)] = maxs[on]
            var.setter(var.base)



from . import Solver, Evaluator
