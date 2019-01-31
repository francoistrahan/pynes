import graphviz

def showTree(root: "Node", prune=False, discard=True, *args, **kwargs):
    root.createPlaceholders()
    eng = GraphvizEngine(root, *args, **kwargs)
    graph = eng.render("svg", prune, discard)
    return graphviz.Source(graph)

from .node import Node
from .render import GraphvizEngine
