from io import StringIO
from time import sleep
from unittest import TestCase

import numpy as np
from os import path

from pyne.cashflow import create as CF
from pyne.strategy import createMaxExpected
from pyne.valueactualizer import IndexedNPV
import matplotlib.pyplot as plt

from tests import IGNORE_DIRECTORY, showTree


EXPECTED_REPORT = r"""

Base Values
                base
Strategic Value    0
Ticket Value      -8
Buy A Ticket      No


Extremums
                       Strategic Value          Ticket Value           \
                                   Low     High          Low     High   
Probability of winning               0       20       -9.998       20   
Value of winning                     0  8.18182     -9.90909  8.18182   

                       Buy A Ticket       
                                Low High  
Probability of winning           No  Yes  
Value of winning                 No  Yes  


Individual Responses
Outname
    Probability of winning  Strategic Value  Ticket Value Buy A Ticket
0             1.000000e-10         0.000000     -9.998000           No
1             1.525051e-08         0.000000     -9.694990           No
2             3.040101e-08         0.000000     -9.391980           No
3             4.555152e-08         0.000000     -9.088970           No
4             6.070202e-08         0.000000     -8.785960           No
5             7.585253e-08         0.000000     -8.482949           No
6             9.100303e-08         0.000000     -8.179939           No
7             1.061535e-07         0.000000     -7.876929           No
8             1.213040e-07         0.000000     -7.573919           No
9             1.364545e-07         0.000000     -7.270909           No
10            1.516051e-07         0.000000     -6.967899           No
11            1.667556e-07         0.000000     -6.664889           No
12            1.819061e-07         0.000000     -6.361879           No
13            1.970566e-07         0.000000     -6.058869           No
14            2.122071e-07         0.000000     -5.755859           No
15            2.273576e-07         0.000000     -5.452848           No
16            2.425081e-07         0.000000     -5.149838           No
17            2.576586e-07         0.000000     -4.846828           No
18            2.728091e-07         0.000000     -4.543818           No
19            2.879596e-07         0.000000     -4.240808           No
20            3.031101e-07         0.000000     -3.937798           No
21            3.182606e-07         0.000000     -3.634788           No
22            3.334111e-07         0.000000     -3.331778           No
23            3.485616e-07         0.000000     -3.028768           No
24            3.637121e-07         0.000000     -2.725758           No
25            3.788626e-07         0.000000     -2.422747           No
26            3.940131e-07         0.000000     -2.119737           No
27            4.091636e-07         0.000000     -1.816727           No
28            4.243141e-07         0.000000     -1.513717           No
29            4.394646e-07         0.000000     -1.210707           No
..                     ...              ...           ...          ...
70            1.060635e-06        11.212707     11.212707          Yes
71            1.075786e-06        11.515717     11.515717          Yes
72            1.090936e-06        11.818727     11.818727          Yes
73            1.106087e-06        12.121737     12.121737          Yes
74            1.121237e-06        12.424747     12.424747          Yes
75            1.136388e-06        12.727758     12.727758          Yes
76            1.151538e-06        13.030768     13.030768          Yes
77            1.166689e-06        13.333778     13.333778          Yes
78            1.181839e-06        13.636788     13.636788          Yes
79            1.196990e-06        13.939798     13.939798          Yes
80            1.212140e-06        14.242808     14.242808          Yes
81            1.227291e-06        14.545818     14.545818          Yes
82            1.242441e-06        14.848828     14.848828          Yes
83            1.257592e-06        15.151838     15.151838          Yes
84            1.272742e-06        15.454848     15.454848          Yes
85            1.287893e-06        15.757859     15.757859          Yes
86            1.303043e-06        16.060869     16.060869          Yes
87            1.318194e-06        16.363879     16.363879          Yes
88            1.333344e-06        16.666889     16.666889          Yes
89            1.348495e-06        16.969899     16.969899          Yes
90            1.363645e-06        17.272909     17.272909          Yes
91            1.378796e-06        17.575919     17.575919          Yes
92            1.393946e-06        17.878929     17.878929          Yes
93            1.409097e-06        18.181939     18.181939          Yes
94            1.424247e-06        18.484949     18.484949          Yes
95            1.439398e-06        18.787960     18.787960          Yes
96            1.454548e-06        19.090970     19.090970          Yes
97            1.469699e-06        19.393980     19.393980          Yes
98            1.484849e-06        19.696990     19.696990          Yes
99            1.500000e-06        20.000000     20.000000          Yes

[100 rows x 4 columns]

Outname
    Value of winning  Strategic Value  Ticket Value Buy A Ticket
0       1.000000e+06         0.000000     -9.909091           No
1       3.010101e+06         0.000000     -9.726354           No
2       5.020202e+06         0.000000     -9.543618           No
3       7.030303e+06         0.000000     -9.360882           No
4       9.040404e+06         0.000000     -9.178145           No
5       1.105051e+07         0.000000     -8.995409           No
6       1.306061e+07         0.000000     -8.812672           No
7       1.507071e+07         0.000000     -8.629936           No
8       1.708081e+07         0.000000     -8.447199           No
9       1.909091e+07         0.000000     -8.264463           No
10      2.110101e+07         0.000000     -8.081726           No
11      2.311111e+07         0.000000     -7.898990           No
12      2.512121e+07         0.000000     -7.716253           No
13      2.713131e+07         0.000000     -7.533517           No
14      2.914141e+07         0.000000     -7.350781           No
15      3.115152e+07         0.000000     -7.168044           No
16      3.316162e+07         0.000000     -6.985308           No
17      3.517172e+07         0.000000     -6.802571           No
18      3.718182e+07         0.000000     -6.619835           No
19      3.919192e+07         0.000000     -6.437098           No
20      4.120202e+07         0.000000     -6.254362           No
21      4.321212e+07         0.000000     -6.071625           No
22      4.522222e+07         0.000000     -5.888889           No
23      4.723232e+07         0.000000     -5.706152           No
24      4.924242e+07         0.000000     -5.523416           No
25      5.125253e+07         0.000000     -5.340680           No
26      5.326263e+07         0.000000     -5.157943           No
27      5.527273e+07         0.000000     -4.975207           No
28      5.728283e+07         0.000000     -4.792470           No
29      5.929293e+07         0.000000     -4.609734           No
..               ...              ...           ...          ...
70      1.417071e+08         2.882461      2.882461          Yes
71      1.437172e+08         3.065197      3.065197          Yes
72      1.457273e+08         3.247934      3.247934          Yes
73      1.477374e+08         3.430670      3.430670          Yes
74      1.497475e+08         3.613407      3.613407          Yes
75      1.517576e+08         3.796143      3.796143          Yes
76      1.537677e+08         3.978880      3.978880          Yes
77      1.557778e+08         4.161616      4.161616          Yes
78      1.577879e+08         4.344353      4.344353          Yes
79      1.597980e+08         4.527089      4.527089          Yes
80      1.618081e+08         4.709825      4.709825          Yes
81      1.638182e+08         4.892562      4.892562          Yes
82      1.658283e+08         5.075298      5.075298          Yes
83      1.678384e+08         5.258035      5.258035          Yes
84      1.698485e+08         5.440771      5.440771          Yes
85      1.718586e+08         5.623508      5.623508          Yes
86      1.738687e+08         5.806244      5.806244          Yes
87      1.758788e+08         5.988981      5.988981          Yes
88      1.778889e+08         6.171717      6.171717          Yes
89      1.798990e+08         6.354454      6.354454          Yes
90      1.819091e+08         6.537190      6.537190          Yes
91      1.839192e+08         6.719926      6.719926          Yes
92      1.859293e+08         6.902663      6.902663          Yes
93      1.879394e+08         7.085399      7.085399          Yes
94      1.899495e+08         7.268136      7.268136          Yes
95      1.919596e+08         7.450872      7.450872          Yes
96      1.939697e+08         7.633609      7.633609          Yes
97      1.959798e+08         7.816345      7.816345          Yes
98      1.979899e+08         7.999082      7.999082          Yes
99      2.000000e+08         8.181818      8.181818          Yes

[100 rows x 4 columns]

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
        print(self.sensitivityAnalysis.baseValues)

        print()
        print()
        print("Extremums")
        print(self.sensitivityAnalysis.extremums)

        print()
        print()
        print("Individual Responses")

        for outName in sorted(self.sensitivityAnalysis.individualResponses.keys()):
            print("Outname")
            print(self.sensitivityAnalysis.individualResponses[outName])
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



from pyne import *
from pyne.sensitivity import SensitivityAnalysis, Variable, Output
