from itertools import repeat
from unittest import TestCase

import pandas as pd
import pyne.cashflow as cf



class TestCashflows(TestCase):

    def test_createFromScalars(self):
        cases = [1, -1, 0, .1]
        for case in cases:
            with self.subTest(case=case):
                result = cf.create(case)
                self.assertIsInstance(result, pd.Series)
                self.assertEqual(1, result.size)
                self.assertEqual(case, result[0])


    def test_createFromSequence(self):
        cases = [[], [0, 1, 2], range(12)]
        for case in cases:
            with self.subTest(case=case):
                result = cf.create(case)
                self.assertIsInstance(result, pd.Series)

                self.assertEqual(len(case), result.size)
                self.assertSequenceEqual(case, result.values.tolist())


    def test_createFromMultipleScalars(self):
        cases = [[], [0, 1, 2], range(12)]
        for case in cases:
            with self.subTest(case=case):
                result = cf.create(*case)
                self.assertIsInstance(result, pd.Series)

                self.assertEqual(len(case), result.size)
                self.assertSequenceEqual(case, result.values.tolist())


    def test_createFromMapping(self):
        CASES = [({}, {}), ({0:-100, 1:2, 3:4}, {}), ({pd.Period("2012-11"):1, pd.Period("2012-12"):2}, {}),
                 ({pd.Timestamp("2012-11-12"):1, pd.Timestamp("2012-12-13"):2}, {}),
                 ({"2012-11":1, "2012-12":2}, {"freq":"M"}), ]

        for number, (args, kwargs) in enumerate(CASES):
            with self.subTest("Case #{}: {}".format(number, args)):
                result = cf.create(args, **kwargs)
                self.assertIsInstance(result, pd.Series, "Case #{}: {}".format(number, args))

                self.assertEqual(len(args), result.size, "Case #{}: {}".format(number, args))

                for k in args.keys():
                    self.assertEqual(args[k], result[k], "Case #{}: {}".format(number, args))


    def test_CombineIndex(self):
        cf1 = [-100]
        cf2 = [0] + [5] * 10
        cf3 = {3:-10, 10:40}

        cfs = (cf1, cf2, cf3)
        cfs = [cf.create(c) for c in cfs]
        cfTot = cf.combineCashflows(cfs)
        EXPECTED = pd.Series({0:- 100, 1:5.0, 2:5.0, 3:- 5.0, 4:5.0, 5:5.0, 6:5.0, 7:5.0, 8:5.0, 9:5.0, 10:45.0,
                              })

        self.assertTrue(cfTot.eq(EXPECTED).all(), msg="Expected:\n{}\n\nReal:\n{}".format(EXPECTED, cfTot))


    def test_CombineDates(self):
        cf1 = cf.create({"2018-01":-100}, freq="M")
        cf2 = pd.Series(5, pd.period_range("2018-02", periods=10, freq="M"))
        cf3 = cf.create({'2018-04':-10, '2018-11':40}, freq="M")

        cfs = (cf1, cf2, cf3)
        cfTot = cf.combineCashflows(cfs)
        EXPECTED = pd.Series(
            [- 100, 5.0, 5.0, - 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 45.0],
            pd.period_range("2018-01", periods=11, freq="M")
        )

        self.assertTrue(cfTot.eq(EXPECTED).all(), msg="Expected:\n{}\n\nReal:\n{}".format(EXPECTED, cfTot))
