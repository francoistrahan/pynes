from unittest import TestCase

from pyne import Decision, Transition, Event, EndGame, Node



class TestPropagate(TestCase):

    def test_propagate(self):
        didNotRain = Transition("No") # No rain, am I glad I did not spend
        didRain = Transition("Yes", payout=-500, probability=.1, ) # Rained on my stuff, lost $500 of goodies
        rainOrNot = Event("Will it Rain ?", [didRain, didNotRain, ]) # no roof: I care about the rain
        doNotBuild = Transition("No", target=rainOrNot) # Don't build (don't spend)
        doBuild = Transition("Yes", payout=-100) # I fix the roof, costs 100$, rain all you want.
        doIBuild = Decision("Do I buid something ?", [doBuild, doNotBuild]) # It's about do rain, do I build a roof.
        root = doIBuild

        assert isinstance(root, Node)

        root.createPlaceholders()
        root.propagatePayouts(0)

        looseTransitions = [doBuild, didRain, didNotRain]
        endGames = [t.target for t in looseTransitions]

        for eg in endGames: self.assertIsInstance(eg, EndGame)

        payouts = [eg.payout() for eg in endGames]

        self.assertSequenceEqual([-100, -500, 0], payouts)
