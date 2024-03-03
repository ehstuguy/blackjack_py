#!/home/geyer/anaconda3/bin/python3

import pandas as pd
import numpy as np
import random


from itertools import product as prod


class shoe_obj:
    def __init__(self, n_decks):
        """ build a deck"""
        self.deck(n_decks)
        self.plcd = 312
        self.reshuffle = False


    def deck(self, n_decks):
        suits = ["♠", "♥", "♦", "♣"]
        vals = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * n_decks
        self.cards = random.shuffle(cards)



    def cut(self):
        """ method used to cut the deck"""
        self.plcd = random.randint(1, 257)  # plastic card used to cut the decks in the shoe


if __name__ == "__main__":
    shoe = shoe_obj(n_decks=6)

    print(shoe.reshuffle)