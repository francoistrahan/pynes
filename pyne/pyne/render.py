import graphviz

from . import Node, Decision, Event, EndGame
from . import Decision


NODE_PREFIXES = {
    Decision: "d",
    Event   : "ev",
    EndGame : "eg",
    }


class GraphvizEngine:
    def __init__(self, root: "Node") -> None:
        super().__init__()
        self.format = format
        self.nodeNumber = None  # type: int
        self.root = root  # type: Node

    def getNextName(self, node):
        self.nodeNumber += 1
        prefix = NODE_PREFIXES[type(node)]
        return "{}{}".format(prefix, self.nodeNumber)

    def render(self, format):
        self.nodeNumber = 0
        self.graph = graphviz.Digraph(format=format)

        self.addNode(self.root)
        return self.graph

    def addNode(self, node: "Node"):
        name = self.getNextName(node)

        self.graph.node(name=name, label=node.name)
        for trans in node.transitions:
            tname = self.addNode(trans.target)
            self.graph.edge(name, tname, trans.name)
        return name
