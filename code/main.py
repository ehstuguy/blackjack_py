#!/home/geyer/anaconda3/bin/python3

import pandas as pd
import numpy as np
import random
from itertools import product as prod

valDict = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11
}

altDict = valDict.copy()
altDict["A"] = 1


class card:

    def __init__(self, cardInfo):
        """Reference card suit or val at any point"""
        self.info = cardInfo
        self.suit = cardInfo[0]
        self.val = cardInfo[1]


class shoe:

    def __init__(self, nDecks):
        """Input a number of decks for the shoe"""
        self.makeShoe(nDecks)
        self.reshuffle = False


    def makeShoe(self, nDecks):
        """Input a number of decks for the shoe"""
        suits = ["♠", "♥", "♦", "♣"]
        vals = [i for i in range(2, 11)] + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * nDecks
        shuffledCards = random.sample(cards, k=len(cards))
        self.cards = [card(rngCard) for rngCard in shuffledCards]


    def cutDeck(self):
        """Method used to cut the deck"""
        self.cut = random.randint(1, 263)


class player:

    def __init__(self, bankroll, playerNum):
        """Starting dollar amount and player number"""
        self.hand = {}
        self.name = f"Player{playerNum}"
        self.bankroll = bankroll


class dealer:
    
    def __init__(self):
        self.hand = {}
        self.name = "Dealer"


class hand:

    def __init__(self, nHand, handBet, playerBankroll):
        """Cards that are initially dealt to player"""
        self.cInfo = [n.info for n in nHand]
        self.cChar = [n.val for n in nHand]
        self.cVal = sum(valDict[n.val] for n in nHand)
        self.Bust = False
        self.bet = handBet
        self.BR = playerBankroll
        self.eval()
       

    def eval(self):
        """Evaluate the player's hand for value and possible moves"""
        self.options = {"Hit": True, "Stand": True, "Surrender": True}
        self.options["Split"] = False
        self.options["Double"] = False
        self.natural = False
        if len(self.cInfo) == 2:
            # Check for naturals
            if self.cVal == 21:
                self.natural = True
            # Split
            if self.cInfo[0][1] == self.cInfo[1][1]:
                self.options["Split"] = True
            # Double-Down
            if self.BR-self.bet >= self.bet:
                self.options["Double"] = True
        else:
            print("we out here")
            return 0, "0.1.1.3"
        
    
    def addCard(self, nCard):
        """Added from hitting or doubling-down"""
        # dict_keys(['info', 'suit', 'val'])
        self.cInfo += [nCard.info]
        self.cChar += [nCard.val]
        self.cVal += valDict[nCard.val]
        if self.cVal > 21:
            self.cVal = sum([altDict[i] for i in self.cChar])
            if self.cVal > 21:
                self.Bust = True
            else:
                self.eval()
        else:
            self.eval()


if __name__ == "__main__":
    # for now, just 1 playable character
    player = player(1000, 1)
    shoe = shoe(6)

    mockDeal = [shoe.cards[12], shoe.cards[6]]
    player.hand[0] = hand(mockDeal, 50, player.bankroll)
    print(player.hand[0].cInfo)
    
    player.hand[0].addCard(shoe.cards[9])
    print(player.hand[0].cInfo)
    print(player.hand[0].Bust)

