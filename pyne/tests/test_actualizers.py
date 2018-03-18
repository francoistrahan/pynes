from unittest import TestCase

from pyne.cashflow import create as CF
from pyne.valueactualizer import *



class TestActualizers(TestCase):

    def test_ttr(self):
        CASES = [({0:-5, 1:1.1, 2:1.1, 3:1.1, 4:1.1, 5:1.1}, 5, dict()), (
            {"2017-01":-5, "2017-02":1.1, "2017-03":1.1, "2017-04":1.1, "2017-05":1.1, "2017-06":1.1}, 5, {"freq":"m"}),

                 ]
        for cf, expected, args in CASES:
            with self.subTest("TTR:{} CF:{}".format(expected, cf)):
                cf = CF(cf, **args)
                self.assertEqual(expected, TTR_ACTUALIZER.actualize(cf))


    def test_indexedNPV(self):
        CASES = [(0, 0, dict()), (0, 1, dict()), (0, 0, {0:-1, 1:2, 3:-1}), (100, 0, {0:100}), (100, .2, {0:100}),
                 (100, .1, {1:110}), (20.6123158680855, .12, {0:-100, 4:10, 5:10, 6:10, 7:10, 8:10, 9:10, 15:500, })]

        for expected, rate, cf in CASES:
            cf = CF(cf)
            with self.subTest("{} from {}".format(expected, cf)):
                actualizer = IndexedNPV(rate)
                self.assertAlmostEqual(expected, actualizer.actualize(cf))


    def test_periodNPV(self):
        CASES = [(pd.Period("2018-01-01", "D"), 0, 0, dict(), None), (pd.Period("2018-01-01", "D"), 0, 1, dict(), None),
                 (pd.Period("2018-01-01", "D"), 0, 0, {"2018-01-01":-1, "2018-01-02":2, "2018-01-03":-1}, "D"),
                 (pd.Period("2018-01-01", "D"), 100, 0, {pd.Period("2018-01-01", "D"):100}, None),
                 (pd.Period("2018-01-01", "D"), 100, .2, {pd.Period("2018-01-01", "D"):100}, None),
                 (pd.Period("2018-01-01", "D"), 100, .1, {pd.Period("2018-01-02", "D"):110}, None),
                 (pd.Period("2018-01", "M"), 100, .1, {pd.Period("2018-02", "M"):110}, None),
                 (pd.Period("2018-01", "M"), 100, .1, {pd.Period("2018-03", "M"):121}, None), (
                     pd.Period("2018-01-01", "D"), 20.6123158680855, .12, {
                         "2018-01-01":-100,
                         "2018-01-05":10,
                         "2018-01-06":10,
                         "2018-01-07":10,
                         "2018-01-08":10,
                         "2018-01-09":10,
                         "2018-01-10":10,
                         "2018-01-16":500,
                     }, "D"), (pd.Period("2018-01", "M"), 20.6123158680855, .12, {
                "2018-01":-100,
                "2018-05":10,
                "2018-06":10,
                "2018-07":10,
                "2018-08":10,
                "2018-09":10,
                "2018-10":10,
                "2019-04":500,
            }, "M"), (pd.Period("2018", "Y"), 20.6123158680855, .12,
                      {"2018":-100, "2022":10, "2023":10, "2024":10, "2025":10, "2026":10, "2027":10, "2033":500,
                       }, "Y"), ]

        for initialPeriod, expected, rate, cf, freq in CASES:
            cf = CF(cf, freq=freq)
            with self.subTest("{} from {}".format(expected, cf)):
                actualizer = PeriodNPV(rate, initialPeriod)
                self.assertAlmostEqual(expected, actualizer.actualize(cf))
