

from copy import deepcopy as dp
from player import Player

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

decision_1 = input("PRESS 1 TO ENTER THE GAME \nPRESS Q TO QUIT THE GAME: \n")
while decision_1 == "1":
    n = int(input("ENTER THE NUMBER OF PLAYERS PLAYING: "))
    count = 0
    player_names = []
    bet = []
    for i in range(1, n+1):
        name = input(f"ENTER PLAYER {i}'s name: ")
        player_names.append(name)
        amount = input(f"ENTER THE STARTING BET AMOUNT FOR {player_names[i-1]}: ")
        bet.append(amount)
    while len(bet) != 0:
        player_0 = Player(dealer)
        

        

    player_decisions = ["hit", "stand", "double_down", "split", "insurance", "surrender"]
    points = 0
    decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.INSURANCE\n 6.SURRENDER\n")
