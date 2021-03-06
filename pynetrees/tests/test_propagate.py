from unittest import TestCase

from pynetrees import EndGame, Node, Solver
from . import buildOrNotTestTree



class TestPropagate(TestCase):

    def test_propagate(self):
        doIBuild = buildOrNotTestTree()
        root = doIBuild  # type: Node

        self.assertEqual(1, root.createPlaceholders())
        solver = Solver(None, None)
        solver.addPayouts = solver.addPayoutsScalar

        root.propagateCashflows(solver, 0)

        payouts = dict(((n.name, n.results.propagatedValue) for n in root.getNodesFlat() if isinstance(n, EndGame)))
        payouts = [payouts[n] for n in ("Done", "NoRoof_Rain", "NoRoof_NoRain")]

        self.assertSequenceEqual([-100, -500, 0], payouts)

        payouts = dict(((n.name, n.results.propagatedCashflow) for n in root.getNodesFlat() if isinstance(n, EndGame)))
        payouts = [payouts[n] for n in ("Done", "NoRoof_Rain", "NoRoof_NoRain")]

        self.assertSequenceEqual([-100, -500, 0], payouts)
