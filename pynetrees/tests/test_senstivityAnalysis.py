from io import StringIO
from time import sleep
from unittest import TestCase

import numpy as np
from os import path

from pynetrees.cashflow import create as CF
from pynetrees.strategy import createMaxExpected
from pynetrees.valueactualizer import IndexedNPV
import matplotlib.pyplot as plt

from tests import IGNORE_DIRECTORY, showTree


EXPECTED_REPORT = r"""

Base Values
                base
Strategic Value    0
Ticket Value      -8
Buy A Ticket      No


Extremums
                       Strategic Value          Ticket Value          Buy A Ticket     
                                   Low     High          Low     High          Low High
Probability of winning               0       20       -9.998       20           No  Yes
Value of winning                     0  8.18182     -9.90909  8.18182           No  Yes


Individual Responses
Outname
    Probability of winning  Strategic Value  Ticket Value Buy A Ticket
0             1.000000e-10          0.00000      -9.99800           No
1             1.525051e-08          0.00000      -9.69499           No
2             3.040101e-08          0.00000      -9.39198           No
3             4.555152e-08          0.00000      -9.08897           No
4             6.070202e-08          0.00000      -8.78596           No
..                     ...              ...           ...          ...
95            1.439398e-06         18.78796      18.78796          Yes
96            1.454548e-06         19.09097      19.09097          Yes
97            1.469699e-06         19.39398      19.39398          Yes
98            1.484849e-06         19.69699      19.69699          Yes
99            1.500000e-06         20.00000      20.00000          Yes

Outname
    Value of winning  Strategic Value  Ticket Value Buy A Ticket
0       1.000000e+06         0.000000     -9.909091           No
1       3.010101e+06         0.000000     -9.726354           No
2       5.020202e+06         0.000000     -9.543618           No
3       7.030303e+06         0.000000     -9.360882           No
4       9.040404e+06         0.000000     -9.178145           No
..               ...              ...           ...          ...
95      1.919596e+08         7.450872      7.450872          Yes
96      1.939697e+08         7.633609      7.633609          Yes
97      1.959798e+08         7.816345      7.816345          Yes
98      1.979899e+08         7.999082      7.999082          Yes
99      2.000000e+08         8.181818      8.181818          Yes

"""

STRATEGY = createMaxExpected()

ACTUALIZER = IndexedNPV(0.1)



class TestSensitivityAnalysis(TestCase):


    def setUp(self):
        self.root = Decision("Buy a loto", [
            Transition("No", CF({0:0})),
            Transition("Yes", CF({0:-10}), target=Event("Win", [
                Transition("No"),
                Transition("Yes", CF({1:22_000_000}), 1 / 10_000_000)
            ]))
        ])

        self.solver = Solver(self.root, STRATEGY, ACTUALIZER)
        self.solver.solve()

        self.sensitivityAnalysis = SensitivityAnalysis(
            self.solver,
            [
                Variable("Probability of winning", self.setProb, 1 / 10_000_000, np.linspace(0.001, 15, 100) / 10_000_000),
                Variable("Value of winning", self.setLot, 22_000_000, np.linspace(1, 200, 100) * 1_000_000),
            ],
            [
                Output("Strategic Value", lambda:self.root.results.strategicValue),
                Output("Ticket Value", lambda:self.root.transit("Yes").target.results.strategicValue),
                Output("Buy A Ticket", lambda:self.root.results.choice.name),
            ])
        self.maxDiff = None


    def setProb(self, prob):
        self.root.transit("Yes", "Yes").probability = prob


    def setLot(self, price):
        self.root.transit("Yes", "Yes").payout[1] = price


    def test_simple(self):
        writer = StringIO()


        def print(*args):
            import builtins

            builtins.print(*args, file=writer)




        print()
        print()
        print("Base Values")
        print(self.sensitivityAnalysis.baseValues.to_string(max_cols=None, max_rows=10))

        print()
        print()
        print("Extremums")
        print(self.sensitivityAnalysis.extremums.to_string(max_cols=None, max_rows=10))

        print()
        print()
        print("Individual Responses")

        for outName in sorted(self.sensitivityAnalysis.individualResponses.keys()):
            print("Outname")
            print(self.sensitivityAnalysis.individualResponses[outName].to_string(max_cols=None, max_rows=10))
            print()

        writer.flush()
        txt = writer.getvalue()

        self.maxDiff = None
        self.assertEqual(EXPECTED_REPORT, txt)

        writer.close()

    def test_graphs(self):
        graphs = self.sensitivityAnalysis.getImpactGraphs(False)
        for k in graphs:
            g = graphs[k] # type: plt.Figure
            g.tight_layout()
            g.savefig(path.join(IGNORE_DIRECTORY,"{}.svg".format(k)), format="svg")



        pow = self.sensitivityAnalysis.individualResponses["Probability of winning"]
        pow["Probability of winning"] *= 1_000_000
        fig,axs = self.sensitivityAnalysis.getIndivisualResponseGraphs() # type: plt.Figure, plt.Axes
        fig.tight_layout()
        fig.savefig(path.join(IGNORE_DIRECTORY,"Individual Responses.svg"), format="svg")



from pynetrees import *
from pynetrees.sensitivity import SensitivityAnalysis, Variable, Output
