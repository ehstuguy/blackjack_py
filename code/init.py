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
        self.__deck__(n_decks)
        self.cut = 312
        self.reshuffle = False


    def __deck__(self, n_decks):
        """assemble deck of cards"""
        suits = ["♠", "♥", "♦", "♣"]
        vals = [i for i in range(2, 11)] + ["J", "Q", "K", "A"]
        print(vals)
        cards = list(prod(suits, vals)) * n_decks
        self.cards = random.sample(cards, k=len(cards))


    def __cut__(self):
        """method used to cut the deck"""
        self.cut = random.randint(1, 257)  # plastic card used to cut the decks in the shoe

  
class table_obj:
    def __init__(self):
        self.seats = 7


class player_obj:
    def __init__(self, money_val):
        self.bankroll = money_val
        self.hand = []


    def __bet__(self, amt):
        self.bet = amt


    def __options__(self, player_hand):
        """Check options player has to do"""
        self.options = {}
        self.options["Hit"] = True
        self.options["Stand"] = True
        self.options["Surrender"] = True
        # Split Logic ================================
        if player_hand[0][1] == player_hand[1][1]:
            self.options["Split"] = True
        else:
            self.options["Split"] = False
        # Double-Down Logic ==========================
        if self.bankroll > self.bet:
            self.options["Double"] = True
        else:
            self.options["Double"] = False


class dealer_obj:
    def __init__(self):
        self.hand = []


if __name__ == "__main__":
    # # General Shoe Tests
    shoe = shoe_obj(n_decks=6)
    # shoe.__cut__()
    # print(shoe.cards[10])
    # print(shoe.cut)

    # # General Player Tests
    player1 = player_obj(10000)
    # player1.__bet__(50)
    # player1.__options__([('♥', 4), ('♠', 4)])
    # print(player1.options)
    
    # # Example How to Deal Cards - While() Loop This
    # print(shoe.cards[0:6])
    # player1.hand = player1.hand + [shoe.cards[0]]
    # shoe.cards.remove(shoe.cards[0])
    # print(player1.hand)
    
    # print(shoe.cards[0:6])
    # player1.hand = player1.hand + [shoe.cards[0]]
    # shoe.cards.remove(shoe.cards[0])
    # print(player1.hand)

    # print(shoe.cards[0:6])
    # player1.hand = player1.hand + [shoe.cards[0]]
    # shoe.cards.remove(shoe.cards[0])
    # print(player1.hand)