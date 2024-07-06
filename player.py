'''
# Player Class for blackjack game
# Written by: Bhavjot Singh
'''
from card import Card
from deck import Deck
import string
from copy import deepcopy as dp

ALPHA = string.ascii_uppercase

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
                self.name = name.title()
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

    def get_points(self, hand:int = None):
        """
        
        """
        if hand != None: 
            return self.hands[hand].get_points()
        return self.points

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
                        id = f"{self.id}{ALPHA[no_hands]}"
                        new_hand = Player(id, self.name, 0, True)
                        self.hands.append(new_hand)
                        self.add_card(new_hand_card, no_hands)
                        self.change_bet("add", self.hands[hi].get_bet(), no_hands)
        else:
            if len(self.cards) == 2:
                if self.cards[0].get_rank() == self.cards[1].get_rank():
                    new_hand2_card = self.remove_card()
                    new_hand1_card = self.remove_card()
                    id1 = f"{self.id}A"; id2 = f"{self.id}B"; 
                    new_hand1 = Player(id1, self.name, 0, True); new_hand2 = Player(id2, self.name, 0, True)
                    self.hands.append(new_hand1); self.hands.append(new_hand2)
                    self.add_card(new_hand1_card, 0); self.add_card(new_hand2_card, 1)
                    self.change_bet("add", self.get_bet(), 0); self.change_bet("add", self.get_bet(), 1)
                    self.bet = 0

    def change_bet(self, mode: str, amount:int = None, hand:int = None):
        """
        
        """
        mode = mode.lower()

        # AGRUMENT CHECKS START
        if mode not in ['add', 'dd', 'give', 'clear', 'win', 'winb']: raise ValueError(f"{mode} is not a valid option for change_bet method.")
        if mode in ['add', 'give']:
            if amount == None: raise ValueError(f"Please enter an amount you want to {mode} to player.")
        if self.split_done == True and self.sub_player == False and hand == None:
            raise ValueError(f"Please enter the hand id to which you want to perform {mode} action.")
        # ARGUMENT CHECKS END

        if mode in ['win','winb','dd','add']:        
            if mode in ['dd','win','winb']:
                if self.sub_player == False and self.split_done == True:
                    amount = self.hands[hand].get_bet()
                elif self.sub_player == False and self.split_done == False:
                    amount = self.bet
                if mode == 'winb':
                    amount *= 1.5

            if mode in ['dd','add']:
                if self.money >= amount:
                    self.money -= amount
                else:
                    raise ValueError("You don't have enough money.")
            
            if self.sub_player == False and self.split_done == True:
                self.hands[hand].change_bet('give', amount)
            elif self.sub_player == False and self.split_done == False:
                self.bet += amount

        elif mode == 'give':
            self.bet += amount

        elif mode == 'clear':
            self.bet = 0

    def reset_hand(self, deck: Deck):
        """
        Transfers the money made by player (if any) in that round to his balance
        and then resets the player parameters for the next round.
        """    
        if self.sub_player == True: raise Exception("Resetting split hands is not allowed.")
        if self.name != 'Dealer':
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
            self.split_done = False
            self.hands = []
        
        while len(self.cards) != 0:
            deck.add_card(self.remove_card())
            self.points = 0
            self.card_points = []

    def quit_money(self):
        """
        Returns the amount of money player made/lost during his playthrough.
        """
        return self.ini_money - self.money

    def card_printer(self, cards) -> string:
        printing_list = []
        no_rows = round(len(cards)/4 + 0.4)
        for row in range(no_rows):
            row_cards = cards[0+row*4:4+row*4]
            for line in range(5):
                row_line = ''
                red_count = 0
                for i in range(len(row_cards)):
                    if row_cards[i].get_suit() in ['hearts','diamonds']:                        
                        row_line += f"\033[31m{repr(row_cards[i]).split('\n')[line]}\033[00m"
                        red_count += 10 # each colored card needs ten more spaces for proper indentation
                    elif row_cards[i].get_suit() == '?':                        
                        row_line += f"\033[35m{repr(row_cards[i]).split('\n')[line]}\033[00m"
                        red_count += 10 # each colored card needs ten more spaces for proper indentation
                    else: 
                        row_line += repr(row_cards[i]).split('\n')[line]
                    if i != len(row_cards)-1:
                        row_line += "  "
                row_line = f"{row_line:^{130+red_count}}"
                printing_list.append(row_line)
        return "\n".join(printing_list)

    def __str__(self) -> str:
        """
        String representation of the players.
        """
        rep=''
        if self.name == "Dealer" and len(self.cards) == 1:
            rep = f"{'\033[31;1;4mDEALER\033[00m':^144}\n{'Balance: \033[34m∞\033[0m':^139}\n{'Hand: \033[35m??\033[0m':^139}\n"
            cards = dp(self.cards)
            cards.append(Card('hearts',2,0))
            rep += self.card_printer(cards)
        elif self.name == "Dealer":
            rep = f"{'\033[31;1;4mDEALER\033[00m':^144}\n{'Balance: \033[34m∞\033[0m':^139}\n{f'Hand: \033[34m{self.points}\033[0m':^139}\n"
            cards = dp(self.cards)
            rep += self.card_printer(cards)
        else:
            rep = f"{f'\033[32;1;4m{self.name.upper()}\033[00m':^144}\n"
            if self.split_done == False and self.sub_player == False:
                if self.money <= 20:
                    rep += f"{f'Balance: \033[31m{self.money}\033[00m   ':>75}"+f"{f'   Stake: \033[34m{self.bet}\033[00m':<75}\n"
                else:
                    rep += f"{f'Balance: \033[34m{self.money}\033[00m   ':>75}"+f"{f'   Stake: \033[34m{self.bet}\033[00m':<75}\n"
                rep += f"{f'Hand: \033[34m{self.points}\033[00m':^140}\n"
                cards = dp(self.cards)
                rep += self.card_printer(cards)  
        
        return rep

# d = Player(0, 'Dealer')
# d.add_card(Card('spades', 'A', 1))
# d.add_card(Card('hearts', 'Q', 1))
# d.add_card(Card('spades', 'K', 1))

# p = Player(1, 'Sharry',300)
# p.add_card(Card('diamonds', 10, 1))
# p.add_card(Card('clubs', 'A', 1))
# p.add_card(Card('spades', 7, 1))
# print(d)
# print(p)