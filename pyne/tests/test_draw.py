from unittest import TestCase, skip

import pandas as pd

import pyne.cashflow
from pyne import *
from pyne.render import GraphvizEngine
from pyne.strategy import *
from pyne.valueactualizer import PeriodNPV
from . import createMineralsSampleTreeScalar, IGNORE_DIRECTORY, showTree



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
        CASES = (("Max Expected", createMaxExpected, False), ("Max Expected", createMaxExpected, True),
                 ("Max Max", createMaxMax, False), ("Max Max", createMaxMax, True), ("Max Min", createMaxMin, False),
                 ("Max Min", createMaxMin, True),)
        for name, sc, p in CASES:
            self.plotMinerals(sc, p, name)


    def plotMinerals(self, strategyCreator, prune, name):
        root = createMineralsSampleTreeScalar()

        solver = Solver(root, strategyCreator())
        solver.solve()

        eng = GraphvizEngine(root)
        graph = eng.render(format="svg", prune=prune)

        filename = "Minerals - {} - {}".format(name, prune and "pruned" or "complete")

        graph.render(view=True, directory=IGNORE_DIRECTORY, filename=filename)


    def test_cashflows(self):
        CF = pyne.cashflow.createMonths
        AN = pyne.cashflow.annuityMonths

        mbaPattern = Event("Pass First Year", [
            Transition("No", probability=0.1),
            Transition("Yes", CF({"2017-1":-20000, "2017-07":-20000}), target=Event("Get a better Job", [
                Transition("No", probability=.2),
                Transition("Yes", AN("2018-01", 12 * 10, 20000 / 12))
            ]))
        ])

        root = Decision("Do an MBA", [
            Transition("No"),
            Transition("Yes", CF({"2016-1":-20000, "2016-07":-20000}), target=Event("Get a Grant", [
                Transition("No", target=mbaPattern.clone()),
                Transition("Yes", CF({"2015-12":10000}), .2, mbaPattern.clone())
            ]))
        ])

        solver = Solver(root, createMaxExpected(), PeriodNPV(0.1 / 12, pd.Period("2015-12", "M")))
        solver.solve()

        showTree(root)
