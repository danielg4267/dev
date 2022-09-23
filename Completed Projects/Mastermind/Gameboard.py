"""
    Daniel Gonzalez
    Mastermind: Gameboard
"""

from Round import *

ROUND_OCCUPIED_SPACE = .9


class Gameboard(Quad):
    """
    Gameboard is a rectangular quad that holds every round of the game within it.
    It keeps track of the current round and calculates the player's current score based
    on that.
    """

    def __init__(self, x, y, height, width, pen=None):
        """Constructor method
        x, y - (x,y) coordinates of the Gameboard's position
        height (int/float) - height of the Gameboard
        width (int/float) - width of the Gameboard
        pen - turtle object used for drawing the Gamebaord,
                not shared among other objects on the Gameboard"""

        Quad.__init__(self, x, y, height, width, pen)
        self.pen.width(4)
        self.current_r = 0  # Used to track current round
        self.rounds = []
        self.create_rounds()

    def create_rounds(self):
        """create_rounds() creates the rounds housed within the Gameboard"""
        # Each round is a quad centered within the Gameboard at differing Y-values.
        # Method divides up the Gamebaord space evenly for each round

        num_pegs = Settings().get_setting('pegs')
        num_rounds = Settings().get_setting('rounds')

        # Rounds can take up the width of the board, but not the entire height, to make sure they fit
        round_height = (self.height * ROUND_OCCUPIED_SPACE) / num_rounds
        round_width = self.width
        x = self.x  # Quads that should be centered within the gameboard (but at different heights)

        # Iterate from the top down, create each round with the given y offset
        start_y = (self.y + (self.height / 2)) - (round_height)
        for i in range(num_rounds):
            y_offset = round_height * i
            y = start_y - y_offset
            self.rounds.append(Round(x, y, round_height, round_width, num_pegs))

    def draw(self):
        """draw() draws the gameboard on the screen, along with all the rounds it has."""

        Quad.draw(self)
        for i in range(len(self.rounds)):
            self.rounds[i].draw(False)

        # Pen used to draw is used as a marker for what the current round is
        # Make it bigger, red, and visible
        self.pen.resizemode("user")
        self.pen.shape("triangle")
        self.pen.shapesize(stretch_wid=2, outline=2)
        self.pen.pencolor(Settings().get_setting('linecolor'))
        self.pen.fillcolor("red")
        x = self.x - self.width / 2 + (self.rounds[self.current_r].pegs[0].radius * 1.15)
        Quad.move_pen_to(self, self.x - self.width / 2, self.rounds[self.current_r].y)
        self.pen.seth(0)
        self.pen.showturtle()

    def clicked(self, x, y):
        """clicked() checks if the Gameboard was clicked at the x,y coordinates given.
            Only returns true if the current round was clicked
            x, y - (x,y) coordinates to check"""
        return self.rounds[self.current_r].clicked(x, y)

    def get_object_at(self, x, y):
        """get_object_at() returns the object at the x,y coordiantes given.
            Returns None if nothing was found.
            x, y - (x,y) coordinates to check"""
        return self.rounds[self.current_r].get_object_at(x, y)

    def get_guess(self):
        """get_guess() obtains the guess of the current round. Returns a list of color strings"""
        return self.rounds[self.current_r].get_guess()

    def fill_bovine(self, bovine):
        """fill_bovine() sets the bulls and cows of the current round
            bovine (tuple, int) - two integers for number of bulls and cows, respectively"""
        self.rounds[self.current_r].fill_bovine(bovine)

    def last_round(self):
        """last_round() checks if this is the last playable round on the gameboard. Returns a boolean"""
        return self.current_r >= len(self.rounds) - 1

    def next_round(self):
        """next_round() sets current_r to the next round in the list, if there is one.
            Moves the marker to that round."""
        if not self.last_round():
            self.current_r += 1
            Quad.move_pen_to(self, self.x - self.width / 2, self.rounds[self.current_r].y)
            self.pen.seth(0)

    def clear_round(self):
        """clear_round() calls reset on the current round only."""
        self.rounds[self.current_r].reset()

    def reset(self):
        """reset() calls reset on all rounds, sets current_r to the first round and moves the marker."""
        while (self.current_r > 0):
            self.rounds[self.current_r].reset()
            self.current_r -= 1
        self.rounds[self.current_r].reset()
        Quad.move_pen_to(self, self.x - self.width / 2, self.rounds[self.current_r].y)
        self.pen.seth(0)

    def get_score(self):
        """get_score() calculates the score out of 100 based on the current round, along with the bonus points
            Returns an integer."""
        settings = Settings()
        score = round(100 - (100 * self.current_r / settings.get_setting('rounds')))
        if settings.get_setting('bonus_enabled'):
            score += settings.get_setting('bonus_points')
        return int(score)
