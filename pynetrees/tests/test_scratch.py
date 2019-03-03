from math import *
from os import path
from unittest import TestCase

import matplotlib.pyplot as plt
import numpy.random as random
import pandas as pd

from tests import IGNORE_DIRECTORY



class TestScratches(TestCase):

    def test_randoms(self):
        n = 1_000_000
        df = pd.DataFrame(
            {
                "Value of Land":random.normal(10, 5, n),
                "Probability of oil":random.uniform(.3, .6, n),
            }
        )  # type: pd.DataFrame

        ngraphs = len(df.columns)
        fig, axs = plt.subplots(ngraphs, 1, figsize=(6, ngraphs * 4))  # type: plt.Figure, plt.Axes

        for i in range(ngraphs):
            ax = axs[i] # type: plt.Axes
            col = df.columns[i]
            serie = df[col]  # type: pd.Series
            serie.hist(ax=ax, bins=30)
            ax.set_axisbelow(True)

        fig.savefig(path.join(IGNORE_DIRECTORY, "test_randoms_histograms.svg"), format="svg")

        print(df.head(3))
        print("...")
        print(df.tail(3))
