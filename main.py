#IMPORTS FOR GLOBAL USE
import random

#GLOBAL VARIABLES
playing = True
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
# SUITS: SPADES, CLUBS, DIAMONDS, HEARTS
suits = (

 ' -------- \n'+'| {}      |\n'+'|   /\   |\n' + '| /    \ |\n' +     
    '|( _/\_ )| \n' + '|   )(   |\n' + '|     {}  |\n' + ' --------',

' -------- \n'+'| {}      |\n' + '|   --   |\n' + 
    '| _(  )_ |\n' + '|(  )(  )| \n' + \
    '|  )__(  |\n' + '|     {}  |\n' + ' --------',

' -------- \n'+'| {}      |\n'+'|   /\   | \n' + '|  /  \  |\n' + 
    '|  \  /  |\n' + '|   \/   |\n' + '|     {}  |\n' + ' --------',

' -------- \n'+'| {}      |\n'+'| __  __ | \n' + 
    '|(  \/  )|\n' + '| \    / |\n' + \
    '|   \/   |\n' + '|     {}  |\n' + ' --------'

)


class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit.format(self.rank,self.rank)


class Deck():

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        full_deck = ''

        for card in self.deck:

            full_deck += '\n' + card.__str__()
        return 'The Deck has: '+ full_deck
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'A':
            self.aces += 1
    
    def aces_check(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1



class Chips():

    def __init__(self, total=2000):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How much do you want to bet? ')) 
        except:
            print('SORRY! Bet must be a number!')
        else:
            if chips.bet > chips.total:
                print('SORRY! Bet exceeds your total bank!\n' + 'You have {} chips available.'.format(chips.total))
            else:
                break

def hit_me(deck, hand):
    hand.add_card(deck.deal())
    hand.aces_check()

def hit_or_stay(deck, hand):
    global playing

    while True:
        x = input('Would you like to hit or stay? (choose h or s): ')

        if x[0].lower() == 'h':
            hit_me(deck, hand)
        elif x[0].lower() == 's':
            print('Player stands, Dealer is in turn.')
            playing = False
        else:
            print('Sorry! Please choose again')
            continue
        break


def show_some(player, dealer):
    print("Dealer's Hand:\n")
    print("<CARD HIDDEN>")
    print(dealer.cards[1])
    print("Player's Hand:", *player.cards, sep=' \n')
    print("Player Has:", player.value)


def show_all(player, dealer):
    print(*player.cards, sep = ' \n')
    print("Player's Hand =", player.value)
    print(*dealer.cards, sep = ' \n')
    print("Dealer's Hand =", dealer.value)

def player_wins(player, dealer, chips):
    print('Player Wins!!')
    chips.win_bet()

    

def player_bust(player, dealer, chips):
    print('Player busted!')
    chips.lose_bet()


def dealer_wins(player, dealer, chips):
    print('Dealer Wins!')
    chips.lose_bet()


def dealer_bust(player, dealer, chips):
    print('Dealer Bust..!')
    chips.win_bet()



def push(player, dealer, chips):
    print('Push, Dealer Wins')
    chips.lose_bet()



#PLAYING THE GAME!!!!!

while True:
    deck = Deck()
    deck.shuffle()

    players_hand = Hand()
    players_hand.add_card(deck.deal())
    players_hand.add_card(deck.deal())

    dealers_hand = Hand()
    dealers_hand.add_card(deck.deal())
    dealers_hand.add_card(deck.deal())

    players_chips = Chips()

    take_bet(players_chips)

    show_some(players_hand, dealers_hand)

    while playing:

        hit_or_stay(deck, players_hand)

        show_some(players_hand, dealers_hand)

        if players_hand.value > 21:
            player_bust(players_hand, dealers_hand, players_chips)
            break
    
    if players_hand.value <= 21:

        while dealers_hand.value < 17:
            hit_me(deck, dealers_hand)

            show_all(players_hand, dealers_hand)

            if dealers_hand.value > 21:
                dealer_bust(players_hand, dealers_hand, players_chips)
                
            elif dealers_hand.value > players_hand.value:
                dealer_wins(players_hand, dealers_hand, players_chips)
            
            elif dealers_hand.value < players_hand.value:
                player_wins(players_hand, dealers_hand, players_chips)

            else:
                push(players_hand, dealers_hand, players_chips)
    

        print('\n Players Chips total: {}'.format(players_chips.total))

        new_game = input('Would you like to play again? choose y or n: ')

        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print('Thanks for playing!')
            break



