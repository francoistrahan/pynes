from collections import namedtuple
from itertools import product

import matplotlib.pyplot as plt
import pandas as pd


IMPACT_COLORS_DIRECT = ("red", "green")
IMPACT_COLORS_REVERSED = list(reversed(IMPACT_COLORS_DIRECT))

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


    def getImpactGraphs(self, invertColors=False, grid=False):

        colors = invertColors and IMPACT_COLORS_REVERSED or IMPACT_COLORS_DIRECT

        rv = dict()
        for outname in self.outputNames:
            exts = self.extremums[outname]
            base = self.baseValues.base[outname]
            exts = exts - base

            fig, ax = plt.subplots(1, 1)
            assert isinstance(fig, plt.Figure)

            exts.plot.barh(stacked=True, left=base, color=colors, ax=ax)
            ax.set(title=outname)
            ax.axvline(base, c="black", label="Base")
            ax.grid(grid)
            ax.legend()

            rv[outname] = fig

        return rv


    def getIndivisualResponseGraphs(self, figScale=(5, 5), hideExtraXLabels=False, hideExtraYLabels=False, grid=True):

        nrow = len(self.outputNames)
        ncol = len(self.variableNames)

        fig, axs = plt.subplots(nrow, ncol, figsize=(figScale[0] * ncol, figScale[1] * nrow))

        for r, c in product(range(nrow), range(ncol)):
            oname = self.outputNames[r]
            vname = self.variableNames[c]
            ax = axs[r][c]
            self.individualResponses[vname].plot.scatter(ax=ax, x=vname, y=oname)
            ax.grid(grid)

            if r == nrow - 1:
                ax.set(xlabel=vname)
            elif hideExtraXLabels:
                ax.set(xlabel="", xticklabels=[])

            if c == 0:
                ax.set(ylabel=oname)
            elif hideExtraYLabels:
                ax.set(ylabel="", yticklabels=[])

        for r in range(nrow):
            rowmin = min(ax.get_ylim()[0] for ax in axs[r])
            rowmax = max(ax.get_ylim()[1] for ax in axs[r])
            for c in range(ncol):
                axs[r][c].set(ylim=((rowmin, rowmax)))

        for c in range(ncol):
            colmin = min(axs[r][c].get_xlim()[0] for r in range(nrow))
            colmax = max(axs[r][c].get_xlim()[1] for r in range(nrow))
            for r in range(nrow):
                axs[r][c].set(xlim=((colmin, colmax)))

        return fig, axs



from . import Solver, Evaluator
