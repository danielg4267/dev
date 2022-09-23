"""
    Daniel Gonzalez
    Mastermind: Circle
"""

from math import sqrt
from Drawable import *


class Circle(Drawable):
    """
        The Circle class represents any circular object on the board. It has
        methods to draw itself empty or full.
    """

    def __init__(self, x, y,
                 radius=10,
                 pen=None):
        """Constructor method
            x,y - (x,y) coordinates of the circle
            radius - radius of the circle
            pen - turtle object used to draw/fill/erase"""

        Drawable.__init__(self, pen)
        self.x = x
        self.y = y
        self.radius = radius

    def fill(self, color, outline=False):
        """fill() draws a circle full of the specified color. Calls draw() if
            no color is given.
            color (str) - a string used by turtle to designate the circle color
            outline (bool) - whether there should be an outline on this circle, else it will match
            the color of the circle"""

        if (color == "" or color is None):
            self.empty()
            return

        # Set colors
        self.pen.fillcolor(color)
        if (outline):
            self.pen.pencolor(Settings().get_setting('linecolor'))
        else:
            self.pen.pencolor(color)

        # Draw circle
        Drawable.move_pen_to(self, self.x + self.radius, self.y)
        self.pen.begin_fill()
        self.pen.circle(self.radius)
        self.pen.end_fill()

    def empty(self):
        """empty() draws the circle and fills it with the generic background color,
            ensuring that it looks empty."""

        Drawable.move_pen_to(self, self.x + self.radius, self.y)
        self.pen.pencolor(Settings().get_setting('linecolor'))
        self.pen.fillcolor(Settings().get_setting('fillcolor'))
        self.pen.begin_fill()
        self.pen.circle(self.radius)
        self.pen.end_fill()

    def clicked(self, x, y):
        """clicked() checks if the (x,y) coordinates given are within the circle's radius
            x, y - (x,y) coordinates to check"""

        return (sqrt((abs(x - self.x) ** 2) + (abs(y - self.y) ** 2)) <= self.radius)
