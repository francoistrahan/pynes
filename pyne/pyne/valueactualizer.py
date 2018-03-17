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



SCALAR_ACTUALIZER = ScalarActualizer()
SUMMING_ACTUALIZER = SummingActualizer()
