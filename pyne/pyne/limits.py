from collections import namedtuple
from functools import partial
from numbers import Real

import pandas as pd


Limit = namedtuple("Limit", ("name", "predicate"))



def failIfUnderThreshold(threshold, value):
    diff = value - threshold

    return diff < 0, abs(diff)

def failIfOverThreshold(threshold, value):
    diff = value - threshold

    return diff > 0, abs(diff)


def valueUnderThreshold(threshold: Real):
    return partial(failIfUnderThreshold, threshold)



def cashflowRollsumUnderThreshold(threshold: Real):
    def predicate(cf: pd.Series):
        value = cf.expanding().sum().min()
        return failIfUnderThreshold(threshold, value)

    return predicate



def expectedTTROverThreshold(threshold: Real):
    def predicate(cfs: list((Real, pd.Series))):
        value = rpExpected((prob, TTR_ACTUALIZER.actualize(cf)) for prob, cf in cfs)
        return failIfOverThreshold(threshold, value)

    return predicate


def valueVarianceOverThreshold(threshold: Real):
    def predicate(values: list((Real, Real))):
        value = rpStandardDeviation(values)
        return failIfOverThreshold(threshold, value)

    return predicate


from .strategy import *
from .valueactualizer import TTR_ACTUALIZER
