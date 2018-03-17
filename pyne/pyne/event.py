from .node import Node



class Event(Node):
    TYPE_NAME = "Event"


    def typeName(self):
        return Event.TYPE_NAME


    def computePossibilities(self, solver):
        ts = self.transitions  # type: list[Transition]

        # Check probabilities and patch if we have a complement
        # This could be optimised out to an init step. Keeping it separated from actual calculation
        probs = [t.probability for t in ts]
        nnprobs = [p for p in probs if p is not None]
        nNones = len(probs) - len(nnprobs)

        if nNones > 1: raise ValueError("Cannot have more than one event without explicit probability")

        totalProb = sum(nnprobs)

        if nNones == 1:
            if totalProb > 1: raise ValueError("Cannot have a complement a probabily exceeding 100%")
            pComplement = 1 - totalProb
            totalProb = 1
        else:
            pComplement = None

        self.results.cashflowDistribution = []
        self.results.valueDistribution = []

        for t in ts:  # type: Transition
            transitionProb = t.probability
            if transitionProb is None:
                transitionProb = pComplement
            else:
                transitionProb /= totalProb

            t.results.probability = transitionProb

            t.target.computePossibilities(solver)
            if t.target.results.deadEnd:
                self.results.deadEnd = True
            else:
                for prob, outcome in t.target.results.cashflowDistribution:
                    self.results.cashflowDistribution.append((transitionProb * prob, outcome))

                for prob, outcome in t.target.results.valueDistribution:
                    self.results.valueDistribution.append((transitionProb * prob, outcome))

        if not self.results.deadEnd:
            self.results.strategicValue = solver.strategy.computeStrategicValue(self.results.valueDistribution)


    def propagateEndgameDistributions(self, currentProbability):
        for t in self.transitions:
            t.target.propagateEndgameDistributions(currentProbability * t.results.probability)


    def clone(self):
        return Event(self.name, [t.clone() for t in self.transitions])



from .transition import Transition
