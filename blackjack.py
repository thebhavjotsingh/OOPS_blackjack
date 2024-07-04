from copy import deepcopy as dp
from player import Player
from deck import Deck
split = False
dealer = Player(0, "dealer")
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
            amount = int(input(f"ENTER THE STARTING BET AMOUNT FOR {name}: "))
            if amount < 20:
                  print("BET AMOUNT CANNOT BE LESS THAN 20.")
                  name = name.upper()
                  amount = int(input(f"ENTER THE STARTING BET AMOUNT FOR {name}: "))
            pl = Player(i,name,amount)
            list_of_players.append(pl)

def card_distribute(players:list):   
      for i in range (len(players)):
            for j in range(2):
                  card = DECK.retrieve_card()
                  players[i].add_card(card)

def round_winner(player, dealer):
      if player.points > dealer.points:
            print("PLAYER WINS")
      elif player.points == dealer.points:
            print("ROUND WAS A TIE.")
      else:
            print("DEALER WINS")

def round_end_menu(players:list):
      count_ = 0
      decision_2 = input("CHOOSE FROM THE FOLLOWING OPTIONS:\n 1.CONTINUE TO NEXT ROUND\n 2. LEAVE GAME\n 3.ENTER NEW PEOPLE ")
      if decision_2 == "1":
            main()
      elif decision_2 == "2":
            d = input("ENTER THE ID OF PLAYERS LEAVING THE GAME SEPARATED BY COMMAS: ")
            list_d = d.split(",")
            for i in range (len(list_d)):
                  players.pop(list_d[i])
                  count_ += 1
            number_of_players -= count_
            return players
      elif decision_2 == "3":
            d = input("ENTER THE NUMBER OF PLAYERS WANTING TO JOIN: ")
            number_of_players += d
            player_creation(number_of_players, players)
            return players

def game_loop(players:list):
      global count 
      global number_of_players
      count += 1
      card = DECK.retrieve_card()
      dealer.add_card(card)
      print(f"ROUND {count}")
      print("FOR DEALER")
      print(dealer)
      card_distribute(players)
      print(number_of_players)
      while (len(players) != 0):
            for i in range(1, number_of_players+1):
                  print(f"PLAYER {i} PLAYING")
                  print(players[i-1])
                  decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.SURRENDER\n")
                  if decision.upper() in ["HIT","1"]:
                        card = DECK.retrieve_card()
                        players[i-1].add_card(card)
                        print(players[i-1])
                  elif decision.upper() in ["STAND", "2"]:
                        pass
                  elif decision.upper() in ["DOUBLE DOWN", "3"]:
                        if count > 2 or split == False:
                              print("DOUBLE DOWN IS NOT AVAILABLE AFTER TWO TURNS")
                              pass
                        players[i-1].bet *= 2
                  elif decision.upper() in ["SPLIT", "4"]:
                        pass
                  elif decision.upper() in ["SURRENDER", "5"]:
                        players[i-1].bet /= 2
                        pass
                  else:
                        print("INCORRECT INPUT")
                        decision = input("Select one of the following choices:\n 1.HIT\n 2.STAND\n 3.DOUBLE DOWN\n 4.SPLIT\n 5.SURRENDER\n")
                  
                        

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



            