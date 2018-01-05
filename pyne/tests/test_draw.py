from unittest import TestCase

from pyne.render import GraphvizEngine
from tests import buildOrNotTestTree


class TestDraw(TestCase):
    def test_scratch(self):
        import graphviz


        EXPECTED = ("digraph GraphName {\n"
                    "	root [label=Root shape=square]\n"
                    "	child [label=Child]\n"
                    "		root -> child [label=\"Edge\"]\n"
                    "}")

        graph = graphviz.Digraph(name="GraphName", format="svg")
        root = graph.node("root", label="Root", shape="square")
        child = graph.node("child", label="Child")
        edge = graph.edge("root", "child", label="Edge")
        self.assertEqual(EXPECTED, graph.source)  # graph.render(filename="/tmp/graph.svg", view=True)

    def test_buildRoof(self):
        root = buildOrNotTestTree()
        root.createPlaceholders()

        root.propagatePayouts(0)
        root.computePossibilities(maxExpectedPayout)

        eng = GraphvizEngine(root)
        graph = eng.render(format="svg")
        graph.render(view=True, directory="../ignore", filename="buildroof")
