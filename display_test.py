from card import Card
from deck import Deck

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
                
                row_line += f"\033[31m{repr(row_cards[i]).split('\n')[line]}\033[00m"
                red_count += 10 # each colored card needs ten more spaces for proper indentation
            else: 
                row_line += repr(row_cards[i]).split('\n')[line]
            if i != 3:
                row_line += "  "
        row_line = f"{row_line:^{78+red_count}}"
        print(row_line)
