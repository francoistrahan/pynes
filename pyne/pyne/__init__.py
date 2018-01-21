from numbers import Real


__all__ = ["Decision", "Event", "Transition", "EndGame", "Node", "Solver"]



def addPayouts(*payouts):
    payouts = [p for p in payouts if p is not None]

    if not payouts: return None

    assert all(isinstance(p, Real) for p in payouts), "Only scalar payouts are supported by now"

    return sum(payouts)



class Holder:

    def clearResults(self):
        self.__dict__.clear()



from .node import Node
from .decision import Decision
from .event import Event
from .transition import Transition
from .endgame import EndGame
from .solver import Solver
