from unittest import TestCase

import pandas as pd

from pyne import Solver
from pyne.strategy import createMaxExpected
from . import createMineralsSampleTree



class TestSolver(TestCase):

    def test_solveBasic(self):
        root = createMineralsSampleTree()
        strategy = createMaxExpected()
        solver = Solver(root, strategy)
        solver.solve()

        EXPECTED = pd.DataFrame({"probability":[0.470, 0.500, 0.015, 0.005, 0.01]},
                                index=[-5000000, -1000000, 25000000, 145000000, 245000000])

        result = solver.payoutDistribution()  # type: pd.DataFrame

        self.assertTrue(result.equals(EXPECTED))

        self.assertEqual(700000, solver.reducedPayout())
