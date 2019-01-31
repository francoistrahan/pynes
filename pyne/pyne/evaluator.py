import numpy as np
import pandas as pd



class Evaluator:

    def __init__(self, solver, setters, getters):
        self.getters = getters
        self.setters = setters
        self.solver = solver

        self.nX = len(setters)
        self.nY = len(getters)


    def evaluate(self, X):
        for i in range(self.nX):
            self.setters[i](X[i])

        self.solver.solve()

        rv = list()
        for i in range(self.nY):
            rv.append(self.getters[i]())

        return rv


    def evaluateMany(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        nrow, ncol = dataFrame.shape

        if ncol != self.nX:
            raise ValueError("Got {} input columns, expected {}".format(ncol, self.nX, self.nY))

        dataFrame = dataFrame.copy()
        for i in range(self.nY):
            dataFrame["{}".format(i)] = np.nan

        for r in range(nrow):
            for c in range(self.nX):
                self.setters[c](dataFrame.iloc[r, c])

            self.solver.solve()

            for c in range(self.nY):
                dataFrame.iloc[r, c + self.nX] = self.getters[c]()

        return dataFrame
