__all__ = ["Decision", "Event", "Transition", "EndGame", "Node", "Solver", "Evaluator"]



class Holder:

    def clear(self):
        d = self.__dict__
        for k in d.keys():
            d[k] = None



class NodeHolder(Holder):

    def __init__(self) -> None:
        self.cashflowDistribution = None
        self.valueDistribution = None
        self.strategicValue = None

        self.propagatedCashflow = None
        self.propagatedValue = None
        self.choice = None

        self.failures = []
        self.deadEnd = False
        self.probability = None



class TransitionHolder(Holder):

    def __init__(self) -> None:
        self.cashflowDistribution = None
        self.valueDistribution = None
        self.strategicValue = None

        self.rejected = False



from .decision import Decision
from .endgame import EndGame
from .evaluator import Evaluator
from .event import Event
from .node import Node
from .solver import Solver
from .transition import Transition
