from copy import deepcopy as dp
from player import Player
from deck import Deck
split = False
dealer = Player(0, 'dealer')
DECK = Deck(6)
number_of_players = 0
count = 0


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

def player_creation(number_of_players:int, list_of_players:list):
      for i in range(len(list_of_players) + 1, number_of_players + 1):
            name = input(f"ENTER PLAYER {i}'s name: ")
            name = name.upper()
            amount = int(input(f"ENTER THE FUNDS YOU HAVE FOR THIS GAME\n {name}: "))
            pl = Player(i,name,amount)
            list_of_players.append(pl)

def set_bet(players: list):
    for i in range(len(players)):
        bet_amount = int(input(f"ENTER THE BET AMOUNT FOR {players[i].name}: "))
        while bet_amount < 20:
            print("BET AMOUNT CANNOT BE LESS THAN 20.")
            bet_amount = int(input(f"ENTER THE BET AMOUNT FOR {players[i].name}: "))
        players[i].change_bet("add", bet_amount)


def card_distribute(players:list):   
      for i in range (len(players)):
            for j in range(2):
                  card = DECK.retrieve_card()
                  players[i].add_card(card)

def card_snatch(players:list, dealer):
      for i in range (len(players)):
            players[i].reset_hand(DECK)

      dealer.reset_hand(DECK)

def round_winner(players:list, dealer):
      print("DEALER HITS UNTILL REACHES HIS POINTS REACH 17.")
      while dealer.points < 17:
            card = DECK.retrieve_card()
            dealer.add_card(card)
            print(dealer)

      if dealer.check_blackjack()  == True:
            print("DEALER WINS. IT'S A BLACKJACK.")
            player.change_bet("clear")

      for player in players:
            if player.check_blackjack() == True:
                  print(f"{player.name} WINS. IT'S A BLACKJACK.")
                  player.change_bet("winb")
            elif player.points > 21:
                  print(f"{player.name} LOST. POINTS REACHED 21")
                  player.change_bet("clear")
            elif dealer.points > 21:
                  print(f"DEALER LOST")
                  player.change_bet("win")
            elif player.points > dealer.points:
                  print(f"{player.name} WINS")
                  player.change_bet("win")
            elif player.points == dealer.points:
                  print("ROUND WAS A TIE.")
            else:
                  print("DEALER WINS")
                  player.change_bet("clear")

def round_end_menu(players:list, dealer):
      global number_of_players
      count_ = 0
      decision_2 = input("CHOOSE FROM THE FOLLOWING OPTIONS:\n 1. CONTINUE TO NEXT ROUND\n 2. LEAVE GAME\n 3. ENTER NEW PEOPLE\n ")
      if decision_2 == "1":
            card_snatch(players, dealer)
            game_loop(players)
      elif decision_2 == "2":
            d = input("ENTER THE ID OF PLAYERS LEAVING THE GAME SEPARATED BY COMMAS: ")
            list_d = d.split(",")
            for player_id in list_d:
                  player_id = int(player_id.strip())
                  player_id -= 1
                  if 0 <= player_id < len(players):
                        players.pop(player_id)
                        count_ += 1
            number_of_players -= count_
            card_snatch(players, dealer)
            game_loop(players)
      elif decision_2 == "3":
            d = input("ENTER THE NUMBER OF PLAYERS WANTING TO JOIN: ")
            new_players = int(d.strip())  # Convert to integer
            number_of_players += new_players
            player_creation(number_of_players, players)
            card_snatch(players, dealer)
            game_loop(players)

def game_loop(players:list):
      global count 
      global number_of_players
      count += 1
      set_bet(players)
      card = DECK.retrieve_card()
      dealer.add_card(card)
      print(f"ROUND {count}")
      print("FOR DEALER")
      print(dealer)
      card_distribute(players)
      while (len(players) != 0):
            for i in range(1, number_of_players+1):
                  while True:
                        if players[i-1].points > 21:
                              print(players[i-1])
                              print("BUSTED. YOU EXCEEDED 21. YOU LOSE.")
                              break
                        if players[i-1].check_blackjack() == True:
                              print(f"{players[i-1].name} HAS A BLACKJACK. CONTINUING TO NEXT PLAYER.")
                              break
                        print(f"PLAYER {i} PLAYING")
                        print(players[i-1])
                        decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.SURRENDER\n")
                        if decision.upper() in ["HIT","1"]:
                              card = DECK.retrieve_card()
                              players[i-1].add_card(card)
                        elif decision.upper() in ["STAND", "2"]:
                              break
                        elif decision.upper() in ["DOUBLE DOWN", "3"]:
                              players[i-1].change_bet("dd")
                              print(f"BET AMOUNT FOR {players[i-1].name} IS INCREASED TO {players[i-1].bet}")
                        elif decision.upper() in ["SPLIT", "4"]:
                              pass
                        elif decision.upper() in ["SURRENDER", "5"]:
                              players[i-1].bet /= 2
                              print(f"AMOUNT LEFT WITH {players[i-1].name} IS {players[i-1].bet}")
                              break
                        else:
                              print("INCORRECT INPUT")
                              decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.SURRENDER\n")
            round_winner(players, dealer)
            round_end_menu(players, dealer)
                        

def main():
      global number_of_players
      decision_1 = input("PRESS G TO ENTER THE GAME \nPRESS Q TO QUIT THE GAME: \n")
      if decision_1.upper() != "G" and decision_1.upper() != "Q":
             print("INCORRECT INPUT")
             main()
      elif decision_1.upper() == "Q":
            print("THANK YOU PLAYING THE GAME! COME AGAIN.")
      elif decision_1.upper() == "G":
            while decision_1.upper() == "G":
                  number_of_players = int(input("ENTER THE NUMBER OF PLAYERS PLAYING: "))
                  players = []
                  player_creation(number_of_players, players)
                  game_loop(players)
     
main()



            