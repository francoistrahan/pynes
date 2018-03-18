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
