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


"""
Ok I figured it out
generate_successors() has to be different from "iterate to the next state"
Note the difference here - there are multiple states that can be derived from an action
generate_successors() should return a list of every possible state
So if you hit, it should return a list of 14 states
If insurance, it can be either the dealer had blackjack and the game is over, the dealer did not have blackjack  

"""

import random

class Deck:

    def __init__(self):
        self.cards = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]
        #random.shuffle(self.cards)

    def draw(self):
        # deck has infinite cards, but in the future worth considering
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
        action = None
        while not valid:
            if choice == 'sp':
                action = Actions.split
                valid = True
            elif choice == 'be':
                action = Actions.bet
                valid = True
            elif choice == 'wa':
                action = Actions.walk
                valid = True
            elif choice == 'do':
                action = Actions.double_down
                valid = True
            elif choice == 'in':
                action = Actions.insurance
                valid = True
            elif choice == "ne":
                action = Actions.next
                valid = True
            elif choice == "su":
                action = Actions.surrender
                valid = True
            elif choice == 'hi':
                action = Actions.hit
                valid = True
            elif choice == 'st':
                action = Actions.stand
                valid = True
            else:
                choice = input("Bad input, try again: ")

        print("Chosen action:", action)
        return action

class DealerAgent(Agent):

    def get_action(self, state):

        print("Current state:", state)
        print("Available actions:", state.get_legal_actions(self.index))
        action = None
        if Actions.insurance in state.get_legal_actions(self.index):
            action = Actions.insurance
        elif Actions.bet in state.get_legal_actions(self.index):
            action = Actions.bet
        elif state.get_hand_value(self.index) < 17:
            action = Actions.hit
        else:
            action = Actions.stand
        print("Chosen action:", action)
        return action

class ExpectimaxAgent(Agent):

    #TODO: How to implement depth?
    #Starting to think depth should just go down per turn
    #So depth of 5 would be 5 moves, regardless of when/where/who
    #Evaluate based on current bets, potential earnings, hands, etc

    def __init__(self, index, depth):
        Agent.__init__(self, index)
        self.depth = depth
        self.goal_earnings = Actions.default_bet * 5
        self.start_cash = 100

    def get_action(self, state):
        actions = state.get_legal_actions(self.index)
        argmax = actions[0]
        max = -9999999
        valueFunc = self.minValue

        for action in actions:
            result = state.generate_successor(self.index, action)
            nextAgent = result.current_player
            if nextAgent == self.index:
                valueFunc = self.maxValue
            value = valueFunc(result, self.depth, nextAgent)
            if value > max:
                max = value
                argmax = action


    def maxValue(self, state, depth, index):
        actions = state.get_legal_actions(index)
        # shouldn't reach this but just in case
        if index == self.index and Actions.walk in actions:
            depth -= 1

        if self.terminalTest(state, depth):
            return self.utility(state)

        valueFunc = self.minValue

        actions = state.get_legal_actions(index)
        v_max = 0

        for action in actions:
            v = 0
            next_states = state.generate_successors(action, index)
            probability = 1/next_states # uniform probability
            for next_state in next_states:
                next_agent = next_state.current_player
                if next_agent == self.index:
                    valueFunc = self.maxValue
                v += probability * valueFunc(next_state, next_agent, depth)
            v_max = max(v_max, v)
        return v_max

    def minValue(self, state, depth, index):
        actions = state.get_legal_actions(index)
        #shouldn't reach this but just in case
        if index == self.index and Actions.walk in actions:
            depth -= 1
        if self.terminalTest(state, depth):
            return self.utility(state)

        valueFunc = self.maxValue
        d = depth
        v_min = 0

        for action in actions:
            v = 0
            next_states = state.generate_successors(action, index)
            probability = 1 / next_states  # uniform probability
            for next_state in next_states:

                next_agent = next_state.current_player
                if not next_agent == self.index:
                    valueFunc = self.minValue

                v += probability * valueFunc(next_state, next_agent, depth)
            v_min = min(v_min, v)
        return v_min

    def terminalTest(self, state, depth):
        return (depth ==0 or state.is_terminal(self.index))

    def utility(self, state):
        self.evaluationFunction(state)

    def evaluationFunction(self, state):
        eval = 0
        player = state.players[self.index]
        dealer = state.players[-1]
        current_earnings = player.wallet - self.start_cash
        eval += (current_earnings - self.goal_earnings)
        for hand in player.hands:
            eval + hand.bet/2
            if hand.value() <= 21:
                eval += hand.value()
            else:
                eval -= hand.value()
        if state.is_terminal(self.index):
            eval = abs(eval) * 10

        return eval



class GameState:

    def __init__(self, num_players = 1, copy = None):
        if copy is None:
            self.num_players = num_players
            self.players = [Player(False), Player(True)]
            self.current_player = 0
            num_players-=1
            for i in range(num_players):
                self.players.insert(0, Player(False))

            for i in range(len(self.players)):
                self._bet(i)

        else:
            self.num_players = copy.num_players
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
        return str

    def generate_successors(self, action, player_index):

        states = []

        if action not in self.get_legal_actions(player_index):
            return states

        if action == Actions.bet:
            for card1 in Deck().cards:
                for card2 in Deck().cards:
                    # when betting, every combination of cards is a successor...
                    hand = Hand(cards=[card1,card2])
                    next_state = GameState(copy=self)
                    next_state._bet(player_index)
                    hand.bet = next_state.players[player_index].hands[0].bet
                    # set cards of that player to this new hand
                    next_state.players[player_index].hands = [hand]
                    states.append(next_state)

        elif action == Actions.walk:
            next_state = GameState(copy=self)
            next_state._walk(player_index)
            states.append(next_state)

        elif action == Actions.insurance:
            next_state = GameState(copy=self)
            next_state._insurance(player_index)
            states.append(next_state)

        elif action == Actions.surrender:
            next_state = GameState(copy=self)
            next_state._surrender(player_index)
            states.append(next_state)

        elif action == Actions.next:
            next_state = GameState(copy=self)
            next_state._next(player_index)
            states.append(next_state)

        elif action == Actions.split:
            for card1 in Deck().cards:
                for card2 in Deck().cards:
                    next_state = GameState(copy=self)
                    next_state._split(player_index, card1, card2)
                    states.append(next_state)

        elif action == Actions.hit:
            for card in Deck().cards:
                next_state = GameState(copy=self)
                next_state._hit(player_index, card)
                states.append(next_state)

        elif action == Actions.double_down:
            for card in Deck().cards:
                next_state = GameState(copy=self)
                next_state._double_down(player_index, card)
                states.append(next_state)

        elif action == Actions.stand:
            next_state = GameState(copy=self)
            next_state._stand(player_index)
            states.append(next_state)

        return states






    def generate_successor(self, action, player_index):

        next_state = GameState(copy=self)

        if action == Actions.bet:
            next_state._bet(player_index)
        elif action == Actions.walk:
            next_state._walk(player_index)
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
        if self.num_players < 1:
            return actions # no one can do anything
        if not player.is_playing:
            return [Actions.next]

        if len(player.hands) == 0:
            if player.wallet >= Actions.default_bet or player.is_dealer:
                actions.append(Actions.bet)
            if not player.is_dealer:
                actions.append(Actions.walk)
            return actions


        # This means they are standing
        # len() of hands > 0 but not using any hand
        if player.currentHand is None: #and self.players[-1].flipped:
            return [Actions.next]

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


        if player.hands[player.currentHand].splittable > 0 \
                and player.wallet >= player.hands[player.currentHand].bet \
                and not player.is_dealer:
            actions.append(Actions.split)

        if player.hands[player.currentHand].value() < 21:
            actions.append(Actions.hit)
            actions.append(Actions.stand)
            if not player.is_dealer:
                actions.append(Actions.double_down)

        return actions

    def is_dealer(self, player_index):

        return self.players[player_index].is_dealer

    def get_num_agents(self):
        return len(self.players)

    def is_terminal(self, player_index):
        return not self.players[player_index].is_playing

    def get_hand_value(self, player_index):
        player = self.players[player_index]
        value = 0
        if player.currentHand is not None:
            value += player.hands[player.currentHand].value()

        return value

    def next_player(self):

        if self.current_player >= len(self.players) - 1:
            print("Round over, final state:\n", self)
            self._settle()
        else:
            self.current_player += 1
            # Standing or not playing
            if not self.players[self.current_player].is_playing:
                self.next_player()

    def _bet(self, player_index):
        if Actions.bet not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].bet(Actions.default_bet)
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def _walk(self, player_index):
        if Actions.walk not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].is_playing = False
        self.next_player()
        self.num_players -= 1

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
                    if not player.is_playing:
                        continue
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
                    if not player.is_playing:
                        continue
                    player.hands[0].bet += player.insurance
                    player.insurance = 0

                self.current_player = 0

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
        player.currentHand = None

        # this cannot be a dealer so this should be fine
        self.current_player += 1

    def _next(self, player_index):
        if Actions.next not in self.get_legal_actions(player_index):
            print("Invalid action")
            return

        # this first branch should never happen, but just in case
        if self.current_player == len(self.players):
            self.current_player = 0
        else:
            self.current_player += 1

    def _hit(self, player_index, card = None):
        if Actions.hit not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].hit(card)
        if self.players[player_index].currentHand is None:
            self.next_player()

    def _double_down(self, player_index, card = None):
        if Actions.double_down not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].double_down(card)
        if self.players[player_index].currentHand is None:
            self.next_player()


    def _stand(self, player_index):
        if Actions.stand not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].stand()
        if self.players[player_index].currentHand is None:
            self.next_player()

    def _split(self, player_index, card1 = None, card2 = None):
        if Actions.split not in self.get_legal_actions(player_index):
            print("Invalid action")
            return
        self.players[player_index].split(card1, card2)

    def _settle(self):
        # all situations only apply to hands under 21 (ie they did not bust)
        # if hand is under dealer and 21, lose entire bet
        # if hand is above dealer or 21, get bet back, and earned amount of bet
        # if hand is equal to dealer, get bet back
        # if dealer busts, every hand that did not bust gets bet back and earned amount of bet
        dealerValue = self.players[-1].hands[0].value()
        for player in self.players:
            if not player.is_playing:
                continue

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
            else:
                player.hands = []
                player.flipped = False
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
            self.walked = False

        else:
            self.wallet = copy.wallet
            self.is_dealer = copy.is_dealer
            self.flipped = copy.flipped
            self.insurance = copy.insurance
            self.is_playing = copy.is_playing
            self.currentHand = copy.currentHand
            self.hands = []
            self.walked = copy.walked
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
            if self.hands[self.currentHand].value() >= 21:
                self._next_hand()
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
            if self.hands[self.currentHand].value() == 21:
                self.stand()

    def walk(self):
        self.is_playing = False

    def hit(self, card = None):
        self.hands[self.currentHand].hit(card)
        if self.hands[self.currentHand].value() >= 21:
            self.stand()

    def split(self, card1 = None, card2 = None):
        new_hand = self.hands[self.currentHand].split(card1, card2)
        if new_hand is not None:
            self.wallet -= new_hand.bet
            self.hands.append(new_hand)
        if self.hands[self.currentHand].value() >= 21:
            self.stand()
    def double_down(self, card = None):
        self.wallet -= self.hands[self.currentHand].bet
        self.hands[self.currentHand].bet *= 2
        self.hands[self.currentHand].hit(card)
        self.stand()

    def stand(self):
        self._next_hand()


class Hand:

    def __init__(self, bet = 0, splittable = 2, copy = None, cards = None): #TODO: CURRENTLY ._BET() IN GENERATESUCCESSORS DOES NOT MAKE THE HAND SPLITTABLE EVEN THO IT IS - THUS, WE SHOULD CREATE A NEW HAND FOR THE PLAYER AND SET IT TO THAT
        if copy is None:
            self.bet = bet
            #self.cards.append("A")
            #self.cards.append("J")

            if cards is None:
                self.cards = []
                for i in range(2):
                    self.cards.append(Deck().draw())
            else:
                self.cards = cards

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

    def split(self, card1 = None, card2 = None):
        if len(self.cards) > 0 :
            self.cards = [self.cards[0]]
            self.splittable -= 1
            new_hand = Hand(copy=self)
            self.hit(card1)
            new_hand.hit(card2)
            if not self.cards[0] == self.cards[1]:
                self.splittable = 0
            if not new_hand.cards[0] == new_hand.cards[1]:
                new_hand.splittable = 0
            return new_hand

    def hit(self, card = None):
        if card is not None:
            self.cards.append(card)
        else:
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
    agents = [ManualAgent(0), ManualAgent(1), ManualAgent(2)]
    game = GameState(2)
    # just trying to test it...
    while game.num_players > 0:
        game = game.generate_successors(agents[game.current_player].get_action(game), game.current_player)[-1]


main()
