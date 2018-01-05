from unittest import TestCase

from pyne import Holder


class TestHolder(TestCase):
    def test_holder(self):
        h = Holder()

        self.assertFalse(hasattr(h, "result"))
        h.result = 123
        self.assertTrue(hasattr(h, "result"))
        self.assertEqual(123, h.result)

        h.clearResults()

        self.assertFalse(hasattr(h, "result"))
        h.result = 124
        self.assertTrue(hasattr(h, "result"))
        self.assertEqual(124, h.result)
