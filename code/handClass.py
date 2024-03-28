#!/home/geyer/anaconda3/bin/python3.11

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
        self.paid = False
        self.push = None
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
                gdBet = player.bankroll >= player.trueBet + player.bet
                sameCards = self.info[0] == self.info[1]
                self.options["Split"] = False
                self.options["Double"] = False
                if sameCards == True and gdBet == True:
                    self.options["Split"] = True
                else:
                    pass
                if gdBet == True:
                    self.options["Double"] = True
                else:
                    pass
        else:
            if self.sum == 21:
                self.stand = True
            elif self.sum > 21:
                self.bust = True
                self.stand = True
            else:
                pass


    def payOut(self, player: object, handBet: int) -> None:
        if self.naturals == True and self.paid == False:
            player.bankroll += int(handBet)
            self.paid = True
        elif self.push == True:
            player.bankroll += 0
        elif self.win == True and self.naturals == False:
            player.bankroll += int(handBet)
        elif self.win == False:
            player.bankroll -= int(handBet)
        else:
            pass

        print(f"\n|Player {player.seat}| Hand:\n {self.info}"
              f"\n value = {self.sum}"
              f"\n win: {self.win}, push: {self.push}"
              f"\n bankroll: {player.bankroll}")


if __name__ == "__main__":
    pass