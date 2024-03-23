valDict = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
    7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11}
altDict = valDict.copy()
altDict["A"] = 1

class Hand:
    def __init__(self, nHand, player):
        """Cards that are initially dealt to player"""
        self.Hand = nHand
        self.Info = [n.info for n in nHand]
        self.Val = [n.val for n in nHand]
        self.Sum = sum(valDict[n.val] for n in nHand)
        if self.Sum > 21 and "A" in self.cVal:
            self.Sum = sum([altDict[i] for i in self.cVal])
        self.Bust = False
        self.Stand = False
        if player.seat != 0:
            self.Bet = player.bet
        self.eval(player)

    def eval(self, player: object):
        """Evaluate the player's hand for value and possible moves"""
        self.options = {"Hit": True, "Stand": True}
        self.naturals = False
        if len(self.Info) == 2:
            if self.Sum == 21:
                self.naturals = True
            elif player.seat != 0:
                self.options["Split"] = False
                self.options["Double"] = False
                # Split
                if self.Info[0][1] == self.Info[1][1]:
                    self.options["Split"] = True
                # Double-Down
                if player.bankroll-player.bet >= player.bet:
                    self.options["Double"] = True

    def addCard(self, nCard, player):
        """Added from hitting or doubling-down"""
        self.Info += [nCard.info]
        self.Val += [nCard.val]
        self.Sum += valDict[nCard.val]
        if self.Sum > 21 and "A" in self.Val:
            self.Sum = sum([altDict[i] for i in self.Val])
            if self.Sum > 21:
                self.Bust = True
            else:
                self.eval(player)
        elif self.Sum > 21:
            self.Bust = True
        else:
            self.eval(player)


if __name__ == "__main__":
    pass
