from .node import Node



class Decision(Node):
    TYPE_NAME = "Decision"


    def __init__(self, name, transitions=None):
        super().__init__(name, transitions)
        self.choice = None # type: Transition


    def typeName(self):
        return Decision.TYPE_NAME


    def computePossibilities(self, decisionStrategy):

        options = [t.target.computePossibilities(decisionStrategy) for t in self.transitions]
        idx, payout = decisionStrategy(options)

        self.choice = self.transitions[idx]

        return payout




from .transition import Transition
