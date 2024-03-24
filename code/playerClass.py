#!/home/geyer/anaconda3/bin/python3.11

class Player:
    def __init__(self, bankroll: int, playerSeat: int) -> None:
        """Starting dollar amount of money and player seat"""
        self.seat = playerSeat
        self.bankroll = bankroll
        self.bet = None
        self.insurance = None
        self.dealt = []
        self.hands = []
        self.done = False

    def addBet(self, amount: int) -> None:
        self.bet = amount

    def reset(self) -> None:
        self.bet = None
        self.dealt = []
        self.hands = []
        self.done = False


if __name__ == "__main__":
    pass
