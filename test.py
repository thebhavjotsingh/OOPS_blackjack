from card import Card
from deck import Deck

deck = Deck(1)

cards = []

for i in range(8):
    cards.append(deck.retrieve_card())

print(cards[0])