"""
    Daniel Gonzalez
    Mastermind: Mastermind
"""

from random import choice
from Settings import Settings
COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]


class Mastermind:

    """The Mastermind is the one that generates the code to be guessed.
    Calculates the number of bulls and cows in each guess made."""


    def __init__(self):
        """Constructor method
        Mastermind just requires Settings to generate its attributes, to ensure
        that it is using the same values/lengths as the player."""

        # Most attributes are determined by the settings file
        self.length = Settings().get_setting('pegs')
        self.colors = Settings().get_setting('colors')
        self.repeats = Settings().get_setting('repeats')
        self.code = self.generate_code(self.colors)

    def new_code(self):
        """new_code() forces the mastermind to reset its code and make a new one."""
        self.code = self.generate_code(self.colors)

    def generate_code(self, colors = COLORS):
        """new_code() generates a code based on colors inputted, of length
        equal to the number of rounds in a game."""

        code = []
        colors = colors.copy()
        colors.append('')
        while (len(code) < self.length):
            color = choice(colors)
            code.append(color)
            if(not self.repeats):
                colors.remove(color)

        # print(code)  # For testing purposes

        return code

    def count_bovine(self, guess):
        """ count_bulls_and_cows() Counts the number of bulls and cows
        there are between two lists of colors
        guess (list of str) - the player's guess of what self.code is
        Returns tuple of 2 integers representing number of (bulls, cows) found
        """
        # To mutate w/o losing originals
        code = self.code.copy()
        guesses = guess.copy()
        bulls, cows = (0, 0)
    
        for i in range(len(guesses)):
            # Do nothing, already counted
            if guesses[i] == "bull" or guesses[i] == "cow":
                continue
            # Bull was found
            elif guesses[i] == code[i]:
                bulls += 1
                guesses[i] = "bull"
                code[i] = "bull"  # To indicate it has been counted

            # Might be a cow
            elif guesses[i] in code:
                for j in range(len(code)):  # Stops if cow is found
                    if code[j] == "bull" or code[j] == "cow":
                        continue
                    # Definitely cow, not a future bull
                    elif code[j] == guesses[i] \
                       and code[j] != guesses[j]:
                        code[j] = "cow" 
                        guesses[i] = "cow"
                        cows += 1
                        break

        return bulls, cows

        
