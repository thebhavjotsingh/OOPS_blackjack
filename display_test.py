from card import Card
from deck import Deck

deck = Deck(1)

cards = []

for i in range(8):
    cards.append(deck.retrieve_card())


no_rows = round(len(cards)/4 + 0.5)
for row in range(no_rows):
    row_cards = cards[0+row*4:4+row*4]
    for line in range(5):
        row_line = ''
        for i in range(len(row_cards)):
            row_line += str(row_cards[i]).split('\n')[line]
            if i != 3:
                row_line += "  "
        row_line = f"{26*' '}{row_line}"
        print(row_line)

                   



