def minPayout(payouts):
    return min(prob * payout for prob, payout in payouts)



def expectedPayout(payouts):
    return sum(prob * payout for prob, payout in payouts)



def maxPayout(payouts):
    return max(prob * payout for prob, payout in payouts)



def maxExpectedPayout(options):
    bestIndex = None
    bestExpectedPayout = float("-inf")
    bestPayouts = None
    for i, payouts in enumerate(options):
        expPayout = expectedPayout(payouts)
        if expPayout > bestExpectedPayout:
            bestIndex = i
            bestExpectedPayout = bestExpectedPayout
            bestPayouts = payouts
    return bestIndex, bestPayouts


def maxMaxPayout(options):
    bestIndex = None
    bestExpectedPayout = float("-inf")
    bestPayouts = None
    for i, payouts in enumerate(options):
        expPayout = maxPayout(payouts)
        if expPayout > bestExpectedPayout:
            bestIndex = i
            bestExpectedPayout = bestExpectedPayout
            bestPayouts = payouts
    return bestIndex, bestPayouts
