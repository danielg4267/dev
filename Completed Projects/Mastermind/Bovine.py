"""
    Daniel Gonzalez
    Mastermind: Bovine
"""

from Circle import *


class Bovine(Circle):

    """In Mastermind, at the end of every round, a player is given clues
    to the success of their guess. A bull represents a correct color in the correct
    place, and a cow represents the correct color in the wrong place. These are represented
    with a number of very small pegs in close proximity to each other.

    Thus, a Bovine is a collection of circles that can be filled and emptied to represent
    the number of bulls and cows a player has guessed. It is implemented with a Circle to
    determine its position and the space it can occupy, then divides that space up to include
    smaller circles."""

    def __init__(self, x, y, radius, pen=None):
        """Constructor method
            x, y - (x,y) coordinates of the center of the bovine
            radius - radius representing how much space the entire bovine can occupy
            pen - a turtle object used to draw, fill, and erase"""

        # A bovine is just a circle containing other circles
        Circle.__init__(self, x, y, radius, pen)
        num_pegs = Settings().get_setting('pegs')
        num_radiuses = num_pegs

        # Number of radiuses to draw (each circle has two
        if (num_radiuses % 2 != 0):
            num_radiuses += 1
        # Calculate size of the radius of each circle to fit them all in two columns
        diameter = radius * 2
        circle_radius = (diameter / num_radiuses)
        pos_y = self.y + self.radius - circle_radius
        left_x = self.x - (circle_radius * 1.1)
        right_x = self.x + (circle_radius * 1.1)
        self.bovines = []

        # Calculate position of each circle
        for i in range(num_pegs):
            y_offset = 0
            if (i % 2 == 0):
                pos_x = left_x
            else:
                pos_x = right_x
                y_offset = circle_radius * 2.1

            self.bovines.append(Circle(pos_x, pos_y, circle_radius, self.pen))
            pos_y -= y_offset

    def draw(self):
        """draw() draws all circles in the bovine without any color.
        See fill_bovine() to for colors"""
        # Draws each circle without color
        for i in range(len(self.bovines)):
            self.bovines[i].empty()

    def fill_bovine(self, bulls, cows, outline=True):
       """fill_bovine() draws all the circles in the bovine, coloring them separately
       to designate bulls and cows. Bulls first, cows after - otherwise, order is not taken
       into account.
       bulls (int) - number of circles that should represent bulls
       cows (int) - number of circles that should represent cows
       outline (bool) - whether to fill but leave an outline. Bulls are drawn using the
                        outline color regardless."""
       j_offset = -1
       for i in range(bulls):
           if i >= len(self.bovines):
               return
           self.bovines[i].fill(Settings().get_setting('bullcolor'), outline)
           j_offset += 1
       for j in range(j_offset + 1, j_offset + 1 + cows, 1):
           if (j >= len(self.bovines)):
               return
           self.bovines[j].fill('red', outline)