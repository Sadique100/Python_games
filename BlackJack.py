# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_amount = 500
player_hand= []
dealer_hand = []
deck = []
hands = 0
bet = 10
insure_bet = 0
split_true = False
deck = []
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
    def __str__(self):
        # return a string representation of a hand
        str_out = "Hand contains : "
        i = 0
        for card in self.hand:
            str_out += str(self.hand[i]) + " "
            i += 1
        return str_out
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.hand:
            value += VALUES.get(card.get_rank())
        for card in self.hand:
            if (value +10 <= 21) and (card.get_rank() == "A"):
                value += 10
        return value
    def get_length(self):
        return len(self.hand)
    def split_card(self):
        return self.hand.pop(1)
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for card
        for card in self.hand:
            card.draw(canvas,[pos[0],pos[1]]) 
            pos[0] += 100

# define deck class 
class Deck:
    def __init__(self):
    # create a Deck object
        self.deck = []
        
        for suit in SUITS:
            for rank in RANKS:
                # card = Card(suit,rank)
                self.deck.append(str(suit)+str(rank))
            
    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)
    def deal_card(self):
       # deal a card object from the deck
        c = self.deck[-1]
        self.deck.remove(c)
        card = Card(str(c)[0], str(c)[-1])
        return card
    def __str__(self):
        # return a string representing the deck
        str_out = "Deck contains : "
        i=0
        for card in self.deck:
            str_out += str(self.deck[i]) +" "
            i+=1
        return str_out
        

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, outcome, score, hands, player_amount, bet, insure_bet, split_true
    insure_bet = 0
    deck = Deck()
    hands += 1
    bet = 10*(1 + int(hands/3))
    player_amount -= bet
    split_true = False
    if in_play == True:
        score -= 1
    else:
        in_play = True   
    print deck
    deck.shuffle()
    print deck
    player_hand = Hand()
    dealer_hand = Hand()
    print deck
    for i in range(4):
        if i%2 == 0:
            player_hand.add_card(deck.deal_card())
        else:
            dealer_hand.add_card(deck.deal_card())
    if player_hand.get_value() == 21:
        outcome = "Player has BlackJack!!"    
    else:
        outcome = "You have "+str(player_hand.get_value())+" Hit or Stand?"
    print str(player_hand)[-2]
    print str(player_hand)[17]
            
def hit():
    global player_hand, deck, score, outcome, in_play, D_D
    print player_hand.get_value()

    if in_play == True:
        if player_hand.get_value() < 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() < 21:
            outcome = "You have "+str(player_hand.get_value())+" Hit or Stand?"
        elif player_hand.get_value() > 21:
            in_play = False
            outcome = "Player Busted :( "
            score -= 1
    else:
        outcome = "You doubled Down!"        


        
def stand():
    global outcome, score, in_play, player_amount
    print str(player_hand.get_length())
    if player_hand.get_value() > 21:
        outcome = "Sorry your Bust :( New Deal?"
    else:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        print dealer_hand
        print dealer_hand.get_value()
        if player_hand.get_value() == 21 and player_hand.get_length() == 2:
            if dealer_hand.get_value() == 21 and dealer_hand.get_length() == 2:
                outcome = "Dealer has BlackJack also -- Push"
                player_amount += bet
                
            else:
                outcome = "BlackJack you won"
                player_amount += bet*(3/2)
                score += 1
        if insure_bet != 0:
            if dealer_hand.get_value() == 21 and dealer_hand.get_length() == 2:
                player_amount += insure_bet*2
            else:
                player_amount -= insure_bet
        if dealer_hand.get_value() > 21:
            outcome = "Dealer Busted - You Won!! New Deal?"
            score += 1
            player_amount += 2*bet
        elif dealer_hand.get_value() <= 21:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome = "You Won!! New Deal?"
                score += 1
                player_amount += 2*bet
            elif dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer won :( New Deal?"
                score -= 1
def double_down():
    global bet, in_play, player_hand, outcome
    if player_hand.get_length() != 2:
        outcome =  "You can only Double down with 2 cards"
    else:
        print "DDDD"
        bet *= 2
        player_hand.add_card(deck.deal_card())
        in_play = False
    if player_hand.get_value() <= 21:   
        outcome = "You have "+str(player_hand.get_value())
    else:
        outcome = "Busted - try to only double down when you have 10 or 11"
"""        
def split():
    global player_hand, player_hand_a, outcome, split_true
   
    if str(player_hand)[-2] == str(player_hand)[17]:
        split_true = True
        player_hand_a = Hand()
        player_hand_a.add_card(player_hand.split_card())
        print player_hand
        print player_hand_a
    else:
        outcome = "You can only split with pairs!"
"""
def input_handler(text_input):
    global bet, player_amount
    input_bet = text_input
    min_bet = 10*(1 + int(hands/3))
    if int(input_bet) < min_bet:
        bet = min_bet
    else:
        bet = int(text_input)
        
def insure_handler(text_input):
    global insure_bet
    if str(dealer_hand)[-2] == "A":
        if int(text_input) > (1/2)*bet:
            insure_bet = (1/2)*bet
        else:
            insure_bet = int(text_input)
    else:
        outcome = "You can only insure when Dealer shows Ace"
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    #global player_hand, dealer_hand, outcome, in_play
    canvas.draw_text("BlackJack", (210, 80), 40, "Red")
    
    player_hand.draw(canvas, [50,470])
    dealer_hand.draw(canvas, [50,100])
    if split_true == True:
        player_hand_a.draw(canvas, [50, 370])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0],100 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text(outcome, (50, 300), 25, "Orange")
    canvas.draw_text(str(score), (550, 80), 25, "Yellow")
    canvas.draw_text("Player Amount: "+str(player_amount), (300, 580),25, "Pink")
    canvas.draw_text("Player Bet: "+str(bet), (400, 400),25, "Pink")
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
deal = frame.add_button("Deal", deal, 200)
Hit = frame.add_button("Hit",  hit, 200)
Stand = frame.add_button("Stand", stand, 200)
D_D = frame.add_button("Double Down?", double_down, 200)


frame.set_draw_handler(draw)
enter_bet = frame.add_input("Bet (min_amount = 10)", input_handler, 50)
insurance_bet = frame.add_input("Insurance Bet?? Bet can be max 1/2 bet", insure_handler, 50)

# get things rolling
frame.start()
dealer_hand = Hand()
player_hand = Hand()


