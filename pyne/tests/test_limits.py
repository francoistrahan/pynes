from unittest import TestCase

from pyne import *
from pyne.cashflow import create as CF
from pyne.limits import *
from pyne.render import GraphvizEngine
from pyne.strategy import createMaxExpected
from pyne.valueactualizer import SummingActualizer



class TestLimits(TestCase):


    def test_cashflow(self):
        firstDecision = Decision("A, B or C", [
            Transition("Highest, Neg", target=Event("A", [toCF_lowE_alwaysPos(), toCF_highestE_startNeg()])),
            Transition("Always Pos", target=Event("B", [toCF_lowE_alwaysPos(), toCF_highE_alwaysPos()])),
            Transition("Possible Deadend", target=Event("C", [toCF_highE_alwaysPos(), Transition("To Deadend",
                                                                                                 target=Decision(
                                                                                                     "Deadend", [
                                                                                                         toCF_lowE_startNeg(),
                                                                                                         toCF_highestE_startNeg()]))])), ])

        root = Event("Do I have a choice", [Transition("No"), Transition("Yes", probability=.1, target=firstDecision)])

        solver = Solver(root, createMaxExpected(), SummingActualizer(),
                        cashflowLimits=[("Cummulative Cashflow Negative", cashflowRollsumUnderThreshold(0))])
        solver.solve()

        self.assertAlmostEqual(5, root.results.strategicValue)

        # showTree(root)


    def test_value(self):
        MINIMUM = 5

        firstDecision = Decision("A, B or C", [
            Transition("Highest, Neg", target=Event("A", [toCF_lowE_alwaysPos(), toCF_highestE_startNeg()])),
            Transition("Always Pos", target=Event("B", [toCF_lowE_alwaysPos(), toCF_highE_alwaysPos()])),
            Transition("Possible Deadend", target=Event("C", [toCF_highE_alwaysPos(), Transition("To Deadend",
                                                                                                 target=Decision(
                                                                                                     "Deadend", [
                                                                                                         toCF_lowE_startNeg(),
                                                                                                         toCF_highestE_startNeg()]))])), ])
        root = Event("Do I have a choice",
                     [toCF_highE_alwaysPos(), Transition("Yes", probability=.1, target=firstDecision)])

        solver = Solver(root, createMaxExpected(), SummingActualizer(),
                        valueLimits=[("Value Negative", valueUnderThreshold(MINIMUM))])
        solver.solve()

        # showTree(root)

        self.assertAlmostEqual(98, root.results.strategicValue)


    def test_cashflowDistribution(self):
        MAXIMUM = 5

        firstDecision = Decision("A, B or C", [
            Transition("Highest, Neg", target=Event("A", [toCF_lowE_alwaysPos(), toCF_highestE_startNeg()])),
            Transition("Always Pos", target=Event("B", [toCF_lowE_alwaysPos(), toCF_highE_alwaysPos()])),
            Transition("Possible Deadend", target=Event("C", [toCF_highE_alwaysPos(), Transition("To Deadend",
                                                                                                 target=Decision(
                                                                                                     "Deadend", [
                                                                                                         toCF_lowE_startNeg(),
                                                                                                         toCF_highestE_startNeg()]))])), ])
        root = Event("Do I have a choice",
                     [toCF_highE_alwaysPos(), Transition("Yes", probability=.1, target=firstDecision)])

        solver = Solver(root, createMaxExpected(), SummingActualizer(),
                        cashflowDistributionLimits=[("Expected TTR too long", expectedTTROverThreshold(MAXIMUM))])
        solver.solve()

        showTree(root)

        self.assertAlmostEqual(98, root.results.strategicValue)



def toCF_highestE_startNeg():
    return Transition("Highest E, Neg", CF({0:-1, 10:999}), 1)  # sum 998



def toCF_highE_alwaysPos():
    return Transition("High E, Always Pos", CF({0:1, 5:97}), 1)  # sum 98



def toCF_lowE_startNeg():
    return Transition("Low E, Neg", CF({0:-1, 1:3}), 1)  # sum 2



def toCF_lowE_alwaysPos():
    return Transition("Low E, Always Pos", CF({0:1, 1:1}), 1)  # sum 2



def showTree(root):
    eng = GraphvizEngine(root, "{}", transitionProbabilityFormat="{}/")
    svg = eng.render("svg")
    svg.view()
