"""
    Daniel Gonzalez
    Mastermind: Popup
"""

from Quad import *

HEADER_MAX_CHAR = 8
BODY_MAX_CHAR = 25


class Popup(Quad):

    """A Popup is a quad that can hold a message and display it to the screen.
    The message can also be changed. If given a list of lines to be written, it will
    make sure each of them is on a separate line in the popup."""

    def __init__(self, x, y, height, width, header="ERROR",
                 body="Something went wrong. Please try again.",
                 color="red"):
        """Constructor method, calculates header/body size and
        calculates where each line for the header and body will go
        x, y - (x,y) coordinates of the center of the quad
        height (int/float) - height of the quad
        width (int/float) - width of the quad
        header (str) - large, bold words to display at the top of the header
        body (str or list of str) - message to display to user
        color (str) - background color of popup"""

        Quad.__init__(self, x, y, height, width)
        self.color = color

        # Sizes are relative to screensize so it will always change as sizes change
        self.header_font_size = int(turtle.screensize()[1] / 20)
        self.header_line_size = self.width / 8

        self.body_font_size = int(turtle.screensize()[1] / 40)
        self.body_line_size = self.width / 12

        self.set_header(header)
        self.set_body(body)

    def draw(self, redraw=1):
        """Displays the popup along with its message. Attempts to resize and redraw
        if the popup was originally too big or small for the message
        Redraw - how many resize attempts the popup has before giving up"""

        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        Quad.draw(self)
        self.pen.end_fill()

        # Move to top of quad, then down a little to avoid writing on the line
        y = self.y + (self.height / 2) - self.width / 5 + self.header_line_size
        # Write each line in the header, iterate down by an offset
        for i in range(len(self.header)):
            y -= self.header_line_size
            Quad.move_pen_to(self, self.x, y)
            self.pen.write(self.header[i], move=False, align="center",
                           font=("Comic Sans MS", self.header_font_size, "bold"))

        y -= self.body_line_size
        # Write each line in the body, iterate down by offset
        for i in range(len(self.body)):
            y -= self.body_line_size
            Quad.move_pen_to(self, self.x, y)
            self.pen.write(self.body[i], move=False, align="center",
                           font=("Comic Sans MS", self.body_font_size, "bold"))

        # If the bottom line of the popup is REALLY far away from the last line of the body
        # or if it's really close, or if it's been overwritten, resize and redraw to look better
        bottom_line = self.y - (self.height / 2) + self.body_line_size / 2
        if (y < bottom_line and redraw > 0):
            self.pen.clear()
            self.height *= 2.5
            self.draw(redraw - 1)
        elif (y - bottom_line > self.height / 2 and redraw > 0):
            self.pen.clear()
            self.height /= 2.5
            self.draw(redraw - 1)

    def set_header(self, header="ERROR"):
        """set_header() sets the header to a new message
        header (str) - message to set the header to"""
        self.header = self.create_lines(header, HEADER_MAX_CHAR)

    def set_body(self, body="Something went wrong."):
        """set_body() sets the body to a new message
        body (str or list of str) - message to set the body to.
        If it is a list, it will make sure each item on the list is
        in its own line (good for enumeration)"""

        self.body = []
        if (isinstance(body, list)):
            for line in body:
                # Create a new line for each line in the list
                self.body.extend(self.create_lines(line, BODY_MAX_CHAR))
        else:
            self.body.extend(self.create_lines(body, BODY_MAX_CHAR))

    def create_lines(self, text, max_char=8):
        """create_lines() takes a string and attempts ot create lines
        that are easy to read and nice to look at that do not extend past
        a certain point. Returns a list of lines.
        text (str) - text to divide into lines
        max_char (int) - max number of characters that should be in a line"""

        # Tries not to end on a word with a dash by checking for spaces in
        # strategic places, but adds a '-' when necessary, but never at the last
        # character of a word.
        # Example:
        # Hello, my name is Dan-
        # iel.

        lines = []
        while len(text) > max_char:
            space = False
            for i in range(max_char, 0, -1):
                if (text[i] == " "):
                    lines.append(text[:i])
                    text = text[i + 1:]
                    space = True
                    break
            if not space:
                lines.append(text[:(max_char - 2)] + '-')
                text = text[(max_char - 2):]

        lines.append(text)
        return lines
