"""
    Daniel Gonzalez
    Mastermind: Controller
"""

from Interface import *
from Player import *
from Mastermind import *
from time import sleep

WAIT = False  # Used to avoid spamming interact and confusing the program and all the turtles


class Game:

    """The Game is the main controller of the game. It handles interactions
    between the user, the Player object, and various objects in the game."""

    def __init__(self):
        """Constructor method
            Loads an interface, a player, and a mastermind"""

        self.settings = Settings()
        self.interface = Interface()

        # Make sure player name exists and is within bounds
        player_name = self.interface.get_str_input("Mastermind",
                                                   "Enter player name:",
                                                   "Please enter between 0 and 16 alphanumeric characters:",
                                                   lambda name: ((not name == None)
                                                                 and (not ''.join(filter(str.isalnum, name)) == "")
                                                                 and (len(''.join(filter(str.isalnum, name)))) <= 16))

        self.player = Player(name=player_name, color="")
        self.interface.write_name(self.player.name)
        self.mastermind = Mastermind()

        # Used to determine whether the game is currently being played, should always be true except for the end
        self.playing = True

        # Used to determine if the screen is clear for playing (ie no popups in the way)
        self.reset = False

    def interact(self, x, y):
        """interact() finds the object at the (x,y) coordinate and interacts with it based on the
            properties of the player, game state, and the object clicked
            x, y - coordinates of where a user has clicked and attempted to interact with the board"""
        global WAIT
        if (not WAIT):
            WAIT = True  # No other actions until we've completed this one!

            # Get object, interact with it
            if (self.playing and not self.reset):
                obj = self.interface.get_object_at(x, y)

                if (isinstance(obj, Peg)):
                    self.interact_peg(obj)
                elif (isinstance(obj, Button)):
                    self.interact_button(obj)

            # Game paused, but not over
            elif (self.playing and self.reset):
                self.interface.hide_popup()
                self.reset = False

            # New game, reset to start
            else:
                self.mastermind.new_code()
                self.interface.reset_all()
                self.playing = True
                self.reset = False
                self.interface.write_score()

            WAIT = False

    def interact_peg(self, peg):
        """interact_peg() attempts to trade colors between the player and the peg, if possible
            peg - peg object to interact with"""

        if (not isinstance(peg, Peg)):
            return

        # Peg has color, player is not holding a color
        if self.player.color == "" and not peg.color == "":
            self.player.give_color(peg.take_color())
            self.interface.write_color(self.player.color)
            peg.draw()

        # Player has color, peg does not
        elif not self.player.color == "" and peg.color == "":
            peg.give_color(self.player.take_color())
            self.interface.write_color(self.player.color)
            peg.draw()

            # Color was given to a peg on the gameboard, meaning somewhere on the menu, a peg is missing a color
            if self.interface.gameboard.clicked(peg.x, peg.y):
                self.interface.reset_menu()

    def interact_button(self, button):
        """interact_button() performs the action specified by the button given
            button - button to interact with"""

        if not isinstance(button, Button):
            return

        if button.shape == "ENTER":
            self.next_round()
        elif button.shape == "QUIT":
            self.quit_sequence()
        elif button.shape == "CLEAR":
            self.clear_round()
        elif button.shape == "HELP":
            self.help()

    def clear_round(self):
        """clear_round() makes sure the gameboard round is cleared, the menu is full,
            and the player is not holding any color."""

        self.interface.clear_round()
        self.player.take_color()
        self.interface.write_color(self.player.color)

    def next_round(self):
        """next_round() performs the actions needed to move to the next round of the game.
            Depending on how the round went, may end the game."""

        guess = self.interface.gameboard.get_guess()
        bovine = self.mastermind.count_bovine(guess)
        self.interface.fill_bovine(bovine)
        self.interface.reset_menu()
        self.player.take_color()
        self.interface.write_color(self.player.color)

        # All bulls, win!
        if (bovine[0] == self.settings.get_setting('pegs')):
            self.win_sequence()

        # If it's not the last round, move to the next one
        elif (not self.interface.gameboard.last_round()):
            self.interface.gameboard.next_round()
            self.interface.write_score()

        # Last round, AND they didn't win! Dang that sucks for them.
        else:
            self.lose_sequence()

    def lose_sequence(self):
        """lose_sequence() performs the actions needed to process the end of the game when
        a player did not win."""

        self.playing = False
        self.reset = True
        self.interface.write_score(0)

        # Format the code for clear display on the popup
        # People like to know what the final answer was!
        display_code = "["
        for i in range(len(self.mastermind.code)):
            if self.mastermind.code[i] == "":
                display_code += "blank"
            else:
                display_code += self.mastermind.code[i]
            if(i < len(self.mastermind.code) - 1):
                display_code += ", "
        display_code += "]"

        # Blank lines help to make it clear where the code starts and ends!
        self.interface.display_popup("You Lose!", ["The code was:", "", "", display_code, "", "",
                                                   "Click anywhere to try again."], "red")

    def win_sequence(self):
        """win_sequence() performs the actions needed to process a win."""
        self.playing = False
        self.reset = True
        difference = self.interface.update_high_score()

        # Different messages based on how well they did, for fun :)
        if (difference > 0):
            self.interface.display_popup("You Win!",
                                         "A win for the history books! Click anywhere to play again.",
                                         "blue")
        elif (difference < 0):
            self.interface.display_popup("You Win!",
                                         "But you can do better than that! Click anywhere to try again.",
                                         "blue")
        else:
            self.interface.display_popup("You Win!",
                                         "So close to beating your best! Click anywhere to try again.",
                                         "blue")

    def quit_sequence(self):
        """quit_sequence() performs actions needed to close the game safely and save scores before exiting."""

        self.interface.display_popup("Exit", "Sorry to see you go! Saving scores and quitting...", "medium violet red")

        # Only save if they actually won at least one game
        if (self.interface.leaderboard.personal_best > 0):
            self.interface.leaderboard.save_score(self.player.name)

        if (Settings().get_setting('export_xml')):
            self.interface.leaderboard.export_xml('leaderboard.xml')

        # Sleep just so the popup is readable before closing
        sleep(2)
        turtle.bye()

    def help(self):
        """help() calls on the interface to display the rules of the game"""
        self.interface.display_popup("How to Play",
                                     ["1. Click peg to hold color",
                                      "2. Click empty peg to give color",
                                      "3. X to clear round",
                                      "4. Checkmark to submit guess",
                                      "5. Power button to save best score and quit",
                                      "6. Circles at the end of each round indicate correct colors in the right space (black) or wrong space (red)"],
                                     "orange")
        self.reset = True
