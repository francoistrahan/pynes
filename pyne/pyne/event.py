
from .node import Node



class Event(Node):

    TYPE_NAME = "Event"


    def __init__(self, name: str, transitions=None):
        super().__init__(name, transitions)


    def typeName(self):
        return Event.TYPE_NAME


    def computePossibilities(self, decisionStrategy):
        ts=self.transitions # type: list[Transition]

        # Check probabilities and patch if we have a complement
        # This could be optimised out to an init step. Keeping it separated from actual calculation
        probs = [t.probability for t in ts]
        nnprobs = [p for p in probs if p is not None]
        nNones = len(probs) - len(nnprobs)

        if nNones > 1: raise ValueError("Cannot have more than one event without explicit probability")

        totalProb = sum(nnprobs)
        if totalProb > 1: raise ValueError("Total probabilites exceed 100%")

        if nNones == 1:
            pComplement = 1 - totalProb
            totalProb = 1

        possibilities = [] # Could be a pipeline, but i expect to be interested into this at each point
        for t in ts:
            transitionProb = t.probability
            if transitionProb is None: transitionProb = pComplement

            for prob,outcome in t.target.computeOutputs(decisionStrategy):
                possibilities.append((transitionProb*prob, outcome))

        return possibilities










from .transition import Transition
