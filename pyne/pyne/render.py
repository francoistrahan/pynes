import graphviz

from . import Node, Decision, Event, EndGame
from . import Decision


NODE_PREFIXES = {
    Decision: "d",
    Event   : "ev",
    EndGame : "eg",
    }

COMMON_NODE_ATTRIBUTES = {
    "style"    : "filled",
    "fontcolor": "white"
    }

NODE_ATTRIBUTES = {
    Decision: {"shape": "box", "fillcolor": "green"},
    Event   : {"shape": "oval", "fillcolor": "red"},
    EndGame : {"shape": "doubleoctagon", "fillcolor": "blue"},
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
        self.graph = graphviz.Digraph(format=format, graph_attr={"rankdir": "LR"})

        self.addNode(self.root, False)

        return self.graph

    def addNode(self, node: "Node", discarded):
        name = self.getNextName(node)
        attr = dict(COMMON_NODE_ATTRIBUTES, **NODE_ATTRIBUTES[type(node)])

        if discarded: attr["fillcolor"] = "lightgrey"

        nodeLabel = node.name
        nodeLabel += "\nR$ = {:,.2f}".format(node.results.reducedPayout)
        if hasattr(node.results, "probability"): nodeLabel += "\n(P= {:.2%}".format(node.results.probability)

        self.graph.node(name=name, label=nodeLabel, **attr)
        for trans in node.transitions:

            discartTrans = discarded or (isinstance(node, Decision) and node.results.choice is not trans)

            tname = self.addNode(trans.target, discartTrans)

            edgeLabel = trans.name
            if trans.payout is not None: edgeLabel += "\n$= {:,.2f}".format(trans.payout)
            if trans.probability is not None: edgeLabel += "\n(P= {:.4%})".format(trans.probability)

            if discartTrans:
                color = "lightgrey"
            else:
                color = "black"

            self.graph.edge(name, tname, edgeLabel, color=color)

        return name
