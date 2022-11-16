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


            """for player in self.players:
                player.bet()
                for i in range(2):
                    player.hit()"""
        else:
            self.current_player = copy.current_player
            self.players = []
            for player in copy.players:
                self.players.append(Player(copy=player))

    def __str__(self):
        str = ""
        for player in self.players:
            if player.is_playing:
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
                    str += "\n"
        return str


    def generate_successor(self, action, player_index):

        next_state = GameState(copy=self)
        """elif action == Actions.insurance:
            next_state._insurance(player_index)
        elif action == Actions.walk:
            next_state._walk(player_index)
        elif action == Actions.surrender:
            next_state._surrender(player_index)"""
        if action == Actions.bet:
            next_state._bet(player_index)
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
        # gotta figure out how to know their current hand isn't standing...
        if player.currentHand is None:
            return actions

        if player.hands[player.currentHand].splittable > 0 and not player.is_dealer:
            actions.append(Actions.split)

        if player.hands[player.currentHand].value() < 21:
            actions.append(Actions.hit)
            actions.append(Actions.stand)
            if not player.is_dealer:
                actions.append(Actions.double_down)

        return actions

    def next_player(self, loop = False):
        if self.current_player >= len(self.players) - 1 and loop:
            self.current_player = 0
        elif self.current_player >= len(self.players) - 1:
            print("Round over")
            self._settle() #TODO: game over, i just dont know what to do yet
        else:
            self.current_player += 1

    def _bet(self, player_index):
        if Actions.bet not in self.get_legal_actions(player_index):
            print("Invalid action", player_index, self.get_legal_actions(player_index))
            return
        self.players[player_index].bet(Actions.default_bet)
        for i in range(2):
            self.players[player_index].hit()

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
                player.is_playing = True
            else:
                player.hands = []
                player.is_playing = True
                self._bet(-1)
        self.current_player = 0



class Player:

    def __init__(self, is_dealer = False, wallet = 100, copy = None):
        if copy is None:
            self.wallet = wallet
            self.is_dealer = is_dealer
            self.is_playing = True
            self.currentHand = None
            self.hands = []
        else:
            self.wallet = copy.wallet
            self.is_dealer = copy.is_dealer
            self.is_playing = copy.is_playing
            self.currentHand = copy.currentHand
            self.hands = []
            for hand in copy.hands:
                self.hands.append(Hand(copy=hand))

    def _next_hand(self):
        if self.currentHand < len(self.hands) - 1:
            self.currentHand += 1
        else:
            self.currentHand = None

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
            self.splittable = splittable
        else:
            self.bet = copy.bet
            self.splittable = copy.splittable
            self.cards = []
            for card in copy.cards:
                self.cards.append(card)

    def split(self):
        if len(self.cards) > 0:
            self.cards = [self.cards[0]]
            new_hand = Hand(self.bet, self.splittable-1)
            new_hand.cards.append(self.cards[0])
            return new_hand

    def hit(self):
        self.cards.append(Deck().draw())

    def value(self):
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

        if ace and value <= 10:
            value += 10

        return value

def main():
    # player, dealer
    agents = [ManualAgent(0), ManualAgent(1)]
    game = GameState(1)
    while game.current_player < 2:
        game = game.generate_successor(agents[game.current_player].get_action(game), game.current_player)   #agents[game.current_player].get_action(game)


main()
