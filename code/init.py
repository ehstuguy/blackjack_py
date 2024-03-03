#!/home/geyer/anaconda3/bin/python3

import pandas as pd
import numpy as np
import random

from itertools import product as prod


val_dict = {
    "J": 10, 
    "Q": 10, 
    "K": 10, 
    "A": 11
}

alt_dict ={
    "J": 10, 
    "Q": 10, 
    "K": 10, 
    "A": 1
}

class shoe_obj:
    def __init__(self, n_decks):
        """initialize"""
        self.deck(n_decks)
        self.plcd = 312
        self.reshuffle = False


    def deck(self, n_decks):
        """assemble deck of cards"""
        suits = ["♠", "♥", "♦", "♣"]
        vals = [i for i in range(2, 11)] + ["J", "Q", "K", "A"]
        print(vals)
        cards = list(prod(suits, vals)) * n_decks
        self.cards = random.sample(cards, k=len(cards))


    def cut(self):
        """method used to cut the deck"""
        self.plcd = random.randint(1, 257)  # plastic card used to cut the decks in the shoe

  
class table_obj:
    def __init__(self):
        self.seats = 7


class player_obj:
    def __init__(self, money_val):
        self.bankroll = money_val
        self.hand = []


    def bet(self, amt):
        pass


    def deal(self):
        pass


class dealer_obj:
    def __init__(self):
        self.hand = []


if __name__ == "__main__":
    shoe = shoe_obj(n_decks=6)
    # print(shoe.cards[0][1])

    player1 = player_obj(10000)
    # print(player1.hand)


    # # Example of how to loop over dealing cards
    print(shoe.cards[0:6])
    print(player1.hand)

    player1.hand = player1.hand.append(shoe.cards[0])
    shoe.cards.remove(shoe.cards[0])
    print(shoe.cards[0:6])
    print(player1.hand)

    player1.hand = player1.hand.append(shoe.cards[0])
    shoe.cards.remove(shoe.cards[0])
    print(shoe.cards[0:6])
    print(player1.hand)

    player1.hand = player1.hand.append(shoe.cards[0])
    shoe.cards.remove(shoe.cards[0])
    print(shoe.cards[0:6])
    print(player1.hand)