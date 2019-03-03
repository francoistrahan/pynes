from abc import ABCMeta, abstractmethod
from numbers import Real

import pandas as pd



class ValueActualizer(metaclass=ABCMeta):

    @abstractmethod
    def actualize(self, cashflow) -> Real:
        pass



class ScalarActualizer(ValueActualizer):

    def actualize(self, cashflow):
        assert isinstance(cashflow, Real)

        return cashflow



class SummingActualizer(ValueActualizer):


    def actualize(self, cashflow) -> Real:
        assert isinstance(cashflow, pd.Series)

        return cashflow.sum()



class TimeToRecoveryActualizer(ValueActualizer):

    def actualize(self, cashflow: pd.Series) -> Real:
        assert isinstance(cashflow, pd.Series)

        cashflow = cashflow.expanding().sum()

        cfiter = iter(cashflow.iteritems())

        # Still positive
        try:
            while True:
                period, amount = next(cfiter)
                if amount < 0:  # switching negative
                    firstNegativePeriod = period
                    break
        except StopIteration:
            return 0

        # Went under zero
        try:
            while True:
                period, amount = next(cfiter)
                if amount >= 0:  # back to positive
                    breakEvenPeriod = period
                    break
        except StopIteration:
            return None

        # Back in black
        try:
            while True:
                period, amount = next(cfiter)
                if amount < 0:  # Going under zero for a second time: cannot evaluate
                    return None
        except StopIteration:
            return breakEvenPeriod - firstNegativePeriod

        # Done



class IndexedNPV(ValueActualizer):

    def __init__(self, ratePerPeriod):
        self.ratePerPeriod = ratePerPeriod


    def actualize(self, cashflow: pd.Series) -> Real:
        npv = 0

        r = self.ratePerPeriod
        for period, amount in cashflow.iteritems():
            npv += amount / pow(1 + self.ratePerPeriod, period)
        return npv


class PeriodNPV(ValueActualizer):
    def __init__(self, ratePerPeriod, initialPeriod):
        self.initialPeriod = initialPeriod
        self.ratePerPeriod = ratePerPeriod


    def actualize(self, cashflow: pd.Series) -> Real:
        npv = 0

        r = self.ratePerPeriod
        t0 = self.initialPeriod
        for period, amount in cashflow.iteritems():
            period = period - t0
            npv += amount / pow(1 + self.ratePerPeriod, period)
        return npv


SCALAR_ACTUALIZER = ScalarActualizer()
SUMMING_ACTUALIZER = SummingActualizer()
TTR_ACTUALIZER = TimeToRecoveryActualizer()
