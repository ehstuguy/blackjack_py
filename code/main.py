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
playAgain = ["y", "yes", "yeah", "sure", "Y", "Yes", "Yeah", "Sure", True, "true"]


class cardObj:

    def __init__(self, cardInfo):
        """Reference card suit or val at any point"""
        self.info = cardInfo
        self.suit = cardInfo[0]
        self.val = cardInfo[1]


class shoeObj:

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
        self.cards = [cardObj(hldr) for hldr in shuffledCards]


    def cutDeck(self):
        """Method used to cut the deck"""
        self.cut = random.randint(1, 263)


class playerObj:

    def __init__(self, bankroll, playerNum, bet):
        """Starting dollar amount"""
        self.hands = {}
        self.name = f"Player{playerNum}"
        self.bankroll = bankroll
        self.bet = bet


class dealerObj:
    
    def __init__(self):
        self.hands = {}
        self.name = "Dealer"


class hand:

    def __init__(self, newHand):
        """Cards that are initially dealt to player"""
        self.hand = newHand
        self.evalHand(newHand)
        pass
        

    def evalHand(self, hand):
        """Evaluate the player's hand for value and possible moves"""
        self.options = {}
        self.options["Hit"] = True
        self.options["Stand"] = True
        self.options["Surrender"] = True
        if len(hand) == 2:
            # # Split Logic
            # if hand[0].val == hand[1].val:
            #     self.options["Split"] = True
            # else:
            #     self.options["Split"] = False
            # # Double-Down Logic
            # if self.bankroll-self.bet >= self.bet:
            #     self.options["Double"] = True
            # else:
            #     self.options["Double"] = False
            # # Check for naturals
            if sum([valDict[hand[0].val], valDict[hand[1].val]]) == 21:
                self.natural = True
            else:
                self.natural = False


def checkHand(hand):
    """Given a hand, this method returns the hand value"""
    cardSymb = [i[1] for i in hand]  # remove suits for calcs
    cardVals = [valDict[i] for i in cardSymb]
    # check for naturals
    if len(cardSymb) == 2:
        handVal = sum(cardVals)
        if handVal == 21:
            choice = "a.1.0 "
            return handVal, (choice, "Blackjack!!")
        else:
            choice = "a.2.0"
            return handVal, (choice, None)
    elif len(cardSymb) > 2 and "A" not in cardSymb:
        # No Aces, 3 or more cards in hand
        handVal = sum(cardVals)
        if handVal == 21:
            choice = "b.1.0"
            return handVal, (choice, "21!")
        elif handVal < 21:
            choice = "b.2.0"
            return handVal, (choice, None)
        else:
            choice = "b.3.0"
            return handVal, (choice, "Bust!")
    else:
        # Aces, 3 or more cards in hand
        handVal = sum(cardVals)
        if handVal == 21:
            choice = "c.1.0"
            return handVal, (choice, "21!")
        elif  handVal < 21:
            choice = "c.2.0"
            return handVal, (choice, None)
        else:
            newHandVal = sum([altDict[i] for i in cardSymb])
            if newHandVal == 21:
                choice = "c.3.1"
                return newHandVal, (choice, "21!")
            elif newHandVal < 21:
                choice = "c.3.2"
                return newHandVal, (choice, None)
            else:
                choice = "c.3.3"
                return newHandVal, (choice, "Bust!")


if __name__ == "__main__":
    # for now, just 1 playable character and the NPC Dealer
    players = [playerObj(1, 1000, 50), dealerObj()]
