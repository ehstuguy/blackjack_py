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


class shoeObj:
    def __init__(self, nDecks):
        """Put 6 decks in the shoe"""
        self.__deck__(nDecks)
        self.cut = 312
        self.reshuffle = False


    def __deck__(self, nDecks):
        """assemble deck of cards"""
        suits = ["♠", "♥", "♦", "♣"]
        vals = [i for i in range(2, 11)] + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * nDecks
        self.cards = random.sample(cards, k=len(cards))


    def __cut__(self):
        """method used to cut the deck"""
        self.cut = random.randint(1, 257)  # plastic card used to cut the decks in the shoe


class playerObj:
    def __init__(self, moneyVal):
        self.bankroll = moneyVal
        self.bet = 0
        self.stand = False


    def evalHand(self, handId, playerHand):
        """Evaluate the player's hand for value and possible moves"""
        self.eval = {}
        self.eval["Hit"] = True
        self.eval["Stand"] = True
        self.eval["Surrender"] = True
        if len(playerHand) == 2:
            # Split Logic
            if playerHand[0][1] == playerHand[1][1]:
                self.eval["Split"] = True
            else:
                self.eval["Split"] = False
            # Double-Down Logic
            if self.bankroll-self.bet >= self.bet:
                self.eval["Double"] = True
            else:
                self.eval["Double"] = False
        self.hand[handId]["options"] = self.eval
        self.eval = {}


class dealerObj:
    def __init__(self):
        self.hand = {}

    
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


def dealCard(tableSeats, dealType):
    # check if there needs to be a reshuffle
    if 312-len(shoe.cards) < shoe.cut:
        shoe.reshuffle = True
    else:
        pass

    if dealType == "Deal":
        # deal first set of cards
        for player in tableSeats:
            player.hand = [shoe.cards[0]]
            del shoe.cards[0]

        for player in tableSeats:
            player.hand += [shoe.cards[0]]
            del shoe.cards[0]
    
    elif dealType == "Split":
        pass

    else:
        # Assuming this is just hit
        pass



if __name__ == "__main__":
    # =====================================================
    # # mock game
    shoe = shoeObj(nDecks=6)
    shoe.__cut__()

    # players at the table
    npcs = 0  # NPCs
    plr = playerObj(1000)
    dlr = dealerObj()


    # simple loop
    while plr.stand == False:
        tableSeats = [plr, dlr]
        dealCard(tableSeats, "Deal")

        for player in tableSeats:
            player.handVal = checkHand(player.hand)


        print(plr.handVal[0], dlr.handVal[0])
    
        if plr.handVal[0] > dlr.handVal[0]:
            print(f"player wins! {plr.handVal[0]} > {dlr.handVal[0]}")
        elif checkHand(plr.hand) > checkHand(dlr.hand):
            print(f"tie! {plr.handVal[0]} = {dlr.handVal[0]}")
        else:
            print(f"player loses! {plr.handVal[0]} < {dlr.handVal[0]}")

        response = input("Give me an input [y/n]: ")
        if response in playAgain:
            print("Another!")
        else:
            print("You sure you don't want to play again?")
            exit()

    #     exit()
        # deal cards

    
    # =====================================================
    # # General Shoe Tests


    # p1.hand[len(p1.hand)] = {'deal': [shoe.cards[2], shoe.cards[3]]}
    # p1.hand[0]["value"] = checkHand(p1.hand[0]["deal"])
    # p1.evalHand(0, p1.hand[0]["deal"])
    # print(p1.hand)

    # p1.hand.pop(0)
    # print(p1.hand)
    

    pass