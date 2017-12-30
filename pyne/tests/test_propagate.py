from unittest import TestCase
from pyne import Decision, Transition, Event, EndGame


class TestPropagate(TestCase):
    def test_propagate(self):
        tree = Decision("Do I buid something ?", [
            Transition("No"),
            Transition("Yes", payout=-100,target=Event("Will it Rain ?", [
                Transition("Yes", payout=-500, probability=.1,),
                Transition("No", payout=-500),
            ]))])
