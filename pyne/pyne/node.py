from abc import ABCMeta, abstractmethod



class Node(metaclass=ABCMeta):

    def __init__(self, name: str, transitions=None):
        self.name = name
        self.transitions = transitions or []


    @abstractmethod
    def typeName(self): pass


    def __str__(self) -> str:
        return "{}: {}".format(self.typeName(), self.name)
