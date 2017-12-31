from unittest import TestCase

import pyne.strategies as strategies
from pyne import Decision



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
        return ["{}: {}".format(d.name, d.choice.name) for d in decisions]


    def test_maxExpected(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        CRITERIA = strategies.maxExpectedPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: No']

        result = self.root.computePossibilities(CRITERIA)

        self.assertEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_maxMax(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        CRITERIA = strategies.maxMaxPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: No']

        result = self.root.computePossibilities(CRITERIA)

        self.assertEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())


    def test_minMin(self):
        EXPECTED = [(0.1, -500), (0.9, 0)]
        CRITERIA = strategies.minMinPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: No']

        result = self.root.computePossibilities(CRITERIA)

        self.assertEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())


    def test_maxMin(self):
        EXPECTED = [(1, -100)]
        CRITERIA = strategies.maxMinPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: Yes']

        result = self.root.computePossibilities(CRITERIA)

        self.assertSequenceEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

    def test_minMax(self):
        EXPECTED = ((1, -100),)
        CRITERIA = strategies.minMaxPayout
        EXPECTED_STRATEGY = ['Do I buid something ?: Yes']

        result = self.root.computePossibilities(CRITERIA)

        self.assertEqual(EXPECTED, result)
        self.assertEqual(EXPECTED_STRATEGY, self.getStrategy())

from . import buildOrNotTestTree
