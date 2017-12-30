from unittest import TestCase

from pyne import addPayouts



class TestAddPayouts(TestCase):

    def test_addScalars(self):

        self.assertEqual(4, addPayouts(1, 2, -3.0, None, 4)) # Note: Mixing ints and floats on purpose...
        self.assertIsNone(addPayouts(None, None, None))
        self.assertIsNone(addPayouts(*[]))
        self.assertIsNone(addPayouts())

