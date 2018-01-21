from unittest import TestCase

from pyne import Solver
from pyne.strategy import createMaxExpected
from . import createMineralsSampleTree



class TestSolver(TestCase):

    def test_solveBasic(self):
        root = createMineralsSampleTree()
        strategy = createMaxExpected()
        solver = Solver(root, strategy)
        solver.solve()

        self.assertEqual([(0.015, 25000000), (0.01, 245000000), (0.005, 145000000), (0.47, -5000000), (0.5, -1000000)],
                         solver.payoutDistribution())
