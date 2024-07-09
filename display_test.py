from card import Card
from deck import Deck
from player import Player

deck = Deck(1)

cards = []

for i in range(16):
    cards.append(deck.retrieve_card())


no_rows = round(len(cards)/4 + 0.5)
for row in range(no_rows):
    row_cards = cards[0+row*4:4+row*4]
    for line in range(5):
        row_line = ''
        red_count = 0
        for i in range(len(row_cards)):
            if row_cards[i].get_suit() in ['hearts','diamonds']:
                
                row_line += f"\033[31m{str(row_cards[i]).split('\n')[line]}\033[00m"
                red_count += 10 # each colored card needs ten more spaces for proper indentation
            else: 
                row_line += str(row_cards[i]).split('\n')[line]
            if i != 3:
                row_line += "  "
        row_line = f"{row_line:^{78+red_count}}"
        print(row_line)

#Dealer
Dealer_cards=[]

for j in range(2):
    Dealer_cards.append(deck.retrieve_card())

Dealer_str='Dealer'
print(f"{Dealer_str:^{78}}")

for line_2 in range(5):
    Dealer_rep = ''
    red_count = 0
    for k in range(len(Dealer_cards)):
        
        if Dealer_cards[k].get_suit() in ['hearts','diamonds']:
                
                Dealer_rep += f"\033[31m{str(Dealer_cards[k]).split('\n')[line_2]}\033[00m"
                red_count += 10 # each colored card needs ten more spaces for proper indentation
        else: 
                Dealer_rep += str(Dealer_cards[k]).split('\n')[line_2]
        if k != 3:
            Dealer_rep += "  "
    Dealer_rep = f"{Dealer_rep:^{78+red_count}}"
    print(Dealer_rep)

print(f"{'POINTS:':^{78}}")
print('\n')


Player1_cards = []

for l in range(2):
    Player1_cards.append(deck.retrieve_card())

logo = r"""
       ______  _                             __ 
      (_____ \| |                           /  |
       _____) ) | ____ _   _  ____  ____   /_/ |
      |  ____/| |/ _  | | | |/ _  )/ ___)    | |
      | |     | ( ( | | |_| ( (/ /| |        | |
      |_|     |_|\_||_|\__  |\____)_|        |_|
                       (____/                    
"""

print(f"{logo:^{178}}")
for line_3 in range(5):
    Player_rep = ''
    red_count = 0
    for m in range(len(Player1_cards)):
        if Player1_cards[m].get_suit() in ['hearts','diamonds']:
                
                Player_rep += f"\033[31m{str(Player1_cards[m]).split('\n')[line_3]}\033[00m"
                red_count += 10 # each colored card needs ten more spaces for proper indentation
        else: 
                Player_rep += str(Player1_cards[m]).split('\n')[line_3]
        
        if m != 3:
            Player_rep += "  "
    Player_rep = f"{Player_rep:^{78+red_count}}"
    print(Player_rep)

print(f"{'POINTS:':^{78}}")
print('\n')
print("\033[31;1;4mHello\033[0m")