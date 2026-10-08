import random
import os
# im going to be gambling

# terminal color codes
RESET = "\033[0m"
RED   = "\033[91m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
CYAN  = "\033[96m"
BOLD  = "\033[1m"
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# deck setup
SUITS = ['♠', '♥', '♦', '♣'] # yeah yeah "unicode in terminal bad", i know but sacrifices must be made for visuals
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
          '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# definitions

## hand
def calculate_hand(hand):
    """Calculates total value, adjusting Aces from 11 to 1 as needed."""
    value = sum(VALUES[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value
## render
def render_card(card):
    """Colors Hearts/Diamonds red, Spades/Clubs default cyan/bold."""
    rank, suit = card
    color = RED if suit in ['♥', '♦'] else CYAN
    return f"{color}[{rank}{suit}]{RESET}"
def render_hand(hand, hide_first=False):
    if hide_first:
        return f"{CYAN}[??]{RESET} " + " ".join(render_card(c) for c in hand[1:])
    return " ".join(render_card(c) for c in hand)
def display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=True):
    clear_screen()
    print(f"{BOLD}=== BLACKJACK ==={RESET}")
    print(f"Bankroll: {GREEN}${bankroll}{RESET} | Current Bet: {YELLOW}${bet}{RESET}\n")
    
    if hide_dealer:
        print(f"Dealer's Hand: {render_hand(dealer_hand, hide_first=True)}")
    else:
        dealer_val = calculate_hand(dealer_hand)
        print(f"Dealer's Hand: {render_hand(dealer_hand)} (Total: {dealer_val})")
        
    player_val = calculate_hand(player_hand)
    print(f"Your Hand:   {render_hand(player_hand)} (Total: {player_val})\n")

## deck
def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


# play round
def get_bet(bankroll):
    while True:
        try:
            bet = int(input(f"Place your bet (1-{bankroll}): $"))
            if 1 <= bet <= bankroll:
                return bet
            print("Invalid bet amount.")
        except ValueError:
            print("Please enter a valid number.")
def play_round(bankroll):
    print(f"\nYour current bankroll: {GREEN}${bankroll}{RESET}")
    bet = get_bet(bankroll)

    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    # check blackjacks
    player_val = calculate_hand(player_hand)
    dealer_val = calculate_hand(dealer_hand)

    if player_val == 21 and dealer_val == 21:
        display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=False)
        print(f"{YELLOW}both have blackjack. its a push, but also how?{RESET}")
        return bankroll
    elif player_val == 21:
        display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=False)
        payout = int(bet * 1.5)
        print(f"{GREEN}{BOLD}blackjack, you won. but how did you get so lucky? (+${payout}){RESET}")
        return bankroll + payout
    elif dealer_val == 21:
        display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=False)
        print(f"{RED}dealer has blackjack. you lose -${bet}.{RESET}")
        return bankroll - bet

    # player turn
    can_double = bankroll >= (bet * 2)
    while True:
        display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=True)
        player_val = calculate_hand(player_hand)

        if player_val > 21:
            print(f"{RED}{BOLD}you went over 21 and bust. you lose -${bet}.{RESET}")
            return bankroll - bet

        options = "[h]it, [s]tand"
        if can_double and len(player_hand) == 2:
            options += ", or [d]ouble down"

        action = input(f"action ({options}): ").strip().lower()
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break
        elif action == 'd' and can_double and len(player_hand) == 2:
            bet *= 2
            player_hand.append(deck.pop())
            display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=True)
            player_val = calculate_hand(player_hand)
            if player_val > 21:
                print(f"{RED}{BOLD}busted on double down! you lose -${bet}.{RESET}")
                return bankroll - bet
            break

    # dealer turn
    display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=False)
    while calculate_hand(dealer_hand) < 17:
        print("dealer hits...")
        dealer_hand.append(deck.pop())
        display_board(player_hand, dealer_hand, bankroll, bet, hide_dealer=False)

    # who won???
    player_final = calculate_hand(player_hand)
    dealer_final = calculate_hand(dealer_hand)
    if dealer_final > 21:
        print(f"{GREEN}{BOLD}dealer busted, you win +${bet}{RESET}")
        return bankroll + bet
    elif player_final > dealer_final:
        print(f"{GREEN}{BOLD}you won with ({player_final} to {dealer_final}) +${bet}{RESET}")
        return bankroll + bet
    elif dealer_final > player_final:
        print(f"{RED}dealer wins. ({dealer_final} to {player_final}) -${bet}{RESET}")
        return bankroll - bet
    else:
        print(f"{YELLOW}push. its a tie. ({player_final} vs {dealer_final}){RESET}")
        return bankroll

# now play, fool
bankroll = 1000
while True:
    clear_screen()
    if bankroll <= 0:
        print(f"{RED}{BOLD}you ran out of money.{RESET}")
        break
    # this is a great system
    bankroll = play_round(bankroll)
    if bankroll <= 0:
        print(f"\n{RED}{BOLD}you are now broke.{RESET}")
        break
    print(f"\n{BOLD}updated bankroll:{RESET} {GREEN}${bankroll}{RESET}")
    again = input("\nplay another hand? (y/n): ").strip().lower()
    if again != 'y':
        print(f"good choice, walked away with {GREEN}${bankroll}{RESET}")
        break
