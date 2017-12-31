def buildOrNotTestTree():
    didNotRain = Transition("No", target=EndGame(name="NoRoof_NoRain"))  # No rain, am I glad I did not spend
    didRain = Transition("Yes", payout=-500, probability=.1,
                         target=EndGame(name="NoRoof_Rain"))  # Rained on my stuff, lost $500 of goodies
    rainOrNot = Event("Will it Rain ?", [didRain, didNotRain, ])  # no roof: I care about the rain
    doNotBuild = Transition("No", target=rainOrNot)  # Don't build (don't spend)
    doBuild = Transition("Yes", payout=-100)  # I fix the roof, costs 100$, rain all you want.
    doIBuild = Decision("Do I buid something ?", [doBuild, doNotBuild])  # It's about do rain, do I build a roof.
    return doIBuild



from pyne import Transition, Event, Decision, EndGame
