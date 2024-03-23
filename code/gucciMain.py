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
        betMsg = (
            f"Player {currPlayer.seat}'s current bankroll: "
            f"{currPlayer.bankroll}\nPlease enter your bet\n>>> ")
        betInput = int(input(betMsg))
        while betInput > currPlayer.bankroll:
            newBetMsg = (
                f"{betInput} is more than you have. Please enter "
                f"an amount lower than {currPlayer.bankroll} "
                "for your bet\n>>> ")
            betInput = int(input(newBetMsg))
        player.addBet(betInput)


def regPlay(currPlayer: object, hand: object) -> None:
    hand.decision = inputArgs("Options", currPlayer, hand=hand)
    if hand.decision == "hit":
        hand.checkHand([shoe.draw()], currPlayer)
    elif hand.decision == "stand":
        hand.stand = True
    elif hand.decision == "double":
        hand.checkHand([shoe.draw()], currPlayer)
        hand.bet = hand.bet * 2
        hand.stand = True
    elif hand.decision == "split":
        pass


def playerHand(currPlayer: object, hand: object) -> None:
    pNatural = hand.naturals
    dNatural = dealer.hands[0].naturals
    while hand.stand != True:
        print(
            f"\nPlayer {currPlayer.seat} Hand "
            f"[{hand.index} of {len(currPlayer.hands)}]:"
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
            hand.optList = [o for o in hand.options if hand.options[o]==True]
            regPlay(currPlayer, hand)

    print(
        f"\nPlayer {currPlayer.seat} Hand "
        f"[{hand.index} of {len(currPlayer.hands)}]:"
        f"\n {hand.info}\n value: {hand.sum}\n")


def playerTurn(currPlayer: object, dlrInfo: list[tuple, tuple]) -> None:
        for idx, hand in enumerate(currPlayer.hands):
            hand.index = idx + 1
            hand.dlrInfo = dlrInfo
            playerHand(currPlayer, hand)  # run it


def compareHands() -> None:
    # # compare to dealer here
    # if pNatural == True or dNatural == True:
    #     pass
    # elif hand.bust == True:
    #     hand.win = False
    # elif hand.sum > dealer.hands[0].sum:
    #     hand.win = True
    # elif hand.sum < dealer.hands[0].sum:
    #     hand.win = False
    pass


def playRound(tableList: list, playerList: list) -> None:
    testHand = [card(('♣', 'A')), card(('♣', 'A'))]

    # inputArgs("Bet", player)  # player adds bet
    for pos in 2 * tableList:
        pos.dealt.append(shoe.draw())  # deal cards

    for pos in tableList:
        pos.hands.append(Hand(pos.dealt, pos))  # evaluate hands

    dealer.hands[0] = Hand(testHand, dealer)
    dlrInfo = [dealer.hands[0].info[0], ("?", "?")]
    print(f"\n{'='*50}\nDealer's Hand:\n {dlrInfo}\n")
    for currPlayer in playerList:
        for idx, hand in enumerate(currPlayer.hands):
            hand.index = idx + 1
            print(f"\nPlayer {currPlayer.seat} Hand "
                  f"[{hand.index} of {len(currPlayer.hands)}]:"
                  f"\n {hand.info}\n value: {hand.sum}\n{'='*50}\n")

    if "A" in dealer.hands[0].cards[0].info:
        inputArgs("Insurance", player)
    # =================================================================
    # show cards and if dealer ace, give players option for insurance
    # =================================================================

    # Player(s) decisions
    for currPlayer in playerList:
            playerTurn(currPlayer, dlrInfo)

    # Dealer's Turn
    while dealer.hands[0].sum < 17:
        dealer.hands[0].checkHand([shoe.draw()], dealer)
    dNat = dealer.hands[0].naturals

    # Evaluate Round
    for currPlayer in playerList:
        for hand in currPlayer.hands:
            compareHands(hand, dealer.hands[0])
            # Players who
            if currPlayer.insurance == True and dNat == True:
                currPlayer.bankroll += currPlayer.bet

    # Prepare for next Round
    for currPlayer in tableList:
        currPlayer.reset()

    print(player)
    print(dealer)
    check = 0


if __name__ == "__main__":
    dealer = Dealer()
    player = Player(1000, 1)

    player.addBet(50)
    shoe = deck(6)
    tableList = [player, dealer]

    while player.done == False:
        playRound(tableList, tableList.copy()[:-1])
        inputArgs("Continue", player)
        # Reshuffle deck
        if len(shoe) < shoe.cut:
            # could move this into the dealing portion of the game
            print("Cut card found, reshuffling")
            shoe = deck(6)
