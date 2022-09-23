"""
    Daniel Gonzalez
    Mastermind: Quad
"""

from Drawable import *


class Quad(Drawable):

    """A quad represents any rectangular object ob the board."""

    def __init__(self, x, y, height, width, pen=None):
        """Constructor method, sets attributes
        x, y - (x,y) coordinates of the center of the quad
        height (int/float) - height of the quad
        width (int/float) - width of the quad
        pen - turtle object used to draw/fill/erase the quad"""
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        Drawable.__init__(self, pen)

    def draw(self):
        """draw() draws a quad, does not fill it."""

        # Start at bottom left corner
        x = self.x - (self.width / 2)
        y = self.y - (self.height / 2)
        Drawable.move_pen_to(self, x, y)
        self.pen.goto(x, y + self.height)
        self.pen.goto(x + self.width, y + self.height)
        self.pen.goto(x + self.width, y)
        self.pen.goto(x, y)

    def erase(self):
        """erase() clears everything the pen has drawn"""
        self.pen.clear()

    def clicked(self, x, y):
        """clicked() checks if the x,y values inputted are within
        the bounds of the quad. Returns bool
        x, y - (x,y) coordinates to check"""

        vert_radius = self.height / 2
        horiz_radius = self.width / 2
        return ((x >= self.x - horiz_radius)
                and (x <= self.x + horiz_radius)
                and (y >= self.y - vert_radius)
                and (y <= self.y + vert_radius))
