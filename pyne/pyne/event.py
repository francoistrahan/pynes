from .node import Node



class Event(Node):

    TYPE_NAME = "Event"


    def __init__(self, name: str, transitions=None):
        super().__init__(name, transitions)


    def typeName(self):
        return Event.TYPE_NAME

