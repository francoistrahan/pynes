from itertools import product
from unittest import TestCase, skip

from pyne.render import GraphvizEngine
from pyne import Decision, Event, Transition, Node
from pyne.strategy import *
from pyne import Solver

from tests import buildOrNotTestTree, createMineralsSampleTreeScalar


class TestDraw(TestCase):
    def test_scratch(self):
        import graphviz


        EXPECTED = ("digraph GraphName {\n"
                    "	root [label=Root shape=square]\n"
                    "	child [label=Child]\n"
                    "	root -> child [label=\"Edge\"]\n"
                    "}")

        graph = graphviz.Digraph(name="GraphName", format="svg")
        root = graph.node("root", label="Root", shape="square")
        child = graph.node("child", label="Child")
        edge = graph.edge("root", "child", label="Edge")
        self.assertEqual(EXPECTED, graph.source)  # graph.render(filename="/tmp/graph.svg", view=True)

    @skip("GUI Test")
    def test_minerals(self):
        CASES = (
            ("Max Expected", createMaxExpected, False),
            ("Max Expected", createMaxExpected, True),
            ("Max Max", createMaxMax, False),
            ("Max Max", createMaxMax, True),
            ("Max Min", createMaxMin, False),
            ("Max Min", createMaxMin, True),
            )
        for name, sc, p in CASES:
            self.plotMinerals(sc, p, name)

    def plotMinerals(self, strategyCreator, prune, name):
        root = createMineralsSampleTreeScalar()

        solver = Solver(root, strategyCreator())
        solver.solve()

        eng = GraphvizEngine(root)
        graph = eng.render(format="svg", prune=prune)

        filename = "Minerals - {} - {}".format(name, prune and "pruned" or "complete")

        graph.render(view=True, directory="../ignore", filename=filename)

