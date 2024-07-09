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
                self.bet = 0
                self.cards = []
                self.card_points = []
                self.points = 0
            else:
                raise KeyError("ID should be an Alphanumeric string in the form of '[player_id(int)][subhand char(alpha)]'")

    def add_card(self, card:Card, hand:int=None):
        """
        Adds a card to the hand of player.
        """
        if hand != None:
            self.hands[hand].add_card(card)
        else:
            self.cards.append(card)
            self.card_points.append(card.get_value())
            self.points = self.point_calc()

    def remove_card(self, hand:int=None):
        """
        Remove a card from a hand of player and returns that card.
        """
        if hand != None:
            card = self.hands[hand].remove_card()
        else:
            card = self.cards.pop()
            self.card_points.remove(card.get_value())
            self.points = self.point_calc()
        return card

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

    def check_blackjack(self):
        """
        
        """
        if len(self.cards) == 2:
            card_ranks = [self.cards[0].get_rank(), self.cards[1].get_rank()]
            if 'A' in card_ranks:
                if ('K' in card_ranks) or ('Q' in card_ranks) or ('J' in card_ranks):
                    return True
        return False

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

    def status_split(self):
        return self.split_done
    
    def sub_exist(self):
        return self.sub_player

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
            self.split_done = True
            if len(self.cards) == 2:
                if self.cards[0].get_rank() == self.cards[1].get_rank():
                    new_hand2_card = self.remove_card()
                    new_hand1_card = self.remove_card()
                    id1 = f"{self.id}A"; id2 = f"{self.id}B"; 
                    new_hand1 = Player(id1, self.name, 0, True); new_hand2 = Player(id2, self.name, 0, True)
                    self.hands.append(new_hand1); self.hands.append(new_hand2)
                    self.add_card(new_hand1_card, 0); self.add_card(new_hand2_card, 1)
                    self.money += self.bet
                    self.change_bet("add", self.bet, 0); self.change_bet("add", self.bet, 1)
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

    def card_printer(self) -> str:
        """
        Method reponsible for printing the cards from player hand(s) in a terminal GUI format. 
        """
        printing_list = []
        if self.split_done == False and self.sub_player == False:
            # Print method when cards haven't been split into sub hands.
            no_rows = round(len(self.cards)/4 + 0.4)
            for row in range(no_rows):
                row_cards = self.cards[0+row*4:4+row*4]
                for line in range(5):
                    row_line = ''
                    red_count = 0
                    for i in range(len(row_cards)):
                        if row_cards[i].get_suit() in ['hearts','diamonds']:                        
                            row_line += f"\033[31m{str(row_cards[i]).split('\n')[line]}\033[00m"
                            red_count += 10 # each colored card needs ten more spaces for proper indentation
                        elif row_cards[i].get_suit() == '?':                        
                            row_line += f"\033[35m{str(row_cards[i]).split('\n')[line]}\033[00m"
                            red_count += 10 # each colored card needs ten more spaces for proper indentation
                        else: 
                            row_line += str(row_cards[i]).split('\n')[line]
                        if i != len(row_cards)-1:
                            row_line += " "
                    # row_line = f"{row_line:^{130+red_count}}"
                    printing_list.append(row_line)
            return "\n".join(printing_list)
        
        elif self.split_done == True and self.sub_player == False:
            # Print method when cards have been split into sub hands.
            lengths=[]
            for i in range(len(self.hands)):
                length = len(self.hands[i].cards)
                lengths.append(length)
            maximum_cards = max(lengths)
            no_rows1 = round(maximum_cards/4+0.4)

            for i in range(no_rows1):
                for line in range(5):
                    row_line = ''
                    for hand in self.hands:
                        for card_index in range(i*4, (i+1)*4):
                            try:
                                if (hand.cards[card_index]).get_suit() in ['hearts','diamonds']:
                                    row_line += f"\033[31m{str(hand.cards[card_index]).split('\n')[line]}\033[00m" + " "
                                else: 
                                    row_line += str(hand.cards[card_index]).split('\n')[line] + " "
                            except:
                                row_line += 6*" "
                        row_line += 4*" "
                    printing_list.append(row_line)
            return "\n".join(printing_list)

    def __str__(self) -> str:
        """
        String representation of the players that includes there name, balance and stakes.
        """
        rep=''
        if self.name == "Dealer" and len(self.cards) == 1:
            rep = f"{'\033[31;1;4mDEALER\033[00m'}\n{'Balance: \033[34m∞\033[0m'}\n{'Hand: \033[35m??\033[0m'}\n"
            cards = dp(self.cards)
            cards.append(Card('hearts',2,0))
            rep += self.card_printer(cards)
        elif self.name == "Dealer":
            rep = f"{'\033[31;1;4mDEALER\033[00m'}\n{'Balance: \033[34m∞\033[0m'}\n{f'Hand: \033[34m{self.points}\033[0m'}\n"
            rep += self.card_printer()
        else:
            rep = f"{f'\033[32;1;4m{self.name.upper()}\033[00m'}\n"
            if self.split_done == False and self.sub_player == False:
                if self.money <= 20:
                    rep += f"{f'Balance: \033[31m{self.money}\033[00m   '}"+f"{f'   Stake: \033[34m{self.bet}\033[00m'}\n"
                else:
                    rep += f"{f'Balance: \033[34m{self.money}\033[00m   '}"+f"{f'   Stake: \033[34m{self.bet}\033[00m'}\n"
                rep += f"{f'Hand: \033[34m{self.points}\033[00m'}\n"
                rep += self.card_printer()

            elif self.split_done == True and self.sub_player == False:
                if self.money <= 20:
                    rep += f"{f'Balance: \033[31m{self.money}\033[00m   '}\n\n"
                else:
                    rep += f"{f'Balance: \033[34m{self.money}\033[00m   '}\n\n"

                point_line = ''
                for i in range(len(self.hands)):
                    rep += f"{f'Stake: \033[34m{self.hands[i].bet}\033[00m':38}"
                    point_line += f"{f'Hand {i+1}: \033[34m{self.hands[i].points}\033[00m':38}"
                rep += f'\n{point_line}\n'
                rep += self.card_printer()
                    
        return rep

d = Player(0, 'Dealer')
d.add_card(Card('spades', 'A', 1))
d.add_card(Card('hearts', 'Q', 1))
d.add_card(Card('spades', 'K', 1))

p = Player(1, 'Sharry',300)
p.add_card(Card('diamonds', 10, 1))
p.add_card(Card('clubs', 10, 1))
p.change_bet('add', 21)
p.player_split()
# p.add_card(Card('spades', 7, 1))
print(d)
print(p)