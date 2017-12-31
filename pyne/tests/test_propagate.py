from unittest import TestCase

from pyne import Decision, Transition, Event, EndGame, Node
from . import buildOrNotTestTree


class TestPropagate(TestCase):

    def test_propagate(self):

        doIBuild = buildOrNotTestTree()
        root = doIBuild

        assert isinstance(root, Node)

        self.assertEqual(1, root.createPlaceholders())
        root.propagatePayouts(0)

        payouts = dict(((n.name, n.payout()) for n in root.getNodesFlat() if isinstance(n, EndGame)))
        payouts = [payouts[n] for n in ("Done", "NoRoof_Rain", "NoRoof_NoRain")]

        self.assertSequenceEqual([-100, -500, 0], payouts)


