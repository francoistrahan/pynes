def maxExpectedValue(options):
    bestIndex = None
    bestExpectedPayout = float("-inf")
    bestPayouts = None
    for i, payouts in enumerate(options):
        expectedPayout = expectedValue(payouts)
        if expectedPayout > bestExpectedPayout:
            bestIndex = i
            bestExpectedPayout = bestExpectedPayout
            bestPayouts = payouts

    return bestIndex, bestPayouts



def expectedValue(payouts):
    return sum(prob * payout for prob, payout in payouts)
