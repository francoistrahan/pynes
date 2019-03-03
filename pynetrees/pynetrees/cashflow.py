from collections import Sequence, Mapping
from functools import partial
from numbers import Real

import pandas as pd



def create(*args, freq=None):
    if len(args) == 0: return pd.Series()

    if len(args) == 1:
        arg = args[0]

        if isinstance(arg, Real):
            args = [arg]
        else:
            args = arg

    if isinstance(args, Sequence):
        return pd.Series(args)

    elif isinstance(args, Mapping):
        keys = args.keys()

        if not keys: return pd.Series()

        types = set(type(k) for k in keys)
        if len(types) != 1: raise ValueError("Index types differ: {}".format(" != ".join(sorted(types))))

        indexType = types.pop()

        if indexType in (int, pd.Period, pd.Timestamp):
            return pd.Series(args)

        if indexType == str:
            rv = pd.Series(args)
            rv.index = pd.PeriodIndex(rv.index, freq=freq)
            return rv

        raise ValueError("")



createDays = partial(create, freq="D")
createMonths = partial(create, freq="M")
createYears = partial(create, freq="Y")



def combineCashflows(cashflows):
    cashflows = iter(cashflows)

    combined = next(cashflows)  # type: pd.Series
    while True:
        try:
            cf = next(cashflows)  # type: pd.Series
        except StopIteration:
            break
        else:
            combined = combined.add(cf, fill_value=0)

    return combined



def indexAnnuity(base, count, amount):
    return pd.Series(amount, index=range(base, base + count))



def periodAnnuity(freq, base, count, amount):
    return pd.Series(amount, index=pd.period_range(base, periods=count, freq=freq))


annuityDays = partial(periodAnnuity, "D")
annuityMonths = partial(periodAnnuity, "M")
annuityYears = partial(periodAnnuity, "Y")
