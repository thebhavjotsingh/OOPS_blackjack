from copy import deepcopy as dp
from player import Player
from deck import Deck
from art import *
import os,time

dealer = Player(0, 'dealer')
DECK = Deck(6)
NUM_PLAYERS = 0
MAX_PLAYERS = 8

def point_chart(players:list):
    '''
    Table of all players' points, earnings/losses. 
    '''
    clear()
    print(logo)
    line = f"  +----+--------------------+---------------+---------------+-------------+"
    print(line); print(f"  | ID |{'Name':^20}|{'Balance':^15}|{'Profit/Loss':^15}|  Cur Points |"); print(line)
    for player in players:
        if player.get_profit() > 0:
            print(f"  |{player.get_id():>4}|{player.get_name()[:20]:^20}| ${player.get_balance():>13,.2f}| \033[32m${player.get_profit():>13,.2f}\033[0m|{player.get_points():>13}|")
        else:
            print(f"  |{player.get_id():>4}|{player.get_name()[:20]:^20}| ${player.get_balance():>13,.2f}| \033[31m${player.get_profit():>13,.2f}\033[0m|{player.get_points():>13}|")
    print(line)
    input("  Press Enter to go back")

def clear():
    '''
    clears the screen
    '''
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')

def next_player_anim():
    """
    Just a fun little animation.
    """
    print('Continuing to the next Player\033[?25l'.upper(),end=''); time.sleep(0.2)
    for __ in range(2):
        for _ in range(3):
            print('.')
            time.sleep(0.2)
            print(f'\033[A\033[{30+_}C',end='')
        time.sleep(0.2)
        print(f'\033[3D\033[K',end='')
    print('\033[?25h\033[2K\033[2A')  

def player_creation(list_of_players:list):
    """
    
    """
    clear()
    print(logo)

    if len(list_of_players) == 0: fid = 0
    else: fid = list_of_players[-1].get_id()

    for i in range(len(list_of_players) + 1, NUM_PLAYERS + 1):

        print(f"  ENTER PLAYER \033[36m{fid+i}\033[0m's NAME: ")
        print(f"  ENTER THE AMOUNT YOU HAVE FOR THIS GAME: \033[33m$\033[0m")
        print("\n  \033[31mNOTE:\033[0m THE MINIMUM AMOUNT REQUIRED TO ENTER THE GAME IS \033[32m$40\033[0m.")

        name = input(f"\033[4A\033[{24+len(str(fid+i))}C\033[33m").strip(); print('\033[0m',end='')
        while (len(name) == 0) or (name.isalpha() == False):
            print("\033[?25l\033[2A\033[31mINVALID INPUT\033[0m"); time.sleep(1.2)
            print('\033[A\033[2K\033[?25h')
            name = input(f"\033[{24+len(str(fid+i))}C\033[33m\033[K"); print('\033[0m',end='')

        amount = input(f"\033[45C\033[33m").strip(); print('\033[0m',end='')
        while amount.isnumeric() == False or int(amount) < 40:
            print("\033[?25l\033[3A\033[31mINVALID INPUT\033[0m"); time.sleep(1.2)
            print('\033[A\033[2K\033[?25h')
            amount = input(f"\033[B\033[45C\033[33m\033[K").strip(); print('\033[0m',end='')

        pl = Player(fid+i,name,int(amount))
        list_of_players.append(pl)
        print('\033[A\033[2K\033[A\033[2K',end='')

def set_bet(players: list):
    clear()
    print(logo)
    print('\033[2B\033[31mNOTE:\033[0m BET AMOUNT CANNOT BE LESS THAN 10.\033[3A\033[2K')
    for i in range(len(players)):
        bet_amount = input(f"ENTER THE BET AMOUNT FOR \033[36m{players[i].get_name().upper()} (ID:{players[i].get_id()})\033[0m: \033[33m").strip(); print('\033[0m',end='')
        while bet_amount.isnumeric() == False or int(bet_amount) < 10:
            print("\033[?25l\033[2A\033[31mINVALID INPUT\033[0m"); time.sleep(1.2)
            print('\033[A\033[2K\033[?25h')
            bet_amount = input(f"\033[2KENTER THE BET AMOUNT FOR \033[36m{players[i].get_name().upper()} (ID:{players[i].get_id()})\033[0m: \033[33m").strip(); print('\033[0m',end='')
        players[i].change_bet("add", int(bet_amount))
        print('\033[A\033[2K',end='')

def input_validator(valid_options, decision):
    while decision.isnumeric() == False or int(decision)-1 not in range(len(valid_options)):
        print('\033[?25l\033[31mINCORRECT INPUT\033[0m'); time.sleep(1.2)
        print('\033[A\033[2K\033[2A\033[?25h')
        decision = input("\033[2K>>> ")
    decision = valid_options[int(decision)-1]
    return decision

def card_distribute(players:list):   
    for i in range (len(players)):
        for _ in range(2):
            card = DECK.retrieve_card()
            players[i].add_card(card)

def card_snatch(players:list):
    for i in range (len(players)):
        players[i].reset_hand(DECK)

    dealer.reset_hand(DECK)

def round_winner(players:list, dealer):
    clear()
    while dealer.get_points() < 17:
        clear()
        card = DECK.retrieve_card()
        dealer.add_card(card)
        print(dealer)
        time.sleep(1.5)

    if dealer.check_blackjack() == True:
        print("\033[31mDEALER WINS. IT'S A BLACKJACK.\033[0m")
        for player in players:
            player.change_bet("clear")
            time.sleep(0.5)
    else:
        if dealer.get_points() > 21:
            print(f"DEALER BUSTED")
            time.sleep(0.5)

        for player in players:
            if player.check_blackjack() == True:
                print(f"\033[32m{player.name} WINS. IT'S A BLACKJACK.\033[0m")
                player.change_bet("winb")
            elif player.points > 21:
                print(f"\033[31m{player.name} BUSTED\033[0m")
                player.change_bet("clear")
            elif dealer.points > 21:
                print(f"\033[32m{player.name} WINS\033[0m")
                player.change_bet("win")
            elif player.points > dealer.points:
                print(f"\033[32m{player.name} WINS\033[0m")
                player.change_bet("win")
            elif player.points == dealer.points:
                print(f"{player.get_name()} TIED WITH DEALER")
            else:
                print(f"\033[31m{player.name} LOST\033[0m")
                player.change_bet("clear")
            time.sleep(0.5)
    card_snatch(players)
    input("Press Enter to Continue... ")

def round_end_menu(players:list):
    global NUM_PLAYERS
    
    while True:
        clear()
        print(logo)
        count_ = 0
        decision_2 = input("CHOOSE FROM THE FOLLOWING OPTIONS:\n 1.CONTINUE TO NEXT ROUND    2.LEAVE GAME    3.ENTER NEW PEOPLE    4.DETAILS TABLE\n(Enter a number)\n>>> ")
        decision_2 = input_validator(['1','2','3','4'], decision_2)

        if decision_2 == "1":
            break

        elif decision_2 == "2":
            out_ids = input("ENTER THE NAMES OF PLAYERS LEAVING THE GAME SEPARATED BY COMMAS: ").lower()
            list_outs = out_ids.split(",")
            
            for player_name in list_outs:
                try:
                    player_name = player_name.strip()
                    player_names = [players[i].get_name().lower() for i in range(len(players))]
                    reps = player_names.count(player_name)
                    if reps == 1:
                        players.pop(player_names.index(player_name))
                        player_names.remove(player_name)
                        count_ += 1                
                    elif reps > 1:
                        # TODO: This is some creative shit which I need to think later. It might possibly alter the id system as well
                        pass

                except:
                    print("",end='')
            NUM_PLAYERS -= count_
            break

        elif decision_2 == "3":
            in_ids = input("ENTER THE NUMBER OF PLAYERS WANTING TO JOIN: ").lower()

            new_players = int(in_ids.strip())  # Convert to integer
            NUM_PLAYERS += new_players
            player_creation(NUM_PLAYERS, players)
            break
        
        elif decision_2 == '4':
            point_chart(players)


def available_decisions(player:Player, hand=None):
    """
    
    """
    if hand == None and player.get_sub_hands() != 0:
        raise Exception("Please specify the hand for which you want the options")
    balance = player.get_balance()
    valid_options = []
    points = player.get_points(hand)
    bet = player.get_bet(hand)
    if points == 21:
        return []
    valid_options += ['HIT','STAND','SURRENDER','DETAILS TABLE']
    if bet < balance:
        valid_options.append("DOUBLE DOWN")
    if player.split_possible(hand):
        valid_options.append("SPLIT")
    return valid_options
    

def game_options(player: Player, players:list, hand=None):
    """
    
    """
    while True:
        clear()
        print(dealer)
        print(player)
        if player.get_points(hand) > 21:
            print(busted)
            time.sleep(1.8)
            break
        if player.check_blackjack() == True:
            print(f"{player.get_name()} HAS A BLACKJACK. CONTINUING TO NEXT PLAYER.")
            time.sleep(1.8)
            break

        valid_options = available_decisions(player,hand)
        valids_str = ''
        for i in range(len(valid_options)): valids_str += f"{i+1}.{valid_options[i]}    "

        if len(valid_options) > 0:
            decision = input(f"Select one of the following choices:\n{valids_str.rstrip()}\n(Enter a number)\n>>> ")
            decision = input_validator(valid_options, decision)

            if decision.upper() == "HIT":
                card = DECK.retrieve_card()
                player.add_card(card, hand)
            elif decision.upper() == "STAND":
                break
            elif decision.upper() == "DETAILS TABLE":
                point_chart(players)
            elif decision.upper() == "SURRENDER":
                player.change_bet('give', -(player.get_bet()/2), hand)
                print(f"AMOUNT LEFT WITH {player.get_name()} IS {player.get_bet()}")
                break
            elif decision.upper() == "DOUBLE DOWN":
                player.change_bet("dd", hand)
                card = DECK.retrieve_card()
                player.add_card(card, hand)
                print(f"BET AMOUNT FOR {player.get_name()} IS INCREASED TO {player.get_bet()}")
            elif decision.upper() == "SPLIT":
                player.player_split()
        else:
            print("You're set for this round.".upper()); time.sleep(1.2)
            break


def game_loop(players:list):
    
    while (len(players) != 0):
        card = DECK.retrieve_card()
        dealer.add_card(card)
        card_distribute(players)
        set_bet(players)
        for i in range(1, NUM_PLAYERS+1):
            if players[i-1].status_split() == True:
                for hand in range(players[i-1].get_sub_hands()):
                    game_options(players[i-1],players, hand)
            else:
                game_options(players[i-1],players)
            next_player_anim()
        round_winner(players, dealer)
        round_end_menu(players)
                        

def main():
    """
    
    """

    global NUM_PLAYERS
    while True:
        clear()
        print(logo)
        print(f"""  Welcome to the game of BlackJack! For the best experience,
    we recommend you maximize your terminal window.
    Select one from the following options:
    {'\033[32m1. ENTER GAME          \033[31m2. EXIT GAME\033[0m':^76}
    (Enter a number)""")
        decision_1 = input("  >>> ")
        decision_1 = input_validator(['1','2'], decision_1)

        if decision_1.upper() == "2":
            print("  THANK YOU PLAYING THE GAME! COME AGAIN.")
            break
        elif decision_1.upper() == "1":
            clear(); print(logo)
            NUM_PLAYERS = int(input("  ENTER THE NUMBER OF PLAYERS PLAYING: \033[33m")); print('\033[0m',end='')
            players = []
            player_creation(players)
            game_loop(players)
     
main()