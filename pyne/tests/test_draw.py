from itertools import product
from unittest import TestCase, skip

from pyne.render import GraphvizEngine
from pyne import Decision, Event, Transition, Node
from pyne.strategy import *

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

    def test_minerals(self):
        i = 0
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
        def buyAndFindWhat(pManganese, pGold, pSilver):
            return Decision("Buy ?", (
                Transition("Yes", payout=-4000000, target=
                Event("Find What ?", (
                    Transition("Manganese", probability=pManganese, payout=30000000),
                    Transition("Gold", probability=pGold, payout=250000000),
                    Transition("Silver", probability=pSilver, payout=150000000),
                    Transition("Nothing"),
                    ))),
                Transition("No")
                ))

        root = Decision("Conduct Survey ?", transitions=(
            Transition("Yes", payout=-1000000, target=
            Event("Survey Positive ?", (
                Transition("Yes", probability=0.5, target=buyAndFindWhat(.03, .02, .01)),
                Transition("No", target=buyAndFindWhat(.0075, .0004, .00175)),
                ))),
            Transition("No", target=buyAndFindWhat(0.01, 0.0005, 0.002))
            ))
        root.createPlaceholders()
        root.propagatePayouts(0)
        root.computePossibilities(strategyCreator())
        root.propagateEndgameDistribution(1)
        eng = GraphvizEngine(root)
        graph = eng.render(format="svg", prune=prune)
        graph.render(view=True, directory="../ignore", filename="Minerals - {} - {}".format(name, prune and "pruned" or "complete"))
