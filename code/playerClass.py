class Player:

    def __init__(self, bankroll: int, playerSeat: int) -> None:
        """Starting dollar amount of money and player seat"""
        self.seat = playerSeat
        self.bankroll = bankroll
        self.dealtHand = []
        self.hands = []


    def addBet(self, amount: int) -> None:
        self.bet = amount


    def clearHand(self) -> None:
        self.dealtHand = []
        self.hands = []
        self.bet = 0


if __name__ == "__main__":
    pass
