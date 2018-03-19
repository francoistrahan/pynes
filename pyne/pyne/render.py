import graphviz

from . import Decision
from . import Node, Event, EndGame


DISCARDED_COLOR = "lightgrey"
REJECTED_COLOR = "red"

NODE_PREFIXES = {Decision:"d", Event:"ev", EndGame:"eg",
                 }

COMMON_NODE_ATTRIBUTES = {"style":"filled", "fontcolor":"white"
                          }

NODE_ATTRIBUTES = {
    Decision:{"shape":"box", "fillcolor":"green"},
    Event:{"shape":"oval", "fillcolor":"orange"},
    EndGame:{"shape":"doubleoctagon", "fillcolor":"blue"},
}



class GraphvizEngine:

    def __init__(self, root: "Node", cashflowFormat="{:,.2f}", strategicValueFormat="{:,.2f}", transitionProbabilityFormat="{:.2%}", computedProbabilityFormat="{:.2%}") -> None:
        super().__init__()
        self.computedProbabilityFormat = computedProbabilityFormat
        self.transitionProbabilityFormat = transitionProbabilityFormat
        self.strategicValueFormat = strategicValueFormat
        self.cashflowFormat = cashflowFormat
        self.format = format
        self.nodeNumber = None  # type: int
        self.root = root  # type: Node


    def getNextName(self, node):
        self.nodeNumber += 1
        prefix = NODE_PREFIXES[type(node)]
        return "{}{}".format(prefix, self.nodeNumber)


    def render(self, format, prune=False, discard=True):
        self.nodeNumber = 0
        self.graph = graphviz.Digraph(format=format, graph_attr={"rankdir":"LR"})

        self.addNode(self.root, False, prune, discard)

        return self.graph


    def addNode(self, node: "Node", discarded, prune, discard):
        name = self.getNextName(node)
        attr = dict(COMMON_NODE_ATTRIBUTES, **NODE_ATTRIBUTES[type(node)])

        if node.results.deadEnd:
            attr["fillcolor"] = REJECTED_COLOR
        elif discard and discarded:
            attr["fillcolor"] = DISCARDED_COLOR

        nodeLabel = node.name
        if node.results.strategicValue is not None:
            nodeLabel += ("\nR$ = " + self.strategicValueFormat).format(node.results.strategicValue)
        if hasattr(node.results, "probability"): nodeLabel += "\n(P= {})".format(self.computedProbabilityFormat).format(node.results.probability)

        self.graph.node(name=name, label=nodeLabel, **attr)
        for trans in node.transitions:

            discartTrans = discarded or (isinstance(node, Decision) and (node.results.choice is not trans))
            if prune and discartTrans: continue

            transitionToDeadend = trans.results.rejected or trans.target.results.deadEnd

            tname = self.addNode(trans.target, discartTrans or transitionToDeadend, prune, discard)

            edgeLabel = trans.name
            if trans.payout is not None: edgeLabel += ("\n$= " + self.cashflowFormat).format(trans.payout)
            if trans.probability is not None: edgeLabel += "\n(P= {})".format(self.transitionProbabilityFormat).format(trans.probability)

            if transitionToDeadend:
                color = REJECTED_COLOR
            elif discard and discartTrans:
                color = DISCARDED_COLOR
            else:
                color = "black"

            self.graph.edge(name, tname, edgeLabel, color=color)

        return name
