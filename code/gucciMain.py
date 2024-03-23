from dealerClass import Dealer
from playerClass import Player
from cardClass import Shoe
from handClass import Hand



def playerTurn(hand: object, dlrInfo: list[tuple[str]]) -> None:
    pass


def playRound(tableList: list, playerList: list) -> None:
    for pos in 2 * tableList:
        pos.dealt.append(shoe.draw())  # deal cards

    for pos in tableList:
        pos.hands.append(Hand(pos.dealt, pos))  # evaluate hands

    dlrInfo = [dealer.hands[0].Info[0], ("?", "?")]
    for player in playerList:
        while player.done == False:
            for hand in player.hands:
                playerTurn(hand, dlrInfo)

            if input(">>> ") == 0:
                player.done = True




    print(player)
    print(dealer)
    check = 0



if __name__ == "__main__":
    dealer = Dealer()
    player = Player(1000, 1)
    player.addBet(50)
    shoe = Shoe(6)

    tableList = [player, dealer]
    playRound(tableList, tableList.copy()[:-1])

