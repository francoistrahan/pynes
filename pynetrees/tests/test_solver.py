from unittest import TestCase

import pandas as pd

from pynetrees import Solver
from pynetrees.strategy import createMaxExpected
from pynetrees.valueactualizer import SUMMING_ACTUALIZER
from . import *



class TestSolver(TestCase):

    def test_solveBasicScalar(self):
        root = createMineralsSampleTreeScalar()
        root = root.clone()  # just to test it somewhere...
        strategy = createMaxExpected()
        solver = Solver(root, strategy)
        solver.solve()

        EXPECTED = pd.DataFrame({"probability":[0.470, 0.500, 0.015, 0.005, 0.01]},
                                index=[-5000000, -1000000, 25000000, 145000000, 245000000])

        result = solver.payoutDistribution()  # type: pd.DataFrame

        self.assertTrue(result.equals(EXPECTED))

        self.assertEqual(700000, solver.strategicValue())


    def test_solveBasicCFPeriods(self):
        root = createMineralsSampleTreeCFPeriod()
        root = root.clone()  # just to test it somewhere...
        strategy = createMaxExpected()
        solver = Solver(root, strategy, SUMMING_ACTUALIZER)
        solver.solve()

        EXPECTED = pd.DataFrame({"probability":[0.470, 0.500, 0.015, 0.005, 0.01]},
                                index=[-5000000, -1000000, 25000000, 145000000, 245000000])

        result = solver.payoutDistribution()  # type: pd.DataFrame

        self.assertTrue(result.equals(EXPECTED))

        self.assertEqual(700000, solver.strategicValue())
