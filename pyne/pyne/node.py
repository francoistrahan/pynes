from abc import ABCMeta, abstractmethod



class Node(metaclass=ABCMeta):

    def __init__(self, name: str, transitions: 'list[Transition]' = None):
        self.name = name
        self.transitions = transitions or [] # type: list[Transition]


    @abstractmethod
    def typeName(self): pass


    def __str__(self) -> str:
        return "{}: {}".format(self.typeName(), self.name)


    def createPlaceholders(self):
        for t in self.transitions:
            t.createPlaceHolders()


    def propagatePayouts(self, current):
        for t in self.transitions:
            t.propagatePayouts(current)

    def getNodesFlat(self):
        yield self
        for t in self.transitions:
            yield from t.target.getNodesFlat()



from .transition import Transition
