class card:
    def __init__(self, card: tuple) -> None:
        """Reference card suit or val at any point"""
        self.info = card
        self.suit = card[0]
        self.val = card[1]


if __name__ == "__main__":
    pass