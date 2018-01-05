class Strategy:
    def __init__(self, reducePayouts, selectBestReducedPayout):
        self.reducePayouts = reducePayouts
        self.selectBestReducedPayout = selectBestReducedPayout


def rpExpected(payouts: list((float, float))) -> float:
    return sum(prob * payout for prob, payout in payouts)


def rpMin(payouts: list((float, float))) -> float:
    return min(payout for prob, payout in payouts)


def rpMax(payouts: list((float, float))) -> float:
    return max(payout for prob, payout in payouts)


def selectMaxRP(reducedPayouts: "list(float)") -> (int, float):
    bestIndex = None
    bestRP = float("-inf")
    for i, rp in enumerate(reducedPayouts):
        if rp > bestRP:
            bestIndex = i
            bestRP = rp

    return bestIndex, bestRP


def selectMinRP(reducedPayouts: "list(float)") -> (int, float):
    bestIndex = None
    bestRP = float("inf")
    for i, rp in enumerate(reducedPayouts):
        if rp < bestRP:
            bestIndex = i
            bestRP = rp

    return bestIndex, bestRP


def createMaxExpected(): return Strategy(rpExpected, selectMaxRP)


def createMinMin(): return Strategy(rpMin, selectMinRP)
def createMaxMax(): return Strategy(rpMax, selectMaxRP)
def createMinMax(): return Strategy(rpMax, selectMinRP)
def createMaxMin(): return Strategy(rpMin, selectMaxRP)
