class Transition:

    def __init__(self, name, payout=None, probability=None, target: "Node" = None) -> None:
        if probability is not None and probability < 0: raise ValueError("Probability cannot be negative")

        self.name = name
        self.payout = payout
        self.target = target
        self.probability = probability
        self.results = TransitionHolder()


    def __str__(self) -> str:
        rv = "Transition: {}".format(self.name)

        details = []
        if self.probability is not None:
            details.append("p={:.4%}".format(self.probability))
        if self.payout is not None:
            details.append("impact={}".format(self.payout))

        details = ", ".join(details)
        if details:
            rv = "{} ({})".format(rv, details)

        return rv


    def createPlaceHolders(self):
        if self.target is None:
            self.target = EndGame(placeholder=True)
            return 1
        else:
            return self.target.createPlaceholders()


    def propagatePayouts(self, current, solver):
        current = solver.addPayouts(current, self.payout)
        return self.target.propagatePayouts(solver, current)



from .endgame import EndGame
from .node import Node
from . import TransitionHolder
