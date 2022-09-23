"""
    Daniel Gonzalez
    Mastermind: Colorable
"""

class Colorable:

    """Colorable represents an object that can hold a color
    or be given a color, like a peg, or the player."""

    def __init__(self, color=""):
        """Constructor method
            color (str) - color string used by turtle for color, empty string used
                        to represent no color"""

        self.color = color

    def take_color(self):
        """take_color() sets the Colorable's color to an empty string and returns
            the value that was stored in the color"""

        color = self.color
        self.color = ""
        return color

    def give_color(self, color):
        """give_color() sets the Colorable's color to the given color string
            color (str) - color string used by turtle for color"""
        self.color = color

    def get_color(self):
        """get_color() returns the color value, but does not set the color to an empty string"""
        return self.color
