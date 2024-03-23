from dealerClass import Dealer
from playerClass import Player
from deckClass import deck
from handClass import Hand

doneList = ["n", "nah", "no", "naw"]


def playerTurn(player: object, hand: object, dlrInfo: list) -> None:
    print(
        f"\n{'='*50}\nDealer's Hand:\n {dlrInfo}\n"
        f"\nPlayer {player.seat} Hand "
        f"[{hand.index} of {len(player.hands)}]:"
        f"\n {hand.info}\n value: {hand.sum}\n{'='*50}\n")
    exit()
    pass


def playRound(tableList: list, playerList: list) -> None:
    for pos in 2 * tableList:
        pos.dealt.append(shoe.draw())  # deal cards

    for pos in tableList:
        pos.hands.append(Hand(pos.dealt, pos))  # evaluate hands

    dlrInfo = [dealer.hands[0].info[0], ("?", "?")]
    for player in playerList:
        while player.done == False:
            for idx, hand in enumerate(player.hands):
                hand.index = idx + 1
                playerTurn(player, hand, dlrInfo)
            contGame = str(input("Continue? [Y/n]\n>>> ")).lower()
            if contGame in doneList:
                player.done = True

    print(player)
    print(dealer)
    check = 0


if __name__ == "__main__":
    dealer = Dealer()
    player = Player(1000, 1)
    player.addBet(50)
    shoe = deck(6)

    tableList = [player, dealer]
    playRound(tableList, tableList.copy()[:-1])