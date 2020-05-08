import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    

class Deck:
    
    def __init__(self):
        self.deck = [] 
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = "" 
        for card in self.deck:
            deck_comp += '\n '+card.__str__()
        return 'The deck has:' + "\n"+deck_comp
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card
    

class Hand:
    
    def __init__(self):

        self.cards = []  
        self.value = 0   
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            

class Chips:
    
    def __init__(self,total):
        self.total = total
        self.bet = 0
    def __str__(self):
    	return self.total.__str__()
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet
        


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Place your bet: "))
        except:
            print("Bet must be an integer!")
            print("\n")
            continue
        else:
            if (chips.bet > chips.total):
                print(f"You only have {chips.total} chips to bet!")
                print("\n")
                continue
            elif (chips.bet == 0):
                print("You need to bet something!")
                print("\n")
                continue
            elif (chips.bet < 0):
                print("You must bet a positive number of chips!")
                print("\n")
                continue
            else:
                print(f"{chips.bet} chips bet - time to play!")
                print("\n")
                break
    return chips.bet

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing
    
    while True:
        next_move = input("Hit or stand? Type 'h' or 's': ")
        if (next_move[0].lower() == "h"):
            hit(deck,hand)
            print("\n")
            break
        elif (next_move[0].lower() == "s"):
            print("\n")
            print("You chose to stand. Dealer's turn: ")
            playing = False
            break
        else:
            print("\n")
            print("ERROR: improper input!")
            print("\n")
            continue

    
def show_some(player,dealer):
    print("\n")
    print("DEALER'S HAND:")
    print("  < card hidden >")
    print(f"  < {dealer.cards[1]} >")
    print("\n")
    
    print("YOUR HAND:")
    for card in player.cards:
        print(f"  < {card} >")
    
def show_all(player,dealer):
    print("\n")
    print("DEALER'S HAND:")
    for card in dealer.cards:
        print(f"  < {card} >")
    print(f"Total: {dealer.value}")
    print("\n")
    
    print("YOUR HAND:")
    for card in player.cards:
        print(f"  < {card} >")
    print(f"Total: {player.value}")
    
def player_busts(chips):
    print("You bust!")
    chips.lose_bet()

def player_wins(chips):
    print("You win!")
    chips.win_bet()

def dealer_busts(chips):
    print("The dealer busts!")
    chips.win_bet()
    
def dealer_wins(chips):
    print("The dealer wins!")
    chips.lose_bet()
    
def push():
    print("It's a tie!")

print("Welcome to blackjack! The goal is to get as close to 21 as possible without going over.")
print("\n")
print("A few rules:")
print("  - The dealer will hit until she reaches 17 or more and does not hit on soft 17.")
print("  - The payout is 1:1 for all wins, including blackjacks.")
print("  - There is no splitting or doubling down.")
print("\n")

while True:
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    while True:
        try:
            starting_chips = int(input("How many chips do you have? "))
        except:
            print("Must input an integer of chips!")
            continue
        if starting_chips == 0:
            print("You must bring SOME chips to play!")
            continue
        elif starting_chips < 0:
            print("You cannot possibly have negative chips!")
            continue
        else:
            print(f"Ok, you are starting with {starting_chips} chips!")
            chips = Chips(total=starting_chips)
            break

    take_bet(chips)
    
    print("\n")
    show_some(player_hand,dealer_hand)
    
    playing = True
    while playing:
        
        hit_or_stand(deck,player_hand)
        
        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(chips)
            break
        else:
            continue

    while dealer_hand.value < 17 and player_hand.value <= 21:
        hit(deck,dealer_hand)
    
    show_all(player_hand,dealer_hand)

    while player_hand.value <= 21:
        if (player_hand.value > dealer_hand.value):
            player_wins(chips)
            break
        elif (dealer_hand.value > 21):
            dealer_busts(chips)
            break
        elif (player_hand.value == dealer_hand.value):
            push()
            break
        elif player_hand.value < dealer_hand.value:
            dealer_wins(chips)
            break
    
    print("\n")
    print(f"Chip total: {chips.total}")
    
    while True:
        try:
            replay = input("Do you want to play again? (y/n): ")
        except:
            print("ERROR: Invalid input!")
            continue
        if replay[0].lower() != "n" and replay[0].lower() != "y":
            print("Must input 'y' or 'n' only!")
            continue
        else:
            break
    if replay[0].lower() == "y":
        continue
    else:
        print("Thanks for playing!")
        break