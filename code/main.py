#!/home/geyer/anaconda3/bin/python3

import numpy as np
import random
from itertools import product as prod

valDict = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, "J": 10, "Q": 10, "K": 10, "A": 11}
altDict = valDict.copy()
altDict["A"] = 1
rmvMsg = "Security is removing you from the casino for incompetence."
retryMsg = "Input unrecognized, choose from: \n"
contDict = {"Y": True, "y": True, "Yes": True, "yes": True,
    "n": False, "N": False, "no": False, "No": False}


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


def decision(opts, dType, incompetent=0):
    # Left room for a comment
    if dType == "Play":
        playerInput = input(f"Make a choice: {opts}\n>>> ").lower()
    elif dType == "Cont":
        playerInput = input("Continue? [Y/n]\n>>> ")
    allChoices = opts + [i.lower() for i in opts]
    # Left room for another comment
    while playerInput not in allChoices:
        if incompetent == 3:
            exit(f"\n{'>:(    '*10}\n{rmvMsg}\n")
        incompetent = incompetent + 1
        playerInput = input(f"{retryMsg}{opts}\n>>> ")

    return playerInput


def playDecision(currPlr, hnd, currHand, shoe):
    while hnd.Stand == False and hnd.Bust == False:
        options = [o for o in hnd.options if hnd.options[o] == True]
        vsHands = (f"\nDealer's Hand:\n {currPlr.dealerHand}\n"
            f"\nHand:\n {hnd.cInfo}\n value: {hnd.cSum}\n")\

        if len(hnd.cHand) > 2:
            pass  # and
        elif hnd.naturals == True and dealer.hands[0].naturals == True:
            exit("Push\n")
        elif hnd.naturals == True:
            exit("Blackjack!")
        elif dealer.hands[0].naturals == True:
            exit("Dealer Blackjack :(")

        if hnd.naturals == False:
            print(vsHands)
            hnd.decision = decision(options)
        else:
            hnd.Stand == True

        # Player decision for non-natural hands play here
        if hnd.decision == "hit":
            hnd.addCard(shoe.cards[0], currPlr.info)
            del shoe.cards[0]
        elif hnd.decision == "stand":
            hnd.Stand = True
        elif hnd.decision == "double":
            hnd.Bet = 2 * hnd.Bet
            hnd.addCard(shoe.cards[0], currPlr.info)
            del shoe.cards[0]
            hnd.Stand = True
        elif hnd.decision == "split":
            split1 = hand([hnd.cHand[0], shoe.cards[0]], currPlr.info)
            del shoe.cards[0]
            split2 = hand([hnd.cHand[1], shoe.cards[0]], currPlr.info)
            del shoe.cards[0]
            currPlr.hands.pop(currHand-1)
            currPlr.hands.insert(currHand-1, split2)
            currPlr.hands.insert(currHand-1, split1)
            hnd = currPlr.hands[0]
        if hnd.Bust == True:
            print("\nBUST!!\n")
        if hnd.cSum == 21:
            hnd.Stand = True


def playGame(shoe, tableList, playerList):
    for player in 2 * tableList:
        player.dealtHand += [shoe.cards[0]]
        del shoe.cards[0]

    # Evaluate the hands of player(s) and dealer
    for player in tableList:
        player.hands.append(hand(player.dealtHand, player.info))

    # Players make there decisions
    dealerInfo = [dealer.hands[0].cInfo[0], ('?', '?')]
    for currPlayer in playerList:
        currHand = 1
        currPlayer.dealerHand = dealerInfo
        while currHand <= len(currPlayer.hands):
            for thisHand in currPlayer.hands:
                playDecision(currPlayer, thisHand, currHand, shoe)
            currHand = currHand + 1

    # Check player's Hand before going to dealer

    # Dealer's turn
    while dealer.hands[0].cSum < 17:
        dealer.hands[0].addCard(shoe.cards[0], dealer.info)
        del shoe.cards[0]

    # evaluate hands later
    for player in tableList:
        print(f"\n{player.info['Name']}")
        if len(player.hands) < 1:
            pass
        else:
            for allHands in player.hands:
                print(allHands.cSum, allHands.cInfo)



if __name__ == "__main__":
    shoe, dealer = (Shoe(6), Dealer())
    player = Player(1000, 1)
    player.addBet(50)

    # deal out cards based on seats at table
    tableList = [player, dealer]
    playerList = [player]

    playerCont = True

    while playerCont == True:
        print(len(shoe.cards), shoe.cut)
        contOpts = list(contDict.keys())
        playerCont = contDict[decision(contOpts, "Cont")]
        del shoe.cards[0:15]
        if len(shoe.cards) <= shoe.cut:
            print("Cut Card Revealed, reshuffling shoe!\n")
            shoe = Shoe(6)
        else:
            pass



    # for player in 2 * tableList:
    #     player.dealtHand += [shoe.cards[0]]
    #     del shoe.cards[0]

    # # Evaluate the hands of player(s) and dealer
    # for player in tableList:
    #     player.hands.append(hand(player.dealtHand, player.info))

    # # Players make there decisions
    # dealerInfo = [dealer.hands[0].cInfo[0], ('?', '?')]
    # for currPlayer in playerList:
    #     currHand = 1
    #     currPlayer.dealerHand = dealerInfo
    #     while currHand <= len(currPlayer.hands):
    #         for thisHand in currPlayer.hands:
    #             playDecision(currPlayer, thisHand, currHand, shoe)
    #         currHand = currHand + 1

    # # Check player's Hand before going to dealer

    # # Dealer's turn
    # while dealer.hands[0].cSum < 17:
    #     dealer.hands[0].addCard(shoe.cards[0], dealer.info)
    #     del shoe.cards[0]

    # for player in tableList:
    #     print(f"\n{player.info['Name']}")
    #     if len(player.hands) < 1:
    #         pass
    #     else:
    #         for allHands in player.hands:
    #             print(allHands.cSum, allHands.cInfo)