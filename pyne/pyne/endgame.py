from . import addPayouts
from .node import Node



class EndGame(Node):
    TYPE_NAME = "EndGame"
    DEFAULT_NAME = "Done"


    def __init__(self, basePayout=None, name: str = None, placeholder: bool = False):
        super().__init__(name or EndGame.DEFAULT_NAME)

        self.placeholder = placeholder
        self.basePayout = basePayout
        self.pushedPayout = None


    def typeName(self):
        return EndGame.DEFAULT_NAME


    def payout(self):
        return addPayouts(self.basePayout, self.pushedPayout)
