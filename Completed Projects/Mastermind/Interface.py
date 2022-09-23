"""
    Daniel Gonzalez
    Mastermind: Interface
"""

from Gameboard import *
from Leaderboard import *
from Menu import *
from Popup import *

DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 675

DEFAULT_X = 200
DEFAULT_Y = 150


class Interface(Drawable):

    """Interface handles the displaying and hiding of anything on the board.
    Has methods for writing the current score, name, etc. Draws all objects
    upon being created."""

    def __init__(self):

        """Constructor method
            Initializes turtle screen and the objects on it.
            Also creates pens used for displaying info to the player."""

        size_multiplier = Settings().get_setting('screensize')
        turtle.delay(0)

        # Initialize turtle screen
        turtle.setup(DEFAULT_WIDTH * size_multiplier, DEFAULT_HEIGHT * size_multiplier)
        turtle.setworldcoordinates(-DEFAULT_X, -DEFAULT_Y,
                                   DEFAULT_X, DEFAULT_Y)
        self.screen = turtle.Screen()

        # Initialize all drawable objects

        self.score_pen = self.new_pen()
        self.name_pen = self.new_pen()
        self.color_pen = self.new_pen()
        self.fontsize = int((DEFAULT_HEIGHT * size_multiplier) / 45)
        self.bg_pen = self.new_pen()
        self.background = Quad(0, 0, DEFAULT_X * 4, DEFAULT_Y * 4, pen=self.bg_pen)
        self.bg_pen.begin_fill()
        self.background.draw()
        self.bg_pen.end_fill()

        # Center of left half of screen, take up ~half in width, a bit more in height
        self.gameboard = Gameboard(-DEFAULT_X / 2, DEFAULT_Y / 5,
                                   DEFAULT_Y * 1.5, DEFAULT_X * .95)

        # Same qualities as the Gameboard, to take up the right half
        self.leaderboard = Leaderboard(DEFAULT_X / 2, DEFAULT_Y / 5,
                                       DEFAULT_Y * 1.5, DEFAULT_X * .95)

        # These values ensure it will encompass the entire bottom of the screen
        self.menu = Menu(0, -DEFAULT_Y * .8,
                         DEFAULT_Y / 3, DEFAULT_X * 1.95)

        # One popup, center screen
        self.popup = Popup(0, 0, 100, 150)

        # Draw all objects except popup
        self.leaderboard.draw()
        self.gameboard.draw()
        self.menu.draw()
        self.write_score()
        self.write_color("")

    def write_name(self, name="Player"):
        """write_name() writes the name inputted in the bottom right corner
        of the screen, above the menu."""

        self.name_pen.clear()
        self.name_pen.penup()
        self.name_pen.goto(self.menu.x + self.menu.width / 2, self.menu.y + self.menu.height / 2)
        self.name_pen.write(name, move=False, align="right",
                            font=("Comic Sans MS", self.fontsize, "bold"))

    def write_score(self, score=None):
        """write_score() writes the score above the menu, center screen. If no score is given,
            gets the score from the Gameboard object
            score (int/float) - player's current score"""

        if score is None:
            score = str(self.gameboard.get_score())

        score = "Score: " + str(score)
        self.score_pen.clear()
        self.score_pen.penup()
        self.score_pen.goto(self.menu.x, self.menu.y + self.menu.height / 2)
        self.score_pen.write(score, move=False, align="center",
                             font=("Comic Sans MS", self.fontsize, "bold"))

    def write_color(self, color=""):
        """write_color() displays the color string inputted, in the color of the
            string, above the menu on the left side of the screen.
            color (str) - string used by turtle for color"""

        self.color_pen.clear()
        if color == "":
            return

        self.color_pen.penup()
        self.color_pen.goto(self.menu.x - self.menu.width / 2, self.menu.y + self.menu.height / 2)
        self.color_pen.color(color)
        self.color_pen.write(color, move=False, align="left",
                             font=("Comic Sans MS", self.fontsize, "bold"))

    def get_str_input(self, header="Mastermind", body="Input string:",
                      error_msg="Invalid. Try Again:",
                      validation=lambda user_input: True):
        """get_str_input() displays a popup to get input from the user. Returns
            the string given.
            header (str) - header to display on the window
            body (str) - body of the popup, displayed above the input box
            error_msg (str) - message to display instead of body if input does not pass validation function
            validation (func*) - function used to validate input"""

        str_input = turtle.Screen().textinput(header, body)
        while not validation(str_input):
            str_input = turtle.Screen().textinput(header, error_msg)

        return str_input

    def display_popup(self, header="ERROR",
                      body="Something went wrong",
                      color="red"):
        """display_popup() shows the popup in the center of the screen with the given header, body, and bg_color.
            header (str) - bold header message displayed at the top of the popup
            body (list of str or str) - body of the popup
            color (str) - color string used by turtle to fill the background of the popup"""

        self.popup.set_header(header)
        self.popup.set_body(body)
        self.popup.color = color
        self.popup.draw()

    def hide_popup(self):
        """hide_popup() removes the popup from the screen"""
        self.popup.erase()

    def get_object_at(self, x, y):
        """get_object_at() returns the object at a given location on the screen
            If none is found, returns None
            x, y - (x,y) coordinates to check"""

        # Only check menu and Gameboard, nothing else to find
        if self.menu.clicked(x, y):
            return self.menu.get_object_at(x, y)
        elif self.gameboard.clicked(x, y):
            return self.gameboard.get_object_at(x, y)
        else:
            return None

    def fill_bovine(self, bovine):
        """fill_bovine() calls on the Gameboard to draw the bovine with the inputted
            number of bulls and cows
            bovine (tuple, int) - two integers for bulls, cows"""
        self.gameboard.fill_bovine(bovine)

    def reset_all(self):
        """reset_all() resets all parts of the game to start a new game"""
        self.hide_popup()
        self.display_popup(header="Loading New Game", body="This will only take a moment.", color="purple")
        self.menu.reset()
        self.gameboard.reset()
        self.hide_popup()

    def clear_round(self):
        """clear_round() resets the current round and the menu"""
        self.gameboard.clear_round()
        self.reset_menu()

    def reset_menu(self):
        """reset_menu() makes sure the menu contains all the colors and displays them"""
        self.menu.reset()

    def update_high_score(self):
        """update_high_score sets the new high score for the current iteration of the game
            Calls on the leaderboard to display and save it.
            Returns the difference between current score and high score."""
        score = self.gameboard.get_score()
        best = self.leaderboard.personal_best
        self.leaderboard.set_best(score)
        self.leaderboard.display_best()
        # Illustrates if a new high score was achieved
        return score - best
