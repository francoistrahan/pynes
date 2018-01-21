class Strategy:
    def __init__(self, computeStrategicValue, selectBestStrategicValue):
        self.computeStrategicValue = computeStrategicValue
        self.selectBestStrategicValue = selectBestStrategicValue

def rpExpected(strategicValues: list((float, float))) -> float:
    return sum(prob * sv for prob, sv in strategicValues)


def rpMin(strategicValues: list((float, float))) -> float:
    return min(sv for prob, sv in strategicValues)


def rpMax(strategicValues: list((float, float))) -> float:
    return max(sv for prob, sv in strategicValues)


def selectMaxRP(strategicValues: "list(float)") -> (int, float):
    bestIndex = None
    bestSV = float("-inf")
    for i, rp in enumerate(strategicValues):
        if rp > bestSV:
            bestIndex = i
            bestSV = rp

    return bestIndex, bestSV


def selectMinRP(strategicValues: "list(float)") -> (int, float):
    bestIndex = None
    bestSV = float("inf")
    for i, rp in enumerate(strategicValues):
        if rp < bestSV:
            bestIndex = i
            bestSV = rp

    return bestIndex, bestSV


def createMaxExpected(): return Strategy(rpExpected, selectMaxRP)


def createMinMin(): return Strategy(rpMin, selectMinRP)
def createMaxMax(): return Strategy(rpMax, selectMaxRP)
def createMinMax(): return Strategy(rpMax, selectMinRP)
def createMaxMin(): return Strategy(rpMin, selectMaxRP)
