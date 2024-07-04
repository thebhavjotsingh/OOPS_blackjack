'''
# Player Class for blackjack game
# Written by: Bhavjot Singh
'''
from card import Card
from deck import Deck
import string
alpha = string.ascii_uppercase

class Player:
    '''
    An object of this class represents a player in a blackjack game.
    Available Functions:
        - add_card(card)
        - point_calc()
    '''
    def __init__(self, id, name:str, money:int = None, sub_player:bool = False) -> None:
        """
        Initializes an instance of a player.
        """
        if sub_player == False:
            self.sub_player = False; self.split_done = False
            if str(id).isnumeric():
                self.id = str(id)
                self.name = name
                self.cards = []
                self.card_points = []
                self.points = 0
                self.ini_money = money
                self.money = money
                self.bet = 0
                self.hands = [] # List of sub-players
            else:
                raise KeyError("ID should be an Integer.")
        else:
            if str(id).isalnum() == True and str(id).isalpha() == False and str(id).isnumeric() == False:
                self.sub_player = True; self.split_done = True
                self.id = str(id)
                self.name = name
                self.bet = None
                self.cards = []
                self.card_points = []
                self.points = 0
            else:
                raise KeyError("ID should be an Alphanumeric string in the form of '[player_id(int)][subhand char(alpha)]'")

    def add_card(self, card:Card, hand:int=None):
        """
        Adds a card to the hand of player.
        """
        if self.split_done == True and self.sub_player == False:
            self.hands[hand].add_card(card)
        else:
            self.cards.append(card)
            self.card_points.append(card.get_value())
            self.points = self.point_calc()

    def remove_card(self, hand:int=None):
        """
        Remove a card from a hand of player and returns that card.
        """
        if self.split_done == True and self.sub_player == False:
            return self.hands[hand].remove_card()
        else:
            return self.cards.pop()

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

    def get_bet(self):
        """
        Retrieve bet amount for the hand.
        """
        return self.bet

    def player_split(self):
        """
        
        """
        if self.sub_player == True: raise Exception("Please perform a split action on player instead of sub-hand.")
        if self.split_done == True:
            no_hands = len(self.hands)
            for hi in no_hands: #Hand index
                hand_cards = self.hands[hi].cards()
                if len(hand_cards) == 2:
                    if hand_cards[0].get_rank() == hand_cards[1].get_rank():
                        new_hand_card = self.remove_card(hi)
                        id = f"{self.id}"
                        new_hand = Player()

    def change_bet(self, mode: str, amount:int = 0, hand:int = None):
        """
        
        """
        if mode.lower() in ['add', 'dd'] and self.sub_player == False:
            if mode.lower() == 'dd': amount = self.hands[hand].get_bet()
            if self.money >= amount:
                self.money -= amount
            else:
                raise ValueError(f"{self.name} doesn't have enough money.")

        if self.split_done == True and self.sub_player == False:
            if hand == None: self.money += amount; raise Exception("Please specify hand for modifying the bet.")
            self.hands[hand].change_bet(mode, amount)

        else:
            if mode.lower() in ['add', 'dd'] and amount != None:
                self.bet += amount
                
            elif mode.lower() == 'clear':
                self.bet = 0

            else:
                self.money += amount
                raise Exception(f"{mode} is not a valid option for changing bet.")

    def reset_hand(self, deck: Deck):
        """
        Transfers the money made by player (if any) in that round to his balance
        and then resets the player parameters for the next round.
        """    
        if self.sub_player == True: raise Exception("Resetting split hands is not allowed.")
        end_money = 0
        if self.split_done == True:
            for hi in range(len(self.hands)): #Hand index
                end_money += self.hands[hi].get_bet()
                while len(self.hands[hi].cards) != 0:
                    deck.add_card(self.hands[hi].remove_card())
        else:
            end_money += self.bet
            self.bet = 0
        self.money += end_money

        while len(self.cards) != 0:
            deck.add_card(self.remove_card())
        self.points = 0
        self.card_points = []
        self.hands = []
        self.split_done = False

    def quit_money(self):
        """
        Returns the amount of money player made/lost during his playthrough.
        """
        return self.ini_money - self.money

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
