from card import Card
from deck import Deck

deck = Deck(6)

hands = []

for i in range(4):
    hand = []
    for j in range(8):
        hand.append(deck.retrieve_card())
    hands.append(hand)

print(hands)