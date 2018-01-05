from unittest import TestCase

from pyne import Decision
import pyne.strategy as strategy


class TestScalarStrategies(TestCase):
    def setUp(self):
        root = buildOrNotTestTree()
        root.createPlaceholders()

        root.propagatePayouts(0)
        self.root = root

    def getStrategy(self):
        nodes = self.root.getNodesFlat()
        decisions = [n for n in nodes if isinstance(n, Decision)]

        # This needs refining
        return ["{}: {}".format(d.name, d.results.choice.name) for d in decisions]

    def test_maxExpected(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        EXPECTED_STRATEGY = ['Do I buid something ?: No']
        CRITERIA = strategy.createMaxExpected()

        self.root.computePossibilities(CRITERIA)
        result = self.root.results.payoutDistribution

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_maxMax(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        EXPECTED_STRATEGY = ['Do I buid something ?: No']
        CRITERIA = strategy.createMaxMax()

        self.root.computePossibilities(CRITERIA)
        result = self.root.results.payoutDistribution

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_minMin(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        EXPECTED_STRATEGY = ['Do I buid something ?: No']
        CRITERIA = strategy.createMinMin()

        self.root.computePossibilities(CRITERIA)
        result = self.root.results.payoutDistribution

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_maxMin(self):
        EXPECTED = [(1, -100)]
        EXPECTED_STRATEGY = ['Do I buid something ?: Yes']
        CRITERIA = strategy.createMaxMin()

        self.root.computePossibilities(CRITERIA)
        result = self.root.results.payoutDistribution

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_minMax(self):
        EXPECTED = ((1, -100),)
        EXPECTED_STRATEGY = ['Do I buid something ?: Yes']
        CRITERIA = strategy.createMinMax()

        self.root.computePossibilities(CRITERIA)
        result = self.root.results.payoutDistribution

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())


from . import buildOrNotTestTree
