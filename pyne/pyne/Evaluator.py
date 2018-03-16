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
