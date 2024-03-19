valDict = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
    7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11}
altDict = valDict.copy()
altDict["A"] = 1

class hand:

    def __init__(self, nHand, playerInfo):
        """Cards that are initially dealt to player"""
        self.cHand = nHand
        self.cInfo = [n.cInfo for n in nHand]
        self.cVal = [n.val for n in nHand]
        self.cSum = sum(valDict[n.val] for n in nHand)
        self.Bust = False
        self.Stand = False
        if playerInfo["Name"] != "Dealer":
            self.Bet = playerInfo["Bet"]
        self.eval(playerInfo)


    def eval(self, pData):
        """Evaluate the player's hand for value and possible moves"""
        self.options = ["Hit", "Stand"]
        self.naturals = False
        if len(self.cInfo) == 2:
            # player has only 2 cards, so check naturals
            if self.cSum == 21:
                self.naturals = True
            if "Player" in pData["Name"]:
                self.options["Split"] = False
                self.options["Double"] = False
                # Split
                if self.cInfo[0][1] == self.cInfo[1][1]:
                    self.options["Split"] = True
                # Double-Down
                if pData["Bankroll"]-pData["Bet"] >= pData["Bet"]:
                    self.options["Double"] = True


    def addCard(self, nCard, pData):
        """Added from hitting or doubling-down"""
        self.cInfo += [nCard.cInfo]
        self.cVal += [nCard.val]
        self.cSum += valDict[nCard.val]
        if self.cSum > 21 and "A" in self.cVal:
            self.cSum = sum([altDict[i] for i in self.cVal])
            if self.cSum > 21:
                self.Bust = True
            else:
                self.eval(pData)
        elif self.cSum > 21:
            self.Bust = True
        else:
            self.eval(pData)


if __name__ == "__main__":
    pass
