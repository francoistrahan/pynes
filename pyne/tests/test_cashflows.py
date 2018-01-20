from unittest import TestCase

import pandas as pd

from pyne.cashflow import cf



class TestCashflows(TestCase):

    def test_createFromScalars(self):
        cases = [1, -1, 0, .1]
        for case in cases:
            with self.subTest(case=case):
                result = cf(case)
                self.assertIsInstance(result, pd.Series)
                self.assertEqual(1, result.size)
                self.assertEqual(case, result[0])


    def test_createFromSequence(self):
        cases = [[], [0, 1, 2], range(12)]
        for case in cases:
            with self.subTest(case=case):
                result = cf(case)
                self.assertIsInstance(result, pd.Series)

                self.assertEqual(len(case), result.size)
                self.assertSequenceEqual(case, result.values.tolist())


    def test_createFromMultipleScalars(self):
        cases = [[], [0, 1, 2], range(12)]
        for case in cases:
            with self.subTest(case=case):
                result = cf(*case)
                self.assertIsInstance(result, pd.Series)

                self.assertEqual(len(case), result.size)
                self.assertSequenceEqual(case, result.values.tolist())


    def test_createFromMapping(self):
        CASES = [({}, {}), ({0:-100, 1:2, 3:4}, {}), ({pd.Period("2012-11"):1, pd.Period("2012-12"):2}, {}),
                 ({pd.Timestamp("2012-11-12"):1, pd.Timestamp("2012-12-13"):2}, {}),
                 ({"2012-11":1, "2012-12":2}, {"freq":"M"}), ]

        for number, (args, kwargs) in enumerate(CASES):
            with self.subTest("Case #{}: {}".format(number, args)):
                result = cf(args, **kwargs)
                self.assertIsInstance(result, pd.Series, "Case #{}: {}".format(number, args))

                self.assertEqual(len(args), result.size, "Case #{}: {}".format(number, args))

                for k in args.keys():
                    self.assertEqual(args[k], result[k], "Case #{}: {}".format(number, args))
