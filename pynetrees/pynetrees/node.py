from abc import ABCMeta, abstractmethod
from typing import Sequence



class Node(metaclass=ABCMeta):

    def __init__(self, name: str, transitions: "Sequence[Transition]" = None):
        self.name = name
        self.transitions = transitions or []  # type: Sequence[Transition]
        self.results = NodeHolder()


    @abstractmethod
    def typeName(self):
        pass


    def __str__(self) -> str:
        return "{}: {}".format(self.typeName(), self.name)


    def createPlaceholders(self):
        rv = 0
        for t in self.transitions:
            rv += t.createPlaceHolders()
        return rv


    def propagateCashflows(self, solver, current):
        for t in self.transitions:
            t.propagateCashflows(current, solver)


    def getNodesFlat(self):
        yield self
        for t in self.transitions:
            if t.target is not None:
                yield from t.target.getNodesFlat()


    def transit(self, *transitionNames) -> "Transition":
        if not transitionNames: raise ValueError("Need at least one transition name")

        target = self
        for name in transitionNames:
            try:
                trans = next(t for t in target.transitions if t.name == name)
            except StopIteration:
                raise KeyError("Node {} has no transition called {}".format(target.name, name))
            target = trans.target

        return trans


    @abstractmethod
    def computePossibilities(self, solver: "Solver"):
        pass


    def propagateEndgameDistributions(self, currentProbability):
        self.results.probability = currentProbability


    @abstractmethod
    def clone(self):
        pass



from .transition import Transition
from . import NodeHolder
