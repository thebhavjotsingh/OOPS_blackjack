from copy import deepcopy as dp
from player import Player
from deck import Deck
split = False
dealer = Player(0, "dealer")
DECK = Deck(6)

logo = r"""
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

def player_creation(n:int, list_of_players:list):
    for i in range(1, n+1):
        name = input(f"ENTER PLAYER {i}'s name: ")
        name = name.upper()
        amount = int(input(f"ENTER THE STARTING BET AMOUNT FOR {name}: "))
        if amount < 20:
            print("BET AMOUNT CANNOT BE LESS THAN 20.")
            name = name.upper()
            amount = int(input(f"ENTER THE STARTING BET AMOUNT FOR {name}: "))
        pl = Player(i,name,amount)
        list_of_players.append(pl)

def card_distribute(players):   
    for i in range (len(players)):
        for j in range(2):
            card = DECK.retrieve_card()
            players[i].add_card(card)

def round(player, dealer):
    if player.points > dealer.points:
        print("PLAYER WINS")

def main():
    count = 0
    decision_1 = input("PRESS G TO ENTER THE GAME \nPRESS Q TO QUIT THE GAME: \n")
    if decision_1.upper() != "G" and decision_1.upper() != "Q":
        print("INCORRECT INPUT")
        main()
    elif decision_1.upper() == "Q":
        print("THANK YOU PLAYING THE GAME! COME AGAIN.")
    elif decision_1.upper() == "G":
        while decision_1.upper() == "G":
            count += 1
            n = int(input("ENTER THE NUMBER OF PLAYERS PLAYING: "))
            players = []
            player_creation(n, players)
            card = DECK.retrieve_card()
            dealer.add_card(card)
            print(f"ROUND {count}")
            print("FOR DEALER")
            print(dealer)
            card_distribute(players)
            while len(players) != 0:
                for i in range(1, n+1):
                    print(f"PLAYER {i} PLAYING")
                    print(players[i-1])
                    decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.SURRENDER\n")
                    if decision.upper() == "HIT" or decision == "1":
                        card = DECK.retrieve_card()
                        players[i-1].add_card(card)
                        print(players[i-1])
                    elif decision.upper() == "STAND" or decision == "2":
                        pass
                    elif decision.upper() == "DOUBLE DOWN" or decision == "3":
                        if count > 2 or split == False:
                            print("DOUBLE DOWN IS NOT AVAILABLE AFTER TWO TURNS")
                            pass
                        players[i-1].bet *= 2
                    elif decision.upper() == "SURRENDER" or decision == "5":
                        players[i-1].bet /= 2
                        pass
    
main()



            