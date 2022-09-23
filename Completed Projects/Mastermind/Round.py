"""
    Daniel Gonzalez
    Mastermind: Round
"""

from Peg import *
from Quad import *
from Bovine import *

PEG_AREA = .7  # How much of the width all the pegs can use, from left to right

PEG_OCCUPIED_SPACE = .8  # How much of the actual space dedicated to a peg that a peg should occupy

class Round(Quad):

    """A Round is one round of the game. A player makes a guess of colors,
    and the game must display the number of bulls and cows made for that round.
    So a Round is a quad which divides its space up to fit pegs for the player
    to make guesses, and a bovine used to display the success of their guess."""

    def __init__(self, x, y, height, width, pen=None):
        """Constructor method, calculates positions and area of pegs
        and the bovines found at the end of each round.
        x, y - (x,y) coordinates of the center of the quad
        height - height of the quad
        width - width of the quad
        pen - turtle object used to draw/erase, shared by all objects in the round"""

        Quad.__init__(self, x, y, height, width, pen)
        self.create_pegs(Settings().get_setting('pegs'))
        self.create_bovine()

    def create_pegs(self, num_pegs, peg_space=PEG_AREA):
        """create_pegs() calculates the position and radius of each peg
        found in the round.
        num_pegs - number of pegs to create
        peg_space - from left to right, how much space in the round can be dedicated
        to drawing pegs (default 70% of the quad)"""

        # Calculate peg size, start positions
        self.pegs = []
        peg_area = self.width * peg_space

        # Calculate a radius based on height/width, choose the smaller of the two as final
        # This is a necessary check as the number of rounds and pegs are variable
        x_peg_radius = ((peg_area / num_pegs) / 2) * PEG_OCCUPIED_SPACE
        y_peg_radius = (self.height / 2) * PEG_OCCUPIED_SPACE
        if (x_peg_radius >= y_peg_radius):
            peg_radius = y_peg_radius
        else:
            peg_radius = x_peg_radius

        # Start position, offset to the right for each peg created
        start_x = self.x - self.width / 2 + (peg_radius * 3)
        for i in range(num_pegs):
            x_offset = ((peg_area / num_pegs) * i)
            x = start_x + x_offset
            y = self.y
            self.pegs.append(Peg(x, y, peg_radius, "", self.pen))

    def create_bovine(self):
        """create_bovine() is similar to create_pegs, but creates a single bovine
        at the end of the round"""
        if (len(self.pegs) == 0):
            return

        # Position should be, from the right side, middle of the empty space in the round
        x = (self.x + (self.width / 2)) - (self.width * ((1 - PEG_AREA) / 2))
        y = self.y
        radius = self.pegs[0].radius
        self.bovine = Bovine(x, y, radius, self.pen)

    def draw(self, outline=False):
        """draw() draws the round, which is a quad, and all the
        objects held within.
        outline (bool) - whether the round's borders should be drawn"""
        if outline:
            Quad.draw(self)
        for i in range(len(self.pegs)):
            self.pegs[i].draw()
        self.bovine.draw()

    def get_object_at(self, x, y):
        """get_object_at() searches for an object at the given
        x,y position, returns it. Returns None if nothing is found.
        x, y - (x,y) coordinates to check"""

        for i in range(len(self.pegs)):
            if self.pegs[i].clicked(x, y):
                return self.pegs[i]

    def get_guess(self):
        """get_guess() returns the colors of each peg in the round, in order."""
        guess = []
        for peg in self.pegs:
            guess.append(peg.color)
        return guess

    def fill_bovine(self, bovine):
        """fill_bovine() displays the bulls and cows in the round's bovine
        bovine (tuple of int) - number of bulls, cows to display"""
        self.bovine.fill_bovine(bovine[0], bovine[1], True)

    def reset(self):
        """reset() removes the color from all the pegs and the bovine, then redraws them."""
        for peg in self.pegs:
            peg.take_color()
            peg.draw()
        self.bovine.draw()
