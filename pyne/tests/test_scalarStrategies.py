from unittest import TestCase

from pyne import Decision
from pyne.strategies import maxExpectedPayout, expectedPayout


class TestScalarStrategies(TestCase):

    def test_ExpectedValue(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        self.assertEqual(-50, expectedPayout(EXPECTED))


    def test_maxExpectedValue(self):
        root = buildOrNotTestTree()
        root.createPlaceholders()

        root.propagatePayouts(0)
        result = root.computePossibilities(maxExpectedPayout)

        EXPECTED = [(0.1, -500), (0.9, 0)]
        self.assertEqual(-50, expectedPayout(EXPECTED))

        self.assertEqual(EXPECTED, result)


        nodes = root.getNodesFlat()
        decisions = [n for n in nodes if isinstance(n, Decision)]

        # This needs refining
        strategy = ["{}: {}".format(d.name, d.choice.name) for d in decisions]

        self.assertEqual(['Do I buid something ?: No'], strategy)


from . import buildOrNotTestTree
