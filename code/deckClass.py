#!/home/geyer/anaconda3/bin/python3.11

import random
import numpy as np

from itertools import product as prod
from cardClass import card

class deck:
    def __init__(self, numDecks: int) -> None:
        """Input a number of decks; 6 is most common"""
        self.makeDeck(numDecks)
        self.cutDeck()

    def makeDeck(self, numDecks: int) -> None:
        suits = ["♠", "♥", "♦", "♣"]
        vals = list(np.arange(2, 11)) + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * numDecks
        shuffledCards = random.sample(cards, k=len(cards))
        self.cards = [card(rngCard) for rngCard in shuffledCards]

    def cutDeck(self) -> None:
        self.cut = random.randint(1, len(self.cards) - 1)
    def draw(self) -> None:
        return self.cards.pop(0)


if __name__ == "__main__":
    pass
    shoe = deck(6)
    print(shoe.cards[0].info)
    pass