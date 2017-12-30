from abc import ABCMeta


class Node(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name


    def __str__(self) -> str:

        return "{}: {}".format(cl, self.name)

