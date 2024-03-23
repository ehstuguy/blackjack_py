valDict = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11}
altDict = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 1}


class Hand:
    def __init__(self, nCard: list[object], player: object) -> None:
        """Cards that are initially dealt to player"""
        self.cards = []
        self.info = []
        self.val = []
        if player.seat != 0:
            self.bet = player.bet   # bet might be doubled later
            self.win = None
            self.decision = None
        self.bust = False
        self.stand = False
        self.naturals = None
        self.checkHand(nCard, player)

    def checkHand(self, nCard: list[object], player: object) -> None:
        self.cards += nCard
        self.info = [n.info for n in self.cards]
        self.val = [n.val for n in self.cards]
        self.sum = sum(valDict[n] for n in self.val)
        if self.sum > 21:
            newSum = sum(altDict[n] for n in self.val)
            if newSum <= 11 and "A" in self.val:
                self.sum = newSum - 1 + 11
            else:
                self.sum = newSum
        # bust or evaluate
        if self.sum > 21:
            self.bust = True
            self.stand = True
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
        else:
            if self.sum == 21:
                self.stand = True
            elif self.sum > 21:
                self.bust = True
                self.stand = True


    def payOut(self, player: object) -> None:
        if self.naturals == True:
            player.bankroll += player.bet * 1.5
        elif self.win == True and self.naturals == False:
            player.bankroll += player.bet
        elif self.win == False:
            player.bankroll -= player.bet


if __name__ == "__main__":
    pass