from unittest import TestCase

from pynetrees.solver import Solver



class TestAddPayouts(TestCase):

    def test_addScalars(self):
        solver = Solver(None, None)
        addPayouts = solver.addPayoutsScalar
        self.assertEqual(4, addPayouts(1, 2, -3.0, None, 4))  # Note: Mixing ints and floats on purpose...
        self.assertIsNone(addPayouts(None, None, None))
        self.assertIsNone(addPayouts(*[]))
        self.assertIsNone(addPayouts())
