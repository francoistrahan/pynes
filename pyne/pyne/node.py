from abc import ABCMeta, abstractmethod
from typing import Sequence


class Node(metaclass=ABCMeta):
    def __init__(self, name: str, transitions: "Sequence[Transition]" = None):
        self.name = name
        self.transitions = transitions or []  # type: Sequence[Transition]
        self.results = Holder()

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

    def propagatePayouts(self, current):
        for t in self.transitions:
            t.propagatePayouts(current)

    def getNodesFlat(self):
        yield self
        for t in self.transitions:
            yield from t.target.getNodesFlat()

    @abstractmethod
    def computePossibilities(self, strategy: "Strategy"):
        pass

    @abstractmethod
    def propagateEndgameDistribution(self, currentProbability):
        pass


from .transition import Transition
from . import Holder
from .strategy import Strategy
