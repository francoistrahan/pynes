from unittest import TestCase



class TestScratches(TestCase):

    def test_multilevelIndexes(self):
        import pandas as pd
        import numpy as np

        outputs = ["out{}".format(i) for i in range(5)]
        extremums = ["min", "max"]

        index = pd.MultiIndex.from_product((outputs, extremums))

        nr = 5

        df = pd.DataFrame(columns=index, index=["row{}".format(i) for i in range(5)])

        for r in range(5):
            for o in range(len(outputs)):
                v = 10 * r + o
                rn = "row{}".format(r)
                o = outputs[o]
                df.loc[rn,(o,"min")] = -v
                df.loc[rn,(o,"max")] = v

        print(df.columns.levels[0])
