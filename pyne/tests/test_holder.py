from unittest import TestCase

from pyne import NodeHolder


class TestHolder(TestCase):
    def test_holder(self):
        h = NodeHolder()

        self.assertIsNone(h.payoutDistribution)
        h.payoutDistribution = 123
        self.assertEqual(123, h.payoutDistribution)
        h.clear()
        self.assertIsNone(h.payoutDistribution)
