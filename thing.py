import random
# im going to be gambling

# terminal color codes
RESET = "\033[0m"
RED   = "\033[91m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
CYAN  = "\033[96m"
BOLD  = "\033[1m"

# deck setup
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
          '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# definitions

## calculate
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
