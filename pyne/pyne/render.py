import graphviz



class GraphvizEngine:

    def __init__(self, root: "Node") -> None:
        super().__init__()
        self.nodeNumber = None  # type: int
        self.root = root  # type: Node


    def getNextName(self):
        self.nodeNumber += 1
        return "node{}".format(self.nodeNumber)


    def render(self):
        self.nodeNumber = 0
        self.graph = graphviz.Digraph()

        self.addNode(self.root)
        return self.graph


    def addNode(self, node: "Node"):
        name = self.getNextName()
        self.graph.node(name=name, label=node.name)
        for trans in node.transitions:
            tname = self.addNode(trans.target)
            self.graph.edge(name, tname, trans.name)
        return name


from .node import Node
