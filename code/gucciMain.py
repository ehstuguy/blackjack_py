#!/home/geyer/anaconda3/bin/python3.11

from dealerClass import Dealer
from playerClass import Player
from deckClass import deck
from cardClass import card
from handClass import Hand

def checkBetInput(betInput: int) -> int:
    try:
        betInput = int(betInput)
        return betInput
    except ValueError:
        print("\nPlease enter a valid number")
        return checkBetInput(input(">>> "))


def inputArgs(argType: str, currPlayer: object, **kwargs) -> None:
    if argType == "Continue":
        contGame = str(input("\nContinue? [Y/n]\n>>> ")).lower()
        if "n" in contGame:
            currPlayer.done = True
        else:
            pass
    elif argType == "Options":
        options = [i.lower() for i in kwargs["hand"].optList]
        print(f"\n{kwargs['hand'].optList}")
        optionStr = "Please make a choice as shown above \n>>> "
        playerInput = str(input(optionStr)).lower()
        while playerInput not in options:
            print(f"\n{kwargs['hand'].optList}")
            playerInput = str(input("Try again\n>>> ")).lower()
        return playerInput
    elif argType == "Insurance":
        insurMsg = "\nDo you want to take Insurance?\n>>> "
        takeInsur = str(input(insurMsg)).lower()
        if "y" in takeInsur:
            currPlayer.insurance = True
    elif argType == "Bet":
        betMsg = (f"\n\nPlayer {currPlayer.seat}'s "
                  f"current bankroll: {currPlayer.bankroll}"
                  "\nPlace your bet\n>>> ")
        betInput = checkBetInput(input(betMsg))
        while betInput > currPlayer.bankroll:
            print("\nYour current bankroll is", currPlayer.bankroll)
            betInput = checkBetInput(input("Try again\n>>> "))
        currPlayer.addBet(betInput)
    elif argType == "Add Funds":
        addFunds = str(input("\nAdd funds? [Y/n]\n>>> ")).lower()
        if "y" in addFunds:
            addMsg = "How much would you like to add?\n>>> "
            addInput = checkBetInput(input(addMsg))
            currPlayer.bankroll += addInput
            print(f"New bankroll: {currPlayer.bankroll}")
    else:
        pass


def specCards() -> list:
    return [card(('♣', "A")), card(('♣', 10))]  # test hand


def regPlay(currPlayer: object, hand: object, **kwargs) -> None:
    dealer = kwargs["dealer"]
    shoe = kwargs["shoe"]
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
        ogHandIdx = hand.index
        for i, crd in enumerate(hand.cards):
            # splitHand = Hand([crd, card(('♦', 10))], currPlayer)
            splitHand = Hand([crd, shoe.draw()], currPlayer)
            splitHand.index = ogHandIdx + i
            currPlayer.hands.insert(splitHand.index, splitHand)
        currIndex = currPlayer.idxNum - 1
        currPlayer.hands.pop(currIndex)
        return currPlayer.hands[currIndex]
    else:
        pass


def playerHand(currPlayer: object, hand: object, **kwargs) -> None:
    dealer = kwargs["dealer"]

    while hand.stand != True:
        pNatural = hand.naturals
        dNatural = dealer.hands[0].naturals
        print(f"\nDealer's Hand\n {currPlayer.dlrInfo}\n"
              f"\nPlayer {currPlayer.seat} Hand "
              f"[{currPlayer.idxNum} of {len(currPlayer.hands)}]:"
              f"\n {hand.info}\n value: {hand.sum}\n")
        if pNatural == True and dNatural == True:
            print("Draw")
            hand.stand = True
        elif pNatural == True:
            print("\nPlayer wins with naturals", hand.sum)
            hand.win = True
            hand.stand = True
            hand.payOut(currPlayer, hand.bet)
        elif dNatural == True:
            print("\nDealer wins with naturals", dealer.hands[0].sum)
            hand.win = True
            hand.stand = True
        else:
            print("\nNormal Play")
            hand.optList = [o for o in hand.options
                            if hand.options[o]==True]
            hand = regPlay(currPlayer, hand, **kwargs)

    # print(f"\nPlayer {currPlayer.seat} Hand "
    #       f"[{currPlayer.idxNum} of {len(currPlayer.hands)}]:"
    #       f"\n {hand.info}\n value: {hand.sum}\n")


def playerTurn(currPlayer: object, dlrInfo: list, **kwargs) -> None:
        for idx, hand in enumerate(currPlayer.hands):
            currPlayer.idxNum = idx + 1
            currPlayer.dlrInfo = dlrInfo
            playerHand(currPlayer, hand, **kwargs)  # run it


def dealerTurn(dealer: object, **kwargs) -> None:
    shoe = kwargs["shoe"]
    while dealer.hands[0].sum < 17:
        dealer.hands[0].checkHand([shoe.draw()], dealer)
    print(f"\n{'='*50}"
          f"\nDealer's Hand:\n {dealer.hands[0].info}"
          f"\n value = {dealer.hands[0].sum}")


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
    else:
        pass
    pHand.payOut(plr, pHand.bet)


def compareSetup(playerList: list, dealer: object, **kwargs) -> None:
    # Evaluate Round
    dNat = dealer.hands[0].naturals
    for currPlayer in playerList:
        for hand in currPlayer.hands:
            compareHands(currPlayer, hand, dealer.hands[0])
            if currPlayer.insurance == True and dNat == True:
                currPlayer.bankroll += currPlayer.bet
                print(f"\n|Player {currPlayer.seat}| Hand:"
                      f"\n {hand.info}"
                      f"\n value = {hand.sum}"
                      f"\n win: {hand.win}, push: {hand.push}"
                      f"\n bankroll: {currPlayer.bankroll}")
            else:
                pass




def playRound(tableList: list, playerList: list, **kwargs) -> None:
    dealer = kwargs["dealer"]
    shoe = kwargs["shoe"]

    for player in playerList:
        inputArgs("Bet", player)  # player adds bet
        # player.addBet(50)

    for pos in 2 * tableList:
        pos.dealt.append(shoe.draw())  # deal cards

    for pos in tableList:
        pos.hands.append(Hand(pos.dealt, pos))  # evaluate hands

    # # test for bugs ===================================================
    # testHand = specCards()
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
    else:
        pass

    if dNat == False:
        # Player(s) decisions
        for currPlayer in playerList:
            playerTurn(currPlayer, dlrInfo, **kwargs)


        bustList = [hand.bust for hand in currPlayer.hands
                    for currPlayer in playerList]
        natList = [hand.naturals for hand in currPlayer.hands
                   for currPlayer in playerList]
        # Dealer's Turn

        if False in bustList and False in natList:
            dealerTurn(dealer, shoe=shoe)
        compareSetup(playerList, dealer)
    elif dNat == True:
        compareSetup(playerList, dealer)
    else:
        pass

    # Prepare for next Round
    print(f"\n{'='*50}\nRound Over:\n")
    for currPlayer in tableList:
        currPlayer.reset()
        if currPlayer.seat != 0:
            print(f"Player {currPlayer.seat}'s bankroll:",
                  currPlayer.bankroll)
        else:
            pass


def main() -> None:
    dealer = Dealer()
    player = Player(1000, 1)
    shoe = deck(6)
    tableList = [player, dealer]
    playerList = [player]

    while player.done == False:
        playRound(tableList, playerList, shoe=shoe, dealer=dealer)
        inputArgs("Continue", player)
        # Reshuffle deck
        if len(shoe.cards) < shoe.cut:
            # could move this into the dealing portion of the game
            print("Cut card found, reshuffling")
            shoe = deck(6)
        elif player.bankroll == 0:
            print("You're out of money, an ATM is down the hall.")
            inputArgs("Add Funds", player)
            if player.bankroll == 0:
                player.done = True
            else:
                pass
        else:
            pass


if __name__ == "__main__":
    main()