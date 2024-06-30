from card import Card
import random

SUITS = ["spades", "hearts", "clubs", "diamonds"]
RANKS = ["A","K","Q","J",2,3,4,5,6,7,8,9,10]

class Deck:
    def __init__(self, num_of_decks:int) -> None:
        """
        Initializes an instance of the deck class.
        """
        self.num_of_decks = num_of_decks
        self.deck = self.generate_deck()
        self.num_of_cards = 52*num_of_decks
        
    def generate_deck(self):
        """
        Generates a deck of cards.
        """
        deck = {}
        for suit in SUITS:
            temp = []
            deck_id = 1
            while deck_id != self.num_of_decks + 1:
                for rank in RANKS:
                    temp.append(Card(suit,rank,deck_id))
                deck_id += 1
            deck[suit] = temp
        return deck
    
    def retrieve_card(self):
        """
        Retrieves a random card.
        """
        suit = random.choice(SUITS)
        the_card = random.choice(self.deck[suit])
        self.deck[suit].remove(the_card)
        self.num_of_cards -= 1
        return the_card
    
    def get_number_of_cards(self):
        """
        Returns the number of remaining cards in the deck.
        """
        return self.num_of_cards

    def get_card(self, suit, rank):
        """
        Retrieves a card matching the description. (Does not mofify the deck.)
        """
        the_suit = self.deck[suit]
        for card in the_suit:
            if card.get_rank() == rank:
                return card
        return ""
    
    def count_card(self,card:Card):
        '''
        Counts and returns the number of cards which have same rank and suit.
        '''
        suit = card.get_suit()
        rank = card.get_rank()
        count = 0
        for item in self.deck[suit]:
            if item.get_rank() == rank:
                count += 1
        return count

    def __str__(self) -> str:
        """
        String representation of the deck.
        """
        heading = """
-----------------------------------------------------------------
|   ♠️ Spades   |   ♥️ Hearts   |   ♣️ Clubs    |  ♦️ Diamonds  |
-----------------------------------------------------------------
"""
        number = f"Number of Cards in deck: {self.num_of_cards}"
        end = f"{'-'*65}\n{number:^65}\n{'-'*65}"
        columns = ""; num = ""
        
        for rank in RANKS:
            for suit in SUITS:
                if self.num_of_decks != 1:
                    num = f"{self.count_card(self.get_card(suit,rank))}x "
                card = str(self.get_card(suit,rank))
                columns += f"|{num+card:^15}"
            columns += "|\n"        
        return heading + columns + end
    
# deck = Deck(6)
# card = deck.retrieve_card()
# print(deck)
# print(card)