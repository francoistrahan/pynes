from collections import namedtuple

import pandas as pd


MIN = "Min"
MAX = "Max"
EXTREMUMS = [MIN, MAX]

Variable = namedtuple("Variable", ["name", "setter", "base", "domain"])
Output = namedtuple("Output", "name getter".split())



def analysis(solver: "Solver", variables: "list(Variable)", outputs: "list(Output)"):
    outputNames = [out.name for out in outputs]
    outputGetters = [out.getter for out in outputs]

    df = pd.DataFrame(
        index=[v.name for v in variables],
        columns=(pd.MultiIndex.from_product((outputNames, EXTREMUMS)))
    )

    for var in variables:
        var.setter(var.base)

    

    for var in variables:  # type: Variable
        X = pd.DataFrame(var.domain)
        evaluator = Evaluator(solver, [var.setter], outputGetters)
        Y = evaluator.evaluateMany(X)
        print(var.name)
        Y = Y.drop(columns=0) # type: pd.DataFrame
        Y.columns = outputNames

        mins = Y.min()
        maxs = Y.max()

        for on in outputNames:
            df.loc[var.name, (on, MIN)] = mins[on]
            df.loc[var.name, (on, MAX)] = maxs[on]
        var.setter(var.base)
    print(df)



from . import Solver, Evaluator
