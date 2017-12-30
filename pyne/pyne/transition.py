from .node import Node



class Transition:
    def __init__(self, name, payout=None, probability=None, target: Node = None) -> None:
        if probability is not None and probability < 0: raise ValueError("Probability cannot be negative")

        self.name = name
        self.payout = payout
        self.target = target
        self.probability = probability


    def __str__(self) -> str:
        rv = "Transition: {}".format(self.name)

        details = []
        if self.probability is not None:
            details.append("p={:.4%}".format(self.probability))
        if self.payout is not None:
            details.append("impact={}".format(self.payout))

        details = ", ".join(details)
        if details:
            rv = "{} ({})".format(rv, details)

        return rv
