from unittest import TestCase
import pandas as pd

from pyne import *
from pyne.cashflow import create as CF
from pyne.render import GraphvizEngine

from pyne.strategy import createMaxExpected
from pyne.valueactualizer import  SummingActualizer

class TestLimits(TestCase):

    def toCF_lowE_alwaysPos(self):
        return Transition("Low E, Always Pos", CF({0:1, 1:1}), 1)  # sum 2


    def toCF_highE_alwaysPos(self):
        return Transition("High E, Always Pos", CF({0:1, 1:97}), 1)  # sum 98


    def toCF_highestE_startNeg(self):
        return Transition("Highest E, Always Pos", CF({0:-1, 1:999}), 1)  # sum 998


    def test_cashflow(self):
        root = Decision("A or B",
                        [Transition("A", target=Event("A", [self.toCF_lowE_alwaysPos(), self.toCF_highestE_startNeg()])),
                         Transition("B", target=Event("B", [self.toCF_lowE_alwaysPos(), self.toCF_highE_alwaysPos()]))])



        solver = Solver(root, createMaxExpected(), SummingActualizer())
        solver.solve()

        self.assertEqual(500, root.results.strategicValue)

        def cummulativeCashflowNeverUnderTreshold(threshold):
            def predicate(cf:pd.Series):
                ss = 0
                for v in cf:
                    ss += v
                    if ss < threshold: return True
                return False


        solver = Solver(root, createMaxExpected(), SummingActualizer(), cashflowLimits=[
            ("Cummulative Cashflow Negative", cummulativeCashflowNeverUnderTreshold(0))
        ])
        solver.solve()

        self.assertEqual(50, root.results.strategicValue)


