import pyne.cashflow



def buildOrNotTestTree():
    didNotRain = Transition("No", target=EndGame(name="NoRoof_NoRain"))  # No rain, am I glad I did not spend
    didRain = Transition("Yes", payout=-500, probability=.1,
                         target=EndGame(name="NoRoof_Rain"))  # Rained on my stuff, lost $500 of goodies
    rainOrNot = Event("Will it Rain ?", [didRain, didNotRain, ])  # no roof: I care about the rain
    doNotBuild = Transition("No", target=rainOrNot)  # Don't build (don't spend)
    doBuild = Transition("Yes", payout=-100)  # I fix the roof, costs 100$, rain all you want.
    doIBuild = Decision("Do I buid something ?", [doBuild, doNotBuild])  # It's about do rain, do I build a roof.
    return doIBuild



def createMineralsSampleTreeScalar():
    def buyAndFindWhat(pManganese, pGold, pSilver):
        return Decision("Buy ?", (Transition("Yes", payout=-4000000, target=Event("Find What ?", (
            Transition("Manganese", probability=pManganese, payout=30000000),
            Transition("Gold", probability=pGold, payout=250000000),
            Transition("Silver", probability=pSilver, payout=150000000), Transition("Nothing"),))), Transition("No")))


    root = Decision("Conduct Survey ?", transitions=(Transition("Yes", payout=-1000000,
                                                                target=Event("Survey Positive ?", (
                                                                    Transition("Yes", probability=50,
                                                                               # to test probability normalization (50:50 chance...)
                                                                               target=buyAndFindWhat(.03, .02, .01)),
                                                                    Transition("No", probability=50,
                                                                               target=buyAndFindWhat(.0075, .0004,
                                                                                                     .00175)),))),
                                                     Transition("No", target=buyAndFindWhat(0.01, 0.0005, 0.002))))
    return root



def createMineralsSampleTreeCFPeriod():
    def CF(*args): return pyne.cashflow.create(*args, freq="M")


    def buyAndFindWhat(pManganese, pGold, pSilver):
        return Decision("Buy ?", (Transition("Yes", payout=CF({"2018-02":-4000000}), target=Event("Find What ?", (
            Transition("Manganese", probability=pManganese, payout=CF({"2018-12":30000000})),
            Transition("Gold", probability=pGold, payout=CF({"2018-12":250000000})),
            Transition("Silver", probability=pSilver, payout=CF({"2018-12":150000000})), Transition("Nothing"),))),
                                  Transition("No")))


    root = Decision("Conduct Survey ?", transitions=(Transition("Yes", payout=CF({"2018-01":-1000000}),
                                                                target=Event("Survey Positive ?", (
                                                                    Transition("Yes", probability=0.5,
                                                                               target=buyAndFindWhat(.03, .02, .01)),
                                                                    Transition("No", target=buyAndFindWhat(.0075, .0004,
                                                                                                           .00175)),))),
                                                     Transition("No", target=buyAndFindWhat(0.01, 0.0005, 0.002))))
    return root



from pyne import Transition, Event, Decision, EndGame
