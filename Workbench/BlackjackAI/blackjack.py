"""
Daniel Gonzalez
CS5100
Fall 2022
Final Project - Blackjack Model

"""

# TODO: Code is a little haphazard in places, clean up logic
# TODO: Need more comments and documentation
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
from math import log
from math import sqrt

class Deck:

    def __init__(self):
        self.cards = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]

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
        self.start_cash = 100
        self.goal_earnings = self.start_cash + Actions.default_bet * 3
        self.action_counts = {Actions.bet: 0,
                              Actions. walk: 0,
                              Actions.insurance: 0,
                              Actions.surrender: 0,
                              Actions.next: 0,
                              Actions.split: 0,
                              Actions.hit: 0,
                              Actions.stand: 0,
                              Actions.double_down: 0}

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

        #print("MANUAL chosen action:", action)
        self.action_counts[action] += 1
        return action

class DealerAgent(Agent):

    def __str__(self):
        return "DealerAgent"

    def get_action(self, state):

        #print("Current state:", state)
        #print("Available actions:", state.get_legal_actions(self.index))
        action = None
        if Actions.insurance in state.get_legal_actions(self.index):
            action = Actions.insurance
        elif Actions.bet in state.get_legal_actions(self.index):
            action = Actions.bet
        elif state.get_hand_value(self.index) < 17:
            action = Actions.hit
        else:
            action = Actions.stand
        #print("DEALER chosen action:", action)
        self.action_counts[action] += 1
        return action

class ExpectimaxAgent(Agent):

    def __init__(self, index, depth):
        Agent.__init__(self, index)
        self.depth = depth

    def __str__(self):
        return "ExpectimaxAgent"

    def get_action(self, state):
        actions = state.get_legal_actions(self.index)

        if Actions.walk in actions:
            if state.players[self.index].wallet >= self.goal_earnings or Actions.bet not in actions:
                return Actions.walk
            else:
                return Actions.bet

        argmax = actions[0]
        max = -9999999
        actionValues = {}
        for action in actions:
            v = 0
            next_states = state.generate_successors(action, self.index)
            probability = 1 / len(next_states)  # uniform probability
            for next_state in next_states:
                next_agent = next_state.current_player
                if next_agent == self.index:
                    valueFunc = self.maxValue
                else:
                    valueFunc = self.minValue
                v += probability * valueFunc(next_state, self.depth, next_agent)
            if v > max:
                max = v
                argmax = action
            actionValues[action] = v

        #print("Evaluating state:", state, "\nActions:", actionValues, "\nChosen action:", argmax)
        #print("EXPECTIMAX chosen action:", argmax)
        self.action_counts[argmax] += 1
        return argmax


    def maxValue(self, state, depth, index):

        if self.terminalTest(state, depth):
            return self.utility(state)

        depth -= 1

        actions = state.get_legal_actions(index)
        v_max = 0
        valueFunc = None

        for action in actions:
            v = 0
            next_states = state.generate_successors(action, index)
            probability = 1/len(next_states) # uniform probability
            for next_state in next_states:
                next_agent = next_state.current_player
                if next_agent == self.index:
                    valueFunc = self.maxValue
                else:
                    valueFunc = self.minValue
                v += probability * valueFunc(next_state, depth, next_agent)
            v_max = max(v_max, v)
        return v_max

    def minValue(self, state, depth, index):


        if self.terminalTest(state, depth):
            return self.utility(state)

        v_min = 999999
        depth -= 1
        valueFunc = None

        actions = state.get_legal_actions(index)
        for action in actions:
            v = 0
            next_states = state.generate_successors(action, index)
            probability = 1 / len(next_states)  # uniform probability
            for next_state in next_states:

                next_agent = next_state.current_player
                if next_agent == self.index:
                    valueFunc = self.maxValue
                else:
                    valueFunc = self.minValue

                v += probability * valueFunc(next_state, depth, next_agent)
            v_min = min(v_min, v)
        return v_min

    def terminalTest(self, state, depth):
        return (depth ==0 or state.is_terminal(self.index))

    def utility(self, state):
        return self.evaluationFunction(state)

    def evaluationFunction(self, state):


        eval = 0
        player = state.players[self.index]
        dealer = state.players[-1]

        round_weight = 8
        earnings_weight = 2
        goalDist_weight = 1

        # total earned from entire game
        current_earnings = player.wallet - self.start_cash
        goalDist = player.wallet - self.goal_earnings

        round_loss = 0
        for hand in player.hands:
            bet = hand.bet
            val = hand.value()

            # Lost the bet!
            if val > 21 or (len(dealer.hands) > 0 and dealer.hands[0].value() > val):
                bet = -bet
            # Agent has a chance to win
            elif val < 21:
                # The closer to 21, the better this will be
                bet /= (21 - val)
            round_loss += bet
        if state.is_terminal(self.index):
            goalDist_weight = 10


        round_loss *= round_weight
        current_earnings *= earnings_weight
        goalDist *= goalDist_weight

        eval += round_loss + current_earnings + goalDist

        return eval

class MCTSAgent(Agent):

    def __init__(self, index):
        Agent.__init__(self, index)
        self.tree = {}
        # Eventually it would be useful to parameterize these
        # but for now they are just hard-coded lol
        self.depth = 10
        self.rollout_depth = 4
        self.c = 1.4
        self.gamma = .7
        self.start_cash = 100
        self.goal = self.start_cash + (Actions.default_bet * 3)
        self.num_simulations = 500

    def __str__(self):
        return "MCTSAgent"

    def get_action(self, state):
        actions = state.get_legal_actions(self.index)
        # Separate rules for walk and bet
        if Actions.walk in actions:
            if state.players[self.index].wallet >= self.goal or Actions.bet not in actions:
                action = Actions.walk
            else:
                action = Actions.bet
        else:
            action = self.mcts(state)

        #print("MCTS chosen action:", action)
        self.action_counts[action] += 1
        return action

    def mcts(self, state):
        self.tree = {}
        root = Node(state)
        self.root = state
        #print("Simulating starting with ", state)
        for i in range(self.num_simulations):
            self.simulate(root, self.depth)

        max = -999999
        argmax = list(root.actions.keys())[0]
        for action in root.actions:
            if root.qvalue(action) >= max:
                argmax = action
                max = root.qvalue(action)
        #print("Final action values:", root.actions, "in state:", state, "Chose action:", argmax)
        return argmax

    def simulate(self, node, depth):
        if depth == 0 or node.state.is_terminal(self.index):
            return 0
        if node.state not in self.tree:
            #print("ROLLOUT FROM STATE:\n", node.state)
            self.tree[node.state] = node
            return self.rollout(node.state, self.rollout_depth)

        # Get node associated with this state
        node = self.tree[node.state]
        action = self.choose_action(node)
        next_state = node.state.generate_successor(action, node.state.current_player)
        next_node = Node(next_state)

        # q = r + y * SIMULATE(s', d-1)
        q = self.reward(node.state, action) + (self.gamma * self.simulate(next_node, depth-1))

        # N(s, a) = N(s, a) + 1
        # N(s) = N(s) + 1
        node.increase_action_visits(action)
        node.increase_state_visits()
        node.update_qvalue(action, q)
        return q

    def choose_action(self, node):
        player_index = node.state.current_player
        actions = list(node.actions.keys())
        #print("Choosing actions for simulated state", node.state, "ACTIONS:", node.actions)
        values = {}

        for action in actions:
            # Q(s,a) + c * sqrt( ln(N(s))/N(s,a))
            uct = node.qvalue(action) + ( self.c * sqrt( log(node.state_visits()) / node.action_visits(action) ) )
            values[action] = uct

        if player_index == self.index:
            arg_m = max(values, key=values.get)
        else:
            arg_m = min(values, key=values.get)


        #print("Chose action for simulation:", arg_m)
        return arg_m

    def rollout(self, state, depth):
        #print("ROLLOUT PATH:\nDEPTH:",depth,"STATE:\n", state)
        if depth == 0 or state.is_terminal(self.index):
            return 0
        action = self.policyAction(state)
        next_state = state.generate_successor(action, state.current_player)
        return self.reward(state, action) + self.gamma * self.rollout(next_state, depth-1)

    def policyAction(self, state):
        actions = state.get_legal_actions(state.current_player)
        action = actions[0]
        # Current player is dealer
        if state.players[state.current_player].is_dealer:
            if Actions.insurance in actions:
                action = Actions.insurance
            elif Actions.bet in actions:
                action = Actions.bet
            elif state.get_hand_value(state.current_player) < 17:
                action = Actions.hit
            else:
                action = Actions.stand

        # Current player is agent
        elif state.current_player == self.index:
            if Actions.insurance in actions:
                dealer_card = state.players[-1].hands[0].value(0)
                if dealer_card == 11:
                    action = Actions.surrender
                else:
                    action = Actions.insurance
            elif Actions.walk in actions:
                # Walk away when agent has won more than they started with
                if(state.players[self.index].wallet >= self.goal) or Actions.bet not in actions:
                    action = Actions.walk
                else:
                    action = Actions.bet
            elif state.get_hand_value(self.index) < 17 and Actions.hit in actions:
                #print("Hellooooo Megan!")
                action = Actions.hit
            elif Actions.stand in actions:
                action = Actions.stand
            else:
                action = actions[0]

        # Current player is some other player (does not affect agent score)
        else:
            action = actions[0]
        #print("Policy action:", action, "actions:", actions)
        return action

    def reward(self, state, action):
        next_state = GameState(copy=state).generate_successor(action, state.current_player)
        player = state.players[self.index]
        next_state_player = next_state.players[self.index]
        if(len(next_state_player.hands) > 0 and len(next_state.players[-1].hands) > 0):
            next_state._settle()
        r = next_state_player.wallet - player.wallet
        return r


class Node:

    def __init__(self, state):
        self.state = state
        self.visits = 1 # if this node has been created, that means it has been visited
        self.actions = {}
        for action in state.get_legal_actions(state.current_player):
            visits = 1
            Qvalue = 999999  # unexplored nodes begin at infinity
            self.actions[action] = (visits, Qvalue)

    def qvalue(self, action):
        return self.actions[action][1]

    def set_all_qvalue(self, value):
        for action in self.actions:
            self.actions[action] = (self.actions[action][0], value)

    def update_qvalue(self, action, q):
        old_q = self.actions[action][1]
        new_q = old_q + ( (q - old_q) / self.actions[action][0] )
        self.actions[action] = (self.actions[action][0], new_q)


    def state_visits(self):
        return self.visits

    def increase_state_visits(self):
        self.visits +=1

    def action_visits(self, action):
        return self.actions[action][0]

    def increase_action_visits(self, action):
        self.actions[action] = (self.actions[action][0]+1, self.actions[action][1])






class GameState:

    def __init__(self, num_players = 1, copy = None):
        if copy is None:
            self.rounds = 0
            self.num_players = num_players
            self.players = [Player(False), Player(True)]
            self.current_player = 0
            num_players-=1
            for i in range(num_players):
                self.players.insert(0, Player(False))

            for i in range(len(self.players)):
                self._bet(i)

        else:
            self.rounds = copy.rounds
            self.num_players = copy.num_players
            self.current_player = copy.current_player
            self.players = []
            for player in copy.players:
                self.players.append(Player(copy=player))

    def __eq__(self, other):
        # First check number of players
        if self.num_players != other.num_players \
        or len(self.players) != len(other.players):
            return False
        # Check that each player is the same
        for i in range(len(self.players)):
            if self.players[i] != other.players[i]:
                return False
        # Check that we are on the same turn
        return (self.current_player == other.current_player)

    def __hash__(self):
        hash_val = (len(self.players), self.num_players, self.current_player)
        for player in self.players:
            hash_val = hash_val + (player,)

        return hash(hash_val)


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
            return [GameState(copy=self)]

        if action == Actions.bet:
            face_cards = ["A", "J", "K", "Q", "10"]
            for card1 in Deck().cards:
                for card2 in Deck().cards:
                    # dealer only has one card if it starts with a face card
                    if self.players[player_index].is_dealer and card1 in face_cards:
                        cards = [card1]
                    else:
                        cards = [card1, card2]
                    # when betting, every combination of cards is a successor...
                    hand = Hand(cards=cards)
                    next_state = GameState(copy=self)
                    next_state._bet(player_index)
                    hand.bet = next_state.players[player_index].hands[0].bet
                    if self.players[player_index].is_dealer:
                        hand.splittable = 0
                    # set cards of that player to this new hand
                    next_state.players[player_index].hands = [hand]
                    states.append(next_state)

        elif action == Actions.walk:
            next_state = GameState(copy=self)
            next_state._walk(player_index)
            states.append(next_state)

        elif action == Actions.insurance:
            if not self.players[player_index].is_dealer:
                next_state = GameState(copy=self)
                next_state._insurance(player_index)
                states.append(next_state)
            else:
                for card in Deck().cards:
                    next_state = GameState(copy=self)
                    next_state._insurance(player_index, card=card)
                    # Every combination of face_card + card in the deck
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
        if(len(self.players) <= player_index):
            print(player_index)
        player = self.players[player_index]
        if self.num_players < 1:
            return [Actions.next] # no one can do anything
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
        return (not self.players[player_index].is_playing) or self.num_players < 1

    def get_hand_value(self, player_index):
        player = self.players[player_index]
        value = 0
        if player.currentHand is not None:
            value += player.hands[player.currentHand].value()

        return value

    def next_player(self):

        if self.current_player >= len(self.players) - 1:
            #print("Round over, final state:\n", self)
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

    def _insurance(self, player_index, card = None):
        if Actions.insurance not in self.get_legal_actions(player_index):
            print("Invalid action")
            return

        # logically, a little messy, but it gets the job done for now
        player = self.players[player_index]
        if player.is_dealer:
            player.flipped = True
            player.hit(card=card)
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
        if self.current_player >= len(self.players)-1:
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
        # if hand is above dealer or == 21, get bet back, and earned amount of bet
        # if hand is equal to dealer, get bet back
        # if dealer busts, every hand that did not bust gets bet back and earned amount of bet
        self.rounds += 1
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

    def __hash__(self):
        values = []
        for hand in self.hands:
            values.append(hand.value())
        while len(values) < 4:
            values.append(0)

        return hash((self.is_dealer, self.flipped, self.insurance, self.is_playing,
         self.currentHand, values[0],values[1],values[2],values[3]))

    def __eq__(self, other):
        if (len(self.hands) != len(other.hands)):
            return False

        for i in range(len(self.hands)):
            if self.hands[i].value() != other.hands[i].value():
                return False


        return (self.is_dealer == other.is_dealer
        and self.flipped == other.flipped
        and self.insurance == other.insurance
        and self.is_playing == other.is_playing
        and self.currentHand == other.currentHand)


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
            # Just make it one card if they have a potential blackjack
            if self.peek():
                self.hands[0].cards = [self.hands[0].cards[0]]
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

    def __init__(self, bet = 0, splittable = 2, copy = None, cards = None):
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
            if len(self.cards) > 1:
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

    e_agents = [ExpectimaxAgent(0, 2), DealerAgent(1)]
    m_agents = [MCTSAgent(0), DealerAgent(1)]
    b_agents = [MCTSAgent(0), ExpectimaxAgent(1, 2), DealerAgent(2)]

    agents = [b_agents, e_agents, m_agents]

    for agent_set in agents:
        for i in range(5):
            game = GameState(len(agent_set)-1)
            while game.num_players > 0:
                game = game.generate_successor(agent_set[game.current_player].get_action(game), game.current_player)

            for j in range(len(agent_set)-1):
                print("\nAgent:", agent_set[j], "\nAgent Actions:", agent_set[j].action_counts, "\nPlayer wallet:",game.players[j].wallet, "\nRounds:", game.rounds)




main()
