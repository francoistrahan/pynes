import pandas as pd
from collections import namedtuple


Limit = namedtuple("Limit", ("name", "predicate"))



def cummulativeCashflowNeverUnderTreshold(threshold):
    def predicate(cf: pd.Series):
        m = cf.expanding().sum().min()

        diff = m - threshold

        if diff < 0:
            return True, -diff
        else:
            return False, diff

        return False


    return predicate
