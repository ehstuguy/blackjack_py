class Dealer:
    def __init__(self) -> None:
        self.seat = 0
        self.dealt = []
        self.hands = []

    def reset(self) -> None:
        self.dealt = []
        self.hands = []


if __name__ == "__main__":
    pass