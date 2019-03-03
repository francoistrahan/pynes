from unittest import TestCase

import numpy as np
import pandas as pd

from pynetrees import *
from pynetrees.cashflow import create as CF
from pynetrees.strategy import createMaxExpected
from pynetrees.valueactualizer import IndexedNPV


STRATEGY = createMaxExpected()

ACTUALIZER = IndexedNPV(0.1)

CASES = [
    (0, -10, 0, "No"),
    (1 / 10_000_000, -8, 0, "No"),
    (10 / 20_000_000, 0, 0, "No"),
    (11 / 20_000_000, 1, 1, "Yes"),
    (1, 19_999_990, 19_999_990, "Yes"),
]

EXPECTED_FRAME = """    Probability  Value Strategy  Value Ticket  Buy
0  0.000000e+00             0.0         -10.0   No
1  1.000000e-07             0.0          -8.0   No
2  5.000000e-07             0.0           0.0   No
3  5.500000e-07             1.0           1.0  Yes
4  1.000000e+00      19999990.0    19999990.0  Yes"""

class TestEvaluator(TestCase):

    def setUp(self):
        self.root = Decision("Buy a loto", [
            Transition("No", CF({0:0})),
            Transition("Yes", CF({0:-10}), target=Event("Win", [
                Transition("No"),
                Transition("Yes", CF({1:22_000_000}), 1 / 10_000_000)
            ]))
        ])

        self.solver = Solver(self.root, STRATEGY, ACTUALIZER)


        def setProb(prob):
            self.root.transit("Yes", "Yes").probability = prob


        self.evaluator = Evaluator(self.solver,
                                   [
                                       setProb
                                   ],
                                   [
                                       lambda:self.root.results.strategicValue,
                                       lambda:self.root.transit("Yes").target.results.strategicValue,
                                       lambda:self.root.results.choice.name,
                                   ]
                                   )


    def test_simpleSolve(self):
        self.solver.solve()
        # showTree(self.root)


    def test_executeOne(self):
        for i, (prob, expectedVTicket, expectedVStrat, expectedBuy) in enumerate(CASES):
            with self.subTest(i):
                vstrat, vticket, buy = self.evaluator.evaluate([prob])
                self.assertAlmostEqual(expectedVStrat, vstrat)
                self.assertAlmostEqual(expectedVTicket, vticket)
                self.assertEqual(expectedBuy, buy)


    def test_executeMany(self):
        df = pd.DataFrame([c[0] for c in CASES])

        df = self.evaluator.evaluateMany(df)
        df.columns = ("Probability", "Value Strategy", "Value Ticket", "Buy")

        self.assertEqual(EXPECTED_FRAME, str(df))


