"""
    Daniel Gonzalez
    Mastermind: Player
"""

from Colorable import *


class Player(Colorable):

    """A Player has a name, and can hold/give colors, therefore it is
    a very simple extension of the Colorable class."""

    def __init__(self, name, color=""):
        """Constructor method
        name - String to represent the player's name
        color - color the player is holding, '' for none."""
        self.name = name
        Colorable.__init__(self, color)
