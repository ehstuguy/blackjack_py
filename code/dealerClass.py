class Dealer:

    def __init__(self) -> None:
        self.seat = 0
        self.dealtHand = []
        self.hands = []


    def clearHand(self) -> None:
        self.dealtHand = []
        self.hands = []
