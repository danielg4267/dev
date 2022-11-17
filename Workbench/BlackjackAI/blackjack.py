"""
Daniel Gonzalez
CS5100
Fall 2022
Final Project - Blackjack Model

"""

# TODO: Code is a little haphazard in places, clean up logic
# TODO: Need more comments and documentation
# TODO: Implement "Walk" action, ie player stops playing, and will no longer be playing
# TODO: Agent is not part of the game model, should be moved out of this file in the future

import random

class Deck:

    def __init__(self):
        self.cards = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"] * 4
        random.shuffle(self.cards)

    def draw(self):
        # maybe pop?
        return random.choice(self.cards)

class Actions:

    default_bet = 10

    bet = "bet"
    walk = "walk"

    insurance = "insurance" # double the bet, if dealer has blackjack immediately get it back, otherwise play with this bet
    surrender = "surrender" # get half your bet back before the game continues
    next = "next" # don't purchase insurance, don't surrender, just next turn

    split = "split"
    hit = "hit"
    stand = "stand"
    double_down = "double down"


class Agent:

    def __init__(self, index):
        self.index = index

    def get_action(self, state):
        print("Get an action!")

class ManualAgent(Agent):

    def get_action(self, state):
        #print(state.players[self.index].hands)
        print("Current state:", state)
        print("Available actions:", state.get_legal_actions(self.index))
        choice = input("Choose action (type first two letters of first word in chosen action): ")
        valid = False
        while not valid:
            if choice == 'sp':
                return Actions.split
            elif choice == 'be':
                return Actions.bet
            elif choice == 'do':
                return Actions.double_down
            elif choice == 'in':
                return Actions.insurance
            elif choice == "ne":
                return Actions.next
            elif choice == "su":
                return Actions.surrender
            elif choice == 'hi':
                return Actions.hit
            elif choice == 'st':
                return Actions.stand
            else:
                choice = input("Bad input, try again: ")

class GameState:

    def __init__(self, num_players = 1, copy = None):
        if copy is None:
            self.players = [Player(False), Player(True)]
            self.current_player = 0
            num_players-=1
            for i in range(num_players):
                self.players.insert(0, Player(False))

            for i in range(len(self.players)):
                self._bet(i)

        else:
            self.current_player = copy.current_player
            self.players = []
            for player in copy.players:
                self.players.append(Player(copy=player))

    def __str__(self):
        str = "Current Player: " + self.current_player.__str__() + "\n"

        for player in self.players:
            if player.is_dealer:
                str += "Dealer:\n" + player.__str__() + "\n"
            else:
                str += "Player:\n" + player.__str__() + "\n"

            """if player.is_playing:
                if player.is_dealer:
                    str += "Dealer:"
                else:
                    str += "Player:"
                    str += player.wallet.__str__()
                for hand in player.hands:
                    str += "["
                    for card in hand.cards:
                        str += card + " "
                    str += "]"
                    str += "\n"""
        return str


    def generate_successor(self, action, player_index):

        next_state = GameState(copy=self)

        '''elif action == Actions.walk:
            next_state._walk(player_index)'''

        if action == Actions.bet:
            next_state._bet(player_index)
        elif action == Actions.insurance:
            next_state._insurance(player_index)
        elif action == Actions.surrender:
            next_state._surrender(player_index)
        elif action == Actions.next:
            next_state._next(player_index)
        elif action == Actions.split:
            next_state._split(player_index)
        elif action == Actions.hit:
            next_state._hit(player_index)
        elif action == Actions.stand:
            next_state._stand(player_index)
        elif action == Actions.double_down:
            next_state._double_down(player_index)

        return next_state

    def get_legal_actions(self, player_index):
        actions = []
        player = self.players[player_index]
        if not player.is_playing:
            return actions

        if len(player.hands) == 0:
            actions.append(Actions.walk)
            if player.wallet >= Actions.default_bet or player.is_dealer:
                actions.append(Actions.bet)
            return actions

        # gotta figure out how to buy insurance...
        #if

        # This means they are standing
        # len() of hands > 0 but not using any hand
        if player.currentHand is None:
            return actions

        #insurance only available if dealer has not flipped their card yet, AND dealer has card value >= 10
        if self.players[-1].is_dealer \
        and not self.players[-1].flipped \
        and self.players[-1].hands[0].value(0) > 9:
            # insurance action for dealer just flips the card and checks for blackjack
            # so dealer can always do insurance
            # player can only purchase insurance if they have enough money
            if player.is_dealer or player.wallet >= player.hands[0].bet:
                actions.append(Actions.insurance)
            # player can surrender as well
            if not player.is_dealer:
                actions.append(Actions.surrender)
                actions.append(Actions.next)
            return actions


        if player.hands[player.currentHand].splittable > 0 and not player.is_dealer:
            actions.append(Actions.split)

        if player.hands[player.currentHand].value() < 21:
            actions.append(Actions.hit)
            actions.append(Actions.stand)
            if not player.is_dealer:
                actions.append(Actions.double_down)

        return actions

    def next_player(self):

        if self.current_player >= len(self.players) - 1:
            print("Round over, final state:\n", self)
            self._settle() #TODO: game over, i just dont know what to do yet
        else:
            self.current_player += 1
            if not self.players[self.current_player].is_playing:
                self.next_player()

    def _bet(self, player_index):
        if Actions.bet not in self.get_legal_actions(player_index):
            print("Invalid action", player_index, self.get_legal_actions(player_index))
            return
        self.players[player_index].bet(Actions.default_bet)
        '''for i in range(2):
            self.players[player_index].hit()'''

    def _insurance(self, player_index):
        if Actions.insurance not in self.get_legal_actions(player_index):
            print("Invalid action")
            return

        # logically, a little messy, but it gets the job done for now
        player = self.players[player_index]
        if player.is_dealer:
            player.flipped = True
            if player.hands[0].value() == 21:

                for player in self.players:
                    if player.insurance > 0:
                        player.wallet += player.insurance * 2
                        player.hands[0].bet = 0
                        player.insurance = 0
                    else:
                        player.hands[0].bet += player.insurance
                        player.insurance = 0
                self._settle()
            else:
                for player in self.players:
                    player.hands[0].bet += player.insurance
                    player.insurance = 0

                self.current_player = 0
                if not self.players[self.current_player].is_playing:
                    self.next_player()
        else:
            player.insurance = player.hands[0].bet
            player.wallet -= player.insurance
            self.current_player += 1

    def _surrender(self, player_index):
        if Actions.surrender not in self.get_legal_actions(player_index):
            print("Invalid action")
            return

        player = self.players[player_index]
        player.wallet += (player.hands[0].bet/2)
        player.hands[0].bet = 0
        player.is_playing = False
        self.current_player += 1 #should not be the dealer, so this should be fine

    def _next(self, player_index):
        if Actions.next not in self.get_legal_actions(player_index):
            print("Invalid action")
            return

        # this first branch should never happen, but just in case
        if self.current_player == len(self.players):
            self.current_player = 0
        else:
            self.current_player += 1

    def _hit(self, player_index):
        if Actions.hit not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].hit()
        if self.players[player_index].currentHand is None:
            self.next_player()

    def _double_down(self, player_index):
        if Actions.double_down not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].double_down()
        if self.players[player_index].currentHand is None:
            self.next_player()


    def _stand(self, player_index):
        if Actions.stand not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].stand()
        if self.players[player_index].currentHand is None:
            self.next_player()

    def _split(self, player_index):
        if Actions.split not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].split()

    def _settle(self):
        # all situations only apply to hands under 21 (ie they did not bust)
        # if hand is under dealer and 21, lose entire bet
        # if hand is above dealer or 21, get bet back, and earned amount of bet
        # if hand is equal to dealer, get bet back
        # if dealer busts, every hand that did not bust gets bet back and earned amount of bet
        dealerValue = self.players[-1].hands[0].value()
        for player in self.players:
            if not player.is_dealer:
                for hand in player.hands:
                    if hand.value() > 21:
                        continue
                    elif dealerValue > 21:
                        player.wallet += (hand.bet * 2)
                    elif hand.value() > dealerValue:
                        player.wallet += (hand.bet*2)
                    elif hand.value() == dealerValue:
                        player.wallet += hand.bet
                player.hands = []
                player.insurance = 0
                player.is_playing = True
            else:
                player.hands = []
                player.is_playing = True
                player.flipped = False
                self._bet(-1)
        self.current_player = 0



class Player:

    def __init__(self, is_dealer = False, wallet = 100, copy = None):

        if copy is None:
            self.wallet = wallet
            self.is_dealer = is_dealer
            self.flipped = not is_dealer
            self.insurance = 0
            self.is_playing = True
            self.currentHand = None
            self.hands = []

        else:
            self.wallet = copy.wallet
            self.is_dealer = copy.is_dealer
            self.flipped = copy.flipped
            self.insurance = copy.insurance
            self.is_playing = copy.is_playing
            self.currentHand = copy.currentHand
            self.hands = []
            for hand in copy.hands:
                self.hands.append(Hand(copy=hand))

    def __str__(self):
        str = "Wallet: " + self.wallet.__str__() + "\n"
        str += "Insurance: " + self.insurance.__str__() + "\n"
        str += "Playing: " + self.is_playing.__str__() + "\n"
        for hand in self.hands:
            str += "Hand:\n"
            str += hand.__str__() + "\n"

        return str


    def _next_hand(self):
        if self.currentHand < len(self.hands) - 1:
            self.currentHand += 1
        else:
            self.currentHand = None
    def peek(self):
        card = self.hands[0].cards[0]

        return card == "A" or card == "J" or card == "K" or card == "Q" or card == "10"
    def bet(self, amount = 10):
        if self.is_dealer:
            self.hands = [Hand(0, 0)]
            self.currentHand = 0

        elif self.wallet >= amount:
            self.wallet -= amount
            self.hands = [Hand(amount)]
            self.currentHand = 0

    def walk(self):
        self.is_playing = False

    def hit(self):
        self.hands[self.currentHand].hit()
        if self.hands[self.currentHand].value() >= 21:
            self.stand()

    def split(self):
        new_hand = self.hands[self.currentHand].split()
        if new_hand is not None:
            self.wallet -= new_hand.bet
            self.hands.append(new_hand)
    def double_down(self):
        self.wallet -= self.hands[self.currentHand].bet
        self.hands[self.currentHand].bet *= 2
        self.hands[self.currentHand].hit()
        self.stand()

    def stand(self):
        self._next_hand()


class Hand:

    def __init__(self, bet = 0, splittable = 2, copy = None):
        if copy is None:
            self.cards = []
            self.bet = bet
            self.cards.append("1")
            self.cards.append("1")
            '''for i in range(2):
                self.hit()'''
            if self.cards[0] == self.cards[1]:
                self.splittable = splittable
            else:
                self.splittable = 0
        else:
            self.bet = copy.bet
            self.splittable = copy.splittable
            self.cards = []
            for card in copy.cards:
                self.cards.append(card)
    def __str__(self):
        str = "Bet: " + self.bet.__str__() + "  |  "
        str += "Value: " + self.value().__str__() + "  |  "
        str += "Split: " + self.splittable.__str__() + " | "
        str += "["
        for card in self.cards:
            str += card + " "
        str += "]"
        return str

    def split(self):
        if len(self.cards) > 0 :
            self.cards = [self.cards[0]]
            self.splittable -= 1
            new_hand = Hand(copy=self)
            new_hand.hit()
            self.hit()
            if not self.cards[0] == self.cards[1]:
                self.splittable = 0
            if not new_hand.cards[0] == new_hand.cards[1]:
                new_hand.splittable = 0
            return new_hand

    def hit(self):
        self.cards.append(Deck().draw())
        if self.splittable > 0 and len(self.cards) > 2:
            self.splittable = 0

    def value(self, cardIndex = None):
        if cardIndex == None:
            value = 0
            ace = False
            for card in self.cards:
                if card == "A":
                    ace = True
                    value +=1
                elif card == "J" or card == "K" or card == "Q":
                    value += 10
                else:
                    value += int(card)

            if ace and value <= 11:
                value += 10

            return value
        else:
            card = self.cards[cardIndex]
            if card == "A":
                return 11
            if card == "J" or card == "K" or card == "Q":
                return 10
            else:
                return int(card)

def main():
    # player, dealer
    agents = [ManualAgent(0), ManualAgent(1)]
    game = GameState(1)
    # just trying to test it...
    while True:
        game = game.generate_successor(agents[game.current_player].get_action(game), game.current_player)   #agents[game.current_player].get_action(game)


main()
