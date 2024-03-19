import random
from itertools import product as prod
import numpy as np


class Shoe:

    def __init__(self, numDecks: int) -> None:
        """Input a number of decks; 6 is most common"""
        self.makeShoe(numDecks)
        self.cutDeck()


    def makeShoe(self, numDecks: int) -> None:
        suits = ["♠", "♥", "♦", "♣"]
        vals = list(np.arange(2, 11)) + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * numDecks
        shuffledCards = random.sample(cards, k=len(cards))
        self.cards = [card(rngCard) for rngCard in shuffledCards]


    def cutDeck(self) -> None:
        self.cut = random.randint(1, random.randint(243, 276))


class card:

    def __init__(self, card: tuple) -> None:
        """Reference card suit or val at any point"""
        self.card = card
        self.suit = card[0]
        self.val = card[1]


if __name__ == "__main__":
    shoe = Shoe(6)
    print(shoe.cards[0].card)
    pass
