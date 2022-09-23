"""
    Daniel Gonzalez
    Mastermind: Peg
"""

from Circle import *
from Colorable import *


class Peg(Circle, Colorable):

    """In the original Mastermind board game, colors are represented with pegs that are
    placed onto the board. Here, Pegs are simply represented with circles. They can hold
    colors and redraw themselves to display the colors they are holding."""

    def __init__(self, x, y, radius=10, color="", pen=None):
        """Constructor method
        x, y - (x,y) coordinates of peg's position on the board
        radius - size of the circle radius representing the peg
        color - color to fill with. '' used to represent no color
        pen - turtle object used to draw/fill/erase"""

        Circle.__init__(self, x, y, radius, pen)
        Colorable.__init__(self, color)

    def draw(self):
        """draw() draws the peg, filling with color if it has one."""
        if (self.color == ""):
            Circle.empty(self)
        else:
            Circle.fill(self, self.color)

    def take_color(self, redraw=True):
        """take_color() sets the color to nothing.
        Returns the color string that the peg did have.
        redraw (bool) - whether to redraw the now empty peg"""
        color = Colorable.take_color(self)
        if (redraw):
            self.draw()
        return color

    def give_color(self, color, redraw=True):
        """give_color() sets the peg's color to the given color string.
        color (str) - color string used by turtle to fill it
        redraw (bool) - whether to redraw the filled peg"""
        Colorable.give_color(self, color)
        if (redraw):
            self.draw()
