valDict = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11}
altDict = valDict.copy()
altDict["A"] = 1

class Hand:
    def __init__(self, nCard, player) -> None:
        """Cards that are initially dealt to player"""
        self.hand = []
        self.info = []
        self.val = []
        if player.seat != 0:
            self.Bet = player.bet
        self.Bust = False
        self.Stand = False
        self.checkHand(nCard, player)

    def checkHand(self, nCard, player) -> None:
        self.info += [n.info for n in nCard]
        self.val += [n.val for n in nCard]
        self.sum = sum(valDict[n.val] for n in nCard)
        if self.sum > 21 and "A" in self.Val:
            self.sum = sum([altDict[i] for i in self.Val])
            if self.sum > 21:
                self.Bust = True
            else:
                self.eval(player)
        elif self.sum > 21:
            self.Bust = True
        else:
            self.eval(player)

    def eval(self, player: object) -> None:
        """Evaluate the player's hand for value and possible moves"""
        self.options = {"Hit": True, "Stand": True}
        self.naturals = False
        if len(self.info) == 2:
            if self.sum == 21:
                self.naturals = True
            elif player.seat != 0:
                self.options["Split"] = False
                self.options["Double"] = False
                if self.info[0][1] == self.info[1][1]:
                    self.options["Split"] = True
                if player.bankroll-player.bet >= player.bet:
                    self.options["Double"] = True


if __name__ == "__main__":
    pass
