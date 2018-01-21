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


    def propagatePayouts(self, solver, current):
        for t in self.transitions:
            t.propagatePayouts(current, solver)


    def getNodesFlat(self):
        yield self
        for t in self.transitions:
            if t.target is not None:
                yield from t.target.getNodesFlat()


    @abstractmethod
    def computePossibilities(self, strategy: "Strategy"):
        pass


    @abstractmethod
    def propagateEndgameDistribution(self, currentProbability):
        pass



from .transition import Transition
from . import NodeHolder
from .strategy import Strategy
