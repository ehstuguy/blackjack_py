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


class Shoe:

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
        self.info = {"Name": f"Player{playerNum}"}
        self.info["Bankroll"] = bankroll
        self.dealtHand = []
        self.hands = []


    def addBet(self, betAmt):
        self.info["Bet"] = betAmt


class Dealer:

    def __init__(self):
        self.info = {"Name": "Dealer"}
        self.dealtHand = []
        self.hands = []


class hand:

    def __init__(self, nHand, playerInfo):
        """Cards that are initially dealt to player"""
        self.cHand = nHand
        self.cInfo = [n.cInfo for n in nHand]
        self.cVal = [n.val for n in nHand]
        self.cSum = sum(valDict[n.val] for n in nHand)
        self.Bust = False
        self.Stand = False
        if playerInfo["Name"] != "Dealer":
            self.Bet = playerInfo["Bet"]
        self.eval(playerInfo)


    def eval(self, pData):
        """Evaluate the player's hand for value and possible moves"""
        self.options = {"Hit": True, "Stand": True}
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
        if self.cSum > 21 and "A" in self.cVal:
            self.cSum = sum([altDict[i] for i in self.cVal])
            if self.cSum > 21:
                self.Bust = True
            else:
                self.eval(pData)
        elif self.cSum > 21:
            self.Bust = True
        else:
            self.eval(pData)


def decision(opts, incompetent=0):
    # Left room for a comment
    playerInput = input(f"Make a choice: {opts}\n>>> ").lower()
    allChoices = opts + [i.lower() for i in opts]
    # Left room for another comment
    while playerInput not in allChoices:
        if incompetent == 3:
            exit(f"\n{'>:(    '*10}\n{rmvlStatement}\n")
        incompetent = incompetent + 1
        playerInput = input(f"{retry}{opts}\n>>> ")

    return playerInput


def playDecision(currPlr, hnd, currHand, shoe):
    while hnd.Stand == False and hnd.Bust == False:
        if len(hnd.cHand) > 2:
            print("3+ cards")
        elif hnd.naturals == True and dealer.hand[0].naturals == True:
            exit("Push")  # for succeeding naturals, payout and delete hand from
        elif hnd.naturals == True:
            exit("Blackjack!")
        elif dealer.hands[0].naturals == True:
            exit("Dealer Blackjack :(")
        print("No Naturals, please continue...")
        options = [o for o in hnd.options if hnd.options[o] == True]

        if hnd.naturals == False:
            print("\nHand:\n", hnd.cInfo, "\n value:", hnd.cSum, "\n")
            hnd.decision = decision(options)
        else:
            hnd.Stand == True

        # Player decision for non-natural hands play here
        if hnd.decision == "hit":
            # Add card
            hnd.addCard(shoe.cards[0], currPlr.info)
            del shoe.cards[0]
            print(hnd.cInfo)
        elif hnd.decision == "stand":
            hnd.Stand = True
        elif hnd.decision == "double":
            # End hand options after adding one more card & 2x bet
            hnd.Bet = 2 * hnd.Bet
            hnd.addCard(shoe.cards[0], currPlr.info)
            del shoe.cards[0]
            hnd.Stand = True
        elif hnd.decision == "split":
            # Split cards and make two new hands
            split1 = hand([hnd.cHand[0], shoe.cards[0]], currPlr.info)
            del shoe.cards[0]
            split2 = hand([hnd.cHand[1], shoe.cards[0]], currPlr.info)
            del shoe.cards[0]
            currPlr.hands.pop(currHand-1)
            currPlr.hands.insert(currHand-1, split2)
            currPlr.hands.insert(currHand-1, split1)
            hnd = currPlr.hands[0]


if __name__ == "__main__":
    # for now, just 1 playable character
    shoe = Shoe(6)
    player = Player(1000, 1)
    player.addBet(50)
    dealer = Dealer()

    # deal out cards based on seats at table
    tableList = [player, dealer]
    playerList = [player]

    playerCards = [card(("♥", 7)), card(("♦", 7))]
    player.hands.append(hand(playerCards, player.info))

    dealerCards = [card(("♥", 10)), card(("♦", 7))]
    dealer.hands.append(hand(dealerCards, dealer.info))

    # # deal out cards based on seats at table ====================
    # for plr in 2 * tableList:
    #     plr.dealtHand += [shoe.cards[0]]
    #     del shoe.cards[0]

    # # Evaluate the hands of player(s) and dealer ================
    # for plr in tableList:
    #     plr.hand[0] = hand(plr.dealtHand, plr.info)
    #     if plr.info["Name"] == "Dealer":
    #         print(plr.info["Name"], [plr.hand[0].cInfo[0], ('?', '?')])
    #     else:
    #         print(plr.info["Name"], plr.hand[0].cInfo)

    for currPlayer in playerList:
        currHand = 1
        while currHand <= len(currPlayer.hands):
            for thisHand in currPlayer.hands:
                playDecision(currPlayer, thisHand, currHand, shoe)
            currHand = currHand + 1

    # dealer's turn =============================================
    while dealer.hands[0].cSum < 17:
        dealer.hands.addCard(shoe.cards[0], dealer.info)
        del shoe.cards[0]

    for player in tableList:
        print(f"\n{player.info['Name']}")
        if len(player.hands) < 1:
            pass
        else:
            for allHands in player.hands:
                print(allHands.cSum, allHands.cInfo)


