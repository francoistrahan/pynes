from unittest import TestCase

from pyne import Decision
import pyne.strategies as strategies



class TestScalarStrategies(TestCase):

    def setUp(self):
        root = buildOrNotTestTree()
        root.createPlaceholders()

        root.propagatePayouts(0)
        self.root = root

    def test_maxExpectedValue(self):

        EXPECTED = [(0.1, -500), (0.9, 0)]
        CRITERIA = strategies.maxExpectedPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: No']

        result = self.root.computePossibilities(CRITERIA)

        self.assertEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())


    def getStrategy(self):
        nodes = self.root.getNodesFlat()
        decisions = [n for n in nodes if isinstance(n, Decision)]

        # This needs refining
        return ["{}: {}".format(d.name, d.choice.name) for d in decisions]



from . import buildOrNotTestTree
