'''
# Player Class for blackjack game
# Written by: Bhavjot Singh
'''

from card import Card

class Player:
    '''
    An object of this class represents a player in a blackjack game.
    Available Functions:
        - add_card(card)
        - point_calc()
    '''
    def __init__(self, id:int, name:str, money:int = None) -> None:
        """
        Initializes an instance of a player.
        """
        self.id = id
        self.name = name
        self.cards = []
        self.card_points = []
        self.points = 0
        self.money = money
        self.bet = 0

    def add_card(self, card: Card):
        """
        Adds a card to the hand of player.
        """
        self.cards.append(card)
        self.card_points.append(card.get_value())
        self.points = self.point_calc()

    def point_calc(self):
        """
        Calculates the total points of the player.
        """
        if 11 not in self.card_points:
            return sum(self.card_points)
        else:
            add = sum(self.card_points)
            if add > 21:
                return add-10
            else:
                return add

    def change_bet(self, mode: str, amount:int = None):
        """
        
        """
        if mode.lower() == 'add' and amount != None:
            if self.money >= amount:
                self.money -= amount
                self.bet += amount
        elif mode.lower() == 'clear':
            self.bet = 0
        elif mode.lower() == 'cash':
            
        else:
            raise Exception(f"{mode} is not a valid option for changing bet.")

    def __str__(self) -> str:
        """
        String representation of the players.
        """
        if self.name == "Dealer" and self.turn == 0:
            rep = f"{self.name}\n[🛑, {str(self.cards[1])}]\nPoints: {self.points - self.cards[0].get_value()}"
        else:
            rep = f"{self.name}\n["
            for card in self.cards:
                rep += f"{str(card)}, "
            rep += f"]\nPoints: {self.points}"    
        
        return rep
