import random
# im going to be gambling

# terminal color codes
RESET = "\033[0m"
RED   = "\033[91m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
CYAN  = "\033[96m"
BOLD  = "\033[1m"

# deck
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
          '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}