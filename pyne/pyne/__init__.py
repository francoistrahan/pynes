from numbers import Real


__all__ = ["Decision", "Event", "Transition", "EndGame", "Node", "Solver"]






class Holder:

    def clear(self):
        d = self.__dict__
        for k in d.keys():
            d[k] = None



class NodeHolder(Holder):

    def __init__(self) -> None:
        self.payoutDistribution = None
        self.reducedPayout = None



class TransitionHolder(Holder):
    pass



from .node import Node
from .decision import Decision
from .event import Event
from .transition import Transition
from .endgame import EndGame
from .solver import Solver
