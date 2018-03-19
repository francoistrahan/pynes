from unittest import TestCase

import numpy as np

from pyne.cashflow import create as CF
from pyne.strategy import createMaxExpected
from pyne.valueactualizer import IndexedNPV


STRATEGY = createMaxExpected()

ACTUALIZER = IndexedNPV(0.1)



class TestSensitivityAnalysis(TestCase):


    def setUp(self):
        self.root = Decision("Buy a loto", [
            Transition("No", CF({0:0})),
            Transition("Yes", CF({0:-10}), target=Event("Win", [
                Transition("No"),
                Transition("Yes", CF({1:22_000_000}), 1 / 10_000_000)
            ]))
        ])

        self.solver = Solver(self.root, STRATEGY, ACTUALIZER)


    def setProb(self, prob):
        self.root.transit("Yes", "Yes").probability = prob


    def setLot(self, price):
        self.root.transit("Yes", "Yes").payout[1] = price


    def test_simple(self):
        sensitivityAnalysis = SensitivityAnalysis(
            self.solver,
            [
                Variable("Probability of winning", self.setProb, 1 / 10_000_000, np.linspace(0.01, 100, 10) / 10_000_000),
                Variable("Value of winning", self.setLot, 22_000_000, np.linspace(10, 200, 10) * 1_000_000),
            ],
            [
                Output("Strategic Value", lambda:self.root.results.strategicValue),
                Output("Ticket Value", lambda:self.root.transit("Yes").target.results.strategicValue),
            ])

        print()
        print()
        print("Base Values")
        print(sensitivityAnalysis.baseValues)

        print()
        print()
        print("Extremums")
        print(sensitivityAnalysis.extremums)

        print()
        print()
        print("Individual Responses")

        for outName in sorted(sensitivityAnalysis.individualResponses.keys()):
            print("Outname")
            print(sensitivityAnalysis.individualResponses[outName])
            print()




from pyne import *
from pyne.sensitivity import SensitivityAnalysis, Variable, Output
