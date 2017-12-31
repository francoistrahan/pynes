from .node import Node



class Decision(Node):
    TYPE_NAME = "Decision"


    def __init__(self, name, transitions=None):
        super().__init__(name, transitions)


    def typeName(self):
        return Decision.TYPE_NAME


    def computePossibilities(self, decisionStrategy):

        options = (t.target.computePossibilities() for t in self.transitions)
        idx, choice = decisionStrategy(options)

        return choice




from .transition import Transition
