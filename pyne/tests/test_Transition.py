import unittest

from pyne.transition import Transition



class TestTransition(unittest.TestCase):

    def test_str(self):
        self.assertEqual("Transition: Coucou", str(Transition("Coucou")))
        self.assertEqual("Transition: Coucou (impact=0)", str(Transition("Coucou", payout=0)))
        self.assertEqual("Transition: Coucou (impact=12.3)", str(Transition("Coucou", payout=12.3)))
        self.assertEqual("Transition: Coucou (impact=[12.3, 3.45])", str(Transition("Coucou", payout=[12.3, 3.45])))
        self.assertEqual("Transition: Coucou (p=10.0000%)", str(Transition("Coucou", probability=.1)))
        self.assertEqual("Transition: Coucou (p=10.0000%, impact=-12.3)",
                         str(Transition("Coucou", probability=.1, payout=-12.3)))
