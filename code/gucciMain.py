from dealerClass import Dealer
from playerClass import Player
from deckClass import deck
from cardClass import card
from handClass import Hand


def inputArgs(argType: str, currPlayer: object, **kwargs) -> None:
    if argType == "Continue":
        contGame = str(input("Continue? [Y/n]\n>>> ")).lower()
        if "n" in contGame:
            currPlayer.done = True
    elif argType == "Options":
        options = [i.lower() for i in kwargs["hand"].optList]
        print(kwargs["hand"].optList)
        optionStr = "Please make a choice as shown above \n>>> "
        playerInput = str(input(optionStr)).lower()
        while playerInput not in options:
            print(kwargs["hand"].optList)
            playerInput = str(input("Try again\n>>> ")).lower()
        return playerInput
    elif argType == "Insurance":
        insurMsg = "Do you want to take Insurance?\n>>> "
        takeInsur = str(input(insurMsg)).lower()
        if "y" in takeInsur:
            currPlayer.insurance = True
    elif argType == "Bet":
        betMsg = (f"Player {currPlayer.seat}'s current bankroll: "
                  f"{currPlayer.bankroll}\nPlace your bet\n>>> ")
        betInput = int(input(betMsg))
        while betInput > currPlayer.bankroll:
            newBetMsg = (f"{betInput} is more than you have. Please "
                         "enter an amount lower than "
                         f"{currPlayer.bankroll} for your bet\n>>> ")
            betInput = int(input(newBetMsg))
        player.addBet(betInput)


def regPlay(currPlayer: object, hand: object) -> None:
    hand.decision = inputArgs("Options", currPlayer, hand=hand)
    if hand.decision == "hit":
        hand.checkHand([shoe.draw()], currPlayer)
        return hand
    elif hand.decision == "stand":
        hand.stand = True
        return hand
    elif hand.decision == "double":
        hand.checkHand([shoe.draw()], currPlayer)
        hand.bet = hand.bet * 2
        hand.stand = True
        return hand
    elif hand.decision == "split":
        for crd in hand.cards:
            splitHand = Hand([crd, card(('♦', 10))], currPlayer)
            currPlayer.hands.insert(hand.index, splitHand)
        currIndex = currPlayer.idxNum - 1
        currPlayer.hands.pop(currIndex)
        return currPlayer.hands[currIndex]


def playerHand(currPlayer: object, hand: object) -> None:
    while hand.stand != True:
        pNatural = hand.naturals
        dNatural = dealer.hands[0].naturals
        dHand = dealer.hands[0]
        print(f"\nDealer's Hand\n {hand.dlrInfo}\n"
              f"\nPlayer {currPlayer.seat} Hand "
              f"[{currPlayer.idxNum} of {len(currPlayer.hands)}]:"
              f"\n {hand.info}\n value: {hand.sum}\n")
        if pNatural == True and dNatural == True:
            print("Draw")
            hand.stand = True
        elif pNatural == True:
            print("Player wins")
            hand.win = True
            hand.stand = True
        elif dNatural == True:
            print("Dealer wins natural", dealer.hands[0].sum)
            hand.win = True
            hand.stand = True
        else:
            print("Normal Play")
            hand.optList = [o for o in hand.options
                            if hand.options[o]==True]
            hand = regPlay(currPlayer, hand)

    print(f"\nPlayer {currPlayer.seat} Hand "
          f"[{currPlayer.idxNum} of {len(currPlayer.hands)}]:"
          f"\n {hand.info}\n value: {hand.sum}\n")


def playerTurn(currPlayer: object, dlrInfo: list[tuple, tuple]) -> None:
        for idx, hand in enumerate(currPlayer.hands):
            currPlayer.idxNum = idx + 1
            hand.dlrInfo = dlrInfo
            playerHand(currPlayer, hand)  # run it


def dealerTurn(dealer: object) -> None:
    while dealer.hands[0].sum < 17:
        dealer.hands[0].checkHand([shoe.draw()], dealer)
    print(f"\n{'='*50}\nDealer's Hand:\n {dealer.hands[0].info}\n "
          f"value = {dealer.hands[0].sum}")


def compareSetup(playerList, dealer) -> None:
    # Evaluate Round
    dNat = dealer.hands[0].naturals
    for currPlayer in playerList:
        for hand in currPlayer.hands:
            compareHands(currPlayer, hand, dealer.hands[0])
            if currPlayer.insurance == True and dNat == True:
                currPlayer.bankroll += currPlayer.bet


def compareHands(plr: object, pHand: object, dHand: object) -> None:
    # # compare to dealer here
    if pHand.naturals == True or dHand.naturals == True:
        pHand.bet = 0
    elif pHand.bust == True:
        pHand.win = False
    elif dHand.bust == True:
        pHand.win = True
    elif pHand.sum > dHand.sum:
        pHand.win = True
    elif pHand.sum < dHand.sum:
        pHand.win = False
    elif pHand.sum == dHand.sum:
        pHand.push = True
    pHand.payOut(plr)


def playRound(tableList: list, playerList: list) -> None:
    # testHand = [card(('♣', 'A')), card(('♣', 'A'))]

    for plr in playerList:
        # inputArgs("Bet", player)  # player adds bet
        plr.addBet(50)

    for pos in 2 * tableList:
        pos.dealt.append(shoe.draw())  # deal cards

    for pos in tableList:
        pos.hands.append(Hand(pos.dealt, pos))  # evaluate hands

    # dealer.hands[0] = Hand(testHand, dealer)
    # player.hands[0] = Hand(testHand, player)

    dlrInfo = [dealer.hands[0].info[0], ("?", "?")]
    print(f"\n{'='*50}\nDealer's Hand:\n {dlrInfo}\n")
    for currPlayer in playerList:
        for idx, hand in enumerate(currPlayer.hands):
            hand.index = idx + 1
            print(f"\nPlayer {currPlayer.seat} Hand "
                  f"[{hand.index} of {len(currPlayer.hands)}]:"
                  f"\n {hand.info}\n value: {hand.sum}\n{'='*50}\n")

    # Insurance for dealer face-up aces
    dNat = dealer.hands[0].naturals
    if "A" in dealer.hands[0].cards[0].info:
        for currPlayer in playerList:
            inputArgs("Insurance", currPlayer)

    if dNat == False:
        # Player(s) decisions
        for currPlayer in playerList:
            playerTurn(currPlayer, dlrInfo)
        # Dealer's Turn
        dealerTurn(dealer)
        compareSetup(playerList, dealer)
    elif dNat == True:
        compareSetup(playerList, dealer)

    # Prepare for next Round
    for currPlayer in tableList:
        currPlayer.reset()
        if currPlayer.seat != 0:
            print(f"Player {currPlayer.seat}'s bankroll:",
                  currPlayer.bankroll)


if __name__ == "__main__":
    dealer = Dealer()
    player = Player(1000, 1)
    shoe = deck(6)
    tableList = [player, dealer]

    while player.done == False:
        playRound(tableList, tableList.copy()[:-1])
        inputArgs("Continue", player)
        # Reshuffle deck
        if len(shoe.cards) < shoe.cut:
            # could move this into the dealing portion of the game
            print("Cut card found, reshuffling")
            shoe = deck(6)
