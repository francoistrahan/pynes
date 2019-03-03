from unittest import TestCase

from pynetrees import NodeHolder



class TestHolder(TestCase):

    def test_holder(self):
        h = NodeHolder()

        self.assertIsNone(h.cashflowDistribution)
        h.cashflowDistribution = 123
        self.assertEqual(123, h.cashflowDistribution)
        h.clear()
        self.assertIsNone(h.cashflowDistribution)
