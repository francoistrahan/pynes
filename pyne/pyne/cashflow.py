import pandas as pd
from numbers import Real
from collections import Sequence, Mapping


def create(*args, freq=None):
    if len(args) == 0: return pd.Series()

    if len(args) == 1 :
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



