from card import Card
from deck import Deck

deck = Deck(6)

hands = []

for i in range(2):
    hand = []
    for j in range(4):
        hand.append(deck.retrieve_card())
    hands.append(hand)

hands[1].append(deck.retrieve_card())
print(hands)



lengths=[]
for i in range(len(hands)):
    length = len(hands[i])
    lengths.append(length)
maximum_cards = max(lengths)
no_rows1 = round(maximum_cards/4+0.4)

for i in range(no_rows1):
    for line in range(5):
        row_line = ''
        for hand in hands:
            for card_index in range(i*4, (i+1)*4):
                try:
                    if hand[card_index].get_suit() in ['hearts','diamonds']:
                        row_line += f"\033[31m{str(hand[card_index]).split('\n')[line]}\033[00m" + " "
                    else: 
                        row_line += str(hand[card_index]).split('\n')[line] + " "
                except:
                    row_line += 6*" "
            row_line += 4*" "
        print(row_line)
                