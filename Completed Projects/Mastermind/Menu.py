"""
    Daniel Gonzalez
    Mastermind: Menu
"""

from Round import *
from Button import *

BUTTONS = ["QUIT", "HELP", "CLEAR", "ENTER"]


class Menu(Round):

    """The Menu is the player's pool of options collected in one place.
    Buttons to interact with the game as well as every color peg they can use
    to guess. It is a quad with all objects in a line down the middle. Its
    similarity ro a Round object makes it an extension of one, and it shares
    those methods."""

    def __init__(self, x, y, height, width, pen=None):
        """Constructor method, creates pegs and buttons
        in positions relative to the menu's position and size.
        x, y - coordinates of the center of the quad
        height - height of the menu
        width - width of the menu (should be much longer)
        pen - turtle object used to draw/erase, shared by all objects
        on the menu"""

        self.colors = Settings().get_setting('colors')
        Quad.__init__(self, x, y, height, width, pen)
        self.pen.width(4)

        # Same exact logic as the Round, reuse the code
        if (len(self.colors) > 8):
            Round.create_pegs(self, len(self.colors), .45)
        else:
            # 8 or more colors looks a little better with less space
            Round.create_pegs(self, len(self.colors), .4)

        for i in range(len(self.colors)):
            self.pegs[i].give_color(self.colors[i], False)
        self.create_button()

    def create_button(self):
        """create_button() generates all the buttons specified in the global variable
        in this file, calculating their appropriate radius and positions based on the
        menu's space and position."""
        self.buttons = []
        # How much space of the menu should be dedicated to the buttons (40%)
        button_area = self.width * .4

        # Calculate how big the buttons can be in regard to the Y direction AND the X direction
        x_button_radius = ((button_area / len(BUTTONS)) / 2) * PEG_OCCUPIED_SPACE
        y_button_radius = (self.height / 2) * PEG_OCCUPIED_SPACE

        # Choosing the smaller of the two guarantees all the buttons will fit in all directions
        if x_button_radius >= y_button_radius:
            button_radius = y_button_radius
        else:
            button_radius = x_button_radius

        # Start on the right, iterate to the left with an x_offset, and create buttons
        start_x = self.x + self.width / 2 - (button_radius * 2.5)
        x_offset = 0
        for i in range(len(BUTTONS)):
            x_offset = (button_area / len(BUTTONS)) * i
            x = start_x - x_offset
            y = self.y
            self.buttons.append(Button(x, y, BUTTONS[i], button_radius, self.pen))

    def draw(self):
        """draw() displays the menu and all the objects contained in it on the turtle screen"""
        self.pen.width(4)
        Quad.draw(self)
        for i in range(len(self.buttons)):
            self.buttons[i].draw()
        self.pen.width(4)
        for i in range(len(self.pegs)):
            self.pegs[i].draw()

    def get_object_at(self, x, y):
        """get_object_at finds the object found at the given x,y position and returns it.
            Returns None if nothing was found."""

        # Left half of the board, has to be a peg
        if x <= self.x:
            return Round.get_object_at(self, x, y)
        else:
            # Check buttons
            for i in range(len(self.buttons)):
                if self.buttons[i].clicked(x, y):
                    return self.buttons[i]

    def reset(self):
        """reset() makes sure every peg in the menu has a color
        and that all colors are on the menu. Redraws anything that was
        not colored correctly."""
        for i in range(len(self.pegs)):
            if (not self.pegs[i].color == self.colors[i]):
                self.pegs[i].give_color(self.colors[i])
                self.pegs[i].draw()
