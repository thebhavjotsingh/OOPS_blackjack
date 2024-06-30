'''
# Card Class
# Written by: Bhavjot Singh
'''
class Card:
    '''
    An object of this class represents a playing card.
    Available functions:
        - get_suit()
        - get_suit_symbol()
        - get_rank()
        - get_value()
        - get_deck_id()
    '''
    def __init__(self, suit:str, rank, deck_id: int) -> None:
        """
        Initializes a card which belongs to a distinct suit and has a distint rank.
        """
        suit = suit.lower()
        suits_name = ["hearts", "clubs", "diamonds", "spades"]
        suits_sym = ["♥️", "♣️", "♦️", "♠️"]
        
        
        if suit not in ["hearts", "clubs", "diamonds", "spades"]:
            raise Exception("Not a valid Suit.")
        if rank not in ["A",2,3,4,5,6,7,8,9,10,"K","J","Q"]:
            raise Exception("Not a valid rank.")
        # if id not in range(1,53):
        #     raise Exception("Not a Valid id.")
        
        if rank in range(2,11):
            self.value = rank
        elif rank in ["K", "J", "Q"]:
            self.value = 10
        elif rank == "A":
            self.value = 11
        else:
            self.value = 0
        
        self.deck_id = deck_id
        suit_sym = suits_sym[suits_name.index(suit)]
        self.suit = suit
        self.suit_sym = suit_sym
        self.rank = rank

    def get_suit(self):
        """
        Returns the suit of the card.
        """
        return self.suit
    
    def get_suit_symbol(self):
        """
        Returns the suit symbol of the card.
        """
        return self.suit_sym
    
    def get_rank(self):
        """
        Returns the rank of the card.
        """
        return self.rank

    def get_value(self):
        """
        Returns the value of the card.
        """
        return self.value
    
    def get_deck_id(self):
        """
        Returns the id of the card.
        """
        return self.deck_id

    def __str__(self) -> str:
        """
        String representation of the card.
        """
        return f"{self.suit_sym}{str(self.rank)}"