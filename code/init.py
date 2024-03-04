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

  
class tableObj:
    def __init__(self):
        self.seats = 7


class playerObj:
    def __init__(self, moneyVal):
        self.bankroll = moneyVal
        self.__bet__(0)
        self.hand = []  


    def __bet__(self, amt):
        self.bet = amt


    def __eval__(self, playerHand):
        """Evaluate the player's hand for value and possible moves"""
        self.eval = {}
        self.eval["hand_val"] = self.__checkVal__(playerHand)
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

    
    def __checkVal__(self, evalHand):
        """Given a hand, this method returns the hand value"""
        cardSymb = [i[1] for i in evalHand]  # remove suits for calcs
        cardVals = [valDict[i] for i in cardSymb]
        # check for naturals
        if len(cardSymb) == 2:
            # 2 cards in hand
            handVal = sum(cardVals)
            if handVal == 21:
                choice = "a.1.0  || "
                # print(choice, handVal, "Blackjack!!")
                return handVal, "Blackjack!!"
            else:
                choice = "a.2.0  || "
                # print(choice, handVal)
                return handVal, None
        elif len(cardSymb) > 2 and "A" not in cardSymb:
            # No Aces, 3 or more cards in hand
            handVal = sum(cardVals)
            if handVal == 21:
                choice = "b.1.0  || "
                # print(choice, handVal, "21!")
                return handVal, "21!"
            elif handVal < 21:
                choice = "b.2.0  || "
                print(choice, handVal)
                return handVal, None
            else:
                choice = "b.3.0  || "
                # print(choice, handVal, "Bust!")
                return handVal, "Bust!"
        else:
            # Aces, 3 or more cards in hand
            handVal = sum(cardVals)
            if handVal == 21:
                choice = "c.1.0  || "
                # print(choice, handVal, "21!")
                return handVal, "21!"
            elif  handVal < 21:
                choice = "c.2.0  || "
                # print(choice, handVal)
                return handVal, None
            else:
                newHandVal = sum([altDict[i] for i in cardSymb])
                if newHandVal == 21:
                    choice = "c.3.1  || "
                    # print(choice, newHandVal, "21!")
                    return newHandVal, "21!"
                elif newHandVal < 21:
                    choice = "c.3.2  || "
                    # print(choice, newHandVal)
                    return newHandVal, None
                else:
                    choice = "b.3.3  || "
                    # print(choice, newHandVal, "Bust!")
                    return newHandVal, "Bust!"                


class dealer_obj:
    def __init__(self):
        self.hand = []

    
    def __checkDealer__(self, evalHand):
        """Given a hand, this method returns the hand value"""
        cardSymb = [i[1] for i in evalHand]  # remove suits for calcs
        cardVals = [valDict[i] for i in cardSymb]
        if "A" in cardSymb and len(cardSymb) == 2:
            handVal = sum(cardVals)
            if handVal == 21:
                choice = "Da.1  || "
                print(choice, handVal, "Blackjack!!")
            else:
                choice = "Da.2  || "
                print(choice, handVal)


if __name__ == "__main__":
    # # General Shoe Tests
    shoe = shoeObj(nDecks=6)
    # shoe.__cut__()
    # print(shoe.cards[10])
    # print(shoe.cut)

    # # General Player Tests
    player1 = playerObj(90)
    player1.__bet__(50)
    print(player1.bet)
    player1.__eval__([('♠', 9), ('♠', 8)])
    print(player1.eval)
    print(player1.hand)

    # =====================================================

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