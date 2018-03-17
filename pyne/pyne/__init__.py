__all__ = ["Decision", "Event", "Transition", "EndGame", "Node", "Solver"]



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



class TransitionHolder(Holder):

    def __init__(self) -> None:
        self.cashflowDistribution = None
        self.valueDistribution = None
        self.strategicValue = None



from .node import Node
from .transition import Transition
from .decision import Decision
from .endgame import EndGame
from .event import Event
from .solver import Solver
from .evaluator import Evaluator
