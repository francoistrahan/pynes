from unittest import TestCase

from pyne.endgame import EndGame



class TestEndGame(TestCase):

    def test_scalarPayouts(self):
        self.assertEqual(None, self.egFromPayouts(None, None).payout())
        self.assertEqual(12.3, self.egFromPayouts(12.3, None).payout())
        self.assertEqual(12.3, self.egFromPayouts(None, 12.3).payout())
        self.assertEqual(-111, self.egFromPayouts(-234, 123).payout())
        self.assertEqual(0, self.egFromPayouts(-123, 123).payout())


    def egFromPayouts(self, basePayout, pushedPayout):
        eg = EndGame(basePayout=basePayout)
        eg.propagatedPayout = pushedPayout
        return eg

