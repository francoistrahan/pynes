from unittest import TestCase

import pandas as pd

from pyne import *
from pyne.cashflow import create as CF
from pyne.render import GraphvizEngine
from pyne.strategy import createMaxExpected
from pyne.valueactualizer import SummingActualizer



class TestLimits(TestCase):

    def toCF_lowE_alwaysPos(self):
        return Transition("Low E, Always Pos", CF({0:1, 1:1}), 1)  # sum 2


    def toCF_lowE_startNeg(self):
        return Transition("Low E, Neg", CF({0:-1, 1:3}), 1)  # sum 2


    def toCF_highE_alwaysPos(self):
        return Transition("High E, Always Pos", CF({0:1, 1:97}), 1)  # sum 98


    def toCF_highestE_startNeg(self):
        return Transition("Highest E, Neg", CF({0:-1, 1:999}), 1)  # sum 998


    def test_cashflow(self):
        firstDecision = Decision("A, B or C", [
            Transition("Highest, Neg", target=Event("A", [self.toCF_lowE_alwaysPos(), self.toCF_highestE_startNeg()])),
            Transition("Always Pos", target=Event("B", [self.toCF_lowE_alwaysPos(), self.toCF_highE_alwaysPos()])),
            Transition("Possible Deadend", target=Event("C", [self.toCF_highE_alwaysPos(), Transition("To Deadend",
                                                                                                      target=Decision(
                                                                                                          "Deadend", [
                                                                                                              self.toCF_lowE_startNeg(),
                                                                                                              self.toCF_highestE_startNeg()]))])), ])

        root = Event("Do I have a choice", [Transition("No"), Transition("Yes", probability=.1, target=firstDecision)])

        solver = Solver(root, createMaxExpected(), SummingActualizer())
        solver.solve()

        self.assertAlmostEqual(50, root.results.strategicValue)


        def cummulativeCashflowNeverUnderTreshold(threshold):
            def predicate(cf: pd.Series):
                m = cf.expanding().sum().min()

                diff = m - threshold

                if diff < 0:
                    return True, -diff
                else:
                    return False, diff

                return False


            return predicate


        solver = Solver(root, createMaxExpected(), SummingActualizer(),
                        cashflowLimits=[("Cummulative Cashflow Negative", cummulativeCashflowNeverUnderTreshold(0))])
        solver.solve()

        eng = GraphvizEngine(root, "{}")
        svg = eng.render("svg")
        svg.view()

        self.assertAlmostEqual(5, root.results.strategicValue)
