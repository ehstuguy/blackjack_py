#!/home/geyer/anaconda3/bin/python3

# import pandas as pd
import numpy as np
import random
from itertools import product as prod

valDict = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11
}

altDict = valDict.copy()
altDict["A"] = 1

hitList = ["y", "Y", True]
rmvlStatement = ("Security has removed you from the casino for "
                 "being incompetent.")
retry = "Input unrecognized, choose from: \n"


class shoe:

    def __init__(self, nDecks):
        """Input a number of decks for the shoe"""
        self.makeShoe(nDecks)
        self.cutDeck()


    def makeShoe(self, nDecks):
        """Input a number of decks for the shoe"""
        suits = ["♠", "♥", "♦", "♣"]
        vals = list(np.arange(2, 11)) + ["J", "Q", "K", "A"]
        cards = list(prod(suits, vals)) * nDecks
        shuffledCards = random.sample(cards, k=len(cards))
        self.cards = [card(rngCard) for rngCard in shuffledCards]


    def cutDeck(self):
        """Method used to cut the deck"""
        self.cut = random.randint(1, random.randint(243, 276))


class card:

    def __init__(self, cardInfo):
        """Reference card suit or val at any point"""
        self.cInfo = cardInfo
        self.suit = cardInfo[0]
        self.val = cardInfo[1]


class Player:

    def __init__(self, bankroll, playerNum):
        """Starting dollar amount and player number"""
        self.hand = {}
        self.info = {"Name": f"Player{playerNum}"}
        self.dealtHand = []
        self.info["Bankroll"] = bankroll


    def addBet(self, betAmt):
        self.info["Bet"] = betAmt


class Dealer:

    def __init__(self):
        self.hand = {}
        self.info = {"Name": "Dealer"}
        self.dealtHand = []


class hand:

    def __init__(self, nHand, playerInfo):
        """Cards that are initially dealt to player"""
        self.cInfo = [n.cInfo for n in nHand]
        self.cVal = [n.val for n in nHand]
        self.cSum = sum(valDict[n.val] for n in nHand)
        self.Bust = False
        self.eval(playerInfo)


    def eval(self, pData):
        """Evaluate the player's hand for value and possible moves"""
        self.options = {"Hit": True, "Stand": True, "Surrender": True}
        self.naturals = False
        if len(self.cInfo) == 2:
            # player has only 2 cards, so check naturals
            if self.cSum == 21:
                self.naturals = True
            if "Player" in pData["Name"]:
                self.options["Split"] = False
                self.options["Double"] = False
                # Split
                if self.cInfo[0][1] == self.cInfo[1][1]:
                    self.options["Split"] = True
                # Double-Down
                if pData["Bankroll"]-pData["Bet"] >= pData["Bet"]:
                    self.options["Double"] = True


    def addCard(self, nCard, pData):
        """Added from hitting or doubling-down"""
        # dict_keys(['cInfo', 'suit', 'val'])
        self.cInfo += [nCard.cInfo]
        self.cVal += [nCard.val]
        self.cSum += valDict[nCard.val]
        if self.cSum > 21:
            self.cSum = sum([altDict[i] for i in self.cVal])
            if self.cSum > 21:
                self.Bust = True
            else:
                self.eval(pData)
        else:
            self.eval(pData)


def decision(playerInput, choices, incompetent=0):
    allChoices = choices + [i.lower for i in choices]
    while str(playerInput) not in allChoices:
        if incompetent == 3:
            exit(f"{rmvlStatement}\n")
        incompetent = incompetent + 1
        playerInput = input(f"{retry}{choices}\n")


if __name__ == "__main__":
    # for now, just 1 playable character
    shoe = shoe(6)
    player = Player(1000, 1)
    player.addBet(50)
    dealer = Dealer()


    # deal out cards based on seats at table
    tableList = [player, dealer]
    playerList = [player]
    for plr in 2 * tableList:
        plr.dealtHand += [shoe.cards[0]]
        del shoe.cards[0]


    # Evaluate the hands of player(s) and dealer
    for plr in tableList:
        plr.hand[0] = hand(plr.dealtHand, plr.info)
        if plr.info["Name"] == "Dealer":
            print(plr.info["Name"], [plr.hand[0].cInfo[0], ('?', '?')])
        else:
            print(plr.info["Name"], plr.hand[0].cInfo)


    # 1.) For Loop to decide players
    # 2.) While loop for each player until number of hands have been played
    # 3.) While loop for each hand until player stands or busts


    # player's turn
    for plr in playerList:
        for h in plr.hand.values():
            # Naturals
            if h.naturals == True:
                if dealer.hand[0].naturals == True:
                    exit("Push")
                else:
                    exit("Blackjack!!")
            choices = [o for o in h.options if h.options[o] == True]
            inText = f"What do you wish to do? {choices}\n"
            h.decision = decision(input(f"{inText}"), choices)

            if h.decision == "Hit":
                # Add card
                pass
            if h.decision == "Stand":
                # Resolve and reveal cards of dealer and player
                pass
            if h.decision == "Surrender":
                # Return 50% bet
                pass
            if h.decision == "Double":
                # Resolve normal and 2*bet for result
                pass
            if h.decision == "Split":
                # will be a bit of a pain in the ass to make this one
                #  - have to remove current hand
                #  - create 2 new hands and eval them
                #  - run each hand through loop like this again
                #  - allow for inf. splits
                pass

    # dealer's turn
    while dealer.hand[0].cSum < 17:
        dealer.hand[0].addCard(shoe.cards[0], dealer.info)
        del shoe.cards[0]
